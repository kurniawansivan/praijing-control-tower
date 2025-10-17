FROM mcr.microsoft.com/devcontainers/base:ubuntu

RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
    sudo postgresql postgresql-contrib postgresql-client postgresql-common \
    curl git build-essential ca-certificates \
 && usermod -aG sudo vscode \
 && echo "vscode ALL=(ALL) NOPASSWD:ALL" > /etc/sudoers.d/90-vscode \
 && chmod 0440 /etc/sudoers.d/90-vscode \
 && rm -rf /var/lib/apt/lists/*
