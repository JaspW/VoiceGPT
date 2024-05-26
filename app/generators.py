import uuid

from pydub import AudioSegment
from openai import AsyncOpenAI

from config import settings

client = AsyncOpenAI(api_key=settings.openai_api_token)

AUDIOS_DIR = 'audios'

def generate_unique_name():
    uuid_value = uuid.uuid4()
    return f"{str(uuid_value)}"

async def generate_response(text):
    response = await client.chat.completions.create(
       messages=[
           {
               "role": "user", 
               "content": text,
               }
           ],
       model="gpt-3.5-turbo",
       )
    return response
