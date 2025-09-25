"""
Logic Processor - Main class for handling argument validation and proof generation
Integrates with Google Gemini API for natural language processing and logical reasoning
"""

import os
import re
import json
import logging
import time
from typing import List, Dict, Optional, Tuple
import google.generativeai as genai
from google.api_core.exceptions import ResourceExhausted
from models import ArgumentRequest, ValidationResult, ProofStep, Counterexample, InferenceRule

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class LogicProcessor:
    """Main processor for logical argument validation and proof generation"""
    
    def __init__(self):
        """Initialize the logic processor with Gemini API"""
        logger.info("Inicializando LogicProcessor...")
        
        # Configure Gemini API
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            logger.error("GEMINI_API_KEY no encontrada en variables de entorno")
            raise ValueError("GEMINI_API_KEY environment variable is required")
        
        logger.info("Configurando API de Google Gemini...")
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-2.0-flash')
        self.last_api_call = 0
        self.min_call_interval = 5  # Seconds between API calls to avoid quota limits
        logger.info("LogicProcessor inicializado correctamente")
        
        # Common logical operators mapping
        self.logical_operators = {
            "and": "∧",
            "y": "∧", 
            "or": "∨",
            "o": "∨",
            "not": "¬",
            "no": "¬",
            "if": "→",
            "si": "→",
            "then": "→",
            "entonces": "→",
            "iff": "↔",
            "si y solo si": "↔"
        }

    def _map_inference_rule(self, rule_name: str) -> Optional[InferenceRule]:
        """Map rule names from Gemini to our InferenceRule enum"""
        # Direct mapping for exact matches
        try:
            return InferenceRule(rule_name)
        except ValueError:
            pass
        
        # Alternative mappings for common variations
        rule_mappings = {
            "Doble Negación": InferenceRule.DOUBLE_NEGATION,
            "Double Negation": InferenceRule.DOUBLE_NEGATION,
            "Contraposición": InferenceRule.CONTRAPOSITION,
            "Contraposition": InferenceRule.CONTRAPOSITION,
            "De Morgan": InferenceRule.DE_MORGAN,
            "DeMorgan": InferenceRule.DE_MORGAN,
            "Ley de De Morgan": InferenceRule.DE_MORGAN,
            "Exportación": InferenceRule.EXPORTATION,
            "Export": InferenceRule.EXPORTATION,
            "Tautología": InferenceRule.TAUTOLOGY,
            "Tautology": InferenceRule.TAUTOLOGY,
            # Add more mappings as needed
        }
        
        mapped_rule = rule_mappings.get(rule_name)
        if mapped_rule:
            logger.debug(f"Regla '{rule_name}' mapeada a '{mapped_rule.value}'")
            return mapped_rule
        
        # Default fallback - log warning and use a generic rule
        logger.warning(f"⚠️ Regla desconocida '{rule_name}', usando Modus Ponens como fallback")
        return InferenceRule.MODUS_PONENS

    async def _safe_api_call(self, prompt: str, operation_name: str = "API call"):
        """Make a safe API call with rate limiting and error handling"""
        # Rate limiting
        current_time = time.time()
        time_since_last = current_time - self.last_api_call
        
        if time_since_last < self.min_call_interval:
            sleep_time = self.min_call_interval - time_since_last
            logger.info(f"⏱️ Esperando {sleep_time:.1f}s para evitar límites de cuota...")
            time.sleep(sleep_time)
        
        try:
            logger.debug(f"🤖 Enviando prompt a Gemini para {operation_name}...")
            response = self.model.generate_content(prompt)
            self.last_api_call = time.time()
            
            logger.debug(f"📥 Respuesta cruda de Gemini ({operation_name}): {response.text}")
            logger.info(f"📊 Tamaño de respuesta ({operation_name}): {len(response.text)} caracteres")
            
            return response
            
        except ResourceExhausted as e:
            logger.error(f"❌ Cuota de API excedida en {operation_name}: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"❌ Error en {operation_name}: {str(e)}")
            raise

    async def validate_argument(self, argument: ArgumentRequest) -> ValidationResult:
        """
        Main method to validate an argument and generate proof or counterexample
        """
        logger.info(f"🔍 Iniciando validación de argumento...")
        logger.debug(f"Premisas: {argument.premises}")
        logger.debug(f"Conclusión: {argument.conclusion}")
        
        try:
            # Step 1: Convert natural language to symbolic logic
            logger.info("📝 Paso 1: Convirtiendo lenguaje natural a lógica simbólica...")
            symbolic_result = await self._convert_to_symbolic(argument.premises, argument.conclusion)
            logger.info(f"✅ Conversión simbólica completada: {symbolic_result}")
            
            # Step 2: Validate the argument and generate proof/counterexample
            logger.info("🔬 Paso 2: Validando argumento y generando prueba/contraejemplo...")
            validation_result = await self._validate_and_prove(
                symbolic_result["premises"],
                symbolic_result["conclusion"],
                symbolic_result["variables"]
            )
            logger.info(f"✅ Validación completada: {validation_result['is_valid']}")
            
            # Step 3: Construct final result
            logger.info("🏗️ Paso 3: Construyendo resultado final...")
            result = ValidationResult(
                is_valid=validation_result["is_valid"],
                symbolic_premises=symbolic_result["premises"],
                symbolic_conclusion=symbolic_result["conclusion"],
                variables_identified=symbolic_result["variables"],
                processing_notes=symbolic_result.get("notes", [])
            )
            
            if validation_result["is_valid"]:
                result.proof_steps = validation_result["proof_steps"]
                logger.info(f"📋 Prueba generada con {len(validation_result['proof_steps'])} pasos")
            else:
                result.counterexample = validation_result["counterexample"]
                logger.info(f"🚫 Contraejemplo generado: {validation_result['counterexample']}")
            
            logger.info("✅ Validación de argumento completada exitosamente")
            return result
            
        except Exception as e:
            logger.error(f"❌ Error durante la validación: {str(e)}")
            logger.exception("Detalles del error:")
            # Return a fallback result with error information
            return ValidationResult(
                is_valid=False,
                symbolic_premises=[f"Error: {str(e)}"],
                symbolic_conclusion="Error en procesamiento",
                variables_identified=[],
                processing_notes=[f"Error durante el procesamiento: {str(e)}"]
            )

    async def _convert_to_symbolic(self, premises: List[str], conclusion: str) -> Dict:
        """Convert natural language statements to symbolic logic"""
        
        prompt = f"""
Eres un experto en lógica proposicional. Tu tarea es convertir argumentos en lenguaje natural al español a su forma simbólica.

ARGUMENTOS A CONVERTIR:
Premisas:
{chr(10).join([f"{i+1}. {premise}" for i, premise in enumerate(premises)])}

Conclusión: {conclusion}

INSTRUCCIONES:
1. Identifica todas las proposiciones atómicas en el argumento
2. Asigna variables proposicionales (P, Q, R, S, etc.) a cada proposición atómica
3. Convierte cada premisa y la conclusión a forma simbólica usando:
   - ∧ para "y"
   - ∨ para "o" 
   - → para "si...entonces"
   - ↔ para "si y solo si"
   - ¬ para "no"
4. Mantén consistencia en las asignaciones de variables

FORMATO DE RESPUESTA (JSON):
{{
    "variables": {{
        "P": "descripción de la proposición P",
        "Q": "descripción de la proposición Q"
    }},
    "premises": ["forma simbólica premisa 1", "forma simbólica premisa 2"],
    "conclusion": "forma simbólica de la conclusión",
    "notes": ["nota explicativa si es necesaria"]
}}

Responde SOLO con el JSON, sin texto adicional.
"""

        try:
            logger.debug(f"Prompt enviado: {prompt[:200]}...")
            
            response = await self._safe_api_call(prompt, "conversión simbólica")
            
            # Try to parse JSON response
            cleaned_response = response.text.strip()
            logger.debug(f"📝 Respuesta limpiada: {cleaned_response}")
            
            # Remove markdown code blocks if present
            if cleaned_response.startswith('```json'):
                cleaned_response = cleaned_response.replace('```json', '').replace('```', '').strip()
                logger.debug(f"🧹 JSON limpiado de markdown: {cleaned_response}")
            elif cleaned_response.startswith('```'):
                cleaned_response = cleaned_response.replace('```', '').strip()
                logger.debug(f"🧹 JSON limpiado de bloques de código: {cleaned_response}")
            
            result = json.loads(cleaned_response)
            logger.info(f"✅ JSON parseado correctamente: {result}")
            
            # Convert variables dict to list for the model
            variables_list = [f"{var}: {desc}" for var, desc in result["variables"].items()]
            logger.debug(f"🔤 Variables convertidas: {variables_list}")
            
            final_result = {
                "premises": result["premises"],
                "conclusion": result["conclusion"],
                "variables": variables_list,
                "notes": result.get("notes", [])
            }
            
            logger.info(f"✅ Conversión simbólica exitosa: {final_result}")
            return final_result
            
        except json.JSONDecodeError as json_error:
            logger.warning(f"⚠️ Error parseando JSON de Gemini: {json_error}")
            logger.warning(f"Respuesta problemática: {response.text if 'response' in locals() else 'No hay respuesta'}")
            logger.info("🔄 Usando conversión simbólica básica como fallback...")
            # Fallback: basic symbolic conversion
            return self._basic_symbolic_conversion(premises, conclusion)
        except Exception as e:
            logger.error(f"❌ Error en conversión simbólica: {str(e)}")
            logger.exception("Detalles del error:")
            raise Exception(f"Error en conversión simbólica: {str(e)}")

    def _basic_symbolic_conversion(self, premises: List[str], conclusion: str) -> Dict:
        """Fallback basic symbolic conversion"""
        logger.info("🔄 Iniciando conversión simbólica básica (fallback)...")
        variables = []
        symbolic_premises = []
        
        # Simple conversion - identify basic patterns
        var_counter = 0
        var_map = {}
        
        all_statements = premises + [conclusion]
        logger.debug(f"Analizando {len(all_statements)} declaraciones...")
        
        for i, stmt in enumerate(all_statements):
            logger.debug(f"Procesando declaración {i+1}: {stmt}")
            # Basic pattern recognition for simple statements
            if "si" in stmt.lower() and "entonces" in stmt.lower():
                logger.debug("Patrón 'si...entonces' detectado")
                parts = stmt.lower().split("entonces")
                if len(parts) == 2:
                    antecedent = parts[0].replace("si", "").strip()
                    consequent = parts[1].strip()
                    logger.debug(f"Antecedente: {antecedent}, Consecuente: {consequent}")
                    
                    if antecedent not in var_map:
                        var_map[antecedent] = chr(80 + var_counter)  # P, Q, R...
                        variables.append(f"{var_map[antecedent]}: {antecedent}")
                        var_counter += 1
                    
                    if consequent not in var_map:
                        var_map[consequent] = chr(80 + var_counter)
                        variables.append(f"{var_map[consequent]}: {consequent}")
                        var_counter += 1
                    
                    symbolic = f"{var_map[antecedent]} → {var_map[consequent]}"
                    if stmt != conclusion:
                        symbolic_premises.append(symbolic)
                    logger.debug(f"Forma simbólica: {symbolic}")
        
        symbolic_conclusion = "Q"  # Default fallback
        
        result = {
            "premises": symbolic_premises if symbolic_premises else [f"P{i+1}" for i in range(len(premises))],
            "conclusion": symbolic_conclusion,
            "variables": variables if variables else ["P: Proposición 1", "Q: Proposición 2"],
            "notes": ["Conversión básica aplicada debido a error en procesamiento avanzado"]
        }
        
        logger.info(f"✅ Conversión básica completada: {result}")
        return result

    async def _validate_and_prove(self, premises: List[str], conclusion: str, variables: List[str]) -> Dict:
        """Validate argument and generate proof or counterexample"""
        
        prompt = f"""
Eres un experto en lógica proposicional y reglas de inferencia. Tu tarea es determinar si un argumento es válido y generar una prueba deductiva paso a paso o un contraejemplo.

ARGUMENTO:
Variables: {', '.join(variables)}
Premisas: {', '.join(premises)}
Conclusión: {conclusion}

REGLAS DE INFERENCIA DISPONIBLES:
- Modus Ponens: P → Q, P ⊢ Q
- Modus Tollens: P → Q, ¬Q ⊢ ¬P  
- Silogismo Hipotético: P → Q, Q → R ⊢ P → R
- Silogismo Disyuntivo: P ∨ Q, ¬P ⊢ Q
- Conjunción: P, Q ⊢ P ∧ Q
- Simplificación: P ∧ Q ⊢ P (o Q)
- Adición: P ⊢ P ∨ Q
- Resolución: (P ∨ Q), (¬P ∨ R) ⊢ (Q ∨ R)

TAREA:
1. Determina si el argumento es VÁLIDO o INVÁLIDO
2. Si es VÁLIDO: Genera una derivación paso a paso usando las reglas de inferencia
3. Si es INVÁLIDO: Proporciona un contraejemplo con asignaciones de verdad

FORMATO DE RESPUESTA (JSON):
Para argumentos VÁLIDOS:
{{
    "is_valid": true,
    "proof_steps": [
        {{
            "step_number": 1,
            "statement": "premisa textual",
            "symbolic_form": "P → Q",
            "justification": "Premisa",
            "rule_applied": "Premisa",
            "references": []
        }},
        {{
            "step_number": 2,
            "statement": "aplicación de regla",
            "symbolic_form": "Q",
            "justification": "Modus Ponens aplicado a pasos 1 y 2",
            "rule_applied": "Modus Ponens", 
            "references": [1, 2]
        }}
    ]
}}

Para argumentos INVÁLIDOS:
{{
    "is_valid": false,
    "counterexample": {{
        "variable_assignments": {{"P": true, "Q": false}},
        "premises_evaluation": [true, true],
        "conclusion_evaluation": false,
        "explanation": "Cuando P=verdadero y Q=falso, las premisas son verdaderas pero la conclusión es falsa"
    }}
}}

Responde SOLO con el JSON, sin texto adicional.
"""

        try:
            logger.debug(f"Prompt de validación: {prompt[:300]}...")
            
            response = await self._safe_api_call(prompt, "validación")
            
            # Try to parse JSON response
            cleaned_response = response.text.strip()
            logger.debug(f"📝 Respuesta de validación limpiada: {cleaned_response}")
            
            # Remove markdown code blocks if present
            if cleaned_response.startswith('```json'):
                cleaned_response = cleaned_response.replace('```json', '').replace('```', '').strip()
                logger.debug(f"🧹 JSON de validación limpiado de markdown: {cleaned_response}")
            elif cleaned_response.startswith('```'):
                cleaned_response = cleaned_response.replace('```', '').strip()
                logger.debug(f"🧹 JSON de validación limpiado de bloques de código: {cleaned_response}")
            
            result = json.loads(cleaned_response)
            logger.info(f"✅ JSON de validación parseado: {result}")
            
            # Convert to our model format if needed
            if result["is_valid"] and "proof_steps" in result:
                logger.info(f"📋 Procesando {len(result['proof_steps'])} pasos de prueba...")
                proof_steps = []
                for i, step_data in enumerate(result["proof_steps"]):
                    logger.debug(f"Paso {i+1}: {step_data}")
                    
                    # Map unknown rules to known ones or use a default
                    rule_applied = step_data.get("rule_applied")
                    if rule_applied:
                        rule_mapped = self._map_inference_rule(rule_applied)
                        logger.debug(f"Regla '{rule_applied}' mapeada a '{rule_mapped}'")
                    else:
                        rule_mapped = None
                    
                    step = ProofStep(
                        step_number=step_data["step_number"],
                        statement=step_data["statement"],
                        symbolic_form=step_data["symbolic_form"],
                        justification=step_data["justification"],
                        rule_applied=rule_mapped,
                        references=step_data.get("references", [])
                    )
                    proof_steps.append(step)
                result["proof_steps"] = proof_steps
                logger.info("✅ Pasos de prueba procesados correctamente")
            
            elif not result["is_valid"] and "counterexample" in result:
                logger.info("🚫 Procesando contraejemplo...")
                counter_data = result["counterexample"]
                logger.debug(f"Datos del contraejemplo: {counter_data}")
                counterexample = Counterexample(
                    variable_assignments=counter_data["variable_assignments"],
                    premises_evaluation=counter_data["premises_evaluation"],
                    conclusion_evaluation=counter_data["conclusion_evaluation"],
                    explanation=counter_data["explanation"]
                )
                result["counterexample"] = counterexample
                logger.info("✅ Contraejemplo procesado correctamente")
            
            logger.info(f"✅ Validación completada: {'VÁLIDO' if result['is_valid'] else 'INVÁLIDO'}")
            return result
            
        except json.JSONDecodeError as json_error:
            logger.warning(f"⚠️ Error parseando JSON de validación: {json_error}")
            logger.warning(f"Respuesta problemática: {response.text if 'response' in locals() else 'No hay respuesta'}")
            logger.info("🔄 Usando validación básica como fallback...")
            # Fallback: basic validity check
            return self._basic_validity_check(premises, conclusion)
        except Exception as e:
            logger.error(f"❌ Error en validación: {str(e)}")
            logger.exception("Detalles del error:")
            raise Exception(f"Error en validación: {str(e)}")

    def _basic_validity_check(self, premises: List[str], conclusion: str) -> Dict:
        """Basic fallback validity check"""
        logger.info("🔄 Iniciando validación básica (fallback)...")
        
        # Very simple heuristic - if conclusion appears in premises, it's likely valid
        conclusion_clean = conclusion.lower().strip()
        logger.debug(f"Conclusión limpiada: '{conclusion_clean}'")
        
        for i, premise in enumerate(premises):
            logger.debug(f"Comparando con premisa {i+1}: '{premise.lower()}'")
            if conclusion_clean in premise.lower():
                logger.info(f"✅ Conclusión encontrada en premisa {i+1} - marcando como VÁLIDO")
                return {
                    "is_valid": True,
                    "proof_steps": [
                        ProofStep(
                            step_number=1,
                            statement=premise,
                            symbolic_form=premise,
                            justification="Premisa",
                            rule_applied="Premisa",
                            references=[]
                        ),
                        ProofStep(
                            step_number=2,
                            statement=conclusion,
                            symbolic_form=conclusion,
                            justification="Se sigue de la premisa anterior",
                            rule_applied="Simplificación",
                            references=[1]
                        )
                    ]
                }
        
        # Default to invalid with basic counterexample
        logger.info("🚫 No se encontró coincidencia - marcando como INVÁLIDO")
        return {
            "is_valid": False,
            "counterexample": Counterexample(
                variable_assignments={"P": True, "Q": False},
                premises_evaluation=[True],
                conclusion_evaluation=False,
                explanation="Contraejemplo básico: no se pudo establecer la validez del argumento"
            )
        }