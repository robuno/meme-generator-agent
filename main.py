#!/usr/bin/env python3
"""
Meme Generator Agent - Main Runner Script

A powerful AI agent that generates funny memes using:
- Hugging Face models for text generation
- BLIP for image captioning  
- Imgflip API for meme creation
- LangChain for agent orchestration

Usage:
    python main.py --keyword "cat" --count 5
    python main.py --keyword "programming" --single
    python main.py --list-templates
"""

import argparse
import sys
import os
from typing import List

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.meme_agent import MemeAgent

def print_banner():
    """Print application banner"""
    banner = """
    ╔══════════════════════════════════════════════════════════════╗
    ║                     MEME GENERATOR AGENT                     ║
    ║                                                              ║
    ║  Powered by AI: Hugging Face + BLIP + Imgflip API            ║
    ║  Generate hilarious memes with just a keyword!               ║
    ╚══════════════════════════════════════════════════════════════╝
    """
    print(banner)

def main():
    """Main function"""
    parser = argparse.ArgumentParser(
        description="AI-powered meme generator using Hugging Face models and Imgflip API",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py --keyword "cat" --count 3
  python main.py --keyword "programming" --single
  python main.py --list-templates
  python main.py --keyword "coffee" --count 1 --retry-limit 5
        """
    )
    
    parser.add_argument(
        "--keyword", 
        type=str, 
        help="Keyword/topic for meme generation"
    )
    
    parser.add_argument(
        "--count", 
        type=int, 
        default=1,
        help="Number of memes to generate (default: 1)"
    )
    
    parser.add_argument(
        "--single", 
        action="store_true",
        help="Generate a single meme (same as --count 1)"
    )
    
    parser.add_argument(
        "--retry-limit", 
        type=int, 
        default=3,
        help="Maximum retry attempts per meme (default: 3)"
    )
    
    parser.add_argument(
        "--list-templates", 
        action="store_true",
        help="List all available meme templates"
    )
    
    parser.add_argument(
        "--verbose", 
        action="store_true",
        help="Enable verbose output"
    )
    
    args = parser.parse_args()
    
    # Print banner
    print_banner()
    
    # Initialize the meme agent
    print("Initializing Meme Generator Agent...")
    try:
        agent = MemeAgent()
        print("Agent initialized successfully!")
    except Exception as e:
        print(f"Failed to initialize agent: {e}")
        sys.exit(1)
    
    # Handle different commands
    if args.list_templates:
        print("\n Fetching available meme templates...")
        templates = agent.list_templates()
        print(f" Found {len(templates)} templates:")
        for i, template in enumerate(templates[:10], 1):  # Show first 10
            print(f"  {i}. {template['name']} (ID: {template['id']})")
        if len(templates) > 10:
            print(f"  ... and {len(templates) - 10} more templates")
        return
    
    if not args.keyword:
        print(" Error: Please provide a keyword using --keyword")
        print(" Example: python main.py --keyword 'cat'")
        sys.exit(1)
    
    # Generate memes
    keyword = args.keyword
    count = 1 if args.single else args.count
    
    print(f"\n Starting meme generation for keyword: '{keyword}'")
    print(f" Target: {count} meme(s)")
    print(f" Retry limit: {args.retry_limit} attempts per meme")
    print("=" * 60)
    
    try:
        if count == 1:
            # Generate single meme
            meme_url = agent.generate_meme(keyword, args.retry_limit)
            if meme_url:
                print(f"\n SUCCESS! Your meme is ready:")
                print(f"{meme_url}")
            else:
                print("\n Failed to generate a meme. Try again with different settings.")
                sys.exit(1)
        else:
            # Generate multiple memes
            meme_urls = agent.generate_multiple_memes(keyword, count, args.retry_limit)
            
            if meme_urls:
                print(f"\n SUCCESS! Generated {len(meme_urls)} memes:")
                for i, url in enumerate(meme_urls, 1):
                    print(f"  {i}. {url}")
            else:
                print("\n Failed to generate any memes. Try again with different settings.")
                sys.exit(1)
                
    except KeyboardInterrupt:
        print("\n Generation interrupted by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n Error during meme generation: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 