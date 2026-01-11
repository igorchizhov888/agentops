# AgentOps Enterprise - Full platform
FROM python:3.12-slim

WORKDIR /app

# Copy agentops source
COPY agentops /app/agentops
COPY setup.py /app/

# Install with enterprise features
RUN pip install --no-cache-dir -e .[enterprise]

# Expose API port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=3s \
  CMD curl -f http://localhost:8000/health || exit 1

CMD ["uvicorn", "agentops.api.server:app", "--host", "0.0.0.0", "--port", "8000"]
