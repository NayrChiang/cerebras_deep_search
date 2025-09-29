#!/usr/bin/env python3
"""
Cerebras Deep Search - Perplexity-style Research Assistant

A deep research assistant that can automatically search the web, analyze multiple sources,
and provide structured insights using Cerebras LLM and Exa search engine.

Usage:
1. Install dependencies: pip install -r requirements.txt
2. Configure API keys in .env file
3. Run: python src/deep_research.py

Required API Keys:
- Cerebras: https://cloud.cerebras.ai
- Exa: https://exa.ai
"""

import os
import sys
import json
from pathlib import Path
from typing import List, Dict, Optional

# Add project root directory to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Load environment variables from .env file
try:
    from dotenv import load_dotenv
    load_dotenv(project_root / ".env")
except ImportError:
    print("Warning: python-dotenv not installed. Install with: pip install python-dotenv")

# Import required libraries
try:
    from exa_py import Exa
    from cerebras.cloud.sdk import Cerebras
except ImportError as e:
    print(f"Error importing required libraries: {e}")
    print("Please install dependencies: pip install -r requirements.txt")
    sys.exit(1)


class DeepResearchAssistant:
    """Perplexity-style deep research assistant using Cerebras and Exa"""
    
    def __init__(self):
        """Initialize the research assistant with API clients"""
        # Get API keys from environment variables
        self.exa_api_key = os.getenv("EXA_API_KEY", "your-exa-api-key")
        self.cerebras_api_key = os.getenv("CEREBRAS_API_KEY", "your-cerebras-api-key")
        
        # Validate API keys
        if self.exa_api_key == "your-exa-api-key":
            raise ValueError("Please configure EXA_API_KEY in .env file")
        if self.cerebras_api_key == "your-cerebras-api-key":
            raise ValueError("Please configure CEREBRAS_API_KEY in .env file")
        
        # Initialize clients
        try:
            self.cerebras_client = Cerebras(api_key=self.cerebras_api_key)
            self.exa_client = Exa(api_key=self.exa_api_key)
            print("✅ API clients initialized successfully")
        except Exception as e:
            print(f"❌ Error initializing API clients: {e}")
            raise
    
    def search_web(self, query: str, num_results: int = 5) -> List[Dict]:
        """
        Search the web using Exa's auto search
        
        Args:
            query: Search query
            num_results: Number of results to return
            
        Returns:
            List of search results with content
        """
        try:
            result = self.exa_client.search_and_contents(
                query,
                type="auto",
                num_results=num_results,
                text={"max_characters": 1000}
            )
            return result.results
        except Exception as e:
            print(f"❌ Error searching web: {e}")
            return []
    
    def ask_ai(self, prompt: str) -> str:
        """
        Get AI response from Cerebras
        
        Args:
            prompt: The prompt to send to the AI
            
        Returns:
            AI response text
        """
        try:
            chat_completion = self.cerebras_client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model="llama-4-scout-17b-16e-instruct",
                max_tokens=600,
                temperature=0.2
            )
            return chat_completion.choices[0].message.content
        except Exception as e:
            print(f"❌ Error getting AI response: {e}")
            return "Error: Could not get AI response"
    
    def research_topic(self, query: str) -> Dict:
        """
        Basic research function that searches and analyzes sources
        
        Args:
            query: Research query
            
        Returns:
            Dictionary with research results
        """
        print(f"🔍 Researching: {query}")
        
        # Search for sources
        results = self.search_web(query, 5)
        print(f"📊 Found {len(results)} sources")
        
        # Get content from sources
        sources = []
        for result in results:
            content = result.text
            title = result.title
            if content and len(content) > 200:
                sources.append({
                    "title": title,
                    "content": content,
                    "url": result.url
                })
        
        print(f"📄 Scraped {len(sources)} sources")
        
        if not sources:
            return {"summary": "No sources found", "insights": [], "sources": 0}
        
        # Create context for AI analysis
        context = f"Research query: {query}\n\nSources:\n"
        for i, source in enumerate(sources[:4], 1):
            context += f"{i}. {source['title']}: {source['content'][:400]}...\n\n"
        
        # Ask AI to analyze and synthesize
        prompt = f"""{context}

Based on these sources, provide:
1. A comprehensive summary (2-3 sentences)
2. Three key insights as bullet points

Format your response exactly like this:
SUMMARY: [your summary here]

INSIGHTS:
- [insight 1]
- [insight 2]
- [insight 3]"""
        
        response = self.ask_ai(prompt)
        print("🧠 Analysis complete")
        
        return {
            "query": query,
            "sources": len(sources),
            "response": response,
            "source_details": sources
        }
    
    def deeper_research_topic(self, query: str) -> Dict:
        """
        Two-layer research for better depth and comprehensive analysis
        
        Args:
            query: Research query
            
        Returns:
            Dictionary with enhanced research results
        """
        print(f"🔍 Researching: {query}")
        
        # Layer 1: Initial search
        results = self.search_web(query, 6)
        sources = []
        for result in results:
            if result.text and len(result.text) > 200:
                sources.append({
                    "title": result.title,
                    "content": result.text,
                    "url": result.url
                })
        
        print(f"Layer 1: Found {len(sources)} sources")
        
        if not sources:
            return {"summary": "No sources found", "insights": [], "sources": 0}
        
        # Get initial analysis and identify follow-up topic
        context1 = f"Research query: {query}\n\nSources:\n"
        for i, source in enumerate(sources[:4], 1):
            context1 += f"{i}. {source['title']}: {source['content'][:300]}...\n\n"
        
        follow_up_prompt = f"""{context1}

Based on these sources, what's the most important follow-up question that would deepen our understanding of "{query}"?

Respond with just a specific search query (no explanation):"""
        
        follow_up_query = self.ask_ai(follow_up_prompt).strip().strip('"')
        
        # Layer 2: Follow-up search
        print(f"Layer 2: Investigating '{follow_up_query}'")
        follow_results = self.search_web(follow_up_query, 4)
        
        for result in follow_results:
            if result.text and len(result.text) > 200:
                sources.append({
                    "title": f"[Follow-up] {result.title}",
                    "content": result.text,
                    "url": result.url
                })
        
        print(f"Total sources: {len(sources)}")
        
        # Final synthesis
        all_context = f"Research query: {query}\nFollow-up: {follow_up_query}\n\nAll Sources:\n"
        for i, source in enumerate(sources[:7], 1):
            all_context += f"{i}. {source['title']}: {source['content'][:300]}...\n\n"
        
        final_prompt = f"""{all_context}

Provide a comprehensive analysis:

SUMMARY: [3-4 sentences covering key findings from both research layers]

INSIGHTS:
- [insight 1]
- [insight 2]
- [insight 3]
- [insight 4]

DEPTH GAINED: [1 sentence on how the follow-up search enhanced understanding]"""
        
        response = self.ask_ai(final_prompt)
        return {
            "query": query,
            "follow_up_query": follow_up_query,
            "sources": len(sources),
            "response": response,
            "source_details": sources
        }
    
    def save_research(self, result: Dict, filename: Optional[str] = None) -> str:
        """
        Save research results to a JSON file
        
        Args:
            result: Research result dictionary
            filename: Optional custom filename
            
        Returns:
            Path to saved file
        """
        if not filename:
            # Create filename from query
            safe_query = "".join(c for c in result["query"] if c.isalnum() or c in (' ', '-', '_')).rstrip()
            safe_query = safe_query.replace(' ', '_')[:50]
            filename = f"research_{safe_query}.json"
        
        output_dir = project_root / "output"
        output_dir.mkdir(exist_ok=True)
        
        filepath = output_dir / filename
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
        
        print(f"💾 Research saved to: {filepath}")
        return str(filepath)


