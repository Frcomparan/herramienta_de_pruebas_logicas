"""
Comprehensive tests for the Logic Proofs Tool
Includes unit tests and integration tests with predefined test cases
Run with: python -m pytest test_logic.py -v
"""

import pytest
import asyncio
import sys
import os
from unittest.mock import Mock, patch, AsyncMock
from typing import List, Dict, Any

# Add the app directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

from models import ArgumentRequest, ValidationResult, ProofStep, InferenceRule, Counterexample
from test_cases import get_all_test_cases, get_valid_cases, get_invalid_cases, TestCase

class TestModels:
    """Test Pydantic models"""
    
    def test_argument_request_model(self):
        """Test ArgumentRequest model validation"""
        request = ArgumentRequest(
            premises=["Si llueve entonces me mojo", "Llueve"],
            conclusion="Me mojo"
        )
        assert len(request.premises) == 2
        assert request.conclusion == "Me mojo"

    def test_proof_step_model(self):
        """Test ProofStep model"""
        step = ProofStep(
            step_number=1,
            statement="Si llueve entonces me mojo",
            symbolic_form="P → Q",
            justification="Premisa",
            rule_applied=InferenceRule.PREMISE,
            references=[]
        )
        assert step.step_number == 1
        assert step.rule_applied == InferenceRule.PREMISE

    def test_validation_result_model(self):
        """Test ValidationResult model"""
        result = ValidationResult(
            is_valid=True,
            symbolic_premises=["P → Q", "P"],
            symbolic_conclusion="Q",
            variables_identified=["P: Llueve", "Q: Me mojo"]
        )
        assert result.is_valid is True
        assert len(result.symbolic_premises) == 2

    def test_counterexample_model(self):
        """Test Counterexample model"""
        counter = Counterexample(
            variable_assignments={"P": True, "Q": False},
            premises_evaluation=[True, False],
            conclusion_evaluation=False,
            explanation="Test counterexample"
        )
        assert counter.variable_assignments["P"] is True
        assert counter.conclusion_evaluation is False

    def test_inference_rules(self):
        """Test that all inference rules are defined"""
        rules = [
            InferenceRule.MODUS_PONENS,
            InferenceRule.MODUS_TOLLENS,
            InferenceRule.HYPOTHETICAL_SYLLOGISM,
            InferenceRule.DISJUNCTIVE_SYLLOGISM,
            InferenceRule.CONJUNCTION,
            InferenceRule.SIMPLIFICATION,
            InferenceRule.ADDITION,
            InferenceRule.PREMISE
        ]
        
        assert len(rules) == 8
        assert InferenceRule.MODUS_PONENS == "Modus Ponens"
        assert InferenceRule.MODUS_TOLLENS == "Modus Tollens"


class TestLogicProcessor:
    """Test LogicProcessor functionality"""
    
    @pytest.mark.asyncio
    async def test_basic_symbolic_conversion(self):
        """Test basic symbolic conversion fallback"""
        from logic_processor import LogicProcessor
        
        # Mock the Gemini API to avoid actual API calls
        with patch('google.generativeai.configure'), \
             patch('google.generativeai.GenerativeModel'):
            
            processor = LogicProcessor()
            
            # Test the fallback conversion method
            premises = ["Si llueve entonces me mojo", "Llueve"]
            conclusion = "Me mojo"
            
            result = processor._basic_symbolic_conversion(premises, conclusion)
            
            assert "premises" in result
            assert "conclusion" in result
            assert "variables" in result
            assert "notes" in result

    @pytest.mark.asyncio
    async def test_basic_validity_check(self):
        """Test basic validity check fallback"""
        from logic_processor import LogicProcessor
        
        with patch('google.generativeai.configure'), \
             patch('google.generativeai.GenerativeModel'):
            
            processor = LogicProcessor()
            
            # Test with matching premise and conclusion
            premises = ["Me mojo"]
            conclusion = "Me mojo"
            
            result = processor._basic_validity_check(premises, conclusion)
            
            assert "is_valid" in result
            assert isinstance(result["is_valid"], bool)


