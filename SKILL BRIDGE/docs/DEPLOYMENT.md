# SkillBridge Deployment Guide

## Pre-Deployment Checklist

- [ ] All dependencies installed
- [ ] Environment variables configured
- [ ] Database setup complete
- [ ] SSL/TLS certificates obtained
- [ ] Backup strategy defined
- [ ] Monitoring tools configured
- [ ] Team trained on deployment

## Production Deployment

### Step 1: Server Setup

#### Linux Server (Ubuntu 20.04 LTS)
```bash
# Update system
sudo apt-get update
sudo apt-get upgrade -y

# Install required packages
sudo apt-get install -y \
  apache2 \
  php7.4 \
  php7.4-mysql \
  php7.4-curl \
  python3 \
  python3-pip \
  mysql-server \
  git \
  curl \
  wget

# Enable PHP modules
sudo a2enmod rewrite
sudo a2enmod ssl
sudo a2enmod proxy
sudo a2enmod proxy_http
```

### Step 2: Database Setup

```bash
# Secure MySQL installation
sudo mysql_secure_installation

# Create database and user
mysql -u root -p
```

```sql
CREATE DATABASE skillbridge_db;
CREATE USER 'skillbridge'@'localhost' IDENTIFIED BY 'strong_password';
GRANT ALL PRIVILEGES ON skillbridge_db.* TO 'skillbridge'@'localhost';
FLUSH PRIVILEGES;

-- Import schema
SOURCE /path/to/database/schema.sql;
SOURCE /path/to/database/sample_data.sql;
```

### Step 3: PHP Backend Setup

```bash
# Create application directory
sudo mkdir -p /var/www/skillbridge
sudo chown -R www-data:www-data /var/www/skillbridge

# Clone repository (or copy files)
git clone <repository> /var/www/skillbridge
cd /var/www/skillbridge

# Set permissions
sudo chmod -R 755 /var/www/skillbridge
```

### Step 4: Apache Configuration

Create `/etc/apache2/sites-available/skillbridge.conf`:

```apache
<VirtualHost *:80>
    ServerName skillbridge.com
    ServerAlias www.skillbridge.com
    DocumentRoot /var/www/skillbridge/frontend

    <Directory /var/www/skillbridge>
        Options Indexes FollowSymLinks
        AllowOverride All
        Require all granted
    </Directory>

    # Proxy ML API
    ProxyPreserveHost On
    ProxyPass /ml http://localhost:5000
    ProxyPassReverse /ml http://localhost:5000

    # Redirect to HTTPS
    Redirect permanent / https://skillbridge.com/

    ErrorLog ${APACHE_LOG_DIR}/skillbridge_error.log
    CustomLog ${APACHE_LOG_DIR}/skillbridge_access.log combined
</VirtualHost>

<VirtualHost *:443>
    ServerName skillbridge.com
    ServerAlias www.skillbridge.com
    DocumentRoot /var/www/skillbridge/frontend

    SSLEngine on
    SSLCertificateFile /etc/letsencrypt/live/skillbridge.com/fullchain.pem
    SSLCertificateKeyFile /etc/letsencrypt/live/skillbridge.com/privkey.pem

    <Directory /var/www/skillbridge>
        Options Indexes FollowSymLinks
        AllowOverride All
        Require all granted
    </Directory>

    ProxyPreserveHost On
    ProxyPass /ml http://localhost:5000
    ProxyPassReverse /ml http://localhost:5000

    ErrorLog ${APACHE_LOG_DIR}/skillbridge_error.log
    CustomLog ${APACHE_LOG_DIR}/skillbridge_access.log combined
</VirtualHost>
```

Enable site:
```bash
sudo a2ensite skillbridge.conf
sudo systemctl restart apache2
```

### Step 5: Python ML Service Setup

```bash
# Create virtual environment
cd /var/www/skillbridge/ml
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create systemd service
sudo nano /etc/systemd/system/skillbridge-ml.service
```

`/etc/systemd/system/skillbridge-ml.service`:
```ini
[Unit]
Description=SkillBridge ML API Service
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory=/var/www/skillbridge/ml
Environment="PATH=/var/www/skillbridge/ml/venv/bin"
ExecStart=/var/www/skillbridge/ml/venv/bin/python app.py
Restart=on-failure

[Install]
WantedBy=multi-user.target
```

Start service:
```bash
sudo systemctl daemon-reload
sudo systemctl enable skillbridge-ml
sudo systemctl start skillbridge-ml
```

