FROM python:3.10-slim

WORKDIR /app

# Copy application code
COPY app/ ./app/

# ✅ Copy templates folder so Flask can render HTML
COPY app/templates/ ./app/templates/

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Optional: for local data storage
VOLUME /clientdata

EXPOSE 5000

CMD ["python", "app/client.py"]



# FROM python:3.10-slim
# WORKDIR /app
# COPY app/ ./app/
# COPY requirements.txt .
# RUN pip install --no-cache-dir -r requirements.txt
# VOLUME /clientdata
# EXPOSE 5000
# CMD ["python", "app/client.py"]
