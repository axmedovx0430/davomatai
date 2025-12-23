# Hugging Face Spaces Deployment Guide

This guide explains how to deploy DavomatAI to Hugging Face Spaces using the provided `Dockerfile.hf`.

## 1. External Database Setup
Hugging Face Spaces do not provide persistent storage for databases. You must use an external PostgreSQL provider.
- **Recommended**: [Neon.tech](https://neon.tech) (Free tier available).
- Create a project and copy the **Connection String** (e.g., `postgresql://user:pass@host/dbname`).

## 2. Hugging Face Space Creation
1. Go to [huggingface.co/new-space](https://huggingface.co/new-space).
2. Name your space (e.g., `davomatai`).
3. Select **Docker** as the SDK.
4. Choose the **Blank** template.
5. Set the Space to **Public** or **Private**.

## 3. Configuration (Secrets)
Go to the **Settings** tab of your Space and add the following **Variables and Secrets**:

| Name | Type | Value |
| :--- | :--- | :--- |
| `DATABASE_URL` | Secret | Your Neon/Supabase connection string |
| `TELEGRAM_BOT_TOKEN` | Secret | Your bot token from @BotFather |
| `SECRET_KEY` | Secret | A long random string for security |
| `API_KEY_SALT` | Secret | A random string for API key hashing |
| `TELEGRAM_ADMIN_CHAT_IDS` | Variable | Your Telegram Chat ID(s) |

## 4. Deployment
1. Upload all project files to the Space repository.
2. **CRITICAL**: Rename `Dockerfile.hf` to `Dockerfile` in the root of the repository (or overwrite the existing one).
3. Hugging Face will automatically start building the image.
4. Once the build is finished, your app will be live at `https://huggingface.co/spaces/YOUR_USERNAME/YOUR_SPACE_NAME`.

## 5. Troubleshooting
- **Memory**: The Space uses the free 16GB RAM tier, which is plenty for the `buffalo_s` model.
- **Sleep**: Free Spaces go to sleep after 48h of inactivity. You can restart them manually from the UI.
- **Logs**: Use the "Logs" tab in HF to see backend/frontend output.
