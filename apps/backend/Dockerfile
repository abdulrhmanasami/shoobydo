FROM python:3.11-slim
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 PIP_NO_CACHE_DIR=1 PORT=8000
WORKDIR /app
RUN apt-get update -y && apt-get install -y --no-install-recommends build-essential && rm -rf /var/lib/apt/lists/*
COPY apps/backend/requirements.txt /app/requirements.txt
RUN pip install --upgrade pip wheel && pip install -r /app/requirements.txt
COPY apps/backend/app /app/app
RUN useradd -m appuser
USER appuser
EXPOSE 8000
CMD ["uvicorn","app.main:app","--host","0.0.0.0","--port","8000"]
