from fastapi import APIRouter, Depends, Request
from src.app.utils.depends import require_admin


router = APIRouter(
    prefix="/api/admin",
    dependencies=[Depends(require_admin)]
)

@router.get("/info")
async def admin_info(
    request: Request
):
    return {"ok"}