# Cloud Deployment Guide

ESP32-CAM Davomat Tizimini cloud hostingga joylashtirish qo'llanmasi.

## Backend Deployment

### Option 1: Railway

1. **Railway.app** ga ro'yxatdan o'ting
2. **New Project** → **Deploy from GitHub**
3. Repository ni tanlang
4. **Add PostgreSQL** plugin qo'shing
5. Environment variables sozlang:
   ```
   DATABASE_URL=(avtomatik qo'shiladi)
   SECRET_KEY=your-secret-key
   TELEGRAM_BOT_TOKEN=your-bot-token
   TELEGRAM_ADMIN_CHAT_IDS=123456789
   INSIGHTFACE_MODEL=buffalo_l
   FACE_MATCH_THRESHOLD=0.5
   ```
6. **Deploy** tugmasini bosing

### Option 2: Render

1. **Render.com** ga ro'yxatdan o'ting
2. **New Web Service** yarating
3. Repository ni ulang
4. Settings:
   - **Build Command**: `pip install -r backend/requirements.txt`
   - **Start Command**: `cd backend && uvicorn main:app --host 0.0.0.0 --port $PORT`
5. **PostgreSQL** database yarating
6. Environment variables qo'shing
7. Deploy qiling

### Option 3: DigitalOcean

1. **Droplet** yarating (Ubuntu 22.04)
2. SSH orqali ulanish:
   ```bash
   ssh root@your-droplet-ip
   ```
3. Dependencies o'rnatish:
   ```bash
   apt update
   apt install -y python3-pip python3-venv postgresql nginx
   ```
4. PostgreSQL sozlash:
   ```bash
   sudo -u postgres psql
   CREATE DATABASE attendance_db;
   CREATE USER attendance_user WITH PASSWORD 'your-password';
   GRANT ALL PRIVILEGES ON DATABASE attendance_db TO attendance_user;
   \q
   ```
5. Loyihani clone qilish:
   ```bash
   cd /var/www
   git clone your-repo-url davomatai
   cd davomatai/backend
   ```
6. Virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```
7. `.env` fayl yaratish
8. Systemd service yaratish:
   ```bash
   nano /etc/systemd/system/davomatai.service
   ```
   ```ini
   [Unit]
   Description=Davomat API
   After=network.target

   [Service]
   User=www-data
   WorkingDirectory=/var/www/davomatai/backend
   Environment="PATH=/var/www/davomatai/backend/venv/bin"
   ExecStart=/var/www/davomatai/backend/venv/bin/uvicorn main:app --host 0.0.0.0 --port 8000

   [Install]
   WantedBy=multi-user.target
   ```
9. Service ishga tushirish:
   ```bash
   systemctl enable davomatai
   systemctl start davomatai
   ```
10. Nginx sozlash:
    ```bash
    nano /etc/nginx/sites-available/davomatai
    ```
    ```nginx
    server {
        listen 80;
        server_name your-domain.com;

        location / {
            proxy_pass http://localhost:8000;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
        }
    }
    ```
11. Nginx enable:
    ```bash
    ln -s /etc/nginx/sites-available/davomatai /etc/nginx/sites-enabled/
    nginx -t
    systemctl restart nginx
    ```

## Frontend Deployment

### Vercel (Tavsiya etiladi)

1. **Vercel.com** ga ro'yxatdan o'ting
2. **Import Project** → GitHub repository
3. Framework: **Next.js** (avtomatik aniqlaydi)
4. Root Directory: `frontend`
5. Environment Variables:
   ```
   NEXT_PUBLIC_API_URL=https://your-backend-url.com
   ```
6. **Deploy** tugmasini bosing

### Netlify

1. **Netlify.com** ga ro'yxatdan o'ting
2. **New site from Git**
3. Repository tanlang
4. Build settings:
   - **Base directory**: `frontend`
   - **Build command**: `npm run build`
   - **Publish directory**: `frontend/.next`
5. Environment variables qo'shing
6. Deploy qiling

## Database Migration

Production database uchun schema yuklash:

```bash
# Local dan
psql -h your-db-host -U your-db-user -d your-db-name -f backend/database/schema.sql

# Yoki Railway/Render dashboard orqali SQL query ishga tushiring
```

## SSL Certificate (HTTPS)

### Let's Encrypt (DigitalOcean)

```bash
apt install certbot python3-certbot-nginx
certbot --nginx -d your-domain.com
```

## Environment Variables Checklist

### Backend
- ✅ `DATABASE_URL`
- ✅ `SECRET_KEY`
- ✅ `TELEGRAM_BOT_TOKEN`
- ✅ `TELEGRAM_ADMIN_CHAT_IDS`
- ✅ `INSIGHTFACE_MODEL`
- ✅ `FACE_MATCH_THRESHOLD`
- ✅ `ALLOWED_ORIGINS`

### Frontend
- ✅ `NEXT_PUBLIC_API_URL`

## ESP32-CAM Configuration

Production backend URL ni `config.h` ga kiriting:

```cpp
#define API_ENDPOINT "https://your-backend-url.com/api/face/upload"
```

## Monitoring

### Logs

**Railway/Render**: Dashboard orqali real-time logs

**DigitalOcean**:
```bash
journalctl -u davomatai -f
```

### Health Check

Backend health endpoint:
```
GET https://your-backend-url.com/health
```

## Backup

### Database Backup

```bash
# Backup
pg_dump -h your-db-host -U your-db-user your-db-name > backup.sql

# Restore
psql -h your-db-host -U your-db-user your-db-name < backup.sql
```

### Automated Backups

Railway va Render avtomatik backup qiladi. DigitalOcean uchun cron job sozlang:

```bash
crontab -e
```
```
0 2 * * * pg_dump -h localhost -U attendance_user attendance_db > /backups/db_$(date +\%Y\%m\%d).sql
```

## Troubleshooting

### Backend ishlamayapti
- Logs tekshiring
- Environment variables to'g'riligini tekshiring
- Database ulanishini tekshiring

### Frontend backend ga ulanmayapti
- CORS sozlamalarini tekshiring
- API URL to'g'riligini tekshiring
- Network tab da xatolarni ko'ring

### InsightFace model yuklanmayapti
- Server RAM yetarli ekanligini tekshiring (kamida 1GB)
- Disk space mavjudligini tekshiring

## Performance Optimization

### Backend
- Gunicorn workers soni: `workers = (2 * CPU_cores) + 1`
- Database connection pool: 10-20
- Redis cache qo'shish (ixtiyoriy)

### Frontend
- Next.js Image Optimization
- Static page generation
- CDN (Vercel avtomatik)

## Security Checklist

- ✅ HTTPS enabled
- ✅ Environment variables xavfsiz
- ✅ Database password kuchli
- ✅ API keys rotate qilinadi
- ✅ CORS to'g'ri sozlangan
- ✅ Rate limiting (ixtiyoriy)

## Cost Estimation

### Free Tier
- **Railway**: $5 credit/month (backend + database)
- **Vercel**: Unlimited (frontend)
- **Total**: ~$0-5/month

### Paid
- **DigitalOcean**: $6-12/month (Droplet + Database)
- **Domain**: $10-15/year

## Support

Muammolar bo'lsa, GitHub Issues da savol bering yoki documentation ni qayta ko'ring.
