FROM python:3.12-slim
WORKDIR /app

# Install Node.js for Shade CLI
RUN apt-get update && apt-get install -y curl && \
    curl -fsSL https://deb.nodesource.com/setup_20.x | bash - && \
    apt-get install -y nodejs

# Install Shade CLI
RUN npm install -g @neardefi/shade-agent-cli

# Copy requirements first for caching
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy remaining files
COPY . .

CMD ["shade-agent-cli", "run", "--python", "main.py"]
