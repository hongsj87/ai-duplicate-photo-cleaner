import pytest
from pathlib import Path
from unittest.mock import patch, MagicMock
from core.hasher import PhotoHasher


def test_md5_returns_string(tmp_path):
    f = tmp_path / "test.jpg"
    f.write_bytes(b"fake image data")
    hasher = PhotoHasher()
    result = hasher.md5(f)
    assert isinstance(result, str)
    assert len(result) == 32


def test_md5_same_content_same_hash(tmp_path):
    f1 = tmp_path / "a.jpg"
    f2 = tmp_path / "b.jpg"
    f1.write_bytes(b"same content")
    f2.write_bytes(b"same content")
    hasher = PhotoHasher()
    assert hasher.md5(f1) == hasher.md5(f2)


def test_md5_different_content_different_hash(tmp_path):
    f1 = tmp_path / "a.jpg"
    f2 = tmp_path / "b.jpg"
    f1.write_bytes(b"content A")
    f2.write_bytes(b"content B")
    hasher = PhotoHasher()
    assert hasher.md5(f1) != hasher.md5(f2)


def test_similarity_score_identical():
    hasher = PhotoHasher()
    h = "0" * 16
    assert hasher.similarity_score(h, h) == 100.0


def test_is_supported():
    hasher = PhotoHasher()
    assert hasher.is_supported(Path("photo.jpg"))
    assert hasher.is_supported(Path("photo.PNG"))
    assert not hasher.is_supported(Path("doc.pdf"))