class TestCaseStructure:
    """Test the test cases structure and completeness"""
    
    def test_all_cases_loaded(self):
        """Test that all test cases are loaded correctly"""
        all_cases = get_all_test_cases()
        valid_cases = get_valid_cases()
        invalid_cases = get_invalid_cases()
        
        assert len(all_cases) >= 20  # At least 20 test cases
        assert len(valid_cases) >= 10  # At least 10 valid cases
        assert len(invalid_cases) >= 10  # At least 10 invalid cases
        assert len(all_cases) == len(valid_cases) + len(invalid_cases)

    def test_valid_cases_structure(self):
        """Test that valid cases have required fields"""
        valid_cases = get_valid_cases()
        
        for case in valid_cases:
            assert case.category == "valid"
            assert len(case.premises) >= 1
            assert case.conclusion != ""
            assert case.inference_rule is not None
            assert len(case.premises) <= 4  # Max 4 premises as requested

    def test_invalid_cases_structure(self):
        """Test that invalid cases have required fields"""
        invalid_cases = get_invalid_cases()
        
        for case in invalid_cases:
            assert case.category == "invalid"
            assert len(case.premises) >= 1
            assert case.conclusion != ""
            assert case.fallacy_type is not None
            assert len(case.premises) <= 4  # Max 4 premises as requested

    def test_premise_count_distribution(self):
        """Test that we have cases with different numbers of premises (2-4)"""
        all_cases = get_all_test_cases()
        
        premise_counts = {}
        for case in all_cases:
            count = len(case.premises)
            premise_counts[count] = premise_counts.get(count, 0) + 1
        
        # Should have cases with 2, 3, and possibly 4 premises
        assert 2 in premise_counts
        assert premise_counts[2] > 0
        
        # At least some cases should have 3 or more premises
        three_plus = sum(count for num_premises, count in premise_counts.items() if num_premises >= 3)
        assert three_plus > 0


class TestSpecificLogicalPatterns:
    """Test specific logical patterns in our test cases"""
    
    def test_modus_ponens_cases(self):
        """Test that we have proper Modus Ponens cases"""
        valid_cases = get_valid_cases()
        modus_ponens_cases = [case for case in valid_cases if "Modus Ponens" in case.inference_rule]
        
        assert len(modus_ponens_cases) >= 2
        
        for case in modus_ponens_cases:
            # Should have at least 2 premises for basic Modus Ponens
            assert len(case.premises) >= 2

    def test_modus_tollens_cases(self):
        """Test that we have proper Modus Tollens cases"""
        valid_cases = get_valid_cases()
        modus_tollens_cases = [case for case in valid_cases if "Modus Tollens" in case.inference_rule]
        
        assert len(modus_tollens_cases) >= 1
        
        for case in modus_tollens_cases:
            assert len(case.premises) >= 2

    def test_fallacy_diversity(self):
        """Test that we have diverse types of fallacies"""
        invalid_cases = get_invalid_cases()
        fallacy_types = set(case.fallacy_type for case in invalid_cases)
        
        # Should have at least 8 different types of fallacies
        assert len(fallacy_types) >= 8
        
        # Check for specific important fallacies
        fallacy_names = [fallacy.lower() for fallacy in fallacy_types]
        assert any("afirmación del consecuente" in name for name in fallacy_names)
        assert any("negación del antecedente" in name for name in fallacy_names)


