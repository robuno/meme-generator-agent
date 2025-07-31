"""
Meme caption generation and cleaning functionality
"""
import re
import random
from typing import Tuple, Optional
from .config import Config
from .models import ModelManager

class CaptionGenerator:
    """Handles meme caption generation and cleaning"""
    
    def __init__(self):
        self.model_manager = ModelManager()
        self.config = Config()
    
    def extract_top_bottom(self, text: str) -> Tuple[Optional[str], Optional[str]]:
        """
        Extract top and bottom text from LLM output
        
        Args:
            text: Raw text from LLM
            
        Returns:
            Tuple of (top_text, bottom_text) or (None, None) if extraction fails
        """
        # Find all top and bottom candidates
        all_tops = re.findall(r"Top text:\s*(.+)", text)
        all_bottoms = re.findall(r"Bottom text:\s*(.+)", text)

        if all_tops and all_bottoms:
            # Pick the LAST pair (most likely to be clean)
            top = all_tops[-1].strip()
            bottom = all_bottoms[-1].strip()

            # Remove leading/trailing quotes (single or double)
            top = re.sub(r'^[\'"]+|[\'"]+$', '', top)
            bottom = re.sub(r'^[\'"]+|[\'"]+$', '', bottom)

            # Remove talker prefixes like Me:, Cat:, John:
            top = re.sub(r'^\s*\w+\s*:\s*', '', top)
            bottom = re.sub(r'^\s*\w+\s*:\s*', '', bottom)

            # Strip again for safety
            return top.strip(), bottom.strip()

        return None, None
    
    def is_bad_caption(self, text: str) -> bool:
        """
        Check if caption contains banned fragments
        
        Args:
            text: Text to check
            
        Returns:
            True if text contains banned fragments
        """
        return any(bad in text for bad in self.config.BANNED_FRAGMENTS)
    
    def generate_clean_captions(self, prompt: str, max_retries: int = 3) -> Tuple[Optional[str], Optional[str]]:
        """
        Generate clean meme captions with retry logic
        
        Args:
            prompt: Prompt for caption generation
            max_retries: Maximum number of retry attempts
            
        Returns:
            Tuple of (top_text, bottom_text) or (None, None) if generation fails
        """
        for attempt in range(max_retries):
            try:
                meme_text = self.model_manager.llm(prompt, temperature=0.95, top_p=0.95)
                print(f"Model Output (Attempt {attempt+1}): {meme_text}")

                top, bottom = self.extract_top_bottom(meme_text)

                # If there is no top/bottom text or if it contains parts of the prompt, retry
                if (not top or not bottom or 
                    self.is_bad_caption(top) or 
                    self.is_bad_caption(bottom)):
                    print(f"Bad caption detected → Retrying... ({attempt+1}/{max_retries})")
                    continue
                else:
                    print(f"Clean Caption Found!\nTop: {top}\nBottom: {bottom}")
                    return top, bottom
                    
            except Exception as e:
                print(f"Error generating caption (attempt {attempt+1}): {e}")
                continue

        print("Could not generate a clean meme caption after retries.")
        return None, None
    
    def generate_meme_prompt(self, keyword: str, image_caption: str, template_name: str) -> str:
        """
        Generate a prompt for meme caption generation
        
        Args:
            keyword: Main keyword for the meme
            image_caption: Description of the image
            template_name: Name of the meme template
            
        Returns:
            Formatted prompt for the LLM
        """
        style_hint = random.choice(self.config.STYLE_HINTS)
        
        prompt = f"""
        You are a witty meme creator. {style_hint}.

        Image description: "{image_caption}"
        Template name: '{template_name}'

        Write ONE funny meme about '{keyword}' using this image and template.

        RULES:
        - Only return exactly TWO lines.
        - First line MUST start with: Top text:
        - Second line MUST start with: Bottom text:
        - No explanations, no code, no HTML, no hashtags.
        - No quotes around the sentences.
        - Do NOT copy the example.

        EXAMPLE (don't copy!):
        Top text: When Monday hits too hard
        Bottom text: And coffee hasn't kicked in yet

        Now write your own meme in that exact format.
        """
        
        return prompt
    
    def score_humor(self, top_text: str, bottom_text: str) -> int:
        """
        Score the humor of a meme caption
        
        Args:
            top_text: Top text of the meme
            bottom_text: Bottom text of the meme
            
        Returns:
            Humor score from 1-10
        """
        score_prompt = f"""You wrote these meme lines:

        Top text: "{top_text}"
        Bottom text: "{bottom_text}"

        How funny and fitting are these two lines together as a meme, on a scale from 1 (not funny at all) to 10 (extremely funny)?
        Only reply with the number score."""

        try:
            score_text = self.model_manager.llm(score_prompt, temperature=0.3)
            print(f"Raw humor score response: {score_text}")

            matches = re.findall(r"\b([1-9]|10)\b", score_text)
            score = int(matches[-1]) if matches else 0

            print(f"Final Score: {score}")
            return score
            
        except Exception as e:
            print(f"Error scoring humor: {e}")
            return 0 