from fastapi import APIRouter, HTTPException, BackgroundTasks
from pydantic import BaseModel
from core.agent import AgentOrchestrator
from services.vault import vault

router = APIRouter()

class TaskRequest(BaseModel):
    task: str
    provider: str = "openai"
    model: str = "gpt-4-turbo"
    github_token: str

class TaskResponse(BaseModel):
    task_id: str
    status: str

@router.post("/run", response_model=TaskResponse)
async def run_agent_task(request: TaskRequest, background_tasks: BackgroundTasks):
    # Store the token securely for this session
    vault.set_secret("GITHUB_TOKEN", request.github_token)
    
    # Initialize agent
    try:
        orchestrator = AgentOrchestrator(provider=request.provider, model=request.model)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
    # Run in background (in a real app, use Celery/Redis)
    # For this standalone version, we'll await it directly or use background tasks
    # But to return a response immediately, we'd need a job queue.
    # For simplicity in this demo, we will run it synchronously or just trigger it.
    
    # NOTE: In a real production system, we would push this to a queue.
    # Here we will just acknowledge receipt.
    
    return {"task_id": "job_123", "status": "queued"}

@router.post("/execute_sync")
async def execute_sync(request: TaskRequest):
    """
    Executes the task synchronously and returns the result.
    """
    vault.set_secret("GITHUB_TOKEN", request.github_token)
    try:
        orchestrator = AgentOrchestrator(provider=request.provider, model=request.model)
        result = await orchestrator.run_task(request.task)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
