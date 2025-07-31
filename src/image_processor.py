"""
Image processing and captioning functionality
"""
import requests
from PIL import Image
from typing import Optional
from .models import ModelManager
from .config import Config

class ImageProcessor:
    """Handles image processing and captioning"""
    
    def __init__(self):
        self.model_manager = ModelManager()
        self.config = Config()
    
    def get_base_caption(self, image_url: str) -> str:
        """
        Get a basic caption for an image using BLIP
        
        Args:
            image_url: URL of the image to caption
            
        Returns:
            Basic caption string
        """
        try:
            # Download and process image
            img = Image.open(requests.get(image_url, stream=True).raw).convert("RGB")
            
            # Generate caption
            inputs = self.model_manager.blip_processor(img, return_tensors="pt").to("cpu")
            out = self.model_manager.blip_model.generate(inputs, max_length=60)
            caption = self.model_manager.blip_processor.decode(out[0], skip_special_tokens=True)
            
            return caption
            
        except Exception as e:
            print(f"Error generating base caption: {e}")
            return "A person in a scene"
    
    def expand_caption_with_llm(self, base_caption: str) -> str:
        """
        Expand a basic caption into a detailed description using LLM
        
        Args:
            base_caption: Basic caption from BLIP
            
        Returns:
            Detailed scene description
        """
        prompt = f"""
        Short image caption: "{base_caption}"

        Rewrite this into a **detailed scene description** for someone who cannot see the image.

        STRICT RULES:
        - DO NOT mention memes or say "this is a meme".
        - DO NOT write code, DO NOT include functions, DO NOT import anything.
        - Only describe what is visually present.
        - Mention if there are panels (left side vs right side).
        - Describe what each person or animal is doing.
        - Include facial expressions and emotions (angry, confused, smug, etc.).
        - Mention animals, objects, and their positions.
        - Only return one clean paragraph in plain English.

        ONLY return the scene description. NOTHING else.
        """
        
        try:
            detailed_caption = self.model_manager.llm(prompt, temperature=0.4)
            return detailed_caption.strip()
        except Exception as e:
            print(f"Error expanding caption: {e}")
            return base_caption
    
    def describe_image(self, image_url: str) -> str:
        """
        Get a detailed description of an image
        
        Args:
            image_url: URL of the image to describe
            
        Returns:
            Detailed image description
        """
        # Get basic caption
        short_caption = self.get_base_caption(image_url)
        print(f"Base caption: {short_caption}")
        
        # Expand with LLM
        detailed_caption = self.expand_caption_with_llm(short_caption)
        print(f"Detailed caption: {detailed_caption}")
        
        return detailed_caption 