#!/usr/bin/env python3
"""
Examples of how to use the Meme Generator Agent programmatically

This script demonstrates various ways to use the meme generator:
1. Generate a single meme
2. Generate multiple memes
3. List available templates
4. Custom configuration
"""

import sys
import os

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.meme_agent import MemeAgent
from src.config import Config

def example_single_meme():
    """Example: Generate a single meme"""
    print("=" * 60)
    print("EXAMPLE 1: Generate a single meme")
    print("=" * 60)
    
    agent = MemeAgent()
    
    keyword = "cat"
    print(f"Generating meme for keyword: '{keyword}'")
    
    meme_url = agent.generate_meme(keyword, retry_limit=3)
    
    if meme_url:
        print(f"Success! Meme URL: {meme_url}")
    else:
        print(" Failed to generate meme")

def example_multiple_memes():
    """Example: Generate multiple memes"""
    print("\n" + "=" * 60)
    print("EXAMPLE 2: Generate multiple memes")
    print("=" * 60)
    
    agent = MemeAgent()
    
    keyword = "programming"
    count = 3
    print(f"Generating {count} memes for keyword: '{keyword}'")
    
    meme_urls = agent.generate_multiple_memes(keyword, num_memes=count, retry_limit=3)
    
    if meme_urls:
        print(f"Success! Generated {len(meme_urls)} memes:")
        for i, url in enumerate(meme_urls, 1):
            print(f"  {i}. {url}")
    else:
        print("Failed to generate any memes")

def example_list_templates():
    """Example: List available templates"""
    print("\n" + "=" * 60)
    print("EXAMPLE 3: List available templates")
    print("=" * 60)
    
    agent = MemeAgent()
    
    templates = agent.list_templates()
    
    print(f"Found {len(templates)} templates:")
    for i, template in enumerate(templates[:5], 1):  # Show first 5
        print(f"  {i}. {template['name']} (ID: {template['id']})")
    
    if len(templates) > 5:
        print(f"  ... and {len(templates) - 5} more templates")

def example_custom_config():
    """Example: Using custom configuration"""
    print("\n" + "=" * 60)
    print("EXAMPLE 4: Custom configuration")
    print("=" * 60)
    
    # You can modify the config before creating the agent
    config = Config()
    config.HUMOR_SCORE_THRESHOLD = 6  # Lower threshold for more memes
    config.MAX_RETRIES = 5  # More retries
    
    print(f"Custom settings:")
    print(f"  - Humor score threshold: {config.HUMOR_SCORE_THRESHOLD}")
    print(f"  - Max retries: {config.MAX_RETRIES}")
    
    agent = MemeAgent()
    
    keyword = "coffee"
    meme_url = agent.generate_meme(keyword, retry_limit=config.MAX_RETRIES)
    
    if meme_url:
        print(f"Success! Meme URL: {meme_url}")
    else:
        print("Failed to generate meme")

def example_error_handling():
    """Example: Error handling"""
    print("\n" + "=" * 60)
    print("EXAMPLE 5: Error handling")
    print("=" * 60)
    
    try:
        agent = MemeAgent()
        
        # Try with a very specific keyword that might not have good templates
        keyword = "quantum physics"
        print(f"Trying to generate meme for: '{keyword}'")
        
        meme_url = agent.generate_meme(keyword, retry_limit=2)
        
        if meme_url:
            print(f"Success! Meme URL: {meme_url}")
        else:
            print("Failed to generate meme (expected for this keyword)")
            
    except Exception as e:
        print(f"Error occurred: {e}")

def main():
    """Run all examples"""
    print("MEME GENERATOR AGENT - EXAMPLES")
    print("This script demonstrates various usage patterns.")
    print()
    
    # Run examples
    example_single_meme()
    example_multiple_memes()
    example_list_templates()
    example_custom_config()
    example_error_handling()
    
    print("\n" + "=" * 60)
    print("All examples completed!")
    print("You can also use the command-line interface:")
    print("   python main.py --keyword 'cat' --count 3")
    print("=" * 60)

if __name__ == "__main__":
    main() 