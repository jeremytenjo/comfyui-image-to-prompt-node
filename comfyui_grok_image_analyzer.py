"""
ComfyUI Custom Node for Grok Image Analysis
Analyzes images using XAI's Grok vision model and generates prompts
"""

import os
import json
import requests
import base64
from io import BytesIO
import torch
import numpy as np
from PIL import Image
from typing import Tuple, Dict, Any
import logging

# Setup logging
logger = logging.getLogger(__name__)


class GrokImageAnalyzer:
    """
    ComfyUI node that analyzes images using Grok API and returns descriptive prompts
    """

    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls) -> Dict[str, Any]:
        return {
            "required": {
                "image": ("IMAGE",),
                "api_key": ("STRING", {
                    "multiline": False,
                    "default": "",
                    "display": "password"
                }),
                "model": (["grok-4-1-fast-non-reasoning"], {
                    "default": "grok-4-1-fast-non-reasoning"
                }),
            },
            "optional": {
                "system_prompt": ("STRING", {
                    "multiline": True,
                    "default": "You are an expert at creating detailed, descriptive prompts for image generation models. Provide rich, specific details.",
                }),
                "user_prompt": ("STRING", {
                    "multiline": True,
                    "default": "Describe this image in detail for use as a prompt for an image generation model. Focus on composition, style, colors, and main subjects.",
                }),
            }
        }

    RETURN_TYPES = ("STRING", "STRING")
    RETURN_NAMES = ("prompt", "preview")
    FUNCTION = "analyze_image"
    CATEGORY = "image/analysis"
    OUTPUT_NODE = True

    def analyze_image(self, image: torch.Tensor, api_key: str, model: str, system_prompt: str = "", user_prompt: str = "") -> Tuple[str, str]:
        """
        Analyze an image using Grok API and return a descriptive prompt

        Args:
            image: Input image as tensor (B, H, W, C)
            api_key: XAI API key
            model: Model name to use
            system_prompt: Optional system context for analysis
            user_prompt: Optional prompt for analysis

        Returns:
            Tuple containing the generated prompt string and preview
        """

        # Validate API key
        if not api_key or api_key.strip() == "":
            api_key = os.environ.get("XAI_API_KEY", "")
            if not api_key:
                raise ValueError("API key not provided and XAI_API_KEY environment variable not set")

        # Convert tensor to PIL Image
        pil_image = self._tensor_to_pil(image)

        # Convert image to base64
        image_base64 = self._image_to_base64(pil_image)

        # Prepare API request
        base_url = os.environ.get("XAI_BASE_URL", "https://api.x.ai/v1")
        api_endpoint = f"{base_url}/chat/completions"

        # Build message content
        content = []

        # Use defaults if prompts are empty
        _system_prompt = system_prompt or "You are an expert at creating detailed, descriptive prompts for image generation models. Provide rich, specific details."
        _user_prompt = user_prompt or "Describe this image in detail for use as a prompt for an image generation model. Focus on composition, style, colors, and main subjects."

        if _system_prompt and _system_prompt.strip():
            content.append({
                "type": "text",
                "text": _system_prompt
            })

        content.append({
            "type": "image_url",
            "image_url": {
                "url": f"data:image/png;base64,{image_base64}"
            }
        })

        content.append({
            "type": "text",
            "text": _user_prompt
        })

        # Make API request
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"
        }

        payload = {
            "model": model,
            "messages": [
                {
                    "role": "user",
                    "content": content
                }
            ],
            "temperature": 0.7,
            "max_tokens": 2048
        }

        try:
            response = requests.post(api_endpoint, headers=headers, json=payload, timeout=60)
            response.raise_for_status()

            data = response.json()
            prompt = data.get("choices", [{}])[0].get("message", {}).get("content", "")

            if not prompt:
                raise ValueError("No analysis returned from Grok API")

            # Display preview in console
            print(f"\n{'='*80}")
            print("GENERATED PROMPT PREVIEW")
            print(f"{'='*80}")
            print(prompt)
            print(f"{'='*80}\n")
            
            logger.info(f"Generated prompt: {prompt}")

            return (prompt, prompt)

        except requests.exceptions.RequestException as e:
            raise RuntimeError(f"Grok API request failed: {str(e)}")
        except json.JSONDecodeError as e:
            raise RuntimeError(f"Failed to parse Grok API response: {str(e)}")
        except Exception as e:
            raise RuntimeError(f"Error analyzing image with Grok: {str(e)}")

    @staticmethod
    def _tensor_to_pil(image: torch.Tensor) -> Image.Image:
        """
        Convert ComfyUI tensor image to PIL Image

        Args:
            image: Tensor of shape (B, H, W, C) with values in [0, 1]

        Returns:
            PIL Image
        """
        # Take first image from batch if multiple
        if image.dim() == 4:
            image = image[0]

        # Convert to numpy and ensure proper range
        image_np = image.detach().cpu().numpy()

        # If values are in [0, 1], scale to [0, 255]
        if image_np.max() <= 1.0:
            image_np = (image_np * 255).astype(np.uint8)
        else:
            image_np = image_np.astype(np.uint8)

        # Handle different channel configurations
        if image_np.shape[-1] == 4:
            # RGBA - convert to RGB
            pil_image = Image.fromarray(image_np[:, :, :3], mode='RGB')
        elif image_np.shape[-1] == 3:
            # RGB
            pil_image = Image.fromarray(image_np, mode='RGB')
        elif image_np.shape[-1] == 1:
            # Grayscale
            pil_image = Image.fromarray(image_np[:, :, 0], mode='L')
        else:
            raise ValueError(f"Unsupported image shape: {image_np.shape}")

        return pil_image

    @staticmethod
    def _image_to_base64(image: Image.Image) -> str:
        """
        Convert PIL Image to base64 string

        Args:
            image: PIL Image

        Returns:
            Base64 encoded string
        """
        buffer = BytesIO()
        image.save(buffer, format="PNG")
        buffer.seek(0)
        image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
        return image_base64


# Export node class and display name
NODE_CLASS_MAPPINGS = {
    "GrokImageAnalyzer": GrokImageAnalyzer,
}

NODE_DISPLAY_NAMES = {
    "GrokImageAnalyzer": "Grok Image Analyzer",
}
