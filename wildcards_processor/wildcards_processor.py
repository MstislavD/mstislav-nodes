import os
import random
import re

# Wildcard syntax: __name__ (name may contain letters, digits, underscores,
# spaces, hyphens, dots and slashes so subfolders like __people/artist__ work).
WILDCARD_RE = re.compile(r"__([\w\s\-./]+?)__")

# Wildcard files live in the 'wildcards' folder next to this module.
WILDCARDS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "wildcards")

# Safety cap: any realistic prompt resolves in a handful of replacements.
# Exceeding this means a file references itself (directly or via a chain).
MAX_REPLACEMENTS = 500

# Try in order: utf-8-sig handles BOM, cp1251 covers Russian wildcard files.
_ENCODINGS = ("utf-8-sig", "cp1251", "latin-1")


def _read_entries(path: str):
    """Read one-entry-per-line file; skip blank lines and '# comment' lines."""
    for enc in _ENCODINGS:
        try:
            with open(path, "r", encoding=enc) as f:
                raw = f.read()
            break
        except UnicodeDecodeError:
            continue

    entries = []
    for line in raw.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        entries.append(line)
    return entries


class WildcardsProcessor:
    """Replaces __name__ wildcards with random lines from wildcards files.

    Files are looked up in the 'wildcards' folder AND in all its subfolders
    (first match in sorted order wins). Recursive: a picked line may itself
    contain wildcards, which are resolved in turn. Unresolvable wildcards
    (no file found / file has no usable entries) are left in place as-is.
    Seeded -> deterministic output.
    """

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "prompt": ("STRING", {
                    "multiline": True,
                    "default": "",
                    "placeholder": "portrait of the __color__ __race__",
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
    RETURN_NAMES = ("processed_prompt",)
    FUNCTION = "process"
    CATEGORY = "utils/text"
    OUTPUT_NODE = False

    def process(self, prompt: str, seed: int):
        if not prompt or not prompt.strip():
            return ("",)
        rng = random.Random(seed)
        return (self._resolve(prompt, rng),)

    # --- internals -------------------------------------------------------

    def _load_entries(self, name: str):
        """Return random-pickable entries for a wildcard name, or None.

        Search order:
          1. exact path (name may itself contain subfolder slashes),
          2. all subfolders of WILDCARDS_DIR (first match in sorted order).
        Returns None when nothing usable is found so the caller can leave
        the placeholder in place. Raises only for unsafe names.
        """
        if not name or ".." in name or name.startswith("/") or os.path.isabs(name):
            raise ValueError(
                f"[WildcardsProcessor] Invalid wildcard name: '__{name}__'"
            )

        # Prefer the file exactly as named; fall back to appending '.txt'.
        candidates = [name]
        if not name.lower().endswith(".txt"):
            candidates.append(name + ".txt")

        # 1) exact path (keeps explicit subfolder refs like __sub/name__ working)
        for cand in candidates:
            path = os.path.join(WILDCARDS_DIR, cand)
            if os.path.isfile(path):
                return _read_entries(path) or None

        # 2) recursive search through all subfolders
        for cand in candidates:
            matches = self._find_in_subfolders(cand)
            for path in matches:
                entries = _read_entries(path)
                if entries:
                    return entries
            # A matching file existed but had no usable entries -> unresolvable.
            if matches:
                return None

        return None  # not found -> leave placeholder in place

    @staticmethod
    def _find_in_subfolders(filename: str):
        """All files matching `filename` (case-insensitive) under WILDCARDS_DIR."""
        matches = []
        target = filename.lower()
        for root, _dirs, files in os.walk(WILDCARDS_DIR):
            for f in files:
                if f.lower() == target:
                    matches.append(os.path.join(root, f))
        return sorted(matches)

    def _resolve(self, text: str, rng: random.Random) -> str:
        """Replace wildcards left-to-right until none remain.

        Wildcards with no resolvable file are left in place untouched.
        """
        replacements = 0
        pos = 0
        missing = set()  # names known to be unresolvable -> skip, keep placeholder

        while True:
            m = WILDCARD_RE.search(text, pos)
            if m is None:
                return text

            name = m.group(1).strip()

            if name in missing:
                pos = m.end()
                continue

            entries = self._load_entries(name)
            if entries is None:
                missing.add(name)
                pos = m.end()
                continue

            replacements += 1
            if replacements > MAX_REPLACEMENTS:
                raise ValueError(
                    f"[WildcardsProcessor] Exceeded {MAX_REPLACEMENTS} wildcard "
                    f"replacements — possible infinite recursion (a wildcard file "
                    f"that references itself). Wildcards dir: {WILDCARDS_DIR}"
                )

            entry = rng.choice(entries)
            text = text[:m.start()] + entry + text[m.end():]
            pos = m.start()  # re-scan the inserted text for nested wildcards


NODE_CLASS_MAPPINGS = {
    "WildcardsProcessor": WildcardsProcessor,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "WildcardsProcessor": "🎲 Wildcards Processor",
}
