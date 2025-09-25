"""
Casos de Prueba Completos para la Herramienta de Pruebas Lógicas
Incluye argumentos válidos e inválidos con sus justificaciones esperadas
"""

from typing import Dict, List, Any
from dataclasses import dataclass

@dataclass
class TestCase:
    """Estructura para definir un caso de prueba"""
    name: str
    category: str  # "valid" or "invalid"
    premises: List[str]
    conclusion: str
    expected_symbolic_premises: List[str]
    expected_symbolic_conclusion: str
    expected_justification: str
    inference_rule: str = None  # Para casos válidos
    fallacy_type: str = None    # Para casos inválidos
    description: str = ""

# ===============================
# CASOS DE PRUEBA VÁLIDOS ✅
# ===============================

VALID_TEST_CASES = [
    TestCase(
        name="Caso 1: Modus Ponens Clásico",
        category="valid",
        premises=[
            "Si la alarma suena, entonces hay un incendio",
            "La alarma está sonando"
        ],
        conclusion="Hay un incendio",
        expected_symbolic_premises=["P → Q", "P"],
        expected_symbolic_conclusion="Q",
        expected_justification="Derivación directa usando la regla de Modus Ponens",
        inference_rule="Modus Ponens",
        description="Afirmación del antecedente - forma más básica de inferencia válida"
    ),

    TestCase(
        name="Caso 2: Modus Tollens Clásico",
        category="valid",
        premises=[
            "Si el sol brilla, no necesito la linterna",
            "Necesito la linterna"
        ],
        conclusion="El sol no brilla",
        expected_symbolic_premises=["P → ¬Q", "Q"],
        expected_symbolic_conclusion="¬P",
        expected_justification="Derivación usando la regla de Modus Tollens",
        inference_rule="Modus Tollens",
        description="Negación del consecuente - inferencia por contraposición"
    ),

    TestCase(
        name="Caso 3: Silogismo Hipotético",
        category="valid",
        premises=[
            "Si hago ejercicio, me sentiré con energía",
            "Si me siento con energía, tendré un día productivo"
        ],
        conclusion="Si hago ejercicio, tendré un día productivo",
        expected_symbolic_premises=["P → Q", "Q → R"],
        expected_symbolic_conclusion="P → R",
        expected_justification="Prueba por Silogismo Hipotético - cadena de implicaciones",
        inference_rule="Silogismo Hipotético",
        description="Transitividad de la implicación"
    ),

    TestCase(
        name="Caso 4: Silogismo Disyuntivo",
        category="valid",
        premises=[
            "La reunión es hoy o es mañana",
            "La reunión no es hoy"
        ],
        conclusion="La reunión es mañana",
        expected_symbolic_premises=["P ∨ Q", "¬P"],
        expected_symbolic_conclusion="Q",
        expected_justification="Derivación por Silogismo Disyuntivo - proceso de eliminación",
        inference_rule="Silogismo Disyuntivo",
        description="Eliminación de alternativas en disyunción"
    ),

    TestCase(
        name="Caso 5: Dilema Constructivo",
        category="valid",
        premises=[
            "Si llueve, me quedaré en casa",
            "Si hace sol, iré a la playa",
            "O llueve o hace sol"
        ],
        conclusion="O me quedaré en casa o iré a la playa",
        expected_symbolic_premises=["P → Q", "R → S", "P ∨ R"],
        expected_symbolic_conclusion="Q ∨ S",
        expected_justification="Prueba compleja usando Dilema Constructivo",
        inference_rule="Dilema Constructivo",
        description="Elección entre consecuencias basada en alternativas"
    ),

    TestCase(
        name="Caso 6: Conjunción y Simplificación",
        category="valid",
        premises=[
            "María estudia matemáticas",
            "María estudia física"
        ],
        conclusion="María estudia matemáticas y física",
        expected_symbolic_premises=["P", "Q"],
        expected_symbolic_conclusion="P ∧ Q",
        expected_justification="Aplicación de la regla de Conjunción",
        inference_rule="Conjunción",
        description="Combinación de proposiciones verdaderas"
    ),

    TestCase(
        name="Caso 7: Adición Lógica",
        category="valid",
        premises=[
            "Juan tiene una bicicleta"
        ],
        conclusion="Juan tiene una bicicleta o tiene un automóvil",
        expected_symbolic_premises=["P"],
        expected_symbolic_conclusion="P ∨ Q",
        expected_justification="Aplicación de la regla de Adición",
        inference_rule="Adición",
        description="Una proposición verdadera implica su disyunción con cualquier otra"
    ),

    TestCase(
        name="Caso 8: Modus Ponens Complejo (3 premisas)",
        category="valid",
        premises=[
            "Si trabajo duro y tengo suerte, entonces tendré éxito",
            "Trabajo duro",
            "Tengo suerte"
        ],
        conclusion="Tendré éxito",
        expected_symbolic_premises=["(P ∧ Q) → R", "P", "Q"],
        expected_symbolic_conclusion="R",
        expected_justification="Modus Ponens con antecedente compuesto",
        inference_rule="Modus Ponens",
        description="Modus Ponens aplicado a una conjunción en el antecedente"
    ),

    TestCase(
        name="Caso 9: Silogismo Disyuntivo Doble",
        category="valid",
        premises=[
            "El problema está en el hardware o en el software",
            "El problema no está en el hardware",
            "Si el problema está en el software, necesitamos reinstalar"
        ],
        conclusion="Necesitamos reinstalar",
        expected_symbolic_premises=["P ∨ Q", "¬P", "Q → R"],
        expected_symbolic_conclusion="R",
        expected_justification="Combinación de Silogismo Disyuntivo y Modus Ponens",
        inference_rule="Combinación de reglas",
        description="Aplicación secuencial de múltiples reglas de inferencia"
    ),

    TestCase(
        name="Caso 10: Simplificación de Conjunción",
        category="valid",
        premises=[
            "Ana es inteligente y trabajadora",
            "Si Ana es inteligente, entonces obtendrá buenas calificaciones"
        ],
        conclusion="Ana obtendrá buenas calificaciones",
        expected_symbolic_premises=["P ∧ Q", "P → R"],
        expected_symbolic_conclusion="R",
        expected_justification="Simplificación seguida de Modus Ponens",
        inference_rule="Simplificación + Modus Ponens",
        description="Extracción de componente de conjunción seguida de inferencia"
    ),

    TestCase(
        name="Caso 11: Cadena de Modus Tollens",
        category="valid",
        premises=[
            "Si el servidor funciona, entonces la aplicación responde",
            "Si la aplicación responde, entonces los usuarios pueden acceder",
            "Los usuarios no pueden acceder"
        ],
        conclusion="El servidor no funciona",
        expected_symbolic_premises=["P → Q", "Q → R", "¬R"],
        expected_symbolic_conclusion="¬P",
        expected_justification="Cadena de Modus Tollens aplicado dos veces",
        inference_rule="Modus Tollens en cadena",
        description="Aplicación transitiva de Modus Tollens"
    ),

    TestCase(
        name="Caso 12: Resolución Simple",
        category="valid",
        premises=[
            "Carlos va al cine o estudia en casa",
            "Carlos no va al cine o termina su proyecto",
            "Carlos no estudia en casa"
        ],
        conclusion="Carlos termina su proyecto",
        expected_symbolic_premises=["P ∨ Q", "¬P ∨ R", "¬Q"],
        expected_symbolic_conclusion="R",
        expected_justification="Aplicación de la regla de Resolución",
        inference_rule="Resolución",
        description="Eliminación de variables complementarias"
    )
]

