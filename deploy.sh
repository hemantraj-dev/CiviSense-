#!/usr/bin/env bash
# ==============================================================================
# CIVISENSE Automated Linux Server Deployment Script
# Supports: Ubuntu 20.04+, Debian 11+, RHEL 8+, CentOS Stream
# ==============================================================================
set -e

echo ">>> Starting CIVISENSE Deployment..."

# 1. Check Node.js
if ! command -v node &> /dev/null; then
    echo ">>> Node.js not detected. Installing Node.js LTS (v20+)..."
    curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
    sudo apt-get install -y nodejs
else
    echo ">>> Node.js $(node -v) detected."
fi

# 2. Setup Destination Directory
APP_DIR="/var/www/civisense"
echo ">>> Setting up application directory at $APP_DIR..."
sudo mkdir -p $APP_DIR
sudo cp -r ./* $APP_DIR/
sudo chown -R www-data:www-data $APP_DIR

# 3. Setup systemd service
echo ">>> Registering systemd daemon service..."
sudo cp civisense.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable civisense
sudo systemctl restart civisense

# 4. Setup Nginx (if installed)
if command -v nginx &> /dev/null; then
    echo ">>> Configuring Nginx reverse proxy..."
    sudo cp nginx.conf /etc/nginx/sites-available/civisense
    sudo ln -sf /etc/nginx/sites-available/civisense /etc/nginx/sites-enabled/
    sudo nginx -t && sudo systemctl reload nginx
    echo ">>> Nginx configured."
fi

# 5. Health Check
echo ">>> Waiting 3 seconds for CIVISENSE service startup..."
sleep 3
curl -s http://127.0.0.1:8000/api/health | grep '"status":"ok"' && echo ">>> SUCCESS: CIVISENSE is live at http://127.0.0.1:8000" || echo ">>> WARNING: Check systemctl status civisense"

echo "=========================================================================="
echo " CIVISENSE Deployment Completed Successfully!"
echo " System status: sudo systemctl status civisense"
echo " View logs:     sudo journalctl -u civisense -f"
echo "=========================================================================="
