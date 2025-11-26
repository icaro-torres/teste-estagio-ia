import math
import re
import logging
from strands import Agent, tool
from strands.models.ollama import OllamaModel 
from app.config import settings

logging.getLogger("strands").setLevel(logging.DEBUG)
logger = logging.getLogger(__name__)

@tool
async def calculator_tool(expression: str) -> str:
    """Useful for solving math problems.

    Args:
        expression: A mathematical expression string like '2 + 2', '1234 * 5678' or 'sqrt(144)'.
    """
    logger.info(f"Tool 'calculator_tool' acionada com: {expression}")
    
    allowed_chars = r"^[0-9+\-*/().,\s\^a-z]*$"
    
    if not re.match(allowed_chars, expression):
        if "_" in expression:
             logger.warning(f"Tentativa de injeção detectada: {expression}")
             return "Erro: A expressão contém caracteres não permitidos."
    
    allowed_names = {
        "sqrt": math.sqrt,
        "pow": math.pow,
        "abs": abs,
        "round": round
    }
    
    try:
        clean_expression = expression.strip().replace("^", "**")
        code = compile(clean_expression, "<string>", "eval")
        
        for name in code.co_names:
            if name not in allowed_names:
                raise ValueError(f"Função não permitida: {name}")
        
        result = eval(code, {"__builtins__": {}}, allowed_names)
        return str(result)
    except Exception as e:
        return f"Error calculating '{expression}': {str(e)}"

def get_agent():
    """
    Configura o Agente usando a classe nativa OllamaModel.
    """
    ollama_model = OllamaModel(
        host=settings.OLLAMA_HOST,
        model_id=settings.OLLAMA_MODEL,
        keep_alive="1h",
        temperature=0.1,
    )

    agent = Agent(
        model=ollama_model,
        tools=[calculator_tool],
        system_prompt="Você é um assistente útil. Se for matemática, use a tool calculator_tool. Responda de forma direta."
    )
    
    return agent