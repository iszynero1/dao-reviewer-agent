import datetime
import asyncio
from fastapi import FastAPI
from pydantic import BaseModel
from config import WHITELIST, BUDGET_LIMIT, APPROVAL_THRESHOLD, DEFAULT_SCORE, WHITELIST_PENALTY, BUDGET_PENALTY
from shade_agent_api import ShadeAgent
from near_sdk import AccountId

app = FastAPI(title="DAO Shade Agent", description="An autonomous agent that evaluates DAO governance proposals")

# Initialize Shade Agent with proper configuration
agent = ShadeAgent( 
    contract_id="ac.proxy.your_account.testnet", # For local development    
    # contract_id="ac-sandbox.your_account.testnet" # For TEE deployment    
    network="testnet",
    key_derivation_path="m/44'/397'/0'"
)
class Proposal(BaseModel):  
    proposer: str  
    budget: int  
    description: str  
    proposal_id: str

class Decision(BaseModel):  
    verdict: str  
    reason: list  
    tx_hash: str
    
class AgentInfo(BaseModel):  
    account_id: str  
    balance: str

class EthAccountInfo(BaseModel):  
    account_id: str  
    balance: str

def load_whitelist():  
    return WHITELIST

async def evaluate_proposal(proposal: Proposal) -> Decision:  
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

    # Submit decision to chain    
    tx_hash = await submit_decision_to_chain(proposal.proposal_id, decision)

    return Decision(verdict=decision, reason=reasons, tx_hash=tx_hash)

async def submit_decision_to_chain(proposal_id: str, decision: str) -> str:  
    """Submit decision to the blockchain using Shade Agent"""  
    tx_payload = {    
        "proposal_id": proposal_id,    
        "decision": decision,    
        "timestamp": str(datetime.datetime.utcnow())  
    }   
    
    # Sign and submit transaction    
    result = await agent.submit_transaction(    
        payload=tx_payload,    
        receiver_id="your_dao_contract.testnet",    
        actions=[{      
            "type": "FunctionCall",      
            "method_name": "submit_decision",      
            "args": tx_payload,      
            "gas": "30000000000000",      
            "deposit": "0"    
        }]  
    )   
    
    return result['transaction']['hash']

@app.on_event("startup")
async def startup_event():  
    """Register agent when starting up"""  
    try:    
        await agent.register()    
        print("Agent registered successfully")  
    except Exception as e:    
        print(f"Registration failed: {str(e)}")

@app.get("/")
async def root():  
    return {"message": "DAO Shade Agent is running", "status": "active"}

@app.get("/api/agent-account", response_model=AgentInfo)
async def get_agent_account():  
    """Endpoint to get agent account info"""  
    account_id = await agent.get_account_id()  
    balance = await agent.get_account_balance()  
    return {"account_id": account_id, "balance": balance}

@app.get("/api/eth-account", response_model=EthAccountInfo)
async def get_eth_account():  
    """Endpoint to get derived Ethereum account info"""  
    account_id = await agent.get_derived_account("ethereum")  
    balance = await agent.get_account_balance(account_id)  
    return {"account_id": account_id, "balance": balance}

@app.post("/api/transaction")
async def submit_transaction(proposal: Proposal):  
    """Endpoint to submit a transaction through the agent"""  
    decision = await evaluate_proposal(proposal)  
    return decision

async def monitor_proposals():  
    """Autonomous function to monitor for new proposals"""  
    while True:    
        try:      
            # Check for new proposals (implement this based on your DAO)            
            new_proposals = await fetch_new_proposals()           
            
            for proposal in new_proposals:        
                await evaluate_proposal(proposal)           
                
            await asyncio.sleep(60) # Check every minute        
        except Exception as e:      
            print(f"Monitoring error: {str(e)}")      
            await asyncio.sleep(60)
if __name__ == "__main__":  
    import uvicorn  
    from concurrent.futures import ThreadPoolExecutor   
    
    # Start monitoring in background    
    executor = ThreadPoolExecutor()  
    loop = asyncio.get_event_loop()  
    loop.run_in_executor(executor, lambda: loop.create_task(monitor_proposals()))   
    uvicorn.run(app, host="0.0.0.0", port=3000) # Changed to port 3000 to match template