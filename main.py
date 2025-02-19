from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from config import Settings
from google import genai
from google.genai import types

app = FastAPI()

settings = Settings()
app.mount("/static", StaticFiles(directory="static"))
templates = Jinja2Templates(directory="templates")

# 初始化 Google Gemini 客戶端
try:
    client = genai.Client(api_key=settings.genai_api_key)
    chat = client.chats.create(
        model="gemini-2.0-flash", 
        config=types.GenerateContentConfig(
            max_output_tokens=200,
            temperature=0.5
        )
    )
except Exception as e:
    print(f"初始化 Google Gemini 客戶端失敗: {e}")
    exit(1)


class ChatRequest(BaseModel):
    message: str

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/chat/")
def chat_with_ai(chat_request: ChatRequest):
    """向 Gemini AI 發送請求"""
    try:
        response = chat.send_message(chat_request.message)

        if hasattr(response, "text") and response.text:
            return {"reply": response.text}
        else:
            raise ValueError("API 回應格式異常，未找到 `text` 屬性")
    except Exception as e:
        print(f"未知錯誤: {e}")
        
    return {"error": "AI 服務無法回應"}