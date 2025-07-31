"""
AI Models initialization and management
"""
import torch
from transformers import (
    AutoTokenizer, 
    AutoModelForCausalLM, 
    pipeline,
    BlipProcessor, 
    BlipForConditionalGeneration
)
from langchain_community.llms import HuggingFacePipeline
from huggingface_hub import login
from .config import Config

class ModelManager:
    """Manages all AI models used in the meme generator"""
    
    def __init__(self):
        self.config = Config()
        self._llm = None
        self._blip_processor = None
        self._blip_model = None
        self._is_initialized = False
    
    def initialize(self):
        """Initialize all models"""
        if self._is_initialized:
            return
            
        # Login to Hugging Face
        login(self.config.HF_TOKEN)
        
        # Initialize text generation model
        self._initialize_text_model()
        
        # Initialize BLIP model for image captioning
        self._initialize_blip_model()
        
        self._is_initialized = True
        print("All models initialized successfully!")
    
    def _initialize_text_model(self):
        """Initialize the text generation model"""
        print("Loading text generation model...")
        
        tokenizer = AutoTokenizer.from_pretrained(self.config.MODEL_NAME)
        model = AutoModelForCausalLM.from_pretrained(
            self.config.MODEL_NAME, 
            device_map="auto", 
            torch_dtype="auto"
        )
        
        pipe = pipeline(
            "text-generation", 
            model=model, 
            tokenizer=tokenizer, 
            max_new_tokens=self.config.MAX_NEW_TOKENS
        )
        
        self._llm = HuggingFacePipeline(pipeline=pipe)
        print("Text generation model loaded!")
    
    def _initialize_blip_model(self):
        """Initialize the BLIP model for image captioning"""
        print("Loading BLIP model for image captioning...")
        
        self._blip_processor = BlipProcessor.from_pretrained(self.config.BLIP_MODEL_NAME)
        self._blip_model = BlipForConditionalGeneration.from_pretrained(
            self.config.BLIP_MODEL_NAME
        ).to("cpu")
        
        print("BLIP model loaded!")
    
    @property
    def llm(self):
        """Get the language model"""
        if not self._is_initialized:
            self.initialize()
        return self._llm
    
    @property
    def blip_processor(self):
        """Get the BLIP processor"""
        if not self._is_initialized:
            self.initialize()
        return self._blip_processor
    
    @property
    def blip_model(self):
        """Get the BLIP model"""
        if not self._is_initialized:
            self.initialize()
        return self._blip_model 