# ===============================
# CASOS DE PRUEBA INVÁLIDOS ❌
# ===============================

INVALID_TEST_CASES = [
    TestCase(
        name="Caso 13: Falacia de Afirmación del Consecuente",
        category="invalid",
        premises=[
            "Si un animal es un perro, entonces es un mamífero",
            "Mi mascota es un mamífero"
        ],
        conclusion="Mi mascota es un perro",
        expected_symbolic_premises=["P → Q", "Q"],
        expected_symbolic_conclusion="P",
        expected_justification="Contraejemplo: P=Falso, Q=Verdadero. La mascota podría ser un gato",
        fallacy_type="Afirmación del Consecuente",
        description="Error al invertir incorrectamente una implicación"
    ),

    TestCase(
        name="Caso 14: Falacia de Negación del Antecedente",
        category="invalid",
        premises=[
            "Si obtienes la nacionalidad, entonces puedes votar",
            "No obtuviste la nacionalidad"
        ],
        conclusion="No puedes votar",
        expected_symbolic_premises=["P → Q", "¬P"],
        expected_symbolic_conclusion="¬Q",
        expected_justification="Contraejemplo: P=Falso, Q=Verdadero. Podrías votar por otra razón",
        fallacy_type="Negación del Antecedente",
        description="Error al negar incorrectamente una implicación"
    ),

    TestCase(
        name="Caso 15: Non Sequitur",
        category="invalid",
        premises=[
            "Todos los planetas giran alrededor del sol",
            "La Tierra es un planeta"
        ],
        conclusion="Por lo tanto, la luna está hecha de queso",
        expected_symbolic_premises=["P", "Q"],
        expected_symbolic_conclusion="R",
        expected_justification="Contraejemplo: P=Verdadero, Q=Verdadero, R=Falso. La conclusión es irrelevante",
        fallacy_type="Non Sequitur",
        description="La conclusión no tiene relación lógica con las premisas"
    ),

    TestCase(
        name="Caso 16: Silogismo Disyuntivo Falaz",
        category="invalid",
        premises=[
            "Un requisito para el trabajo es tener un título universitario o tener 5 años de experiencia",
            "Juan tiene un título universitario"
        ],
        conclusion="Por lo tanto, Juan no tiene 5 años de experiencia",
        expected_symbolic_premises=["P ∨ Q", "P"],
        expected_symbolic_conclusion="¬Q",
        expected_justification="Contraejemplo: P=Verdadero, Q=Verdadero. Juan podría tener ambas cosas",
        fallacy_type="Falsa Dicotomía",
        description="Malinterpretación del 'o' inclusivo como exclusivo"
    ),

    TestCase(
        name="Caso 17: Generalización Apresurada",
        category="invalid",
        premises=[
            "Pedro es mexicano y es chef",
            "Roberto es mexicano y es chef"
        ],
        conclusion="Todos los mexicanos son chefs",
        expected_symbolic_premises=["P ∧ Q", "R ∧ S"],
        expected_symbolic_conclusion="∀x (Mx → Cx)",
        expected_justification="Contraejemplo: Existen mexicanos que no son chefs",
        fallacy_type="Generalización Apresurada",
        description="Conclusión general basada en casos particulares insuficientes"
    ),

    TestCase(
        name="Caso 18: Conversión Ilícita",
        category="invalid",
        premises=[
            "Todos los médicos son inteligentes",
            "Ana es inteligente"
        ],
        conclusion="Ana es médico",
        expected_symbolic_premises=["∀x (Mx → Ix)", "Ia"],
        expected_symbolic_conclusion="Ma",
        expected_justification="Contraejemplo: Ana podría ser inteligente sin ser médico",
        fallacy_type="Conversión Ilícita",
        description="Error al convertir una proposición universal"
    ),

    TestCase(
        name="Caso 19: Falso Dilema",
        category="invalid",
        premises=[
            "O estudias medicina o no tendrás un buen futuro",
            "No estudias medicina"
        ],
        conclusion="No tendrás un buen futuro",
        expected_symbolic_premises=["P ∨ ¬Q", "¬P"],
        expected_symbolic_conclusion="¬Q",
        expected_justification="Contraejemplo: Existen otras carreras que pueden dar un buen futuro",
        fallacy_type="Falso Dilema",
        description="Presentación de solo dos alternativas cuando existen más"
    ),

    TestCase(
        name="Caso 20: Composición Falaz",
        category="invalid",
        premises=[
            "Cada jugador del equipo es excelente",
            "Un equipo está formado por jugadores"
        ],
        conclusion="El equipo es excelente",
        expected_symbolic_premises=["∀x (Jx → Ex)", "E es conjunto de J"],
        expected_symbolic_conclusion="Ee",
        expected_justification="Contraejemplo: Jugadores excelentes individuales pueden no trabajar bien en equipo",
        fallacy_type="Falacia de Composición",
        description="Error al atribuir al todo las propiedades de las partes"
    ),

    TestCase(
        name="Caso 21: Argumento Circular",
        category="invalid",
        premises=[
            "Dios existe porque lo dice la Biblia",
            "La Biblia es verdadera porque es palabra de Dios"
        ],
        conclusion="Por lo tanto, Dios existe",
        expected_symbolic_premises=["P porque Q", "Q porque P"],
        expected_symbolic_conclusion="P",
        expected_justification="Razonamiento circular: la conclusión se usa para justificar las premisas",
        fallacy_type="Petición de Principio",
        description="La conclusión se asume en las premisas"
    ),

    TestCase(
        name="Caso 22: Falacia del Hombre de Paja",
        category="invalid",
        premises=[
            "María dice que deberíamos reducir el presupuesto militar",
            "María quiere eliminar completamente el ejército"
        ],
        conclusion="La propuesta de María es peligrosa para la seguridad nacional",
        expected_symbolic_premises=["P propone reducir", "P propone eliminar"],
        expected_symbolic_conclusion="P es peligrosa",
        expected_justification="Distorsión del argumento original: reducir ≠ eliminar",
        fallacy_type="Hombre de Paja",
        description="Distorsión de la posición del oponente para refutarla más fácilmente"
    ),

    TestCase(
        name="Caso 23: Post Hoc Ergo Propter Hoc",
        category="invalid",
        premises=[
            "Ayer rompí un espejo",
            "Hoy tuve mala suerte"
        ],
        conclusion="Romper el espejo causó mi mala suerte",
        expected_symbolic_premises=["P ocurrió antes", "Q ocurrió después"],
        expected_symbolic_conclusion="P causó Q",
        expected_justification="Correlación temporal no implica causación",
        fallacy_type="Post Hoc",
        description="Confundir secuencia temporal con relación causal"
    ),

    TestCase(
        name="Caso 24: Apelación a la Autoridad Falaz",
        category="invalid",
        premises=[
            "Einstein era un genio de la física",
            "Einstein creía en Dios"
        ],
        conclusion="Por lo tanto, Dios existe",
        expected_symbolic_premises=["P es experto en física", "P cree Q"],
        expected_symbolic_conclusion="Q es verdad",
        expected_justification="La autoridad en un campo no implica autoridad en todos los campos",
        fallacy_type="Apelación a la Autoridad Inapropiada",
        description="Apelar a autoridad fuera de su área de expertise"
    )
]

