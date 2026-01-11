# AgentOps Docker Deployments

## Open Source (SQLite)
```bash
cd docker/oss
docker-compose up -d
```

Uses agentic_sdk with SQLite storage.

## Enterprise (PostgreSQL + Redis)
```bash
cd docker/enterprise
docker-compose up -d
```

Full stack:
- API Server: http://localhost:8000
- PostgreSQL: localhost:5432
- Redis: localhost:6379

## Architecture
```
OSS:     [agentic_sdk CLI] → SQLite
Enterprise: [API Server] → PostgreSQL + Redis
```
