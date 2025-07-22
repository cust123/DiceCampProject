FROM python:3.10-slim
WORKDIR /app
COPY app/ ./app/
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
VOLUME /serverdata
EXPOSE 5001
CMD ["python", "app/server.py"]
