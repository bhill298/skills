import re
import sys
import os


def parse_mbp(file_path):
    if not os.path.exists(file_path):
        print(f"Error: File not found - {file_path}")
        sys.exit(1)

    with open(file_path, "rb") as f:
        data = f.read()

    # This regex looks for Windows drive letters followed by paths ending in common audio extensions.
    # It accounts for the binary nature of the file by reading as bytes.
    pattern = b"([A-Za-z]:\\\\[^\x00]+?\\.(?:flac|mp3|m4a|wav|ogg|wma|ape|alac))"
    matches = re.findall(pattern, data, re.IGNORECASE)

    seen = set()
    paths = []
    for match in matches:
        try:
            # Decode the byte string to a standard UTF-8 string
            path = match.decode("utf-8", errors="ignore")

            # Deduplicate while preserving order
            if path not in seen:
                seen.add(path)
                paths.append(path)
        except Exception:
            pass

    return paths


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python scripts/parse_mbp.py <path_to_playlist.mbp>")
        sys.exit(1)

    extracted_paths = parse_mbp(sys.argv[1])
    for p in extracted_paths:
        print(p)
