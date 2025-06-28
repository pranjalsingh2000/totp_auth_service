from fastapi import HTTPException, status
from functools import wraps
from typing import Callable, Any
import traceback

def handle_errors(func: Callable) -> Callable:
    @wraps(func)
    def wrapper(*args, **kwargs) -> Any:
        try:
            return func(*args, **kwargs)
        except HTTPException as e:
            # Let FastAPI handle HTTPExceptions normally
            raise e
        except Exception as e:
            traceback.print_exc()  # Optional: log full traceback
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=str(e)
            )
    return wrapper
