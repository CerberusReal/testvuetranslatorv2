# НЕ ИСПОЛЬЗУЕТСЯ
# НЕ ИСПОЛЬЗУЕТСЯ
# НЕ ИСПОЛЬЗУЕТСЯ
# НЕ ИСПОЛЬЗУЕТСЯ
# НЕ ИСПОЛЬЗУЕТСЯ
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from openai import OpenAI
from dotenv import load_dotenv
# НЕ ИСПОЛЬЗУЕТСЯ
load_dotenv()
# НЕ ИСПОЛЬЗУЕТСЯ
app = FastAPI()
# НЕ ИСПОЛЬЗУЕТСЯ
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Разрешаем запросы с любых портов (включая 5173)
    allow_credentials=True,
    allow_methods=["*"],  # Разрешаем любые типы запросов (POST, GET и т.д.)
    allow_headers=["*"],
)
# НЕ ИСПОЛЬЗУЕТСЯ
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("key")
)
# НЕ ИСПОЛЬЗУЕТСЯ
# какие данные к нам прилетят от Vue
class TranslateRequest(BaseModel):
    text: str
    source_lang: str  
    output_lang: str  

# Ловим POST-запрос от Vue на адрес http://localhost:8000/translate
@app.post("/translate")
async def translate(req: TranslateRequest):
    system_prompt = (
        f"Ты — профессиональный переводчик. Переведи следующий текст с {req.source_lang} на {req.output_lang}. "
        "Отвечай только переводом, без лишних комментариев."
    )
    
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": req.text}
    ]

    response = client.chat.completions.create(
        model="nvidia/nemotron-3-super-120b-a12b:free",
        messages=messages
    )
    
    translation = response.choices[0].message.content
    
    # Отдаем в Vue текст перевода
    return {"translation": translation}