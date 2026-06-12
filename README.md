docker build -t my-telegram-bot .

docker run -d \
  --name telegram-bot \
  --restart unless-stopped \
  -e TELEGRAM_TOKEN=your_token_here \
  my-telegram-bot
