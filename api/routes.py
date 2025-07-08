from fastapi import APIRouter
from pydantic import BaseModel
from services.response_generator import ResponseGenerator
from services.product_loader import load_products_from_db
from services.similarity_search import find_similar_question, load_questions

router = APIRouter()
questions = load_questions()

class ChatRequest(BaseModel):
    text: str

# Ürünleri veritabanından yükle
products = load_products_from_db()

# ResponseGenerator'ı ürün listesi ile başlat
response_generator = ResponseGenerator(products=products, debug=True)

# Basit onay bekleme durumu (global değişken)
pending_confirmation = None

@router.post("/chat")
async def chat_endpoint(request: ChatRequest):
    global pending_confirmation
    user_text = request.text.strip().lower()

    if pending_confirmation:
        if user_text in ["evet", "yes", "doğru", "tamam"]:
            answer = response_generator.generate(pending_confirmation)
            pending_confirmation = None
            return {"response": answer}
        else:
            # Kullanıcı onaylamadı, onay durumunu temizle
            pending_confirmation = None

    match, score = find_similar_question(user_text, questions, threshold=0.85)
    if match and score > 0.65:
        pending_confirmation = match
        return {"response": f"Bunu mu demek istediniz: '{match}'?"}

    response = response_generator.generate(user_text)
    return {"response": response}
