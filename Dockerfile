# CIVISENSE Multi-Platform Production Dockerfile
FROM node:22-alpine

# Set working directory
WORKDIR /app

# Copy application manifest
COPY package.json ./

# Copy core server, database, and front/back assets
COPY server.js ./
COPY civisense.db ./
COPY frontend/ ./frontend/
COPY backend/ ./backend/

# Expose HTTP port
EXPOSE 8000

# Set environment variables
ENV NODE_ENV=production
ENV PORT=8000

# Automated healthcheck probe
HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
  CMD wget --no-verbose --tries=1 --spider http://127.0.0.1:8000/api/health || exit 1

# Start CIVISENSE Server
CMD ["node", "server.js"]
