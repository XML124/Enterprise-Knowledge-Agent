# AWS Deployment Guide

Target services:
- ECR: Docker image registry
- ECS/Fargate: FastAPI container runtime
- RDS PostgreSQL: pgvector datastore
- S3: source-document storage
- Secrets Manager: API keys and database secrets
- IAM: least-privilege permissions
- CloudWatch: logs and metrics
- Application Load Balancer: HTTP entry point

## Suggested sequence
1. Create ECR repository.
2. Build and push the Docker image.
3. Create RDS PostgreSQL and enable `vector` extension.
4. Store secrets in Secrets Manager.
5. Create ECS/Fargate task definition and service.
6. Add an ALB health check at `/health`.
7. Send application logs to CloudWatch.

## Minimum operational metrics
- HTTP 5xx rate
- task restarts
- CPU/memory
- request latency
- LLM latency and failures
- retrieval latency
- empty/low-confidence retrieval rate
- token usage/cost

## Next production improvements
- Terraform
- authentication/SSO
- AWS WAF
- OpenTelemetry tracing
- SQS/background ingestion workers
- autoscaling
- document-level access control
- load testing
- security scanning
