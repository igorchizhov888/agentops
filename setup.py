"""
AgentOps - Enterprise Platform for AI Agent Operations

Built on agentic_sdk with enterprise features.
"""

from setuptools import setup, find_packages

setup(
    name="agentops",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "agentic-sdk>=0.1.0",  # Our OSS dependency
        "fastapi>=0.104.0",
        "uvicorn>=0.24.0",
        "psycopg2-binary>=2.9.9",
        "redis>=5.0.0",
    ],
    extras_require={
        "enterprise": [
            "python-saml>=1.15.0",
            "pyjwt>=2.8.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "agentops=agentops.cli.main:cli",
        ],
    },
    author="Igor Chizhov",
    description="Enterprise Platform for AI Agent Operations",
    python_requires=">=3.11",
)
