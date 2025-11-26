# Exemplo de como essa aplicação seria provisionada na AWS
# Demonstração de Conhecimento em IaC (Infra as Code)

provider "aws" {
  region = "us-east-1"
}

resource "aws_ecr_repository" "api_repo" {
  name = "iateste-api"
}

resource "aws_ecs_cluster" "main" {
  name = "iateste-cluster"
}

resource "aws_ecs_task_definition" "api_task" {
  family                   = "iateste-api-task"
  network_mode             = "awsvpc"
  requires_compatibilities = ["FARGATE"]
  cpu                      = 1024
  memory                   = 2048
  execution_role_arn       = "arn:aws:iam::123456789012:role/ecsTaskExecutionRole"

  container_definitions = jsonencode([
    {
      name      = "api"
      image     = "${aws_ecr_repository.api_repo.repository_url}:latest"
      essential = true
      portMappings = [
        {
          containerPort = 8000
          hostPort      = 8000
        }
      ]
      environment = [
        { name = "APP_NAME", value = "Teste IA API Prod" }
        # Em prod, usaríamos um endpoint Bedrock ou Ollama em outra instância
      ]
    }
  ])
}