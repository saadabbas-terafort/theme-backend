import os
import uuid
from supabase import create_client
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
SUPABASE_BUCKET = os.getenv("SUPABASE_BUCKET")


supabase = create_client(SUPABASE_URL , SUPABASE_KEY)


def img_upload(image_file , folder):
    extension = image_file.name.split(".")[-1]
    img_file =f"{uuid.uuid4()}.{extension}"
    file_path =f"{folder}/{img_file}"
    file_data =image_file.read()
    supabase.storage.from_(SUPABASE_BUCKET).upload(file_path, file_data)
    return supabase.storage.from_(SUPABASE_BUCKET).get_public_url(file_path)
        
        
        
