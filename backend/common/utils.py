"""
Common utilities for the backend
"""


def format_file_size(size_bytes: int) -> str:
    """
    Format file size in human readable format
    """
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.2f} TB"


def validate_mime_type(mime_type: str) -> bool:
    """
    Validate if MIME type is allowed
    """
    allowed_types = [
        'application/pdf',
        'image/jpeg',
        'image/png',
        'image/tiff',
        'application/msword',
        'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
        'application/vnd.ms-excel',
        'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    ]
    return mime_type in allowed_types
