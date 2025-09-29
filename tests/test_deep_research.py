"""
Deep Research Test File
"""
import pytest
import os
from pathlib import Path
import sys

# Add project root directory to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root / "src"))

from deep_research import DeepResearchAssistant


class TestDeepResearch:
    """Deep Research Test Class"""
    
    def test_initialization_without_api_keys(self):
        """Test that initialization fails without proper API keys"""
        # Temporarily remove API keys
        original_exa = os.environ.get("EXA_API_KEY")
        original_cerebras = os.environ.get("CEREBRAS_API_KEY")
        
        os.environ["EXA_API_KEY"] = "your-exa-api-key"
        os.environ["CEREBRAS_API_KEY"] = "your-cerebras-api-key"
        
        with pytest.raises(ValueError, match="Please configure EXA_API_KEY"):
            DeepResearchAssistant()
        
        # Restore original values
        if original_exa:
            os.environ["EXA_API_KEY"] = original_exa
        if original_cerebras:
            os.environ["CEREBRAS_API_KEY"] = original_cerebras
    
    def test_search_web_function_exists(self):
        """Test that search_web method exists and is callable"""
        # This test assumes API keys are configured
        try:
            assistant = DeepResearchAssistant()
            assert hasattr(assistant, 'search_web')
            assert callable(assistant.search_web)
        except ValueError:
            # Skip if API keys not configured
            pytest.skip("API keys not configured for testing")
    
    def test_ask_ai_function_exists(self):
        """Test that ask_ai method exists and is callable"""
        try:
            assistant = DeepResearchAssistant()
            assert hasattr(assistant, 'ask_ai')
            assert callable(assistant.ask_ai)
        except ValueError:
            # Skip if API keys not configured
            pytest.skip("API keys not configured for testing")
    
    def test_research_topic_function_exists(self):
        """Test that research_topic method exists and is callable"""
        try:
            assistant = DeepResearchAssistant()
            assert hasattr(assistant, 'research_topic')
            assert callable(assistant.research_topic)
        except ValueError:
            # Skip if API keys not configured
            pytest.skip("API keys not configured for testing")
    
    def test_deeper_research_topic_function_exists(self):
        """Test that deeper_research_topic method exists and is callable"""
        try:
            assistant = DeepResearchAssistant()
            assert hasattr(assistant, 'deeper_research_topic')
            assert callable(assistant.deeper_research_topic)
        except ValueError:
            # Skip if API keys not configured
            pytest.skip("API keys not configured for testing")
    
    def test_save_research_function_exists(self):
        """Test that save_research method exists and is callable"""
        try:
            assistant = DeepResearchAssistant()
            assert hasattr(assistant, 'save_research')
            assert callable(assistant.save_research)
        except ValueError:
            # Skip if API keys not configured
            pytest.skip("API keys not configured for testing")


if __name__ == "__main__":
    pytest.main([__file__])
