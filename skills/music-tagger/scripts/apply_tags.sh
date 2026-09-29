#!/bin/bash
# Safely apply metadata to an audio file using ffmpeg (which requires a temp file)
if [ "$#" -lt 2 ]; then
    echo "Usage: $0 <file> <key=value> [key=value...]"
    echo 'Example: $0 "song.flac" "title=New Title" "artist=The Band"'
    exit 1
fi

FILE="$1"
shift

if [ ! -f "$FILE" ]; then
    echo "Error: File not found - $FILE"
    exit 1
fi

METADATA_ARGS=()
for arg in "$@"; do
    METADATA_ARGS+=("-metadata" "$arg")
done

# Create a safe temp file based on original extension
EXTENSION="${FILE##*.}"
TEMP_FILE="${FILE%.*}_temp_tagging.${EXTENSION}"

# Suppress ffmpeg output and run copy
ffmpeg -v quiet -i "$FILE" "${METADATA_ARGS[@]}" -c copy "$TEMP_FILE" -y

if [ $? -eq 0 ]; then
    mv -f "$TEMP_FILE" "$FILE"
else
    echo "Error: Failed to apply tags to $FILE"
    rm -f "$TEMP_FILE"
    exit 1
fi
