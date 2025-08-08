# DAO Shade Agent

An autonomous agent that evaluates DAO governance proposals using FastAPI and Shade Protocol, with on-chain decision recording.

## Features
- ✅ **Proposal Evaluation**:
  - Checks proposer whitelist status
  - Validates proposal budgets against limits
  - Scores proposals using configurable rules
- ⛓ **Blockchain Integration**:
  - Records decisions on NEAR blockchain
  - Uses Shade Agents for autonomous operation
  - Verifiable TEE execution
- 🚀 **API Endpoints**:
  - RESTful interface for proposal submission
  - Health monitoring endpoints

## How It Works
1. Receives proposals via API or blockchain events
2. Evaluates based on:
   - **Whitelist Status** (Configurable in `config.py`)
   - **Budget Validation** (Default limit: 10,000)
   - **Scoring System** (Starts at 8, deducts for violations)
3. Submits decisions to NEAR blockchain via Shade Agent
4. Returns verdict with on-chain transaction hash

## Prerequisites
- Python 3.12+
- Docker Desktop
- NEAR CLI (`npm install -g near-cli`)
- Shade Agent CLI ([Install Instructions](#shade-agent-setup))

## Quick Start
```bash
# Clone repository
git clone https://github.com/YOUR_USERNAME/dao-shade-agent.git
cd dao-shade-agent

# Install dependencies
pip install -r requirements.txt

# Build and run (requires Docker)
docker build -t dao-agent .
docker run -p 5000:5000 dao-agent