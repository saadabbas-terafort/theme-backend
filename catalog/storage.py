import os
import uuid
from pathlib import Path

from supabase import create_client

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
SUPABASE_BUCKET = os.getenv("SUPABASE_BUCKET")


def get_supabase_client():
    if not SUPABASE_URL:
        raise ValueError("SUPABASE_URL is missing from environment variables.")
    if not SUPABASE_KEY:
        raise ValueError("SUPABASE_KEY is missing from environment variables.")
    if not SUPABASE_BUCKET:
        raise ValueError("SUPABASE_BUCKET is missing from environment variables.")
    return create_client(SUPABASE_URL, SUPABASE_KEY)


def img_upload(image_file, folder):
    extension = Path(image_file.name).suffix.lower()
    file_name = f"{uuid.uuid4()}{extension}"
    file_path = f"{folder.strip('/')}/{file_name}"
    file_data = image_file.read()
    client = get_supabase_client()

    try:
        client.storage.from_(SUPABASE_BUCKET).upload(file_path, file_data)
    except Exception as exc:
        raise RuntimeError(f"Supabase upload failed for {file_path}: {exc}") from exc

    return client.storage.from_(SUPABASE_BUCKET).get_public_url(file_path)
