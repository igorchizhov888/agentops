# AgentOps Project Structure

## Two Separate Repositories

### agentic_sdk (OSS Core)
- Location: ~/agentic_sdk
- GitHub: https://github.com/igorchizhov888/agentic_sdk
- Contains: All core functionality
  - Observability (tracing)
  - Prompt Management
  - Evaluation Framework
  - Tool Registry
  - A/B Testing
- Storage: SQLite
- Deployment: Single instance

### agentops (Enterprise Platform)
- Location: ~/agents
- GitHub: https://github.com/igorchizhov888/agentops
- Contains: Enterprise layer
  - Imports from agentic_sdk
  - Framework integrations
  - REST API
  - Web Dashboard
  - PostgreSQL support
- Depends on: agentic_sdk as installed package

## Relationship
```
agentops/
  imports from → agentic_sdk (installed via pip)
```

## Development Workflow

1. Work on core features in ~/agentic_sdk
2. Work on enterprise features in ~/agents
3. agentops uses: from agentic_sdk.observability import AgentTracer

## Next Steps

1. Build framework integrations (LangChain, CrewAI)
2. Create REST API
3. Build web dashboard
4. Add PostgreSQL implementation

Status: Foundation complete, ready for Phase 2