def main():
    """Main function to run the deep research assistant"""
    print("=" * 60)
    print("🔍 Cerebras Deep Search - Perplexity-style Research Assistant")
    print("=" * 60)
    print()
    
    try:
        # Initialize the research assistant
        assistant = DeepResearchAssistant()
        
        while True:
            print("\nOptions:")
            print("1. Basic research")
            print("2. Deep research (two-layer)")
            print("3. Exit")
            
            choice = input("\nEnter your choice (1-3): ").strip()
            
            if choice == "1":
                query = input("\nEnter your research query: ").strip()
                if query:
                    result = assistant.research_topic(query)
                    print("\n" + "="*50)
                    print("RESEARCH RESULTS")
                    print("="*50)
                    print(f"Query: {result['query']}")
                    print(f"Sources analyzed: {result['sources']}")
                    print(f"\n{result['response']}")
                    print("="*50)
                    
                    save = input("\nSave results? (y/n): ").strip().lower()
                    if save == 'y':
                        assistant.save_research(result)
            
            elif choice == "2":
                query = input("\nEnter your research query: ").strip()
                if query:
                    result = assistant.deeper_research_topic(query)
                    print("\n" + "="*50)
                    print("ENHANCED RESEARCH RESULTS")
                    print("="*50)
                    print(f"Query: {result['query']}")
                    if 'follow_up_query' in result:
                        print(f"Follow-up: {result['follow_up_query']}")
                    print(f"Sources analyzed: {result['sources']}")
                    print(f"\n{result['response']}")
                    print("="*50)
                    
                    save = input("\nSave results? (y/n): ").strip().lower()
                    if save == 'y':
                        assistant.save_research(result)
            
            elif choice == "3":
                print("👋 Goodbye!")
                break
            
            else:
                print("❌ Invalid choice")
    
    except Exception as e:
        print(f"❌ Error: {e}")
        print("Please check your API keys and dependencies")


if __name__ == "__main__":
    main()
