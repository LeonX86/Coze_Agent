import mysql.connector
from typing import List, Dict, Any
from datetime import datetime

class DatabaseManager:
    def __init__(self):
        self.db_config = {
            'host': 'localhost',
            'user': 'userdata',
            'password': '',
            'database': 'userdata'
        }

    def get_connection(self):
        """获取数据库连接"""
        return mysql.connector.connect(**self.db_config)

    def get_user_history(self, uid: str, limit: int = 5) -> List[Dict[str, str]]:
        """
        获取用户最近30分钟的历史对话记录
        """
        conn = None
        cursor = None
        try:
            conn = self.get_connection()
            cursor = conn.cursor()

            query = """
            SELECT raw_query, role, dt
            FROM dialogue
            WHERE coze_uid = %s
            AND dt >= NOW() - INTERVAL 30 MINUTE
            ORDER BY dt DESC
            LIMIT %s
            """

            cursor.execute(query, (uid, limit))
            results = cursor.fetchall()

            history = []
            for row in results:
                history.append({
                    'time': row[2].strftime('%Y-%m-%d %H:%M:%S') if row[2] else '',
                    'role': row[1],
                    'content': row[0]
                })

            return history

        except Exception as e:
            print(f"获取历史记录失败: {str(e)}")
            import traceback
            traceback.print_exc()
            return []

        finally:
            if cursor:
                cursor.close()
            if conn and conn.is_connected():
                conn.close()