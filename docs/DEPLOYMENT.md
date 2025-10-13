# Deployment Guide

## Hugging Face Spaces (Recommended - FREE)

### Prerequisites
- Hugging Face account
- OpenAI API key

### Step-by-Step Deployment

#### 1. Create a New Space

1. Go to [Hugging Face Spaces](https://huggingface.co/spaces)
2. Click "Create new Space"
3. Fill in the details:
   - **Name**: `youtube-transcriber-pro`
   - **License**: MIT
   - **SDK**: Gradio
   - **Hardware**: CPU Basic (free tier)

#### 2. Prepare Your Code

Create a `app.py` file (rename from `app_gradio.py`):

```python
# app.py - Entry point for Hugging Face Spaces
from app_gradio import main

if __name__ == "__main__":
    main()
```

#### 3. Create README.md Header

Add this to the top of your README.md:

```yaml
---
title: YouTube Transcriber Pro
emoji: 🎥
colorFrom: blue
colorTo: purple
sdk: gradio
sdk_version: 4.19.0
app_file: app.py
pinned: false
license: mit
---
```

#### 4. Push Your Code

```bash
# Clone your Space repository
git clone https://huggingface.co/spaces/YOUR_USERNAME/youtube-transcriber-pro
cd youtube-transcriber-pro

# Copy your files
cp -r ../youtube-transcriber/* .

# Commit and push
git add .
git commit -m "Initial deployment"
git push
```

#### 5. Configure Secrets

1. Go to your Space settings
2. Navigate to "Repository secrets"
3. Add secret:
   - **Name**: `OPENAI_API_KEY`
   - **Value**: Your OpenAI API key

#### 6. Wait for Build

The Space will automatically build and deploy. Check the logs for any errors.

---

## Docker Deployment

### Dockerfile

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create necessary directories
RUN mkdir -p transcripts temp_audio vector_db

# Expose Gradio port
EXPOSE 7860

# Set environment variables
ENV GRADIO_SERVER_NAME=0.0.0.0
ENV GRADIO_SERVER_PORT=7860

# Run the application
CMD ["python", "app_gradio.py"]
```

### Build and Run

```bash
# Build image
docker build -t youtube-transcriber .

# Run container
docker run -p 7860:7860 \
  -e OPENAI_API_KEY=your-key-here \
  -v $(pwd)/transcripts:/app/transcripts \
  youtube-transcriber
```

### Docker Compose

```yaml
version: '3.8'

services:
  transcriber:
    build: .
    ports:
      - "7860:7860"
    environment:
      - OPENAI_API_KEY=${OPENAI_API_KEY}
    volumes:
      - ./transcripts:/app/transcripts
      - ./vector_db:/app/vector_db
    restart: unless-stopped
```

Run with:
```bash
docker-compose up -d
```

---

## Local Development with ngrok

For quick sharing during development:

```bash
# Install ngrok
# Windows: choco install ngrok
# Mac: brew install ngrok

# Run your app
python app_gradio.py

# In another terminal, expose it
ngrok http 7860
```

You'll get a public URL like: `https://abc123.ngrok.io`

---

## AWS Deployment

### Using AWS EC2

#### 1. Launch EC2 Instance

- **AMI**: Ubuntu 22.04 LTS
- **Instance Type**: t3.small (minimum)
- **Security Group**: Allow inbound on port 7860

#### 2. Connect and Setup

```bash
# SSH into instance
ssh -i your-key.pem ubuntu@your-instance-ip

# Update system
sudo apt update && sudo apt upgrade -y

# Install Python and dependencies
sudo apt install -y python3-pip python3-venv ffmpeg

# Clone repository
git clone <your-repo-url>
cd youtube-transcriber

# Setup virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
nano .env
# Add: OPENAI_API_KEY=your-key-here
```

#### 3. Run with systemd

Create service file:

```bash
sudo nano /etc/systemd/system/transcriber.service
```

Content:

```ini
[Unit]
Description=YouTube Transcriber Pro
After=network.target

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/home/ubuntu/youtube-transcriber
Environment="PATH=/home/ubuntu/youtube-transcriber/venv/bin"
ExecStart=/home/ubuntu/youtube-transcriber/venv/bin/python app_gradio.py
Restart=always

[Install]
WantedBy=multi-user.target
```

Enable and start:

```bash
sudo systemctl daemon-reload
sudo systemctl enable transcriber
sudo systemctl start transcriber
sudo systemctl status transcriber
```

#### 4. Setup Nginx Reverse Proxy

```bash
sudo apt install -y nginx

sudo nano /etc/nginx/sites-available/transcriber
```

Content:

```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:7860;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

Enable:

```bash
sudo ln -s /etc/nginx/sites-available/transcriber /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

---

## Google Cloud Run

### 1. Prepare Dockerfile

Use the Docker configuration above.

### 2. Build and Push

```bash
# Set project
gcloud config set project YOUR_PROJECT_ID

# Build image
gcloud builds submit --tag gcr.io/YOUR_PROJECT_ID/transcriber

# Deploy
gcloud run deploy transcriber \
  --image gcr.io/YOUR_PROJECT_ID/transcriber \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars OPENAI_API_KEY=your-key-here
```

---

## Monitoring and Maintenance

### Health Checks

Add to your app:

```python
@app.route("/health")
def health():
    return {"status": "healthy"}
```

### Logging

Configure logging:

```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)
```

### Backup Strategy

Regular backups of transcripts:

```bash
# Cron job for daily backups
0 2 * * * tar -czf /backups/transcripts-$(date +\%Y\%m\%d).tar.gz /app/transcripts
```

---

## Security Best Practices

1. **Never commit API keys**
   - Use environment variables
   - Add `.env` to `.gitignore`

2. **Rate limiting**
   - Implement request throttling
   - Use API key rotation

3. **Input validation**
   - Validate all URLs
   - Sanitize filenames

4. **HTTPS only**
   - Use SSL certificates
   - Redirect HTTP to HTTPS

5. **Regular updates**
   - Keep dependencies updated
   - Monitor security advisories

---

## Troubleshooting

### Common Issues

**Issue**: FFmpeg not found
```bash
# Solution: Install FFmpeg
sudo apt install ffmpeg  # Ubuntu/Debian
brew install ffmpeg      # Mac
choco install ffmpeg     # Windows
```

**Issue**: Out of memory
```bash
# Solution: Increase swap space or upgrade instance
sudo fallocate -l 2G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
```

**Issue**: Port already in use
```bash
# Solution: Change port in config.py
GRADIO_PORT = 7861  # Use different port
```

---

## Cost Optimization

### Hugging Face Spaces
- **Free tier**: CPU Basic (sufficient for most use cases)
- **Upgrade**: Only if you need GPU or more resources

### AWS EC2
- **Use spot instances**: 70% cheaper
- **Auto-scaling**: Scale down during low usage
- **Reserved instances**: For long-term deployments

### OpenAI API
- **Monitor usage**: Set up billing alerts
- **Batch processing**: Process multiple videos together
- **Cache results**: Avoid re-transcribing same videos

---

## Performance Tuning

### Optimize Gradio

```python
app.launch(
    server_port=7860,
    share=False,
    show_error=True,
    enable_queue=True,  # Enable request queuing
    max_threads=4       # Limit concurrent requests
)
```

### Parallel Processing

For multiple videos:

```python
from concurrent.futures import ThreadPoolExecutor

def process_parallel(urls):
    with ThreadPoolExecutor(max_workers=3) as executor:
        results = list(executor.map(process_video, urls))
    return results
```

---

## Support

For deployment issues:
- Check logs: `docker logs <container-id>`
- Review Gradio docs: https://www.gradio.app/docs/
- Open an issue on GitHub
