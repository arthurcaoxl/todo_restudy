import os
from fastapi import HTTPException, Security
from fastapi.security import APIKeyHeader

API_KEY_NAME = "X-API-Key"
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)

async def verify_api_key(api_key: str = Security(api_key_header)):
    print(f"[AUTH] verify_api_key called with key: {api_key}")  # 调试
    expected_key = os.getenv("API_KEY")
    if not expected_key:
        raise HTTPException(status_code=500, detail="API_KEY not configured")
    if not api_key or api_key != expected_key:
        raise HTTPException(status_code=403, detail="Invalid or missing API Key")
    return api_key
