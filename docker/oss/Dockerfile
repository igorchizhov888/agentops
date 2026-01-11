# AgentOps Open Source - Uses agentic_sdk core
FROM python:3.12-slim

WORKDIR /app

# Install agentic_sdk
RUN pip install --no-cache-dir agentic-sdk

# Expose CLI
ENTRYPOINT ["agentic-sdk"]
CMD ["--help"]
