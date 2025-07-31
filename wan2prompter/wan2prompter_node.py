import requests

class Wan2PrompterNode:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "description": ("STRING", {"default": "", "multiline": True}),
                "action": ("STRING", {"default": ""}),
                "api_key": ("STRING", {"default": ""}),
            }
        }
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("wan2_prompt",)
    FUNCTION = "generate_wan2_prompt"
    CATEGORY = "Video"
    OUTPUT_NODE = True

    def generate_wan2_prompt(self, description, action, api_key):
        if not api_key:
            return ("Error: API key required.",)
        
        system_prompt = (
            "You are an expert in writing Wan 2.1 NSFW video prompts. "
            "Given a vague scene description and a specific action or motion, "
            "generate a concise, explicit Wan 2.1 style video prompt focusing on the action, setting, and mood. "
            "Avoid verbose descriptions or labeling; output only the prompt text, no headers or extra commentary."
        )
        
        user_content = f"Scene: {description.strip()}\nAction: {action.strip()}"
        
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_content}
        ]
        
        headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
        data = {
            "model": "grok-3-latest",
            "messages": messages,
            "temperature": 0.3,
            "stream": False
        }
        try:
            resp = requests.post("https://api.x.ai/v1/chat/completions", json=data, headers=headers)
            resp.raise_for_status()
            prompt = resp.json().get("choices", [{}])[0].get("message", {}).get("content", "").strip()
            if not prompt:
                prompt = "No output generated."
            return (prompt,)
        except Exception as e:
            return (f"API call failed: {e}",)
