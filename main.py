from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from api.routes import router
import os
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Geliştirme için, prod için domain gir
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(router)

# Static dosya klasörünü tanıt
app.mount("/static", StaticFiles(directory="static"), name="static")

# Ana sayfada index.html dosyasını dön
@app.get("/", response_class=HTMLResponse)
async def root():
    index_path = os.path.join("static", "index.html")
    with open(index_path, "r", encoding="utf-8") as f:
        return f.read()
