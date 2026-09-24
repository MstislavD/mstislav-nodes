"""Loads a random .png image from a folder (optionally recursive)."""

import random
from pathlib import Path

import numpy as np
import torch
from PIL import Image, ImageOps


class LoadRandomImage:
    """Picks a random .png from a folder and loads it as an IMAGE tensor.

    Seeded like the other nodes in this pack: the same seed always picks
    the same file, as long as the folder contents are unchanged (the
    candidate list is sorted by full path first). Only ``.png`` files
    are considered, matched case-insensitively.
    """

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "folder_path": ("STRING", {
                    "default": "",
                    "placeholder": "C:/path/to/your/png/folder",
                }),
                "seed": ("INT", {
                    "default": 0,
                    "min": 0,
                    "max": 0xFFFFFFFFFFFFFFFF,
                    "step": 1,
                    "display": "number",
                }),
            },
            "optional": {
                "recursive": ("BOOLEAN", {
                    "default": False,
                    "label_on": "search subfolders",
                    "label_off": "top level only",
                }),
            },
        }

    RETURN_TYPES = ("IMAGE", "STRING")
    RETURN_NAMES = ("image", "file_name")
    FUNCTION = "pick_and_load"
    CATEGORY = "utils/image"
    OUTPUT_NODE = False

    def pick_and_load(self, folder_path: str, seed: int, recursive: bool = False):
        folder = Path(folder_path).expanduser()
        if not folder.is_dir():
            raise ValueError(f"Load Random Image: folder not found: {folder_path!r}")

        candidates = folder.rglob("*") if recursive else folder.iterdir()
        files = sorted(
            p for p in candidates
            if p.is_file() and p.suffix.lower() == ".png"
        )
        if not files:
            scope = "recursively" if recursive else "at the top level only"
            raise ValueError(
                f"Load Random Image: no .png files found in {folder} ({scope})"
            )

        chosen = random.Random(seed).choice(files)

        with Image.open(chosen) as img:
            img = ImageOps.exif_transpose(img)
            img = img.convert("RGB")
            tensor = torch.from_numpy(np.asarray(img).astype(np.float32) / 255.0)
        tensor = tensor.unsqueeze(0)

        return (tensor, chosen.name)


NODE_CLASS_MAPPINGS = {
    "LoadRandomImage": LoadRandomImage,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "LoadRandomImage": "🖼️ Load Random Image",
}
