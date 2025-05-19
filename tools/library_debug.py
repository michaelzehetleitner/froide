import argparse
import json
import plistlib
import sys
from pathlib import Path


def load_library(path: Path) -> dict:
    with path.open("rb") as f:
        return plistlib.load(f)


def find_track_ids(
    library: dict,
    track_ids: list[int] | None = None,
    persistent_ids: list[str] | None = None,
) -> list[int]:
    tracks = library.get("Tracks", {})
    ids = set()
    if track_ids:
        for tid in track_ids:
            if str(tid) in tracks:
                ids.add(int(tid))
    if persistent_ids:
        pid_map = {info.get("Persistent ID"): int(tid) for tid, info in tracks.items()}
        for pid in persistent_ids:
            tid = pid_map.get(pid)
            if tid is not None:
                ids.add(tid)
    return sorted(ids)


def get_playlists_for_track(library: dict, track_id: int) -> list[dict]:
    playlists = []
    for pl in library.get("Playlists", []):
        items = pl.get("Playlist Items")
        if not items:
            continue
        for item in items:
            if item.get("Track ID") == track_id:
                playlists.append(
                    {
                        "id": pl.get("Playlist ID"),
                        "name": pl.get("Name"),
                    }
                )
                break
    return playlists


def collect_info(library: dict, track_ids: list[int]) -> list[dict]:
    result = []
    tracks = library.get("Tracks", {})
    for tid in track_ids:
        info = tracks.get(str(tid))
        if not info:
            continue
        data = {
            "track_id": tid,
            "persistent_id": info.get("Persistent ID"),
            "name": info.get("Name"),
            "info": info,
            "playlists": get_playlists_for_track(library, tid),
        }
        result.append(data)
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description="Debug iTunes Library.xml")
    parser.add_argument("xml_path", type=Path, help="Path to Library.xml")
    parser.add_argument("--track-id", type=int, nargs="*", dest="track_ids")
    parser.add_argument("--persistent-id", nargs="*", dest="persistent_ids")
    args = parser.parse_args()

    library = load_library(args.xml_path)
    ids = find_track_ids(library, args.track_ids, args.persistent_ids)
    result = collect_info(library, ids)
    json.dump(result, indent=2, fp=sys.stdout)


if __name__ == "__main__":
    main()
