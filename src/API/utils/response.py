from fastapi.responses import JSONResponse
from datetime import datetime

#Gera o erro padrão

def erro_padrao(status_code: int, error: str, message: str, path: str, details: list = None):
    if details is None:
        details = []

    return JSONResponse(
        status_code=status_code,
        content={
            "error": error,
            "message": message,
            "details": details,
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "path": path
        }
    )