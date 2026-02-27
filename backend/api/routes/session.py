from fastapi import APIRouter

router = APIRouter(prefix="/sessions", tags=["sessions"])

@router.post("")
def create_session():
    return {"session_id": "demo_session"}

@router.get("/{session_id}")
def get_session(session_id: str):
    return {"session_id": session_id}

