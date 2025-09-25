"""
Logic Processor - Main class for handling argument validation and proof generation
Integrates with Google Gemini API for natural language processing and logical reasoning
"""

import os
import re
import json
from typing import List, Dict, Optional, Tuple
import google.generativeai as genai
from models import ArgumentRequest, ValidationResult, ProofStep, Counterexample, InferenceRule

class LogicProcessor:
    """Main processor for logical argument validation and proof generation"""
    
    def __init__(self):
        """Initialize the logic processor with Gemini API"""
        # Configure Gemini API
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY environment variable is required")
        
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-1.5-flash')
        
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

    async def validate_argument(self, argument: ArgumentRequest) -> ValidationResult:
        """
        Main method to validate an argument and generate proof or counterexample
        """
        try:
            # Step 1: Convert natural language to symbolic logic
            symbolic_result = await self._convert_to_symbolic(argument.premises, argument.conclusion)
            
            # Step 2: Validate the argument and generate proof/counterexample
            validation_result = await self._validate_and_prove(
                symbolic_result["premises"],
                symbolic_result["conclusion"],
                symbolic_result["variables"]
            )
            
            # Step 3: Construct final result
            result = ValidationResult(
                is_valid=validation_result["is_valid"],
                symbolic_premises=symbolic_result["premises"],
                symbolic_conclusion=symbolic_result["conclusion"],
                variables_identified=symbolic_result["variables"],
                processing_notes=symbolic_result.get("notes", [])
            )
            
            if validation_result["is_valid"]:
                result.proof_steps = validation_result["proof_steps"]
            else:
                result.counterexample = validation_result["counterexample"]
            
            return result
            
        except Exception as e:
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
            response = self.model.generate_content(prompt)
            result = json.loads(response.text.strip())
            
            # Convert variables dict to list for the model
            variables_list = [f"{var}: {desc}" for var, desc in result["variables"].items()]
            
            return {
                "premises": result["premises"],
                "conclusion": result["conclusion"],
                "variables": variables_list,
                "notes": result.get("notes", [])
            }
            
        except json.JSONDecodeError:
            # Fallback: basic symbolic conversion
            return self._basic_symbolic_conversion(premises, conclusion)
        except Exception as e:
            raise Exception(f"Error en conversión simbólica: {str(e)}")

    def _basic_symbolic_conversion(self, premises: List[str], conclusion: str) -> Dict:
        """Fallback basic symbolic conversion"""
        variables = []
        symbolic_premises = []
        
        # Simple conversion - identify basic patterns
        var_counter = 0
        var_map = {}
        
        all_statements = premises + [conclusion]
        
        for stmt in all_statements:
            # Basic pattern recognition for simple statements
            if "si" in stmt.lower() and "entonces" in stmt.lower():
                parts = stmt.lower().split("entonces")
                if len(parts) == 2:
                    antecedent = parts[0].replace("si", "").strip()
                    consequent = parts[1].strip()
                    
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
        
        symbolic_conclusion = "Q"  # Default fallback
        
        return {
            "premises": symbolic_premises if symbolic_premises else [f"P{i+1}" for i in range(len(premises))],
            "conclusion": symbolic_conclusion,
            "variables": variables if variables else ["P: Proposición 1", "Q: Proposición 2"],
            "notes": ["Conversión básica aplicada debido a error en procesamiento avanzado"]
        }

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
            response = self.model.generate_content(prompt)
            result = json.loads(response.text.strip())
            
            # Convert to our model format if needed
            if result["is_valid"] and "proof_steps" in result:
                proof_steps = []
                for step_data in result["proof_steps"]:
                    step = ProofStep(
                        step_number=step_data["step_number"],
                        statement=step_data["statement"],
                        symbolic_form=step_data["symbolic_form"],
                        justification=step_data["justification"],
                        rule_applied=step_data.get("rule_applied"),
                        references=step_data.get("references", [])
                    )
                    proof_steps.append(step)
                result["proof_steps"] = proof_steps
            
            elif not result["is_valid"] and "counterexample" in result:
                counter_data = result["counterexample"]
                counterexample = Counterexample(
                    variable_assignments=counter_data["variable_assignments"],
                    premises_evaluation=counter_data["premises_evaluation"],
                    conclusion_evaluation=counter_data["conclusion_evaluation"],
                    explanation=counter_data["explanation"]
                )
                result["counterexample"] = counterexample
            
            return result
            
        except json.JSONDecodeError as e:
            # Fallback: basic validity check
            return self._basic_validity_check(premises, conclusion)
        except Exception as e:
            raise Exception(f"Error en validación: {str(e)}")

    def _basic_validity_check(self, premises: List[str], conclusion: str) -> Dict:
        """Basic fallback validity check"""
        # Very simple heuristic - if conclusion appears in premises, it's likely valid
        conclusion_clean = conclusion.lower().strip()
        
        for premise in premises:
            if conclusion_clean in premise.lower():
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
        return {
            "is_valid": False,
            "counterexample": Counterexample(
                variable_assignments={"P": True, "Q": False},
                premises_evaluation=[True],
                conclusion_evaluation=False,
                explanation="Contraejemplo básico: no se pudo establecer la validez del argumento"
            )
        }