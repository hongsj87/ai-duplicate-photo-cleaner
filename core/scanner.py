from pathlib import Path
from typing import List, Dict
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm
from .hasher import PhotoHasher


class PhotoScanner:
    """Multi-threaded photo scanner with duplicate detection."""

    def __init__(self, threshold: int = 90, workers: int = 4):
        self.threshold = threshold
        self.workers = workers
        self.hasher = PhotoHasher()

    def scan(self, directory: str) -> List[Path]:
        """Recursively scan directory for supported photos."""
        root = Path(directory)
        return sorted(
            p for p in root.rglob("*")
            if p.is_file() and self.hasher.is_supported(p)
        )

    def compute_hashes(self, photos: List[Path]) -> Dict[Path, dict]:
        """Compute hashes for all photos in parallel."""
        results = {}

        def _hash_one(path: Path):
            return path, {
                "md5": self.hasher.md5(path),
                "phash": self.hasher.phash(path),
                "size": path.stat().st_size,
            }

        with ThreadPoolExecutor(max_workers=self.workers) as executor:
            futures = {executor.submit(_hash_one, p): p for p in photos}
            for future in tqdm(as_completed(futures), total=len(photos), desc="Hashing"):
                path, data = future.result()
                results[path] = data

        return results

    def find_duplicates(self, hashes: Dict[Path, dict]) -> List[List[Path]]:
        """Group duplicate/similar photos."""
        groups: List[List[Path]] = []
        visited: set = set()
        paths = list(hashes.keys())

        # Pass 1: exact MD5 matches
        md5_map: Dict[str, List[Path]] = {}
        for path, data in hashes.items():
            if data["md5"]:
                md5_map.setdefault(data["md5"], []).append(path)
        for group in md5_map.values():
            if len(group) > 1:
                groups.append(group)
                visited.update(group)

        # Pass 2: perceptual hash similarity
        remaining = [p for p in paths if p not in visited]
        for i, p1 in enumerate(remaining):
            if p1 in visited:
                continue
            h1 = hashes[p1]["phash"]
            if not h1:
                continue
            group = [p1]
            for p2 in remaining[i + 1:]:
                if p2 in visited:
                    continue
                h2 = hashes[p2]["phash"]
                if h2 and self.hasher.similarity_score(h1, h2) >= self.threshold:
                    group.append(p2)
            if len(group) > 1:
                groups.append(group)
                visited.update(group)

        return groups
