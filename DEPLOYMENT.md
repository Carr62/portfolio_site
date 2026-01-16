# Django Portfolio - Digital Ocean Deployment Guide

## Security Improvements Completed ✓

### Fixed Issues:
1. ✅ SECRET_KEY moved to environment variable
2. ✅ Email credentials moved to environment variables
3. ✅ Production security headers added
4. ✅ ALLOWED_HOSTS configured for production
5. ✅ HTTPS enforcement in production
6. ✅ Secure cookie settings
7. ✅ HSTS headers configured

## Prerequisites

- Digital Ocean account
- Domain name (optional but recommended)
- PostgreSQL or MySQL database

## Environment Variables Required

Create these environment variables in your Digital Ocean App Platform:

```bash
# Critical Security Settings
SECRET_KEY=<generate-new-secret-key>
DEBUG=False
ALLOWED_HOSTS=your-app-name.ondigitalocean.app,your-domain.com

# Database (Digital Ocean will provide DATABASE_URL automatically)
DATABASE_URL=postgresql://user:password@host:5432/dbname

# Email Configuration
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
```

### Generate a New SECRET_KEY

Run this Python command to generate a secure secret key:

```python
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

## Digital Ocean Deployment Steps

### Option 1: Deploy with App Platform (Recommended)

1. **Push code to GitHub**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git branch -M main
   git remote add origin <your-repo-url>
   git push -u origin main
   ```

2. **Create App on Digital Ocean**
   - Go to App Platform: https://cloud.digitalocean.com/apps
   - Click "Create App"
   - Choose GitHub repository
   - Select your repository and branch

3. **Configure Build Settings**
   - Build Command: `pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate`
   - Run Command: `gunicorn portfolio_site.wsgi:application`

4. **Add Environment Variables**
   - Go to Settings → Environment Variables
   - Add all variables from the list above
   - Make sure DEBUG=False for production

5. **Add Database (Managed PostgreSQL)**
   - In App Settings, click "Create Resource"
   - Choose "Dev Database" or "Database"
   - Digital Ocean will automatically set DATABASE_URL

6. **Configure Domain (Optional)**
   - Go to Settings → Domains
   - Add your custom domain
   - Update ALLOWED_HOSTS to include your domain

### Option 2: Deploy with Droplet + Nginx

1. **Create Ubuntu Droplet**
   - Choose Ubuntu 22.04 LTS
   - Select size (Basic $6/month is sufficient for start)
   - Add SSH key

2. **SSH into your droplet**
   ```bash
   ssh root@your-droplet-ip
   ```

3. **Install dependencies**
   ```bash
   apt update
   apt install -y python3-pip python3-venv nginx postgresql postgresql-contrib
   ```

4. **Setup project**
   ```bash
   cd /opt
   git clone <your-repo-url> portfolio
   cd portfolio
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

5. **Configure environment variables**
   ```bash
   nano /opt/portfolio/.env
   # Add all environment variables
   ```

6. **Setup database**
   ```bash
   sudo -u postgres psql
   CREATE DATABASE portfolio_db;
   CREATE USER portfolio_user WITH PASSWORD 'your-password';
   GRANT ALL PRIVILEGES ON DATABASE portfolio_db TO portfolio_user;
   \q
   ```

7. **Run migrations and collect static**
   ```bash
   python manage.py migrate
   python manage.py collectstatic --noinput
   ```

8. **Setup Gunicorn service**
   ```bash
   nano /etc/systemd/system/gunicorn.service
   ```
   
   Add:
   ```ini
   [Unit]
   Description=gunicorn daemon
   After=network.target

   [Service]
   User=root
   Group=www-data
   WorkingDirectory=/opt/portfolio
   EnvironmentFile=/opt/portfolio/.env
   ExecStart=/opt/portfolio/venv/bin/gunicorn --workers 3 --bind unix:/opt/portfolio/portfolio.sock portfolio_site.wsgi:application

   [Install]
   WantedBy=multi-user.target
   ```

9. **Setup Nginx**
   ```bash
   nano /etc/nginx/sites-available/portfolio
   ```
   
   Add:
   ```nginx
   server {
       listen 80;
       server_name your-domain.com;

       location = /favicon.ico { access_log off; log_not_found off; }
       
       location /static/ {
           alias /opt/portfolio/staticfiles/;
       }
       
       location /media/ {
           alias /opt/portfolio/media/;
       }

       location / {
           proxy_pass http://unix:/opt/portfolio/portfolio.sock;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
           proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
           proxy_set_header X-Forwarded-Proto $scheme;
       }
   }
   ```

10. **Enable and start services**
    ```bash
    ln -s /etc/nginx/sites-available/portfolio /etc/nginx/sites-enabled
    systemctl start gunicorn
    systemctl enable gunicorn
    systemctl restart nginx
    ```

11. **Setup SSL with Let's Encrypt**
    ```bash
    apt install certbot python3-certbot-nginx
    certbot --nginx -d your-domain.com
    ```

## Post-Deployment Checklist

- [ ] Verify DEBUG=False in production
- [ ] Test HTTPS redirect works
- [ ] Verify static files load correctly
- [ ] Test contact form email sending
- [ ] Check admin panel access
- [ ] Monitor application logs
- [ ] Set up database backups
- [ ] Configure monitoring/alerts

## Security Best Practices

1. **Never commit .env file** - Added to .gitignore
2. **Use strong SECRET_KEY** - Generate new one for production
3. **Enable firewall** - Only allow ports 22, 80, 443
4. **Regular updates** - Keep dependencies updated
5. **Database backups** - Schedule automated backups
6. **Monitor logs** - Set up log monitoring
7. **Use HTTPS only** - Enforce SSL redirect

## Troubleshooting

### Static files not loading
```bash
python manage.py collectstatic --noinput
```

### Database connection errors
- Check DATABASE_URL format
- Verify database credentials
- Ensure database is running

### 502 Bad Gateway
- Check Gunicorn service status: `systemctl status gunicorn`
- Check logs: `journalctl -u gunicorn`

### Email not sending
- Verify EMAIL_HOST_PASSWORD is correct
- Use Gmail App Password, not regular password
- Check firewall allows outbound port 587

## Additional Resources

- Digital Ocean App Platform: https://docs.digitalocean.com/products/app-platform/
- Django Deployment Checklist: https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/
- Let's Encrypt: https://letsencrypt.org/

## Support

For issues, check:
- Application logs in Digital Ocean dashboard
- Django error logs
- Nginx error logs: `/var/log/nginx/error.log`
