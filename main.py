from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import os

from api.routes import router
from services.product_loader import load_products_from_db
from services.response_generator import ResponseGenerator

# FastAPI uygulamasını oluştur
app = FastAPI()

# CORS ayarları (geliştirme için açık)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Prod ortamında domain kısıtlaması yap
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Ürünleri veritabanından yükle
products = load_products_from_db()

# ResponseGenerator nesnesini başlat ve router'a aktar
response_generator = ResponseGenerator(products=products, debug=True)

# Chat router'a generator'ı bağlayarak gönderiyoruz
app.include_router(router)

# Statik dosyaları sun
app.mount("/static", StaticFiles(directory="static"), name="static")

# Ana sayfa olarak index.html dön
@app.get("/", response_class=HTMLResponse)
async def root():
    
    index_path = os.path.join(os.path.dirname(__file__), "static", "index.html")
    with open(index_path, "r", encoding="utf-8") as f:
        return f.read()
