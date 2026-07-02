import random


class RandomSublist:
    """Picks N random, unique entries from a comma-separated list."""

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "input_string": ("STRING", {
                    "multiline": True,
                    "default": "",
                    "placeholder": "apple, banana, cherry, date, elderberry",
                }),
                "number_of_choices": ("INT", {
                    "default": 3,
                    "min": 1,
                    "max": 9999,
                    "step": 1,
                    "display": "number",
                }),
                "seed": ("INT", {
                    "default": 0,
                    "min": 0,
                    "max": 0xFFFFFFFFFFFFFFFF,
                    "step": 1,
                    "display": "number",
                }),
            },
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("selected_entries",)
    FUNCTION = "pick"
    CATEGORY = "utils/text"
    OUTPUT_NODE = False

    def pick(self, input_string: str, number_of_choices: int, seed: int):
        raw = [s.strip() for s in input_string.split(",")]
        entries = [e for e in raw if e]

        if not entries:
            return ("",)

        rng = random.Random(seed)
        k = min(number_of_choices, len(entries))
        selected = rng.sample(entries, k)

        return (", ".join(selected),)


NODE_CLASS_MAPPINGS = {
    "RandomSublist": RandomSublist,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "RandomSublist": "🔀 Random Sublist",
}
