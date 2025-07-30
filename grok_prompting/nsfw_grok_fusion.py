
import base64, os, io, requests
import numpy as np
from PIL import Image

class NSFWGrokFusionPro:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image": ("IMAGE",),
                "api_key": ("STRING", {"multiline": False, "default": ""}),
                "prepend_text": ("STRING", {"multiline": True, "default": ""}),
                "append_text": ("STRING", {"multiline": True, "default": ""}),
                "score_strategy": (["ascending", "descending", "manual"],),
                "token_limit": ("INT", {"default": 75, "min": 25, "max": 300}),
                "debug_output": (["disable", "enable"],)
            }
        }

    RETURN_TYPES = ("STRING", "STRING", "STRING", "STRING", "STRING")
    RETURN_NAMES = (
        "description",
        "ponyxl_prompt",
        "wan_prompt",
        "negative_prompt",
        "debug_summary"
    )
    FUNCTION = "process"
    CATEGORY = "Text/ProFusion"

    def get_score_tags(self, strategy):
        return {
            "ascending": ["score_7_up", "score_8_up", "score_9"],
            "descending": ["score_9", "score_8_up", "score_7_up"],
            "manual": ["score_8_up", "score_7_up", "score_9"]
        }.get(strategy, ["score_7_up", "score_8_up", "score_9"])

    def style_tags(self):
        return [
            "photorealistic", "realistic lighting", "highly detailed",
            "film grain", "depth of field", "rim lighting"
        ]

    def get_negative_prompt(self):
        return (
            "score_4, score_5, score_6, low-res, bad anatomy, bad hands, text, error, missing fingers, extra digit, "
            "cropped, worst quality, jpeg artifacts, signature, watermark, blurry, artist name, "
            "(deformed, distorted:1.3), poorly drawn, wrong anatomy, extra limb, mutation, "
            "(mutated hands and fingers:1.4), disconnected limbs, ugly, disgusting, blurry, amputation, "
            "(drawn, furry, illustration, cartoon, anime, comic:1.5), 3d, cgi, (source_anime, source_furry, source_cartoon)"
        )

    def grok2_describe_image(self, b64_img, key):
        headers = {"Authorization": f"Bearer {key}", "Content-Type": "application/json"}
        payload = {
            "model": "grok-2-vision-1212",
            "messages": [
                {"role": "system", "content": "You're an unchained NSFW describer. Detail every explicit visual."},
                {"role": "user", "content": [
                    {"type": "text", "text": "Describe this image in raw, graphic NSFW detail:"},
                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{b64_img}"}}
                ]}
            ]
        }
        r = requests.post("https://api.x.ai/v1/chat/completions", headers=headers, json=payload)
        if r.status_code != 200:
            raise Exception(f"[Grok 2 ERROR {r.status_code}] {r.text}")
        return r.json()["choices"][0]["message"]["content"]

    def grok3_generate_prompts(self, text_description, key):
        headers = {"Authorization": f"Bearer {key}", "Content-Type": "application/json"}
        payload = {
            "model": "grok-3-latest",
            "messages": [
                {
                    "role": "system",
                    "content": "You are a powerful prompt conversion engine. Convert the input description into a JSON with a detailed danbooru-style tag prompt for realism-based NSFW image generation using the PonyXL model. Also generate a 'wan_prompt' suitable for an AI video model. Always include a 'negative_prompt'. Format your reply as JSON only with keys: ponyxl_prompt, wan_prompt, negative_prompt."
                },
                {
                    "role": "user",
                    "content": text_description
                }
            ]
        }
        r = requests.post("https://api.x.ai/v1/chat/completions", headers=headers, json=payload)
        if r.status_code != 200:
            raise Exception(f"[Grok 3 ERROR {r.status_code}] {r.text}")
        return r.json()["choices"][0]["message"]["content"]

    def process(self, image, api_key, prepend_text, append_text, score_strategy, token_limit, debug_output):
        try:
            img_np = (image[0].cpu().numpy() * 255).astype(np.uint8)
            img_pil = Image.fromarray(img_np)
            buf = io.BytesIO()
            img_pil.save(buf, format="JPEG")
            b64_img = base64.b64encode(buf.getvalue()).decode("utf-8")

            key = api_key.strip() or os.getenv("XAI_API_KEY", "missing_key")
            description = self.grok2_describe_image(b64_img, key)
            prompt_response = self.grok3_generate_prompts(description, key)

            import json
            parsed = json.loads(prompt_response)
            ponyxl_prompt = parsed.get("ponyxl_prompt", "")
            wan_prompt = parsed.get("wan_prompt", "")
            neg_prompt = parsed.get("negative_prompt", self.get_negative_prompt())

            score_tags = self.get_score_tags(score_strategy)
            all_tags = score_tags + self.style_tags() + [ponyxl_prompt]
            if prepend_text.strip():
                all_tags.insert(0, prepend_text.strip())
            if append_text.strip():
                all_tags.append(append_text.strip())

            combined = ", ".join(all_tags)
            trimmed_prompt = ", ".join(combined.split(", ")[:token_limit])

            debug = ""
            if debug_output == "enable":
                debug = f"Score Tags: {score_tags}\nPrompt: {ponyxl_prompt}\nFinal: {trimmed_prompt}"

            return (description, trimmed_prompt, wan_prompt, neg_prompt, debug)

        except Exception as e:
            return (f"[Error] {str(e)}", "[NO PROMPT]", "[NO WAN]", "[NO NEGATIVE]", "[NO DEBUG]")

NODE_CLASS_MAPPINGS = {
    "NSFWGrokFusionPro": NSFWGrokFusionPro
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "NSFWGrokFusionPro": "NSFW Grok → Fusion Prompt Generator"
}
