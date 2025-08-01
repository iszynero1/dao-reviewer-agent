
# DAO Shade Agent

An autonomous agent that evaluates DAO governance proposals using FastAPI.

## Features
- Checks proposer whitelist status
- Validates proposal budgets against limits
- Returns approve/reject decisions with reasoning
- RESTful API with FastAPI

## How it Works
The agent evaluates proposals based on:
- **Whitelist Status**: Proposer must be in approved list
- **Budget Validation**: Budget must not exceed the limit (10,000)
- **Scoring System**: Starts with 8 points, deducts for violations
- **Decision Threshold**: Approves if score >= 6

## API Endpoints
- `GET /` - Health check
- `POST /evaluate/` - Evaluate a proposal

## Sample Request
```json
{
  "proposer": "alice.near",
  "budget": 5000,
  "description": "Community garden project"
}
```

## Setup
1. Install dependencies: The system will auto-install from requirements.txt
2. Run the application: Click the Run button
3. Test at: Your repl URL + `/docs` for interactive API docs

## Configuration
Edit `config.py` to modify:
- Whitelist of approved proposers
- Budget limits
- Scoring thresholds