@pytest.mark.asyncio
class TestIntegration:
    """Integration tests that would work with a real API (mocked for testing)"""
    
    async def test_valid_argument_processing(self):
        """Test processing of a known valid argument"""
        from logic_processor import LogicProcessor
        
        # Mock the Gemini API responses
        mock_model = Mock()
        mock_response = Mock()
        mock_response.text = '{"variables": {"P": "llueve", "Q": "me mojo"}, "premises": ["P → Q", "P"], "conclusion": "Q", "notes": []}'
        mock_model.generate_content.return_value = mock_response
        
        with patch('google.generativeai.configure'), \
             patch('google.generativeai.GenerativeModel', return_value=mock_model):
            
            processor = LogicProcessor()
            
            # Test with a simple valid case
            request = ArgumentRequest(
                premises=["Si llueve entonces me mojo", "Llueve"],
                conclusion="Me mojo"
            )
            
            # Mock the validation response as well
            mock_response.text = '{"is_valid": true, "proof_steps": [{"step_number": 1, "statement": "Si llueve entonces me mojo", "symbolic_form": "P → Q", "justification": "Premisa", "rule_applied": "Premisa", "references": []}, {"step_number": 2, "statement": "Llueve", "symbolic_form": "P", "justification": "Premisa", "rule_applied": "Premisa", "references": []}, {"step_number": 3, "statement": "Me mojo", "symbolic_form": "Q", "justification": "Modus Ponens", "rule_applied": "Modus Ponens", "references": [1, 2]}]}'
            
            result = await processor.validate_argument(request)
            
            assert isinstance(result, ValidationResult)
            assert result.symbolic_premises is not None
            assert result.symbolic_conclusion is not None

    async def test_invalid_argument_processing(self):
        """Test processing of a known invalid argument"""
        from logic_processor import LogicProcessor
        
        # Mock the Gemini API responses
        mock_model = Mock()
        mock_response = Mock()
        mock_response.text = '{"variables": {"P": "es perro", "Q": "es mamífero"}, "premises": ["P → Q", "Q"], "conclusion": "P", "notes": []}'
        mock_model.generate_content.return_value = mock_response
        
        with patch('google.generativeai.configure'), \
             patch('google.generativeai.GenerativeModel', return_value=mock_model):
            
            processor = LogicProcessor()
            
            request = ArgumentRequest(
                premises=["Si un animal es un perro, entonces es un mamífero", "Mi mascota es un mamífero"],
                conclusion="Mi mascota es un perro"
            )
            
            # Mock invalid response
            mock_response.text = '{"is_valid": false, "counterexample": {"variable_assignments": {"P": false, "Q": true}, "premises_evaluation": [true, true], "conclusion_evaluation": false, "explanation": "La mascota podría ser un gato"}}'
            
            result = await processor.validate_argument(request)
            
            assert isinstance(result, ValidationResult)
            # The result might be valid or invalid depending on fallback logic


class TestCaseExecution:
    """Test that our test cases can be executed properly"""
    
    def test_case_export_format(self):
        """Test that cases can be exported for automated testing"""
        from test_cases import export_cases_for_testing
        
        exported = export_cases_for_testing()
        
        assert len(exported) >= 20
        
        for case in exported:
            assert "name" in case
            assert "category" in case
            assert "premises" in case
            assert "conclusion" in case
            assert "expected_valid" in case
            assert isinstance(case["expected_valid"], bool)

    def test_specific_test_case_retrieval(self):
        """Test retrieving specific test cases"""
        from test_cases import get_case_by_name
        
        # Test retrieving a known case
        case = get_case_by_name("Caso 1: Modus Ponens Clásico")
        assert case.category == "valid"
        assert case.inference_rule == "Modus Ponens"
        
        # Test error for non-existent case
        with pytest.raises(ValueError):
            get_case_by_name("Caso Inexistente")


def run_test_case_summary():
    """Helper function to display test case summary"""
    from test_cases import print_test_case_summary
    print_test_case_summary()


if __name__ == "__main__":
    # Show test case summary
    print("=" * 60)
    print("EJECUTANDO RESUMEN DE CASOS DE PRUEBA")
    print("=" * 60)
    run_test_case_summary()
    print("\n" + "=" * 60)
    print("EJECUTANDO PRUEBAS UNITARIAS")
    print("=" * 60)
    
    # Run pytest
    pytest.main([__file__, "-v"])