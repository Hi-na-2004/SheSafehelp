# SheSafe - Deployment Guide

This guide covers deploying SheSafe to various platforms.

## 🚀 Deployment Options

### 1. Local Development (Already Running)

You're already running locally! Just use:
```bash
cd backend
python app.py
```

### 2. Heroku Deployment

#### Prerequisites
- Heroku account
- Heroku CLI installed

#### Steps

1. **Install Gunicorn**
```bash
pip install gunicorn
pip freeze > requirements.txt
```

2. **Create Procfile**
```bash
echo "web: cd backend && gunicorn app:app" > Procfile
```

3. **Create runtime.txt**
```bash
echo "python-3.10.13" > runtime.txt
```

4. **Initialize Git (if not already)**
```bash
git init
git add .
git commit -m "Initial commit"
```

5. **Create Heroku app**
```bash
heroku create shesafe-app
```

6. **Set environment variables**
```bash
heroku config:set FLASK_SECRET_KEY=your_secret_key
heroku config:set TWILIO_ACCOUNT_SID=your_sid
heroku config:set TWILIO_AUTH_TOKEN=your_token
heroku config:set TWILIO_PHONE_NUMBER=your_number
```

7. **Deploy**
```bash
git push heroku main
```

8. **Open app**
```bash
heroku open
```

### 3. AWS EC2 Deployment

#### Launch EC2 Instance

1. **Create EC2 instance** (Ubuntu 22.04 LTS)
2. **Connect via SSH**
```bash
ssh -i your-key.pem ubuntu@your-instance-ip
```

3. **Install dependencies**
```bash
sudo apt update
sudo apt install python3-pip python3-venv nginx -y
```

4. **Clone repository**
```bash
git clone your-repo-url
cd SheSafehelp
```

5. **Setup virtual environment**
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install gunicorn
```

6. **Create systemd service**
```bash
sudo nano /etc/systemd/system/shesafe.service
```

Add:
```ini
[Unit]
Description=SheSafe Application
After=network.target

[Service]
User=ubuntu
WorkingDirectory=/home/ubuntu/SheSafehelp/backend
Environment="PATH=/home/ubuntu/SheSafehelp/venv/bin"
ExecStart=/home/ubuntu/SheSafehelp/venv/bin/gunicorn --workers 3 --bind 0.0.0.0:5000 app:app

[Install]
WantedBy=multi-user.target
```

7. **Configure Nginx**
```bash
sudo nano /etc/nginx/sites-available/shesafe
```

Add:
```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
    
    location /static {
        alias /home/ubuntu/SheSafehelp/frontend/static;
    }
}
```

8. **Enable and start services**
```bash
sudo ln -s /etc/nginx/sites-available/shesafe /etc/nginx/sites-enabled/
sudo systemctl enable shesafe
sudo systemctl start shesafe
sudo systemctl restart nginx
```

### 4. Docker Deployment

#### Create Dockerfile

```dockerfile
FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

WORKDIR /app/backend

EXPOSE 5000

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "3", "app:app"]
```

#### Create docker-compose.yml

```yaml
version: '3.8'

services:
  web:
    build: .
    ports:
      - "5000:5000"
    environment:
      - FLASK_SECRET_KEY=${FLASK_SECRET_KEY}
      - TWILIO_ACCOUNT_SID=${TWILIO_ACCOUNT_SID}
      - TWILIO_AUTH_TOKEN=${TWILIO_AUTH_TOKEN}
      - TWILIO_PHONE_NUMBER=${TWILIO_PHONE_NUMBER}
    volumes:
      - ./data:/app/data
```

#### Build and run

```bash
docker-compose up -d
```

### 5. Azure App Service

1. **Install Azure CLI**
2. **Login**
```bash
az login
```

3. **Create resource group**
```bash
az group create --name SheSafeRG --location eastus
```

4. **Create App Service plan**
```bash
az appservice plan create --name SheSafePlan --resource-group SheSafeRG --sku B1 --is-linux
```

5. **Create web app**
```bash
az webapp create --resource-group SheSafeRG --plan SheSafePlan --name shesafe-app --runtime "PYTHON:3.10"
```

6. **Configure environment variables**
```bash
az webapp config appsettings set --resource-group SheSafeRG --name shesafe-app --settings FLASK_SECRET_KEY=your_key
```

7. **Deploy code**
```bash
az webapp up --name shesafe-app --resource-group SheSafeRG
```

### 6. Google Cloud Platform (Cloud Run)

1. **Install gcloud CLI**
2. **Build container**
```bash
gcloud builds submit --tag gcr.io/YOUR_PROJECT_ID/shesafe
```

3. **Deploy to Cloud Run**
```bash
gcloud run deploy shesafe \
  --image gcr.io/YOUR_PROJECT_ID/shesafe \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars FLASK_SECRET_KEY=your_key
