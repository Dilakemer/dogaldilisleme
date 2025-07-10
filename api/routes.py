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

    # 1) Onay bekleniyorsa
    if pending_confirmation:
        if user_text in ["evet", "yes", "doğru", "tamam", "aynen"]:
            # Onaylandıktan sonra intent'e göre uygun işleyici çağrılır
            intent = response_generator.classifier.classify(pending_confirmation)
            if intent in ["customers_min_products", "customers_by_product"]:
                answer = response_generator.generate(pending_confirmation)
            else:
                answer = response_generator.generate_final_answer_with_sql(pending_confirmation)
            pending_confirmation = None
            return {"response": answer}
        else:
            pending_confirmation = None
            return {"response": "Tamam, başka bir soru sorabilirsiniz."}

    # 2) Intent belli ise onay gerek yok
    intent = response_generator.classifier.classify(user_text)
    if intent in ["customers_min_products", "customers_by_product"]:
        response = response_generator.generate_with_sql(user_text)
        return {"response": response}
    
    if intent == "customers_by_city":
        # doğrudan SQL’li cevap üret
        answer = response_generator.generate(user_text)
        return {"response": answer}

    # 3) Similarity bazlı soru eşleşmesi
    match, score = find_similar_question(user_text, questions)
    if match:
        print(f"Benzerlik skoru: {score}")  # Logla skorları kontrol için
        if score > 0.5:  # Direkt cevap eşik değerini düşürdüm
            return {"response": response_generator.generate_final_answer_with_sql(match)}
        elif score > 0.45:  # Onay aralığını daralttım
            pending_confirmation = match
            return {"response": f"Bunu mu demek istediniz: '{match}'?"}
        else:
            return {"response": "Üzgünüm, sorduğunuzu anlayamadım."}

    # 4) Fallback intent analizi ile cevap
    return {"response": response_generator.generate(user_text)}