# ===============================
# FUNCIONES AUXILIARES
# ===============================

def get_all_test_cases() -> List[TestCase]:
    """Retorna todos los casos de prueba"""
    return VALID_TEST_CASES + INVALID_TEST_CASES

def get_valid_cases() -> List[TestCase]:
    """Retorna solo los casos válidos"""
    return VALID_TEST_CASES

def get_invalid_cases() -> List[TestCase]:
    """Retorna solo los casos inválidos"""
    return INVALID_TEST_CASES

def get_case_by_name(name: str) -> TestCase:
    """Busca un caso por nombre"""
    all_cases = get_all_test_cases()
    for case in all_cases:
        if case.name == name:
            return case
    raise ValueError(f"Caso de prueba '{name}' no encontrado")

def print_test_case_summary():
    """Imprime un resumen de todos los casos de prueba"""
    valid_cases = get_valid_cases()
    invalid_cases = get_invalid_cases()
    
    print("=" * 60)
    print("RESUMEN DE CASOS DE PRUEBA - HERRAMIENTA DE PRUEBAS LÓGICAS")
    print("=" * 60)
    print(f"Total de casos: {len(get_all_test_cases())}")
    print(f"Casos válidos: {len(valid_cases)}")
    print(f"Casos inválidos: {len(invalid_cases)}")
    print()
    
    print("CASOS VÁLIDOS ✅:")
    print("-" * 40)
    for i, case in enumerate(valid_cases, 1):
        print(f"{i:2d}. {case.name}")
        print(f"    Regla: {case.inference_rule}")
        print(f"    Premisas: {len(case.premises)}")
        print()
    
    print("CASOS INVÁLIDOS ❌:")
    print("-" * 40)
    for i, case in enumerate(invalid_cases, 1):
        print(f"{i:2d}. {case.name}")
        print(f"    Falacia: {case.fallacy_type}")
        print(f"    Premisas: {len(case.premises)}")
        print()

def export_cases_for_testing() -> List[Dict[str, Any]]:
    """Exporta los casos en formato dict para testing automatizado"""
    cases = []
    for test_case in get_all_test_cases():
        cases.append({
            "name": test_case.name,
            "category": test_case.category,
            "premises": test_case.premises,
            "conclusion": test_case.conclusion,
            "expected_valid": test_case.category == "valid",
            "description": test_case.description
        })
    return cases

if __name__ == "__main__":
    # Mostrar resumen cuando se ejecuta el script directamente
    print_test_case_summary()