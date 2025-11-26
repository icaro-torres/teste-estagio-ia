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
        if "_" in expression: return "Erro: Caracteres não permitidos."
    
    allowed_names = {"sqrt": math.sqrt, "pow": math.pow, "abs": abs, "round": round}
    try:
        clean = expression.strip().replace("^", "**")
        code = compile(clean, "<string>", "eval")
        for name in code.co_names:
            if name not in allowed_names: raise ValueError(f"Função proibida: {name}")
        return str(eval(code, {"__builtins__": {}}, allowed_names))
    except Exception as e:
        return f"Error calculating '{expression}': {str(e)}"

@tool
async def devops_knowledge_tool(topic: str) -> str:
    """Useful for retrieving technical definitions about DevOps, Cloud, and Infrastructure.
    Use this tool when the user asks about specific technical concepts like Docker, Kubernetes, CI/CD, or Terraform.

    Args:
        topic: The technical topic or keyword to search for.
    """
    logger.info(f"Tool 'devops_knowledge_tool' acionada para: {topic}")
    
    knowledge_base = {
        "docker": "Docker é uma plataforma de containerização que empacota aplicação e dependências em uma unidade padronizada, garantindo portabilidade entre ambientes.",
        "kubernetes": "Kubernetes (K8s) é um sistema open-source para orquestração de containers, automatizando deploy, escalabilidade e gestão de aplicações containerizadas.",
        "ci/cd": "CI/CD (Integração e Entrega Contínuas) é um método para entregar apps com frequência, usando automação nas etapas de build, teste e deploy.",
        "terraform": "Terraform é uma ferramenta de IaC (Infraestrutura como Código) que permite provisionar e gerenciar infraestrutura em nuvem usando arquivos de configuração declarativos.",
        "rag": "RAG (Retrieval-Augmented Generation) é uma técnica que otimiza a saída de um LLM referenciando uma base de conhecimento autoritativa externa antes de gerar a resposta."
    }
    
    topic_lower = topic.lower()
    for key, content in knowledge_base.items():
        if key in topic_lower:
            return f"[FONTE: Base de Conhecimento Interna] \nDefinição Técnica: {content}"
            
    return "Desculpe, esse termo técnico não consta na minha base de conhecimento de DevOps."

def get_agent():
    ollama_model = OllamaModel(
        host=settings.OLLAMA_HOST,
        model_id=settings.OLLAMA_MODEL,
        keep_alive="1h",
        temperature=0.1,
    )

    system_prompt = (
        "Você é um assistente técnico especializado em Engenharia de Software. "
        "1. Para cálculos, USE a 'calculator_tool'. "
        "2. Para conceitos técnicos de DevOps e Cloud, USE a 'devops_knowledge_tool' para buscar definições precisas. "
        "3. Se a tool retornar uma definição, use-a para compor sua resposta."
    )

    agent = Agent(
        model=ollama_model,
        tools=[calculator_tool, devops_knowledge_tool],
        system_prompt=system_prompt
    )
    
    return agent