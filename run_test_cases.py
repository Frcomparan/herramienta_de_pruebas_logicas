"""
Script para ejecutar pruebas manuales de los casos de prueba
Permite probar casos individuales contra la aplicación real
"""

import asyncio
import sys
import os
import json
from typing import Dict, Any, List

# Add the app directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

from test_cases import get_all_test_cases, get_valid_cases, get_invalid_cases, TestCase
from models import ArgumentRequest, ValidationResult
from logic_processor import LogicProcessor

class TestRunner:
    """Ejecutor de pruebas para casos predefinidos"""
    
    def __init__(self):
        self.processor = None
        self.results = []
        
    async def initialize(self):
        """Inicializar el procesador lógico"""
        try:
            self.processor = LogicProcessor()
            print("✅ Procesador lógico inicializado correctamente")
            return True
        except Exception as e:
            print(f"❌ Error inicializando procesador: {e}")
            print("💡 Asegúrate de tener configurada la GEMINI_API_KEY")
            return False
    
    async def run_single_case(self, test_case: TestCase) -> Dict[str, Any]:
        """Ejecutar un caso de prueba individual"""
        print(f"\n🔍 Ejecutando: {test_case.name}")
        print(f"📝 Descripción: {test_case.description}")
        print(f"📊 Categoría: {test_case.category}")
        print(f"📋 Premisas ({len(test_case.premises)}):")
        
        for i, premise in enumerate(test_case.premises, 1):
            print(f"   {i}. {premise}")
        
        print(f"🎯 Conclusión: {test_case.conclusion}")
        print(f"🔬 Esperado: {'VÁLIDO' if test_case.category == 'valid' else 'INVÁLIDO'}")
        
        try:
            # Crear request y procesar
            request = ArgumentRequest(
                premises=test_case.premises,
                conclusion=test_case.conclusion
            )
            
            print("⏳ Procesando...")
            result = await self.processor.validate_argument(request)
            
            # Analizar resultado
            actual_valid = result.is_valid
            expected_valid = test_case.category == "valid"
            is_correct = actual_valid == expected_valid
            
            print(f"📊 Resultado: {'VÁLIDO' if actual_valid else 'INVÁLIDO'}")
            print(f"✅ Correcto: {'SÍ' if is_correct else 'NO'}")
            
            if result.symbolic_premises:
                print(f"🔤 Simbólico Premisas: {result.symbolic_premises}")
            if result.symbolic_conclusion:
                print(f"🔤 Simbólico Conclusión: {result.symbolic_conclusion}")
            
            if result.is_valid and result.proof_steps:
                print("📝 Prueba generada:")
                for step in result.proof_steps:
                    print(f"   {step.step_number}. {step.statement} [{step.rule_applied}]")
            
            if not result.is_valid and result.counterexample:
                print("🚫 Contraejemplo generado:")
                print(f"   Variables: {result.counterexample.variable_assignments}")
                print(f"   Explicación: {result.counterexample.explanation}")
            
            test_result = {
                "name": test_case.name,
                "category": test_case.category,
                "expected_valid": expected_valid,
                "actual_valid": actual_valid,
                "is_correct": is_correct,
                "symbolic_premises": result.symbolic_premises,
                "symbolic_conclusion": result.symbolic_conclusion,
                "has_proof": bool(result.proof_steps),
                "has_counterexample": bool(result.counterexample),
                "processing_notes": result.processing_notes
            }
            
            self.results.append(test_result)
            return test_result
            
        except Exception as e:
            print(f"❌ Error ejecutando caso: {e}")
            error_result = {
                "name": test_case.name,
                "category": test_case.category,
                "expected_valid": expected_valid,
                "actual_valid": None,
                "is_correct": False,
                "error": str(e)
            }
            self.results.append(error_result)
            return error_result
    
    async def run_multiple_cases(self, cases: List[TestCase], stop_on_error: bool = False):
        """Ejecutar múltiples casos de prueba"""
        print(f"\n🚀 Ejecutando {len(cases)} casos de prueba...")
        print("=" * 60)
        
        for i, case in enumerate(cases, 1):
            print(f"\n[{i}/{len(cases)}] " + "=" * 40)
            
            result = await self.run_single_case(case)
            
            if stop_on_error and result.get("error"):
                print("\n⚠️ Deteniendo ejecución por error")
                break
            
            # Pausa breve para evitar rate limiting
            await asyncio.sleep(1)
    
    def print_summary(self):
        """Imprimir resumen de resultados"""
        if not self.results:
            print("\n📊 No hay resultados para mostrar")
            return
        
        print("\n" + "=" * 60)
        print("📊 RESUMEN DE RESULTADOS")
        print("=" * 60)
        
        total = len(self.results)
        correct = sum(1 for r in self.results if r.get("is_correct", False))
        errors = sum(1 for r in self.results if "error" in r)
        
        print(f"📋 Total de casos: {total}")
        print(f"✅ Casos correctos: {correct}")
        print(f"❌ Casos incorrectos: {total - correct - errors}")
        print(f"💥 Errores: {errors}")
        print(f"📈 Precisión: {(correct/total)*100:.1f}%" if total > 0 else "N/A")
        
        # Desglose por categoría
        valid_results = [r for r in self.results if r.get("category") == "valid"]
        invalid_results = [r for r in self.results if r.get("category") == "invalid"]
        
        if valid_results:
            valid_correct = sum(1 for r in valid_results if r.get("is_correct", False))
            print(f"\n📊 Casos VÁLIDOS: {valid_correct}/{len(valid_results)} correctos")
        
        if invalid_results:
            invalid_correct = sum(1 for r in invalid_results if r.get("is_correct", False))
            print(f"📊 Casos INVÁLIDOS: {invalid_correct}/{len(invalid_results)} correctos")
        
        # Casos incorrectos
        incorrect = [r for r in self.results if not r.get("is_correct", False) and "error" not in r]
        if incorrect:
            print(f"\n⚠️ CASOS INCORRECTOS:")
            for r in incorrect:
                expected = "VÁLIDO" if r.get("expected_valid") else "INVÁLIDO"
                actual = "VÁLIDO" if r.get("actual_valid") else "INVÁLIDO"
                print(f"   • {r['name']}: Esperado {expected}, Obtenido {actual}")
    
    def save_results(self, filename: str = "test_results.json"):
        """Guardar resultados en archivo JSON"""
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(self.results, f, indent=2, ensure_ascii=False)
            print(f"\n💾 Resultados guardados en: {filename}")
        except Exception as e:
            print(f"\n❌ Error guardando resultados: {e}")


