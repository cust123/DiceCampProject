FROM python:3.10-slim
WORKDIR /app
COPY app/ ./app/
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
VOLUME /clientdata
EXPOSE 5000
CMD ["python", "app/client.py"]
