"""
Configuration settings for the Meme Generator Agent
"""
import os
from typing import Optional

class Config:
    """Configuration class for the meme generator"""
    
    # Hugging Face settings
    HF_TOKEN: Optional[str] = os.getenv("HF_TOKEN", "ADD_YOUR_HF_TOKEN_HERE")
    
    # Model settings
    MODEL_NAME: str = "TheBloke/vicuna-7B-1.1-HF"
    BLIP_MODEL_NAME: str = "Salesforce/blip-image-captioning-large"
    
    # Imgflip API settings
    IMGFLIP_USERNAME: str = os.getenv("IMGFLIP_USERNAME", "ADD_YOUR_IMGFLIP_USERNAME_HERE")
    IMGFLIP_PASSWORD: str = os.getenv("IMGFLIP_PASSWORD", "ADD_YOUR_IMGFLIP_PASSWORD_HERE")
    
    # Generation settings
    MAX_NEW_TOKENS: int = 256
    MAX_RETRIES: int = 3
    HUMOR_SCORE_THRESHOLD: int = 7
    
    # Style hints for meme generation
    STYLE_HINTS = [
        "Make it sarcastic",
        "Make it absurd", 
        "Make it dark humor",
        "Make it wholesome but funny",
        "Make it chaotic and silly"
    ]
    
    # Banned fragments for caption cleaning
    BANNED_FRAGMENTS = [
        "MUST", "RULES", "DO NOT", "Top text", "Bottom text",
        "line", "Only return", "STRICT", "Example",
        "First line", "Second line"
    ] 