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
Replaces `__name__` wildcards in a prompt with random lines from
`wildcards/name.txt` (one entry per line, `#` lines are comments).
Recursive: a picked line may itself contain wildcards, which are resolved
in turn until no wildcard syntax remains. Seeded — same seed, same output.

**Inputs:**
- `prompt` — text with `__name__` placeholders
- `seed` — random seed

**Output:**
- `processed_prompt` — fully resolved text

**Wildcard files:** place `.txt` files in
`wildcards_processor/wildcards/`. Example: `__color__` reads
`wildcards/color.txt`. Subfolders work too: `__people/artist__` reads
`wildcards/people/artist.txt`. Missing files raise an error; a file that
references itself (directly or via a chain) is caught after 500
replacements. The shipped `color.txt`, `race.txt`, `scene.txt` are
examples — delete or overwrite them freely.

## Installation

Clone into `ComfyUI/custom_nodes/`:

```bash
cd ComfyUI/custom_nodes
git clone https://github.com/MstislavD/mstislav-nodes.git
```
