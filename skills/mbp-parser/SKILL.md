---
name: mbp-parser
description: Parse MusicBee playlist files (.mbp) to extract the absolute paths of the audio files they contain.
---

# MusicBee Playlist (.mbp) Parser

MusicBee playlist files (`.mbp`) are binary files, but the file paths for the audio tracks are stored as plaintext strings within the binary structure.

This skill provides a pre-written Python script that safely extracts these paths without needing to re-write a parser each time.

## Provided Scripts

A generalized Python script is located within this skill's directory to automatically extract file paths:
- `scripts/parse_mbp.py`

### Usage

You can execute the script directly using the `bash` tool (or `python` directly), passing the `.mbp` file as the argument:

```bash
python scripts/parse_mbp.py "MusicBee\Playlists\playlist.mbp"
```

The script will output a clean, deduplicated list of all absolute paths inside the playlist. You can easily pipe this output to a `.txt` file or feed it directly into another process via `xargs`.

Example:
```bash
python scripts/parse_mbp.py "Mozart.mbp" > paths.txt
```
