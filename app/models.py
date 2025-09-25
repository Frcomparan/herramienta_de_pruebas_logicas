"""
Data models for the logical proofs application
"""

from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from enum import Enum

class InferenceRule(str, Enum):
    """Standard inference rules"""
    MODUS_PONENS = "Modus Ponens"
    MODUS_TOLLENS = "Modus Tollens"
    HYPOTHETICAL_SYLLOGISM = "Silogismo Hipotético"
    DISJUNCTIVE_SYLLOGISM = "Silogismo Disyuntivo"
    CONJUNCTION = "Conjunción"
    SIMPLIFICATION = "Simplificación"
    ADDITION = "Adición"
    CONSTRUCTIVE_DILEMMA = "Dilema Constructivo"
    RESOLUTION = "Resolución"
    PREMISE = "Premisa"

class ProofStep(BaseModel):
    """A single step in a logical proof"""
    step_number: int
    statement: str
    symbolic_form: str
    justification: str
    rule_applied: Optional[InferenceRule] = None
    references: List[int] = []  # References to previous steps

class Counterexample(BaseModel):
    """A counterexample for invalid arguments"""
    variable_assignments: Dict[str, bool]
    premises_evaluation: List[bool]
    conclusion_evaluation: bool
    explanation: str

class ValidationResult(BaseModel):
    """Result of argument validation"""
    is_valid: bool
    symbolic_premises: List[str]
    symbolic_conclusion: str
    proof_steps: Optional[List[ProofStep]] = None
    counterexample: Optional[Counterexample] = None
    variables_identified: List[str] = []
    processing_notes: List[str] = []

class ArgumentRequest(BaseModel):
    """Request model for argument validation"""
    premises: List[str]
    conclusion: str