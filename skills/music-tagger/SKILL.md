---
name: music-tagger
description: Read and modify music file metadata tags (Title, Artist, Album, etc.) for audio files like MP3 and FLAC. Contains general tagging rules, classical music specific conventions, and technical instructions for command-line tagging using ffmpeg.
---

# Music Tag Editor

This skill provides comprehensive instructions for tagging music files. It relies on `ffmpeg` and `ffprobe`, which handle the underlying tag format differences (e.g., ID3v2 for MP3s vs Vorbis Comments for FLACs) seamlessly.

## Provided Scripts
A reusable shell script is provided in this skill's directory to simplify the safe application of tags using `ffmpeg` without worrying about manual temporary files. 

- `scripts/apply_tags.sh`

**Usage Example:**
```bash
./scripts/apply_tags.sh "song.flac" "title=New Title" "album=My Album" "artist=The Band"
```

## General Music Tagging Guidelines
When tagging general music (Pop, Rock, Jazz, Hip-Hop, etc.):
- **Title (`title`)**: The name of the specific song.
- **Artist (`artist`)**: The primary artist, band, or singer.
- **Album (`album`)**: The name of the album the song appears on.
- **Album Artist (`album_artist`)**: For compilations, this is often "Various Artists". Otherwise, it matches the main Artist. It is crucial for keeping albums from fragmenting in music players.
- **Track (`track`)**: The sequence number of the song on the album (e.g., "1" or "1/12").
- **Date/Year (`date`)**: The year of original release. Look it up via web search or Wikidata if unsure; do not guess.
- **Genre (`genre`)**: The primary genre.

## Classical Music Tagging Conventions
Classical music requires strict conventions that differ from standard pop music. Always map classical metadata as follows:

- **Title (`title`)**: The movement name (e.g., "I. Allegro", "No. 1 Andante Con Moto"). For standalone single-movement pieces, use the piece name. **Do not repeat the overarching piece/album name in the title** if it is a multi-movement work.
- **Artist (`artist`)**: The Composer (e.g., "Ludwig van Beethoven", "Wolfgang Amadeus Mozart").
- **Album (`album`)**: The overarching Piece Name or Collection (e.g., "Symphony No. 5 in C minor, Op. 67" or "Consolations, S. 172").
- **Album Artist (`album_artist`)**: The Performer(s), Ensemble, and/or Conductor (e.g., "Karl Böhm", "Evgeny Kissin").
- **Date (`date`)**: The year the piece was composed or published.
- **Track (`track`)**: The movement number. Convert Roman numerals (I, II, III) or "No. X" designations in the filename/movement name into standard integers for the track number. For standalone single-movement pieces (e.g., "Hungarian Rhapsody No. 2"), the track number should always be `1`.
- **Genre (`genre`)**: Always set to "Classical".

### Classical Examples
**Multi-movement Symphony:** Mozart's Symphony No. 1, Movement 1, performed by Karl Böhm.
- `title`: "I. Molto allegro"
- `artist`: "Wolfgang Amadeus Mozart"
- `album`: "Sinfonie Nr. 1 in Es-Dur KV 16"
- `album_artist`: "Karl Bohm"
- `track`: "1"

**Single-movement / Standalone Piece:** Chopin's Nocturne No. 1, performed by Yundi Li.
- `title`: "Nocturne No. 1 in B flat minor, Op. 9 No. 1"
- `artist`: "Frédéric Chopin"
- `album`: "Nocturne No. 1 in B flat minor, Op. 9 No. 1"  *(Matches Title)*
- `album_artist`: "Yundi Li"
- `track`: "1"  *(Always 1 for single pieces)*

## Technical Implementation & Takeaways

### Tooling Caveats (ffmpeg over exiftool)
- `exiftool` does not natively support writing metadata to FLAC files on all systems and will throw errors.
- Always use `ffmpeg` for writing/modifying tags and `ffprobe` for reading tags. 

### Reading Tags
To read all existing metadata from an audio file in a human-readable JSON format, use:
```bash
ffprobe -v quiet -print_format json -show_format "path/to/song.flac"
```
Look for standard fields inside `format.tags`. Tag names may be uppercase or lowercase.

### Writing/Modifying Tags (Manual via ffmpeg)
If you don't use the provided `scripts/apply_tags.sh` script, you must copy the audio stream without re-encoding by using `-c copy`. Because `ffmpeg` cannot write in-place to the same file, you must output to a temporary file and then move it back to overwrite the original.

**Example Command:**
```bash
ffmpeg -v quiet -i "path/to/song.mp3" -metadata title="I. Allegro" -metadata artist="Wolfgang Amadeus Mozart" -c copy "temp.mp3" -y && mv -f "temp.mp3" "path/to/song.mp3"
```
To remove a specific tag entirely, set it to an empty value (`-metadata genre=""`).

### Batch Processing & Scripting Takeaways
When processing an entire library or playlist, previous agents have found the following workflow to be the most reliable:
1. **Use Python to generate Shell/Bash Scripts:** Parsing complex filenames (with regex for Roman numerals, opus numbers, etc.) is error-prone in pure bash. Write a Python script to iterate through paths, map the tags, and generate a `.sh` file full of `ffmpeg` and `mv` commands.
2. **Handle Temp Files Safely:** When generating commands in a loop, either use unique temp file names (e.g., `temp_0.flac`, `temp_1.flac`) or execute them sequentially so `temp.flac` is continually overwritten and moved sequentially without race conditions. (The provided `scripts/apply_tags.sh` script handles temp files automatically.)
3. **Suppress Output:** `ffmpeg` is very noisy. Use `-v quiet` or append `> /dev/null 2>&1` to the commands in your generated bash script to prevent terminal overflow.
4. **MBP Playlists:** MusicBee `.mbp` files are binary. Do not parse them as text using `strings` or `cat`. Use the `mbp-parser` skill (specifically the `scripts/parse_mbp.py` script) to extract raw file paths reliably before applying any tagging logic.
