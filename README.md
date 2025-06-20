# Insta Unban Bot

Automatically checks unbanned Instagram usernames and sends updates via Telegram/Discord.

## How to Deploy
## How to Deploy

1. Install dependencies:

2. Set up your `.env` file using `.env.example` as a template.

3. Run locally for testing:

4. For Railway deployment:
- Ensure you have a `Procfile` with this content:
  ```
  worker: python bot.py
  ```
- Push your code to GitHub.
- Connect your GitHub repo to Railway.
- Railway will auto-detect the `requirements.txt` and `Procfile` to deploy.

