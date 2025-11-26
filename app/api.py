from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, ConfigDict
from app.agent import get_agent
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

class ChatRequest(BaseModel):
    message: str
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "message": "Quanto é 10 + 1?"
            }
        }
    )

class ChatResponse(BaseModel):
    response: str

@router.post("/chat", response_model=ChatResponse, tags=["Chat"])
async def chat_endpoint(request: ChatRequest):
    logger.info(f"Recebendo mensagem: {request.message}")
    
    try:
        agent = get_agent()
        result = agent(request.message)
        
        final_answer = str(result.message)
        
        try:
            msg = result.message
            content = None
            
            if hasattr(msg, "content"):
                content = msg.content
            elif isinstance(msg, dict):
                content = msg.get("content")
            
            if content and isinstance(content, list) and len(content) > 0:
                first_block = content[0]
                if hasattr(first_block, "text"):
                    final_answer = first_block.text
                elif isinstance(first_block, dict):
                    final_answer = first_block.get("text", str(first_block))
                    
        except Exception as e:
            logger.warning(f"Erro ao limpar resposta (usando bruto): {e}")

        return ChatResponse(response=final_answer)
        
    except Exception as e:
        logger.error(f"Erro interno: {e}")
        raise HTTPException(status_code=500, detail=str(e))