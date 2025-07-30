from .flux_prompter      import FluxPrompterNode
from .flux_dual_prompter import FluxDualPromptNode

NODE_CLASS_MAPPINGS = {
    "FluxPrompterNode":     FluxPrompterNode,
    "FluxDualPromptNode":   FluxDualPromptNode,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "FluxPrompterNode":     "Flux Prompter Node",
    "FluxDualPromptNode":   "Flux Dual Prompt Node (Grok)",
}

print("\033[34mflux_prompter package: \033[92mLoaded FluxPrompterNode & FluxDualPromptNode\033[0m")