```

## 🔒 Production Checklist

### Security
- [ ] Change default SECRET_KEY
- [ ] Enable HTTPS/SSL
- [ ] Set up firewall rules
- [ ] Use environment variables for secrets
- [ ] Implement rate limiting
- [ ] Enable CORS properly
- [ ] Set up authentication (if needed)

### Performance
- [ ] Use production WSGI server (Gunicorn/uWSGI)
- [ ] Set up CDN for static files
- [ ] Enable caching
- [ ] Optimize database queries
- [ ] Use connection pooling
- [ ] Monitor memory usage

### Monitoring
- [ ] Set up logging
- [ ] Configure error tracking (Sentry)
- [ ] Set up uptime monitoring
- [ ] Monitor API usage
- [ ] Track performance metrics
- [ ] Set up alerts

### Database
- [ ] Use PostgreSQL/MySQL for production
- [ ] Set up backups
- [ ] Configure connection pooling
- [ ] Implement data retention policy

### Scaling
- [ ] Use load balancer
- [ ] Set up auto-scaling
- [ ] Use Redis for caching
- [ ] Implement queue system for heavy tasks
- [ ] Use CDN for static content

## 🌐 Domain & SSL Setup

### Using Let's Encrypt (Free SSL)

```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d yourdomain.com
```

### Auto-renewal
```bash
sudo certbot renew --dry-run
```

## 📊 Monitoring Setup

### Using PM2 (Process Manager)

```bash
npm install -g pm2
pm2 start backend/app.py --name shesafe --interpreter python3
pm2 startup
pm2 save
```

### Logs
```bash
pm2 logs shesafe
pm2 monit
```

## 🔧 Environment Variables for Production

```env
# Flask
FLASK_ENV=production
FLASK_SECRET_KEY=generate_strong_random_key_here

# Database (if using PostgreSQL)
DATABASE_URL=postgresql://user:password@host:5432/dbname

# Twilio
TWILIO_ACCOUNT_SID=your_production_sid
TWILIO_AUTH_TOKEN=your_production_token
TWILIO_PHONE_NUMBER=your_production_number

# Emergency Contacts
EMERGENCY_CONTACTS=+1234567890,+0987654321

# Monitoring (optional)
SENTRY_DSN=your_sentry_dsn
```

## 📱 Mobile App Deployment

### React Native (Future)

1. **Android**
```bash
cd mobile
npx react-native run-android --variant=release
```

2. **iOS**
```bash
cd mobile/ios
pod install
cd ..
npx react-native run-ios --configuration Release
```

## 🧪 Testing in Production

1. **Health check**
```bash
curl https://your-domain.com/api/health
```

2. **Test API endpoints**
```bash
# Test toxicity detection
curl -X POST https://your-domain.com/api/toxicity/analyze \
  -H "Content-Type: application/json" \
  -d '{"text": "test message"}'
```

3. **Monitor logs**
```bash
# Heroku
heroku logs --tail

# AWS
tail -f /var/log/shesafe/app.log

# Docker
docker logs -f container_name
```

## 🚨 Troubleshooting

### Common Issues

1. **Port already in use**
```bash
sudo lsof -i :5000
kill -9 PID
```

2. **Permission denied**
```bash
sudo chown -R $USER:$USER /path/to/SheSafehelp
chmod +x start.sh
```

3. **Module not found**
```bash
pip install -r requirements.txt --force-reinstall
```

4. **Database connection failed**
- Check database credentials
- Verify network connectivity
- Check firewall rules

## 📞 Support

For deployment issues:
1. Check logs first
2. Verify environment variables
3. Test API endpoints
4. Check firewall/security groups
5. Verify SSL certificates
6. Contact support or open issue

---

Happy Deploying! 🚀

