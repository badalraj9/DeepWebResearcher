#!/usr/bin/env python3
"""
Test script for LaTeX Executive Summary functionality
"""

import os
import sys
from dotenv import load_dotenv

# Add the current directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from draftagent import conduct_research_workflow, select_content_style

def test_latex_executive_summary():
    """Test the LaTeX executive summary functionality"""
    
    print("🧪 Testing LaTeX Executive Summary Functionality")
    print("=" * 55)
    
    # Test query
    test_query = "Digital Transformation in Healthcare"
    
    print(f"📝 Test Query: {test_query}")
    print(f"🎨 Content Style: LaTeX Executive Summary (Style 5)")
    
    try:
        # Test the content style selection
        content_style = select_content_style(5)
        print(f"✅ Content Style Selected: {content_style}")
        
        # Conduct research with LaTeX executive summary style
        print("\n🔍 Conducting research with LaTeX executive summary style...")
        result = conduct_research_workflow(test_query, content_style)
        
        if result.get("status") == "completed":
            print("✅ Research completed successfully!")
            
            # Check if the draft content has LaTeX executive summary structure
            draft_content = result.get('draft_content', '')
            
            print(f"\n📊 Results Summary:")
            print(f"   - Research Output Length: {len(result.get('research_output', ''))} characters")
            print(f"   - Draft Content Length: {len(draft_content)} characters")
            print(f"   - References Count: {len(result.get('references', []))}")
            
            # Check for LaTeX executive summary structure indicators
            executive_summary_indicators = [
                "Executive Summary:", "Objectives", "Methodology", 
                "Key Findings", "Recommendations", "Conclusion"
            ]
            
            found_indicators = []
            for indicator in executive_summary_indicators:
                if indicator.lower() in draft_content.lower():
                    found_indicators.append(indicator)
            
            print(f"\n📋 LaTeX Executive Summary Structure Check:")
            print(f"   - Found {len(found_indicators)} executive summary structure indicators")
            for indicator in found_indicators:
                print(f"     ✅ {indicator}")
            
            if len(found_indicators) >= 4:
                print("\n🎉 LaTeX Executive Summary test PASSED!")
                print("   The executive summary contains proper LaTeX-style structure.")
            else:
                print("\n⚠️  LaTeX Executive Summary test PARTIAL")
                print("   Some executive summary structure elements may be missing.")
            
            # Check for executive summary characteristics
            executive_characteristics = [
                "concise", "overview", "strategic", "business", "executive",
                "high-level", "actionable", "recommendations"
            ]
            
            found_characteristics = []
            for characteristic in executive_characteristics:
                if characteristic.lower() in draft_content.lower():
                    found_characteristics.append(characteristic)
            
            print(f"\n📈 Executive Summary Characteristics:")
            print(f"   - Found {len(found_characteristics)} executive-focused terms")
            for characteristic in found_characteristics:
                print(f"     ✅ {characteristic}")
            
            # Show a preview of the content
            print(f"\n📄 Content Preview (first 500 characters):")
            print("-" * 50)
            print(draft_content[:500] + "..." if len(draft_content) > 500 else draft_content)
            print("-" * 50)
            
        else:
            print("❌ Research failed!")
            print(f"   Error: {result.get('error', 'Unknown error')}")
            
    except Exception as e:
        print(f"❌ Test failed with exception: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    # Load environment variables
    load_dotenv()
    
    # Check if required API keys are set
    if not os.getenv("OPENROUTER_API_KEY"):
        print("❌ OPENROUTER_API_KEY not found in environment variables")
        print("   Please set your OpenRouter API key in the .env file")
        sys.exit(1)
    
    if not os.getenv("TAVILY_API_KEY"):
        print("❌ TAVILY_API_KEY not found in environment variables")
        print("   Please set your Tavily API key in the .env file")
        sys.exit(1)
    
    # Run the test
    test_latex_executive_summary() 