### Step 6: SSL/TLS Certificate (Let's Encrypt)

```bash
sudo apt-get install certbot python3-certbot-apache

sudo certbot certonly --apache -d skillbridge.com -d www.skillbridge.com

# Auto-renewal
sudo certbot renew --dry-run
```

### Step 7: Firewall Configuration

```bash
sudo ufw enable
sudo ufw allow 22/tcp      # SSH
sudo ufw allow 80/tcp      # HTTP
sudo ufw allow 443/tcp     # HTTPS
sudo ufw allow 3306/tcp    # MySQL (if remote access needed)
sudo ufw allow 5000/tcp    # ML API (internal)
```

### Step 8: Environment Configuration

Update `/var/www/skillbridge/.env`:
```
APP_ENV=production
DB_HOST=localhost
DB_USER=skillbridge
DB_PASSWORD=strong_password
DB_NAME=skillbridge_db

JWT_SECRET=production_jwt_secret_key_change_this
BLOCKCHAIN_API_KEY=your_blockchain_key
```

### Step 9: Monitoring & Logging

#### ELK Stack Setup
```bash
# Install Elasticsearch
sudo apt-get install elasticsearch

# Install Kibana
sudo apt-get install kibana

# Install Filebeat
sudo apt-get install filebeat
```

## Continuous Integration/Deployment

### GitHub Actions Workflow

Create `.github/workflows/deploy.yml`:

```yaml
name: Deploy to Production

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v2
    
    - name: Deploy to Server
      uses: appleboy/ssh-action@master
      with:
        host: ${{ secrets.SERVER_HOST }}
        username: ${{ secrets.SERVER_USER }}
        key: ${{ secrets.SERVER_KEY }}
        script: |
          cd /var/www/skillbridge
          git pull origin main
          composer install
          python3 -m pip install -r requirements.txt
          systemctl restart skillbridge-ml
          systemctl restart apache2
```

## Monitoring

### Health Checks
```bash
# Backend API
curl https://skillbridge.com/api/health

# ML Service
curl http://localhost:5000/health

# Database
mysql -u skillbridge -p -e "SELECT 1"
```

### Log Files
- Apache: `/var/log/apache2/skillbridge_*.log`
- PHP: `/var/log/php-fpm.log`
- MySQL: `/var/log/mysql/error.log`
- Python: `/var/log/skillbridge-ml.log`

## Backup Strategy

### Daily Backups
```bash
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/backups/skillbridge"

# Database backup
mysqldump -u skillbridge -p skillbridge_db > $BACKUP_DIR/db_$DATE.sql

# Application backup
tar -czf $BACKUP_DIR/app_$DATE.tar.gz /var/www/skillbridge

# Upload to cloud storage
aws s3 cp $BACKUP_DIR/ s3://skillbridge-backups/
```

## Performance Tuning

### MySQL Configuration
```ini
[mysqld]
max_connections=200
slow_query_log=1
slow_query_log_file=/var/log/mysql/slow.log
long_query_time=2
```

### Apache Configuration
```apache
<IfModule mpm_prefork_module>
    StartServers         10
    MinSpareServers      5
    MaxSpareServers      10
    MaxRequestWorkers    250
    MaxConnectionsPerChild 4000
</IfModule>
```

## Rollback Procedure

```bash
# Check current version
git log --oneline -n 5

# Revert to previous version
git revert HEAD

# Restart services
sudo systemctl restart apache2
sudo systemctl restart skillbridge-ml

# Verify health
curl https://skillbridge.com/api/health
```

## Security Hardening

### Additional Security Measures
```bash
# Set file permissions
chmod 644 /var/www/skillbridge/config/.env
chmod 755 /var/www/skillbridge

# Disable directory listing
sudo echo "Options -Indexes" >> /var/www/skillbridge/.htaccess

# Install Fail2Ban
sudo apt-get install fail2ban

# Configure PHP security
sudo nano /etc/php/7.4/fpm/php.ini
# Set: disable_functions = exec, passthru, system, proc_open
#      upload_max_filesize = 10M
#      post_max_size = 10M
```

## Disaster Recovery Plan

1. **Regular Backups**: Daily database + application backups
2. **Redundancy**: Database replication to standby server
3. **Recovery Time Objective (RTO)**: < 1 hour
4. **Recovery Point Objective (RPO)**: < 15 minutes

---

**Last Updated**: May 28, 2024
**Version**: 1.0.0
