from fastapi import Depends, HTTPException
from src.app.core.auth_cfg import security


def require_admin(get_current_user = Depends(security.token_required())):
    role = get_current_user.role
    
    if role != "admin":
        raise HTTPException(
            status_code=403,
            detail="Forbidden"
        )
    
    return get_current_user