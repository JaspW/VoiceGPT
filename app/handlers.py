import os
import pydub
import tracemalloc

from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from openai import OpenAI

import app.keyboards as kb
import app.states as st
from app.generators import generate_response
from app.generators import generate_unique_name
from bot import bot
from config import settings

client = OpenAI()

client_openai = OpenAI(api_key=settings.openai_api_token)

router = Router()

tracemalloc.start()


@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    await message.answer('Добро пожаловать в OpenAI Bot!',
                         reply_markup=kb.main)
    await state.clear()
    

@router.message(F.text == 'Chat')
async def chatting(message: Message, state: FSMContext):
    await message.answer('Введите Ваш запрос')
    await state.clear(st.Chat.text)
    

@router.message(st.Chat.text)
async def chatting_result(message: Message, state: FSMContext):
    await state.set_state(st.Chat.process)
    response = await generate_response(message.text)
    await message.answer(response.choices[0].message.content)
    await state.clear()


@router.message(st.Chat.process)
async def chatting_error(message: Message, state: FSMContext):
    await message.answer('Подождите ответа или напишите /start чтобы сбросить состояние.')
    

async def convert_ogg_to_mp3(file_path: str) -> str:
    audio: pydub.AudioSegment = pydub.AudioSegment.from_ogg(file_path)
    mp3_path = file_path.replace('.ogg', '.mp3')
    audio.export(mp3_path, format="mp3")
    return mp3_path    
    

@router.message(F.voice)
async def voice_chatting(message: Message, state: FSMContext):
    await state.set_state(st.Chat.process)
        
    voice = message.voice
    audio_file_info = await bot.get_file(voice.file_id)
    audio_file_path = audio_file_info.file_path
    downloaded_file = await bot.download_file(audio_file_path)
    
    ogg_path = f"{voice.file_id}.ogg"
    with open(ogg_path, 'wb') as f:
        f.write(downloaded_file.getvalue())
    
    mp3_path = await convert_ogg_to_mp3(ogg_path)
    
    mp3_transcription = open(mp3_path, "rb")
    transcription = client_openai.audio.transcriptions.create(
        model="whisper-1", 
        file=mp3_transcription,
        response_format="text"
    )
    transcripted_text = transcription

    answer = await generate_response(transcripted_text)
    
    output_filepath = f"{generate_unique_name}.mp3"
    response = client.audio.speech.create(
        model="tts-1",
        voice="alloy",
        input="Today is a wonderful day to build something people love!"
    )
    
    response.stream_to_file(output_filepath)
    
    await message.reply_audio(audio=output_filepath)
    
    os.remove(ogg_path)
    os.remove(mp3_path)
    
    await state.clear()