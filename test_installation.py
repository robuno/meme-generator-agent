#!/usr/bin/env python3
"""
Test script to verify Meme Generator Agent installation and basic functionality
"""

import sys
import os

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

def test_imports():
    """Test if all modules can be imported"""
    print("Testing module imports...")
    
    try:
        from src.config import Config
        print("Config module imported")
        
        from src.models import ModelManager
        print("Models module imported")
        
        from src.imgflip_api import ImgflipAPI
        print("Imgflip API module imported")
        
        from src.image_processor import ImageProcessor
        print("Image processor module imported")
        
        from src.caption_generator import CaptionGenerator
        print("Caption generator module imported")
        
        from src.meme_agent import MemeAgent
        print("Meme agent module imported")
        
        return True
        
    except ImportError as e:
        print(f"Import error: {e}")
        return False

def test_configuration():
    """Test configuration loading"""
    print("\n Testing configuration...")
    
    try:
        from src.config import Config
        
        config = Config()
        print(f"Configuration loaded")
        print(f"   - Model: {config.MODEL_NAME}")
        print(f"   - BLIP Model: {config.BLIP_MODEL_NAME}")
        print(f"   - Max tokens: {config.MAX_NEW_TOKENS}")
        print(f"   - Humor threshold: {config.HUMOR_SCORE_THRESHOLD}")
        
        return True
        
    except Exception as e:
        print(f"Configuration error: {e}")
        return False

def test_api_connection():
    """Test Imgflip API connection"""
    print("\n Testing Imgflip API connection...")
    
    try:
        from src.imgflip_api import ImgflipAPI
        
        api = ImgflipAPI()
        templates = api.get_all_templates()
        
        if templates:
            print(f"API connection successful")
            print(f"   - Found {len(templates)} templates")
            print(f"   - First template: {templates[0]['name']}")
            return True
        else:
            print("⚠️ API returned no templates (might be rate limited)")
            return True  # Not a critical failure
            
    except Exception as e:
        print(f"API connection error: {e}")
        print("   This might be due to network issues or API limits")
        return False

def test_model_loading():
    """Test if models can be loaded (without downloading)"""
    print("\n Testing model loading...")
    
    try:
        from src.models import ModelManager
        
        # This will only test the ModelManager creation, not full model loading
        # to avoid downloading large models during testing
        manager = ModelManager()
        print("Model manager created successfully")
        print("   (Full model loading will happen on first use)")
        
        return True
        
    except Exception as e:
        print(f"Model manager error: {e}")
        return False

def run_all_tests():
    """Run all tests"""
    print("MEME GENERATOR AGENT - INSTALLATION TEST")
    print("=" * 60)
    
    tests = [
        ("Module Imports", test_imports),
        ("Configuration", test_configuration),
        ("API Connection", test_api_connection),
        ("Model Loading", test_model_loading),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n📋 Running: {test_name}")
        if test_func():
            passed += 1
            print(f"{test_name} - PASSED")
        else:
            print(f"{test_name} - FAILED")
    
    print("\n" + "=" * 60)
    print(f"Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("All tests passed! Installation is successful.")
        print("\n You can now try:")
        print("   python main.py --keyword 'cat'")
        print("   python examples.py")
    elif passed >= total - 1:
        print("Most tests passed. Minor issues detected.")
        print("The application should still work for basic usage.")
    else:
        print("Multiple tests failed. Please check the installation.")
        print("Try running: python install.py")
    
    print("=" * 60)

if __name__ == "__main__":
    run_all_tests() 