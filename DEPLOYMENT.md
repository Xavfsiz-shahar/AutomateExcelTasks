# 🚀 Deployment Guide / Руководство по развёртыванию

## 🐳 Docker (Recommended for Production)

### Quick Start

```bash
# Build and run
docker-compose up -d

# Check status
docker-compose ps

# View logs
docker-compose logs -f

# Stop
docker-compose down
```

Access: **http://localhost:5000**

### Features

- ✅ Multi-stage build (smaller image)
- ✅ Non-root user (security)
- ✅ Health checks
- ✅ Persistent database (volume)
- ✅ Gunicorn for production
- ✅ Auto-restart

### Data Persistence

Database stored in: `./data/uploads.db`

To backup:
```bash
# Backup database
docker cp excel-automation:/app/data/uploads.db ./backup.db

# Restore database
docker cp ./backup.db excel-automation:/app/data/uploads.db
```

---

## 💻 Native (Windows)

### For Development

```bash
pip install -r requirements.txt
python app.py
```

### For Production

```bash
pip install -r requirements.txt
pip install gunicorn

# Run with gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

---

## 🔧 Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `FLASK_ENV` | `development` | `production` for prod |
| `PORT` | `5000` | Server port |
| `DATABASE_PATH` | `uploads.db` | Database file path |
| `TEMPLATE_FILE` | `static\file\Шаблон.xlsx` | Template path |
| `USE_DOCKER` | `false` | `true` for Docker mode |

### Docker Example

```bash
docker run -d \
  -p 5000:5000 \
  -e FLASK_ENV=production \
  -e DATABASE_PATH=/app/data/uploads.db \
  -v $(pwd)/data:/app/data \
  excel-automation
```

---

## 📊 Monitoring

### Health Check

```bash
curl http://localhost:5000/
```

### Database Size

```bash
# Linux/Docker
du -h data/uploads.db

# Windows
dir data\uploads.db
```

---

## 🔄 Updates

### Docker

```bash
# Pull latest code
git pull

# Rebuild and restart
docker-compose down
docker-compose build --no-cache
docker-compose up -d
```

### Native

```bash
# Pull latest code
git pull

# Restart application
# Stop current instance (Ctrl+C)
python app.py
```

---

## 🔐 Security Recommendations

1. **Change SECRET_KEY** in production
2. **Use HTTPS** (reverse proxy)
3. **Restrict file uploads** to trusted users
4. **Regular database backups**
5. **Update dependencies** regularly

---

## 📈 Performance Tips

1. **Database:** SQLite is fine for <100 users
2. **File size:** Limit template complexity
3. **Concurrent uploads:** Gunicorn workers = CPU cores
4. **Caching:** Browser caching enabled

---

**Need help?** Open an issue on GitHub

