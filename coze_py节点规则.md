# Coze 代码节点编写规则

## 1. 基本模板
```python
async def main(args: Args) -> Output:
    params = args.params
    input_data = params.get('输入变量名', 默认值)
    
    # 处理逻辑
    
    ret: Output = {
        "输出变量名": 输出值
    }
    return ret
```

## 2. Python 环境限制

### 基础环境
- 基于 Python 3.11.3 标准库
- **不支持的模块**：curses、dbm、ensurepip、fcntl、grp、idlelib、lib2to3、msvcrt、pwd、resource、syslog、termios、tkinter、turtle.py、turtledemo、venv、winreg、winsound、**multiprocessing**、**threading**、**sockets**、pty、tty
- 不支持 Http.client 方式的请求

### 第三方库
- **仅支持两个第三方库**：`requests_async` 和 `numpy`
- 使用 `requests_async` 必须搭配 `await`：
```python
import requests_async as requests

async def main(args: Args) -> Output:
    url = args.params['url']
    response = await requests.get(url)
    ret = {
        'code': response.status_code,
        'res': response.text,
    }
    return ret
```

### 异步要求
- **禁止使用** `time.sleep()`（阻塞调用影响性能）
- **推荐使用** `asyncio.sleep()` 异步版本
- 所有 HTTP 请求必须使用 `await`

## 3. 关键注意事项

### 输入数据结构
- 飞书多维表格等数据源返回的是**字典**，格式：`{"items": [...], "has_more": bool}`
- 真正的数据在 `data['items']` 列表中
- `fields` 字段通常是 **JSON 字符串**，需要 `json.loads()` 解析

### 输出要求
- **必须返回指定的数据类型**（如要求 str list 就必须是字符串列表）
- 所有输出元素用 `str()` 转换确保类型正确
- 无法使用 `print()` 调试，调试信息要放在输出结果中

### 代码规范
- 不使用面向对象
- 不写 `def main()` 主函数（Coze 自动调用 async main）
- 使用类型注解：`Args` 和 `Output`
- 导入必要的库：`json`, `datetime` 等
- HTTP 请求使用 `requests_async`

## 4. 典型处理流程

### 数据处理
```python
# 获取数据
items = data.get('items', [])

# 遍历处理
for item in items:
    # 解析 JSON 字符串
    fields_str = item.get('fields', '{}')
    fields = json.loads(fields_str)
    
    # 提取字段（注意字段可能是列表）
    value = fields.get('字段名', [])
    
    # 提取文本并清理
    text = value[0]['text'] if value else "无"
    text = text.replace('\n', ' ')
```

### HTTP 请求示例
```python
import requests_async as requests

async def main(args: Args) -> Output:
    url = "http://api.example.com/data"
    
    # GET 请求
    response = await requests.get(url)
    
    # POST 请求
    response = await requests.post(url, json={"key": "value"})
    
    ret = {
        "status": response.status_code,
        "data": response.json()
    }
    return ret
```

## 6. 调试技巧
- 将调试信息收集到列表中：`debug_list.append(f"信息: {str(变量)}")`
- 在输出结果中包含调试信息：`{"result": debug_list + result_list}`
- 先用最简单的代码测试数据结构和类型

## 7. 常见错误
- ❌ 使用 `import requests` → 必须使用 `import requests_async as requests`
- ❌ `requests.get(url)` 不加 await → 必须 `await requests.get(url)`
- ❌ 使用 `time.sleep()` → 改用 `await asyncio.sleep()`
- ❌ 使用不支持的模块（threading、sockets 等） → 使用异步方案
- ❌ 直接对字符串使用 `.get()` → 先 `json.loads()` 解析
- ❌ 返回类型不匹配 → 用 `[str(x) for x in list]` 确保类型
- ❌ 找不到数据 → 检查是 `data` 还是 `data['items']`