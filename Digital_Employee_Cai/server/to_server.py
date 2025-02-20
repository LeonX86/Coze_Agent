from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import json
import os
from to_server_db import save_dialogue_to_mysql,save_task_to_mysql


app = FastAPI()

# 定义请求数据模型


class DialogueData(BaseModel):
    task_id: str
    coze_uid: str
    raw_query: str
    query: str
    role: str


# 定义保存数据的文件路径
DIALOGUE_HISTORY_FILE = "dialogue.json"


def load_dialogue_history():
    """加载历史数据"""
    if os.path.exists(DIALOGUE_HISTORY_FILE):
        try:
            with open(DIALOGUE_HISTORY_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except json.JSONDecodeError:
            return []
    return []


def save_dialogue_history(task_data: dict):
    """
    保存历史数据到文件和数据库

    Args:
        task_data: POST请求中的任务数据
    """
    try:
        # 保存到文件
        history = load_dialogue_history()
        history.append(task_data)
        with open(DIALOGUE_HISTORY_FILE, 'w', encoding='utf-8') as f:
            json.dump(history, f, ensure_ascii=False, indent=2)

        # 直接保存到MySQL
        save_dialogue_to_mysql(task_data)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"保存失败: {str(e)}")


@app.post("/dialogue")
async def create_task(task: DialogueData):
    try:
        # 将TaskData模型转换为字典
        task_dict = task.model_dump()

        # 直接传递task_dict到save_history
        save_dialogue_history(task_dict)

        return {"status": "success", "message": "任务数据已保存"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# 添加新的数据模型
class TaskInfo(BaseModel):
    task_id: str
    task_type: str
    task_num: int
    coze_uid: str
    product: str


# 定义新的任务历史文件
TASK_HISTORY_FILE = "task.json"


def load_task_history():
    """加载任务历史数据"""
    if os.path.exists(TASK_HISTORY_FILE):
        try:
            with open(TASK_HISTORY_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except json.JSONDecodeError:
            return []
    return []


def save_task_history(task_data: dict):
    """保存任务历史数据到文件和数据库"""
    try:
        # 保存到文件
        history = load_task_history()
        history.append(task_data)
        with open(TASK_HISTORY_FILE, 'w', encoding='utf-8') as f:
            json.dump(history, f, ensure_ascii=False, indent=2)

        # 保存到MySQL
        save_task_to_mysql(task_data)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"保存失败: {str(e)}")


@app.post("/task")
async def create_task_info(task: TaskInfo):
    try:
        task_dict = task.model_dump()
        save_task_history(task_dict)
        return {"status": "success", "message": "任务数据已保存"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5266)

    # uvicorn to_server:app --host 0.0.0.0 --port 5266
