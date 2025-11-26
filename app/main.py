from fastapi import FastAPI
from app.api import router
from app.config import settings

try:
    from app.utils import PerformanceMiddleware
except ImportError:
    PerformanceMiddleware = None

tags_metadata = [
    {
        "name": "Chat",
        "description": "Interação principal com o Agente de IA.",
    },
    {
        "name": "Health",
        "description": "Monitoramento de disponibilidade.",
    },
]

app = FastAPI(
    title=settings.APP_NAME,
    version="1.0.0",
    description="API do Desafio DreamSquad",
    openapi_tags=tags_metadata
)

if PerformanceMiddleware:
    app.add_middleware(PerformanceMiddleware)

app.include_router(router)

@app.get("/health", tags=["Health"])
def health_check():
    return {"status": "ok", "service": settings.APP_NAME}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)