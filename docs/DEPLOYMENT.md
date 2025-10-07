# Deployment Guide

## Prerequisites

- Docker and Docker Compose (for containerized deployment)
- Kubernetes cluster (for K8s deployment)
- Python 3.11+ and Node.js 18+ (for local development)

## Docker Compose Deployment

### 1. Quick Start

```bash
# Clone the repository
git clone https://github.com/stone-PETER/SIH25-KMRL-doc-support.git
cd SIH25-KMRL-doc-support

# Navigate to Docker directory
cd deployment/docker

# Start all services
docker-compose up -d

# Check status
docker-compose ps

# View logs
docker-compose logs -f
```

### 2. Services

The Docker Compose setup includes:
- PostgreSQL (port 5432)
- Redis (port 6379)
- Elasticsearch (port 9200)
- Backend API (port 8000)
- Frontend (port 3000)
- n8n (port 5678)

### 3. Stop Services

```bash
docker-compose down

# Remove volumes (will delete all data)
docker-compose down -v
```

## Kubernetes Deployment

### 1. Prerequisites

- kubectl configured with cluster access
- Container images built and pushed to registry

### 2. Build and Push Images

```bash
# Build backend image
cd backend
docker build -t your-registry/kmrl-backend:latest .
docker push your-registry/kmrl-backend:latest

# Build frontend image
cd ../frontend
docker build -t your-registry/kmrl-frontend:latest .
docker push your-registry/kmrl-frontend:latest
```

### 3. Deploy to Kubernetes

```bash
cd deployment/kubernetes

# Create namespace
kubectl apply -f namespace.yaml

# Deploy databases
kubectl apply -f postgres-deployment.yaml
kubectl apply -f redis-deployment.yaml
kubectl apply -f elasticsearch-deployment.yaml

# Wait for databases to be ready
kubectl wait --for=condition=ready pod -l app=postgres -n kmrl-doc-automation --timeout=300s

# Deploy application
kubectl apply -f backend-deployment.yaml
kubectl apply -f frontend-deployment.yaml

# Check deployment status
kubectl get pods -n kmrl-doc-automation
kubectl get services -n kmrl-doc-automation
```

### 4. Access the Application

```bash
# Get frontend service external IP
kubectl get service frontend -n kmrl-doc-automation

# Port forward for local access (if LoadBalancer not available)
kubectl port-forward service/frontend 3000:80 -n kmrl-doc-automation
kubectl port-forward service/backend 8000:8000 -n kmrl-doc-automation
```

### 5. Scale Services

```bash
# Scale backend
kubectl scale deployment backend --replicas=5 -n kmrl-doc-automation

# Scale frontend
kubectl scale deployment frontend --replicas=3 -n kmrl-doc-automation
```

## Configuration

### Backend Configuration

Create a `.env` file in the backend directory:

```bash
cp backend/.env.example backend/.env
```

Edit the `.env` file with your settings:
- Database credentials
- Redis connection
- Storage configuration
- API keys

### Frontend Configuration

Create a `.env` file in the frontend directory:

```
REACT_APP_API_URL=http://localhost:8000/api/v1
```

## Database Migration

```bash
# Access the backend container
docker exec -it kmrl-backend bash

# Run migrations (if using Alembic)
alembic upgrade head
```

## Monitoring

### View Logs

**Docker:**
```bash
docker-compose logs -f backend
docker-compose logs -f frontend
```

**Kubernetes:**
```bash
kubectl logs -f deployment/backend -n kmrl-doc-automation
kubectl logs -f deployment/frontend -n kmrl-doc-automation
```

### Health Checks

```bash
# Backend health
curl http://localhost:8000/health

# Database connection
curl http://localhost:8000/api/v1/documents
```

## Troubleshooting

### Backend won't start
- Check database connection in logs
- Verify environment variables
- Ensure PostgreSQL is running

### Frontend can't connect to backend
- Check CORS configuration
- Verify API_URL environment variable
- Check network connectivity

### Database connection failed
- Verify database credentials
- Check if PostgreSQL container is running
- Ensure database exists

## Backup and Restore

### Backup PostgreSQL

```bash
docker exec kmrl-postgres pg_dump -U postgres document_automation > backup.sql
```

### Restore PostgreSQL

```bash
cat backup.sql | docker exec -i kmrl-postgres psql -U postgres document_automation
```

## Security Considerations

1. Change default passwords in production
2. Use secrets management (K8s secrets, AWS Secrets Manager)
3. Enable SSL/TLS for all connections
4. Configure firewall rules
5. Use non-root users in containers
6. Scan images for vulnerabilities
7. Keep dependencies updated

## Production Checklist

- [ ] Change all default passwords
- [ ] Configure SSL certificates
- [ ] Set up monitoring and alerting
- [ ] Configure backup strategy
- [ ] Set resource limits
- [ ] Enable logging aggregation
- [ ] Configure auto-scaling
- [ ] Set up CI/CD pipeline
- [ ] Configure disaster recovery
- [ ] Perform security audit
