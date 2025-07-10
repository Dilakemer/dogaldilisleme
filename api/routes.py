from fastapi import APIRouter
from pydantic import BaseModel
from services.response_generator import ResponseGenerator
from services.product_loader import load_products_from_db
from services.similarity_search import find_similar_question, load_questions

router = APIRouter()
questions = load_questions()

class ChatRequest(BaseModel):
    text: str

products = load_products_from_db()
response_generator = ResponseGenerator(products=products, debug=True)

pending_confirmation = None

@router.post("/chat")
async def chat_endpoint(request: ChatRequest):
    global pending_confirmation
    user_text = request.text.strip().lower()

    # 1) Onay bekleniyorsa
    if pending_confirmation:
        if user_text in ["evet", "yes", "doğru", "tamam", "aynen"]:
            # Onay sonrası yine gerçek girdiyi işliyoruz
            answer = response_generator.generate(pending_confirmation)
            pending_confirmation = None
            return {"response": answer}
        else:
            pending_confirmation = None
            return {"response": "Tamam, başka bir soru sorabilirsiniz."}

    # 2) Similarity bazlı kontrol (sadece intent unknown ise)
    match, score = find_similar_question(user_text, questions)
    if match:
        print(f"Benzerlik skoru: {score}")  # Log için
        if score > 0.5:
            # Direkt gerçek girdiyi kullanarak cevap üret
            response = response_generator.generate(user_text)
            return {"response": response}
        elif score > 0.45:
            # Onay için gerçek girdiyi sakla
            pending_confirmation = user_text
            return {"response": f"Bunu mu demek istediniz: '{match}'?"}
        else:
            return {"response": "Üzgünüm, sorduğunuzu anlayamadım."}

    # 3) Fallback: doğrudan intent sınıflandırıp handler çağır
    response = response_generator.generate(user_text)
    return {"response": response}
