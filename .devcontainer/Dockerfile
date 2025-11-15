FROM mcr.microsoft.com/devcontainers/python:1-3.13

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Set environment variables for uv
ENV UV_LINK_MODE=copy \
    UV_COMPILE_BYTECODE=1 \
    UV_PYTHON_DOWNLOADS=never

# Install additional system packages if needed
RUN apt-get update && export DEBIAN_FRONTEND=noninteractive \
    && apt-get -y install --no-install-recommends \
    git \
    postgresql-client \
    && apt-get clean -y && rm -rf /var/lib/apt/lists/*

# Set the working directory
WORKDIR /workspace