async def main():
    """Función principal"""
    print("🧠 HERRAMIENTA DE PRUEBAS LÓGICAS - EJECUTOR DE CASOS DE PRUEBA")
    print("=" * 60)
    
    runner = TestRunner()
    
    if not await runner.initialize():
        print("\n❌ No se pudo inicializar. Verifica la configuración de la API.")
        return
    
    while True:
        print("\n🎯 OPCIONES:")
        print("1. 📋 Ejecutar todos los casos de prueba")
        print("2. ✅ Ejecutar solo casos válidos")
        print("3. ❌ Ejecutar solo casos inválidos") 
        print("4. 🔍 Ejecutar caso específico")
        print("5. 📊 Ver resumen de casos disponibles")
        print("6. 💾 Guardar últimos resultados")
        print("7. 🚪 Salir")
        
        try:
            choice = input("\n👉 Selecciona una opción (1-7): ").strip()
            
            if choice == "1":
                cases = get_all_test_cases()
                await runner.run_multiple_cases(cases)
                runner.print_summary()
                
            elif choice == "2":
                cases = get_valid_cases()
                await runner.run_multiple_cases(cases)
                runner.print_summary()
                
            elif choice == "3":
                cases = get_invalid_cases()
                await runner.run_multiple_cases(cases)
                runner.print_summary()
                
            elif choice == "4":
                cases = get_all_test_cases()
                print("\n📋 Casos disponibles:")
                for i, case in enumerate(cases, 1):
                    status = "✅" if case.category == "valid" else "❌"
                    print(f"{i:2d}. {status} {case.name}")
                
                try:
                    case_num = int(input(f"\n👉 Selecciona un caso (1-{len(cases)}): "))
                    if 1 <= case_num <= len(cases):
                        await runner.run_single_case(cases[case_num - 1])
                    else:
                        print("❌ Número de caso inválido")
                except ValueError:
                    print("❌ Por favor ingresa un número válido")
                    
            elif choice == "5":
                from test_cases import print_test_case_summary
                print_test_case_summary()
                
            elif choice == "6":
                runner.save_results()
                
            elif choice == "7":
                print("\n👋 ¡Hasta luego!")
                break
                
            else:
                print("❌ Opción inválida")
                
        except KeyboardInterrupt:
            print("\n\n👋 Interrumpido por el usuario. ¡Hasta luego!")
            break
        except Exception as e:
            print(f"\n❌ Error inesperado: {e}")


if __name__ == "__main__":
    # Verificar que existe el archivo .env
    if not os.path.exists(".env"):
        print("❌ Archivo .env no encontrado.")
        print("💡 Copia .env.template a .env y configura tu GEMINI_API_KEY")
        print("📖 Consulta README.md para más información")
        sys.exit(1)
    
    # Ejecutar
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n👋 ¡Hasta luego!")
    except Exception as e:
        print(f"❌ Error crítico: {e}")
        sys.exit(1)