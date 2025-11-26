#!/bin/bash

# ==============================================================================
# Script de Automação - Teste IA API
# ==============================================================================

GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

banner() {
    echo -e "${BLUE}"
    echo "############################################################"
    echo "#              🚀 AUTO-SETUP TESTE IA API                  #"
    echo "############################################################"
    echo -e "${NC}"
}

check_prerequisites() {
    echo -e "${YELLOW}🔍 Verificando ambiente...${NC}"
    
    if ! docker info > /dev/null 2>&1; then
        echo -e "${RED}❌ Erro: Docker não está rodando!${NC}"
        echo "Por favor, inicie o Docker Desktop e tente novamente."
        exit 1
    fi
}

start_app() {
    echo -e "${GREEN}🧹 Limpando ambiente anterior...${NC}"
    docker-compose down > /dev/null 2>&1

    echo -e "${GREEN}🏗️  Construindo e iniciando containers (Modo Detached)...${NC}"
    docker-compose up -d --build

    echo -e "${YELLOW}⏳ Aguardando a IA carregar (Cold Start)... Isso pode levar alguns segundos.${NC}"
    
    local retries=0
    local max_retries=60

    while true; do
        if curl -s http://localhost:8000/health | grep -q "ok"; then
            echo -e "\n${GREEN}✅ SUCESSO! A API está online e pronta.${NC}"
            break
        fi

        retries=$((retries+1))
        if [ $retries -ge $max_retries ]; then
            echo -e "\n${RED}❌ Tempo limite excedido. Verifique se o Docker tem memória suficiente.${NC}"
            echo -e "Dica: Rode 'docker-compose logs' para ver o erro."
            exit 1
        fi

        printf "."
        sleep 2
    done

    echo -e "${BLUE}============================================================${NC}"
    echo -e "👉 Swagger UI:   ${GREEN}http://localhost:8000/docs${NC}"
    echo -e "👉 Health Check: ${GREEN}http://localhost:8000/health${NC}"
    echo -e "${BLUE}============================================================${NC}"
    
    echo -e "${YELLOW}📜 Exibindo logs em tempo real (Ctrl+C para sair)...${NC}\n"
    docker-compose logs -f
}

run_tests() {
    echo -e "${GREEN}🧪 Rodando bateria de testes automatizados...${NC}"
    docker-compose run --rm api pytest tests/ -v
}

banner
check_prerequisites

case "$1" in
    test)
        run_tests
        ;;
    help)
        echo "Uso: ./run.sh [opcao]"
        echo "  (vazio) : Inicia a aplicação"
        echo "  test    : Roda os testes unitários"
        ;;
    *)
        start_app
        ;;
esac