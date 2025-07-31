#!/usr/bin/env python3
"""
Installation script for Meme Generator Agent
"""

import os
import sys
import subprocess
import platform

def print_banner():
    """Print installation banner"""
    banner = """
    ╔══════════════════════════════════════════════════════════════╗
    ║                 MEME GENERATOR AGENT SETUP                   ║
    ║                                                              ║
    ║  Installing dependencies and setting up the environment...   ║
    ╚══════════════════════════════════════════════════════════════╝
    """
    print(banner)

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 8):
        print("Error: Python 3.8 or higher is required")
        print(f"   Current version: {sys.version}")
        return False
    print(f"Python version: {sys.version}")
    return True

def install_requirements():
    """Install required packages"""
    print("\nInstalling required packages...")
    
    try:
        subprocess.check_call([
            sys.executable, "-m", "pip", "install", "-r", "requirements.txt"
        ])
        print("All packages installed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error installing packages: {e}")
        return False

def create_env_file():
    """Create .env file with template"""
    env_content = """# Meme Generator Agent Environment Variables
# Replace these with your actual credentials

# Hugging Face Token (optional - free tier available)
HF_TOKEN=your_huggingface_token_here

# Imgflip Credentials (optional - free tier available)
IMGFLIP_USERNAME=your_imgflip_username_here
IMGFLIP_PASSWORD=your_imgflip_password_here
"""
    
    if not os.path.exists(".env"):
        with open(".env", "w") as f:
            f.write(env_content)
        print("Created .env template file")
        print("Edit .env file with your credentials (optional)")
    else:
        print("ℹ.env file already exists")

def test_installation():
    """Test if the installation works"""
    print("\nTesting installation...")
    
    try:
        # Test importing the main module
        sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))
        from src.config import Config
        from src.models import ModelManager
        
        print("Core modules imported successfully")
        
        # Test configuration
        config = Config()
        print("Configuration loaded successfully")
        
        return True
        
    except ImportError as e:
        print(f"Import error: {e}")
        return False
    except Exception as e:
        print(f"Test failed: {e}")
        return False

def print_next_steps():
    """Print next steps for the user"""
    print("\n" + "=" * 60)
    print("INSTALLATION COMPLETE!")
    print("=" * 60)
    print("\nNext steps:")
    print("1. (Optional) Edit .env file with your API credentials")
    print("2. Try generating a meme:")
    print("   python main.py --keyword 'cat'")
    print("3. Run examples to see all features:")
    print("   python examples.py")
    print("4. Check available templates:")
    print("   python main.py --list-templates")
    print("\nFor more information, see README.md")
    print("=" * 60)

def main():
    """Main installation function"""
    print_banner()
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Install requirements
    if not install_requirements():
        print("Installation failed. Please check the error messages above.")
        sys.exit(1)
    
    # Create environment file
    create_env_file()
    
    # Test installation
    if not test_installation():
        print("Installation test failed. Please check the error messages above.")
        sys.exit(1)
    
    # Print next steps
    print_next_steps()

if __name__ == "__main__":
    main() 