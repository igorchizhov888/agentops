# AgentOps - Enterprise Platform for AI Agent Operations

Enterprise features built on [agentic_sdk](https://github.com/igorchizhov888/agentic_sdk).

## What is AgentOps?

AgentOps extends the open-source agentic_sdk with:
- **Framework Integrations**: LangChain, CrewAI, AutoGen adapters
- **REST API**: FastAPI server for multi-user deployments
- **Web Dashboard**: Real-time monitoring and analytics
- **PostgreSQL**: Multi-instance storage (vs SQLite)
- **Enterprise Auth**: SAML, OAuth, RBAC

## Architecture
```
AgentOps (Enterprise)
  └── imports from agentic_sdk (OSS Core)
      ├── Observability
      ├── Prompt Management
      ├── Evaluation
      ├── Tool Registry
      └── A/B Testing
```

## Installation

### Option 1: Use OSS Core Only
```bash
pip install agentic-sdk
```

### Option 2: Use Enterprise Platform
```bash
pip install agentops
```

## Quick Start (OSS)
```bash
docker-compose -f docker/oss/docker-compose.yml up
```

## Quick Start (Enterprise)
```bash
docker-compose -f docker/enterprise/docker-compose.yml up
```

Access:
- API: http://localhost:8000
- Dashboard: http://localhost:3000

## Development
```bash
# Install agentic_sdk first
pip install -e ~/agentic_sdk

# Install agentops
pip install -e .
```

## Status

- ✓ Core infrastructure (from agentic_sdk)
- 🚧 Framework integrations (in progress)
- 🚧 REST API (in progress)
- 🚧 Web Dashboard (planned)

## License

Apache 2.0
