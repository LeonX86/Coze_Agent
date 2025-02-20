from fastapi import FastAPI, HTTPException, Query
from typing import Dict, List
from to_coze_db import DatabaseManager
import uvicorn
from pydantic import BaseModel

class HistoryItem(BaseModel):
    time: str
    role: str
    content: str

app = FastAPI()
db_manager = DatabaseManager()

@app.get("/history", response_model=List[HistoryItem])
async def get_history(
    uid: str = Query(..., description="用户ID"),
    limit: int = Query(default=5, ge=1, le=100, description="返回记录的数量限制")
):
    """
    获取用户历史记录
    """
    try:
        history = db_manager.get_user_history(uid=uid, limit=limit)
        return history
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# 之前的产品列表保持不变
product_names = [
    "兰风 春日清荷口红",
    "兰风 春日桃花口红",
    "兰风 夏日海风口红",
    "兰风 夏日热情口红",
    "兰风 秋日枫叶口红",
    "兰风 秋日金菊口红",
    "兰风 冬日雪晴口红",
    "兰风 冬日樱桃口红",
    "兰风 春日野蓝口红"
]

@app.get("/products", response_model=List[str])
async def get_products():
    """获取产品列表"""
    return product_names

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5267)