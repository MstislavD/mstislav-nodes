# mstislav-nodes

Custom ComfyUI nodes by Mstislav.

## Nodes

### 🔀 Random Sublist
Picks N random, unique entries from a comma-separated string.

**Inputs:**
- `input_string` — comma-separated list of entries
- `number_of_choices` — how many unique entries to select
- `seed` — random seed

**Output:**
- `selected_entries` — comma-separated string of selected entries

### 🎲 Wildcards Processor
Replaces `__name__` wildcards in a prompt with random lines from wildcard
files (one entry per line, `#` lines are comments). Recursive: a picked
line may itself contain wildcards, which are resolved in turn until no
resolvable wildcard syntax remains. Seeded — same seed, same output.

**Inputs:**
- `prompt` — text with `__name__` placeholders
- `seed` — random seed

**Output:**
- `processed_prompt` — resolved text (unresolved placeholders kept as-is)

**Wildcard files:** the `wildcards_processor/wildcards/` folder is your
content — it is gitignored and ships empty, so create your own `.txt`
files there. Lookup searches the whole folder tree: `__color__` finds
`wildcards/color.txt` or a `color.txt` in any subfolder (e.g.
`wildcards/ffpc_booru/color.txt`); explicit paths work too —
`__ffpc_booru/color__` reads that exact file. First match wins (sorted,
case-insensitive).

**Missing wildcards:** if no file is found (or the file has only
blank/comment lines), the `__name__` placeholder is left in the output
untouched — nothing raises. A file that references itself (directly or
via a chain) is caught after 500 replacements.

## Installation

Clone into `ComfyUI/custom_nodes/`:

```bash
cd ComfyUI/custom_nodes
git clone https://github.com/MstislavD/mstislav-nodes.git
```
