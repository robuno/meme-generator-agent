"""
Main Meme Agent that orchestrates all components
"""
from typing import List, Optional
from .models import ModelManager
from .imgflip_api import ImgflipAPI
from .image_processor import ImageProcessor
from .caption_generator import CaptionGenerator
from .config import Config

class MemeAgent:
    """Main agent that generates memes using AI"""
    
    def __init__(self):
        self.config = Config()
        self.model_manager = ModelManager()
        self.imgflip_api = ImgflipAPI()
        self.image_processor = ImageProcessor()
        self.caption_generator = CaptionGenerator()
        
        # Initialize models
        self.model_manager.initialize()
    
    def generate_meme(self, keyword: str, retry_limit: int = 3) -> Optional[str]:
        """
        Generate a single meme for the given keyword
        
        Args:
            keyword: Main keyword for the meme
            retry_limit: Maximum number of retry attempts
            
        Returns:
            URL of the generated meme or None if failed
        """
        print(f"Generating meme for keyword: '{keyword}'")
        
        for attempt in range(retry_limit):
            print(f"Attempt {attempt + 1} / {retry_limit}")
            
            try:
                # 1. Select a meme template
                template = self.imgflip_api.search_template(keyword)
                print(f"Selected Template: {template['name']}")
                
                # 2. Get image description
                template_url = template["url"]
                image_caption = self.image_processor.describe_image(template_url)
                print(f"Image caption: {image_caption}")
                
                # 3. Generate meme prompt
                prompt = self.caption_generator.generate_meme_prompt(
                    keyword, image_caption, template['name']
                )
                
                # 4. Generate captions
                top, bottom = self.caption_generator.generate_clean_captions(prompt)
                
                if not top or not bottom:
                    print("Couldn't parse Top/Bottom text. Retrying...")
                    continue
                
                print(f"Final Top text: {top}")
                print(f"Final Bottom text: {bottom}")
                
                # 5. Generate the meme
                meme_url = self.imgflip_api.generate_meme(template["id"], top, bottom)
                
                if not meme_url:
                    print("Failed to generate meme. Retrying...")
                    continue
                
                # 6. Score the humor
                score = self.caption_generator.score_humor(top, bottom)
                
                if score >= self.config.HUMOR_SCORE_THRESHOLD:
                    print(f"Funny meme found! Score: {score}")
                    return meme_url
                else:
                    print(f"Meme not funny enough (score: {score}). Retrying...")
                    
            except Exception as e:
                print(f"Error in attempt {attempt + 1}: {e}")
                continue
        
        print("Could not generate a funny meme after all attempts.")
        return None
    
    def generate_multiple_memes(self, keyword: str, num_memes: int = 5, retry_limit: int = 3) -> List[str]:
        """
        Generate multiple memes for the given keyword
        
        Args:
            keyword: Main keyword for the memes
            num_memes: Number of memes to generate
            retry_limit: Maximum number of retry attempts per meme
            
        Returns:
            List of meme URLs
        """
        meme_urls = []
        
        print(f"Generating {num_memes} memes for keyword: '{keyword}'")
        
        for meme_num in range(num_memes):
            print(f"\n--- Meme {meme_num + 1} / {num_memes} ---")
            
            meme_url = self.generate_meme(keyword, retry_limit)
            
            if meme_url:
                meme_urls.append(meme_url)
                print(f"Meme {meme_num + 1} generated successfully!")
            else:
                print(f"Failed to generate meme {meme_num + 1}")
        
        print(f"\nGenerated {len(meme_urls)} out of {num_memes} memes successfully!")
        return meme_urls
    
    def list_templates(self) -> List[dict]:
        """
        Get list of all available meme templates
        
        Returns:
            List of template dictionaries
        """
        return self.imgflip_api.get_all_templates() 