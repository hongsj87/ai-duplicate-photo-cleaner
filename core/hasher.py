import hashlib
import imagehash
from PIL import Image
from pathlib import Path
from typing import Optional


class PhotoHasher:
    """Multi-algorithm photo hasher: MD5 (exact) + pHash (perceptual)."""

    SUPPORTED_FORMATS = {".jpg", ".jpeg", ".png", ".heic", ".webp", ".bmp", ".gif"}

    def md5(self, path: Path) -> Optional[str]:
        """Compute MD5 checksum for exact-duplicate detection."""
        try:
            h = hashlib.md5()
            with open(path, "rb") as f:
                for chunk in iter(lambda: f.read(8192), b""):
                    h.update(chunk)
            return h.hexdigest()
        except Exception:
            return None

    def phash(self, path: Path, hash_size: int = 16) -> Optional[str]:
        """Compute perceptual hash for near-duplicate detection."""
        try:
            img = Image.open(path).convert("RGB")
            return str(imagehash.phash(img, hash_size=hash_size))
        except Exception:
            return None

    def hamming_distance(self, hash1: str, hash2: str) -> int:
        h1 = imagehash.hex_to_hash(hash1)
        h2 = imagehash.hex_to_hash(hash2)
        return h1 - h2

    def similarity_score(self, hash1: str, hash2: str, max_dist: int = 64) -> float:
        """Return similarity score 0-100."""
        dist = self.hamming_distance(hash1, hash2)
        return max(0.0, (1 - dist / max_dist) * 100)

    def is_supported(self, path: Path) -> bool:
        return path.suffix.lower() in self.SUPPORTED_FORMATS
