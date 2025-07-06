┌─────────────────────────────────────────────────────────────┐
│                    POLITECHECK APPLICATION                  │
├─────────────────────────────────────────────────────────────┤
│  Backend API (Python/Pyramid)                              │
│  ├── Tisane NLP Integration                                │
│  ├── Redis Cache Client                                    │
│  ├── Health Endpoints (/health)                            │
│  └── RESTful API Endpoints                                 │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│                    KUBERNETES CLUSTER                       │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────────┐    ┌─────────────────┐                │
│  │   Backend API   │    │   Redis Cache   │                │
│  │   Deployment    │    │   StatefulSet   │                │
│  │   (2-3 replicas)│    │   (1 replica)   │                │
│  └─────────────────┘    └─────────────────┘                │
│           │                       │                        │
│  ┌─────────────────┐    ┌─────────────────┐                │
│  │  ClusterIP Svc  │    │  ClusterIP Svc  │                │
│  │   (Port 8002)   │    │   (Port 6379)   │                │
│  └─────────────────┘    └─────────────────┘                │
└─────────────────────────────────────────────────────────────┘

# Deployment Configuration
- Replicas: 2 (scales 2-3 with HPA)
- Image: politecheck:latest
- Port: 8002
- Health Checks: /health endpoint
- Security: runAsUser: 1000

✅ Horizontal Pod Autoscaler (HPA): Scales based on CPU usage (80% threshold)
✅ Health Probes: Liveness (30s delay) and Readiness (5s delay) probes
✅ Service Account: Dedicated service account for RBAC
✅ ConfigMap/Secret Integration: Environment variables from K8s resources

# Redis Configuration
- Architecture: Standalone
- Persistence: 1Gi PVC (ReadWriteOnce)
- Memory: 256MB max, LRU eviction
- Authentication: Disabled (internal cluster)
- Resources: 250m-500m CPU, 256Mi-512Mi RAM

✅ Persistent Storage: 1Gi volume with auto-provisioning
✅ Memory Management: 256MB limit with LRU eviction policy
✅ Security Context: runAsUser: 1001, fsGroup: 1001
✅ Network Policy: Restricted ingress/egress

# ConfigMap (politecheck-config)
- POLITECHECK_ENV: "prod"
- REDIS_HOST: "politecheck-redis-master"
- REDIS_PORT: "6379"
- TISANE_BASE_URL: "https://api.tisane.ai/parse"
- LOG_LEVEL: "INFO"

Backend Pods → politecheck-backend:8002 (ClusterIP)
Backend Pods → politecheck-redis-master:6379 (Redis)


Health Monitoring
✅ Liveness Probes: /health endpoint (30s intervals)
✅ Readiness Probes: /health endpoint (5s intervals)
✅ Resource Monitoring: CPU/Memory metrics for HPA
Logging
✅ Structured logging (INFO level)
✅ Application logs via kubectl logs
✅ Redis logs via Bitnami chart