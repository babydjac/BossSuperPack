class KontextPromptForge:
    @classmethod
    def INPUT_TYPES(cls):
        return {"required": {"idea": ("STRING", {"multiline": True, "default": "a man with a sword in a fantasy landscape"})}}

    RETURN_TYPES = ("STRING",)
    FUNCTION = "forge"
    CATEGORY = "text"

    def forge(self, idea):
        prompt = self.apply_kontext_rules(idea)
        return (prompt,)

    def apply_kontext_rules(self, idea):
        lines = []
        if "change" in idea.lower() or "transform" in idea.lower():
            lines.append("Be specific and clear: avoid vague language.")
            lines.append("Use step-by-step editing when applicable.")
            lines.append("Explicitly state what should stay the same.")
        if "style" in idea.lower():
            lines.append("Transform to [specific style], while maintaining composition or character unchanged.")
        elif "background" in idea.lower():
            lines.append("Change the background to [new background], keep the subject in the exact same position and pose.")
        elif "text" in idea.lower():
            lines.append("Replace '[original text]' with '[new text]', maintain the same font style.")
        else:
            lines.append("Change [object] to [new state], keep [key traits] unchanged.")
        return "
".join(lines) + f"

>> Generated from vague idea:
\"{idea.strip()}\""

