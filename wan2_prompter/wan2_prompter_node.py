import requests

WAN2_PROMPT_GUIDE = """
You are an expert prompt writer for Wan 2.1 AI video generation.  
Generate concise, vivid, and cinematic video prompts that follow this structure:  
Subject (clear, brief description of main focus), Scene (environment details), Motion (specific movement details), Camera Language (camera angles, movements), Atmosphere (mood and lighting), Stylization (visual style).  

Avoid verbosity, do not add labels or headers, focus on smooth camera moves and natural scene descriptions.  
Keep prompt length around 80-100 words, vivid yet concise.

Example:  
"Full-body cinematic shot of a curvy woman slipping into tight jeans, slow and deliberate, accentuating wide hips and thick thighs. Camera pans upward from behind, lingering on her round booty as she adjusts fabric with a teasing tug. Soft morning light filters through a window, casting gentle shadows. Motion is smooth, seductive, unhurried, capturing every provocative detail."
"""

class Wan2PrompterNode:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "idea": ("STRING", {"default": "", "multiline": True}),
                "api_key": ("STRING", {"default": ""}),
            }
        }
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("wan2_prompt",)
    FUNCTION = "generate_prompt"
    CATEGORY = "Video"
    OUTPUT_NODE = True

    def generate_prompt(self, idea, api_key):
        if not api_key:
            return ("Error: API key required.",)
        system_prompt = WAN2_PROMPT_GUIDE + "\nUser input:\n" + idea.strip() + "\nGenerate the Wan 2.1 video prompt only."
        headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
        data = {
            "model": "grok-3-latest",
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": idea.strip()}
            ],
            "temperature": 0.3,
            "stream": False
        }
        try:
            resp = requests.post("https://api.x.ai/v1/chat/completions", json=data, headers=headers)
            resp.raise_for_status()
            result = resp.json().get("choices", [{}])[0].get("message", {}).get("content", "")
            if not result:
                result = "No output returned. Try with a clearer idea."
            # Remove any labels like **Wan2.1 NSFW Video Prompt** if present
            cleaned = result.replace("**Wan2.1 NSFW Video Prompt**:", "").strip()
            return (cleaned,)
        except Exception as e:
            return (f"API call failed: {e}",)
