"""
Imgflip API integration for meme template search and generation
"""
import requests
from typing import List, Dict, Optional
from .config import Config

class ImgflipAPI:
    """Handles Imgflip API interactions"""
    
    def __init__(self):
        self.config = Config()
        self.base_url = "https://api.imgflip.com"
    
    def search_template(self, keyword: str) -> Dict:
        """
        Search for meme templates based on keyword
        
        Args:
            keyword: Search term for meme template
            
        Returns:
            Dict containing template information
        """
        try:
            response = requests.get(f"{self.base_url}/get_memes")
            response.raise_for_status()
            
            memes = response.json()["data"]["memes"]
            matches = [m for m in memes if keyword.lower() in m["name"].lower()]
            
            if matches:
                template = matches[0]
                print(f"Found template: {template['name']}")
                return template
            else:
                template = memes[0]
                print(f"No exact match found, using: {template['name']}")
                return template
                
        except requests.RequestException as e:
            print(f"Error searching for template: {e}")
            # Return a default template if API fails
            return {
                "id": "101716",
                "name": "Yo Dawg Heard You",
                "url": "https://i.imgflip.com/1g8my4.jpg"
            }
    
    def generate_meme(self, template_id: str, top_text: str, bottom_text: str) -> Optional[str]:
        """
        Generate a meme using Imgflip API
        
        Args:
            template_id: ID of the meme template
            top_text: Text for the top of the meme
            bottom_text: Text for the bottom of the meme
            
        Returns:
            URL of the generated meme or None if failed
        """
        try:
            payload = {
                "template_id": template_id,
                "username": self.config.IMGFLIP_USERNAME,
                "password": self.config.IMGFLIP_PASSWORD,
                "text0": top_text,
                "text1": bottom_text
            }
            
            response = requests.post(f"{self.base_url}/caption_image", data=payload)
            response.raise_for_status()
            
            result = response.json()
            
            if result.get("success"):
                meme_url = result["data"]["url"]
                print(f"Meme generated successfully: {meme_url}")
                return meme_url
            else:
                print(f"Failed to generate meme: {result.get('error_message', 'Unknown error')}")
                return None
                
        except requests.RequestException as e:
            print(f"Error generating meme: {e}")
            return None
    
    def get_all_templates(self) -> List[Dict]:
        """
        Get all available meme templates
        
        Returns:
            List of all meme templates
        """
        try:
            response = requests.get(f"{self.base_url}/get_memes")
            response.raise_for_status()
            
            return response.json()["data"]["memes"]
            
        except requests.RequestException as e:
            print(f"Error fetching templates: {e}")
            return [] 