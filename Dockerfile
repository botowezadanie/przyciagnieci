FROM python:3.11-slim

WORKDIR /app

RUN pip install --no-cache-dir python-telegram-bot==20.7

# jawnie kopiujemy KONKRETNE pliki
COPY przyciagnieci.py /app/przyciagnieci.py
COPY przyciagnieci.png /app/przyciagnieci.png

CMD ["python", "/app/przyciagnieci.py"]
