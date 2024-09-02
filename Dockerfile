FROM python:3.9-slim-buster

WORKDIR /app

RUN apt-get update && apt-get install -y netcat && rm -rf /var/lib/apt/lists/*

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

# Make the entrypoint script executable
RUN chmod +x entrypoint.sh

# Use the entrypoint script
ENTRYPOINT ["/bin/sh", "entrypoint.sh"]