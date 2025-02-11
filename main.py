from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from config import Settings

import requests
import os

app = FastAPI()

settings = Settings()
app.mount("/static", StaticFiles(directory="static"))
templates = Jinja2Templates(directory="templates")

# 這裡以 OpenAI GPT API 作為範例
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "your-api-key-here")

class ChatRequest(BaseModel):
    message: str

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    print(settings.app_name)
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/chat/")
async def chat_with_ai(chat_request: ChatRequest):
    """向 OpenAI ChatGPT 發送請求"""

    url = "https://api.openai.com/v1/chat/completions"
    headers = {"Authorization": f"Bearer {OPENAI_API_KEY}", "Content-Type": "application/json"}
    payload = {
        "model": "gpt-3.5-turbo",
        "messages": [{"role": "user", "content": chat_request.message}]
    }
    response = requests.post(url, json=payload, headers=headers)
    
    if response.status_code == 200:
        reply = response.json()["choices"][0]["message"]["content"]
        return {"reply": reply}
    else:
        return {"error": "AI 服務無法回應", "status_code": response.status_code}
