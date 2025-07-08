from fastapi import APIRouter
from pydantic import BaseModel
from services.response_generator import ResponseGenerator

router = APIRouter()

class ChatRequest(BaseModel):
    text: str

response_generator = ResponseGenerator(products=None, debug=True)  # Ürün listesini istersen ekle

@router.post("/chat")
async def chat_endpoint(request: ChatRequest):
    response = response_generator.generate(request.text)
    return {"response": response}
