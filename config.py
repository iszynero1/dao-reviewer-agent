
---

### 2. `dao-shade-agent/main.py`
```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import json

app = FastAPI()

class Proposal(BaseModel):
    id: str
    title: str
    description: str
    proposer: str
    budget: float
    duration: str
    category: str

class Decision(BaseModel):
    proposal_id: str
    decision: str
    reasons: list[str]
    score: int

def load_whitelist():
    return ["alice.near", "bob.near"]

def evaluate_proposal(proposal: Proposal) -> Decision:
    reasons = []
    score = 8
    
    # Check whitelist
    if proposal.proposer not in load_whitelist():
        reasons.append("Proposer not whitelisted")
        score -= 3
    
    # Check budget
    if proposal.budget > 10000:
        reasons.append("Budget exceeds limit")
        score -= 2
    
    # Make decision
    decision = "approve" if score >= 6 else "reject"
    return Decision(
        proposal_id=proposal.id,
        decision=decision,
        reasons=reasons,
        score=score
    )

@app.post("/evaluate")
async def evaluate(proposal: Proposal):
    return evaluate_proposal(proposal)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
