from fastapi import APIRouter

router = APIRouter(prefix="/export", tags=["export"])

@router.get("/gstr1")
def export_gstr1():
    return {"status": "not_implemented"}

