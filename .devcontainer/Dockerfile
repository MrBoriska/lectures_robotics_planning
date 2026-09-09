# Lightweight Node base image based on Debian Bookworm Slim
FROM node:22-bookworm-slim

LABEL maintainer="Robotics Motion Planning Course Team"
LABEL description="DevContainer environment for Marp presentations with interactive algorithm widgets"

# Install essential lightweight packages & Chromium for Marp PDF/image export
RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    curl \
    ca-certificates \
    chromium \
    fonts-liberation \
    fonts-dejavu-core \
    fonts-freefont-ttf \
    && rm -rf /var/lib/apt/lists/*

# Environment variables for headless Chromium & Marp CLI
ENV CHROME_PATH=/usr/bin/chromium \
    PUPPETEER_EXECUTABLE_PATH=/usr/bin/chromium \
    PUPPETEER_SKIP_CHROMIUM_DOWNLOAD=true \
    MARP_NO_SANDBOX=true

# Switch to standard non-root user 'node' (UID 1000)
USER node
WORKDIR /workspace

# Default command
CMD ["sleep", "infinity"]
