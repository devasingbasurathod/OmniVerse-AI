"""Shared utility helpers."""

from datetime import datetime


def format_datetime(iso_string):
    """Format ISO datetime string for display."""
    try:
        dt = datetime.fromisoformat(iso_string)
        return dt.strftime("%b %d, %Y %H:%M")
    except (ValueError, TypeError):
        return iso_string or "—"


def format_file_size(size_bytes):
    """Human-readable file size."""
    if size_bytes < 1024:
        return f"{size_bytes} B"
    if size_bytes < 1024 * 1024:
        return f"{size_bytes / 1024:.1f} KB"
    return f"{size_bytes / (1024 * 1024):.1f} MB"
