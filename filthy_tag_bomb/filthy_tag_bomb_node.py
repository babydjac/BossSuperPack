import requests

TEMPLATES = [
    "candid photo of two skinny horny 18 year old rave girls kissing, (breast grab:1.6), ((topless)), perky huge breasts, plump lips, young, youthful, petite, playful, horny, big eyes, wide eyes, (pale skin, blushing, sweaty skin, flushed cheeks, realistic skin, detailed skin, skin pores, skin blemishes), (long hair, damp hair), (colorful eye makeup, detailed makeup, rave makeup, festival makeup), in a dense crowd, at a rave, indoors, dark lighting, low light, poorly lit, real skin, intricately detailed eyes, detailed lips, 16K, (subsurface scattering:0.9)",
    "A captivating woman,age 20,with platinum blonde hair,fully naked. She stands on a balcony overlooking the city at night,the soft glow of the streetlights illuminating her figure.,Photorealistic,Hyperrealistic,Hyperdetailed,analog style,soft lighting,subsurface scattering,realistic,heavy shadow,masterpiece,best quality,ultra realistic,8k,golden ratio,Intricate,High Detail,film photography,soft focus,",
    "BREATHTAKING realistic 16K RAW photograph OF A BEAUTIFUL blonde TOPLESS 21-year-old woman with TOTALLY NAKED BREASTS and with pixie cut blonde hair, she is SKIING in Swiss Alps, she is wearing bright yellow and blue ski pants and ski helmet with mirrored goggles, she has gorgeous attractive beautiful phenomenal BIG voluptuous TOTALLY NAKED BREASTS with large areolas, realistic skin texture with natural skin imperfections and tiny freckles, the photo captures the FEELINGS OF JOY and DESIRE FOR LOVE, St. Moritz ski resort in the background, photorealism with intricate details, professional visual composition, deep focus, sophisticated color grading, award-winning erotic explicit nsfw photograph",
    "16K RAW ultrahigh resolution erotic sexually explicit photograph capturing these feelings: Through these eyes, no one will ever look as perfect as you did. Through this heart, no love will ever surpass my love for you. Highly detailed exciting arousing photograph of a blonde shorthaired nude 24-year-old Norwegian woman with fit body and gorgeous breasts and blonde trimmed pussy sitting in a green garden, film grain",
    "(amazing transcendental's dream:3.5) Create a image of a beautiful naked Italian woman, emo, narrow waist, wide hips, not muscular, and narrow jawline. Topless boobs out. She is looking at the viewer suggestively, teasing her tits. Large round breasts. The girl has detailed pale skin. Her long black hair frames her pale face, and her eyes, accentuated with dark makeup, shine with an intense light. Diamond necklace.  (maximum ultra high definition image quality and rendering:3), maximum image detail, maximum realistic render, (((ultra realist style))), realist side lighting, , 8K high definition,  realist soft lighting, (amazing special effect:3.5)"
]

class FilthyTagBombPromptNode:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "template_number": (
                    "CHOICE", {
                        "choices": ["1", "2", "3", "4", "5"],
                        "default": "1"
                    }
                ),
                "custom_idea": ("STRING", {"default": "", "multiline": True}),
                "api_key": ("STRING", {"default": ""}),
            }
        }
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("tag_bomb_prompt",)
    FUNCTION = "process"
    CATEGORY = "utils"
    OUTPUT_NODE = True

    def process(self, template_number, custom_idea, api_key):
        idx = int(template_number) - 1
        template = TEMPLATES[idx]
        if not api_key:
            return (f"No API key provided.",)
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"
        }
        system_prompt = (
            "You are an expert at writing maximally explicit, taglist-based prompts for FLUX/SDXL models. "
            "Given a user idea and a template prompt, ALWAYS rewrite the user's idea as a single comma-separated, weighted, explicit taglist using the exact structure, density, and anatomical focus of the template. "
            "Never write English sentences or paragraphs—only a dense, explicit, comma-separated taglist, with parentheticals, weights, and visual body/anatomy focus just like the template. "
            f"Template prompt:\n{template}\n"
            "Output ONLY the new taglist prompt, nothing else."
        )
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": custom_idea.strip()}
        ]
        data = {
            "model": "grok-3-latest",
            "messages": messages,
            "stream": False,
            "temperature": 0.2
        }
        try:
            resp = requests.post("https://api.x.ai/v1/chat/completions", json=data, headers=headers)
            resp.raise_for_status()
            result = resp.json().get("choices", [{}])[0].get("message", {}).get("content", "")
            if not result:
                result = "No output returned. Try a different prompt or template."
            return (result,)
        except Exception as e:
            return (f"Error calling Grok API: {e}",)
