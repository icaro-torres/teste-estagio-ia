import pytest
import asyncio
from app.agent import calculator_tool

def run_sync(coroutine):
    return asyncio.run(coroutine)


def test_basic_arithmetic():
    """Testa operações básicas."""
    assert run_sync(calculator_tool("2 + 2")) == "4"
    assert run_sync(calculator_tool("10 - 5")) == "5"
    assert run_sync(calculator_tool("1234 * 5678")) == "7006652"
    assert run_sync(calculator_tool("10 / 2")) == "5.0"

def test_advanced_math():
    """Testa funções permitidas."""
    assert float(run_sync(calculator_tool("sqrt(144)"))) == 12.0
    assert float(run_sync(calculator_tool("pow(2, 3)"))) == 8.0
    assert run_sync(calculator_tool("abs(-50)")) == "50"
    assert run_sync(calculator_tool("round(3.14159, 2)")) == "3.14"

def test_complex_expressions():
    """Testa precedência."""
    assert run_sync(calculator_tool("(2 + 3) * 4")) == "20"


def test_security_import_injection():
    """Tenta injeção de código."""
    payload = "__import__('os').system('ls')"
    result = run_sync(calculator_tool(payload))
    assert "Erro" in result or "não permitida" in result

def test_security_file_access():
    """Tenta ler arquivos."""
    payload = "open('/etc/passwd').read()"
    result = run_sync(calculator_tool(payload))
    assert "Erro" in result or "não permitida" in result

def test_invalid_syntax():
    """Testa sintaxe inválida."""
    result = run_sync(calculator_tool("2 + * 2"))
    assert "Error" in result