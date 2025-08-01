# FastAPI 

from fastapi import FastAPI
from pydantic import BaseModel
from config import WHITELIST, BUDGET_LIMIT, APPROVAL_THRESHOLD, DEFAULT_SCORE, WHITELIST_PENALTY, BUDGET_PENALTY

app = FastAPI(title="DAO Shade Agent", description="An autonomous agent that evaluates DAO governance proposals")

class Proposal(BaseModel):
    proposer: str
    budget: int
    description: str

class Decision(BaseModel):
    verdict: str
    reason: list

def load_whitelist():
    return WHITELIST

def evaluate_proposal(proposal: Proposal) -> Decision:
    reasons = []
    score = DEFAULT_SCORE

    # Check whitelist
    if proposal.proposer not in load_whitelist():
        reasons.append("Proposer not whitelisted")
        score -= WHITELIST_PENALTY

    # Check budget
    if proposal.budget > BUDGET_LIMIT:
        reasons.append("Budget exceeds limit")
        score -= BUDGET_PENALTY

    # Make decision
    decision = "approve" if score >= APPROVAL_THRESHOLD else "reject"

    return Decision(verdict=decision, reason=reasons)

@app.get("/")
async def root():
    return {"message": "DAO Shade Agent is running", "status": "active"}

@app.post("/evaluate/")
async def evaluate(proposal: Proposal):
    decision = evaluate_proposal(proposal)
    return decision

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000)
