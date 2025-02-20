import mysql.connector
from datetime import datetime
from typing import Dict, Any


def save_dialogue_to_mysql(dialogue_data: Dict[str, Any]) -> bool:
    """
    将任务数据保存到MySQL数据库

    Args:
        task_data: POST请求中的任务数据字典
    """
    conn = None
    cursor = None

    try:
        # 数据库连接配置
        db_config = {
            'host': 'localhost',
            'user': 'userdata',
            'password': '',
            'database': 'userdata'
        }

        # 建立数据库连接
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        # 插入数据的SQL语句
        insert_sql = """
        INSERT INTO dialogue
        (task_id, coze_uid, raw_query, query, role, dt)
        VALUES (%s, %s, %s, %s, %s, CURRENT_TIMESTAMP)
        """

        # 直接使用task_data中的值
        values = (
            dialogue_data['task_id'],
            dialogue_data['coze_uid'],
            dialogue_data['raw_query'],
            dialogue_data['query'],
            dialogue_data['role']
        )

        # 执行插入操作
        cursor.execute(insert_sql, values)

        # 提交事务
        conn.commit()

        return True

    except Exception as e:
        print(f"保存到MySQL失败: {str(e)}")
        if conn and conn.is_connected():
            conn.rollback()
        return False

    finally:
        # 关闭数据库连接
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()


def save_task_to_mysql(task_data: Dict[str, Any]) -> bool:
    """
    将任务数据保存到MySQL数据库的task表

    Args:
        task_data: POST请求中的任务数据字典
    """
    conn = None
    cursor = None

    try:
        # 数据库连接配置
        db_config = {
            'host': 'localhost',
            'user': 'userdata',
            'password': '',
            'database': 'userdata'
        }

        # 建立数据库连接
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        # 插入数据的SQL语句
        insert_sql = """
        INSERT INTO task
        (task_id, task_type, task_num, coze_uid, product, dt)
        VALUES (%s, %s, %s, %s, %s, CURRENT_TIMESTAMP)
        """

        # 准备数据
        values = (
            task_data['task_id'],
            task_data['task_type'],
            task_data['task_num'],
            task_data['coze_uid'],
            task_data['product']
        )

        # 执行插入操作
        cursor.execute(insert_sql, values)

        # 提交事务
        conn.commit()

        return True

    except Exception as e:
        print(f"保存到MySQL失败: {str(e)}")
        if conn and conn.is_connected():
            conn.rollback()
        return False

    finally:
        # 关闭数据库连接
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()