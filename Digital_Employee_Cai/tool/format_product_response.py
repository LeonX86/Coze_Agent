from typing import List, Dict, Any

async def process_product_list(product_str: str) -> List[str]:
    """
    处理产品字符串，转换为产品列表

    Args:
        product_str: 带方括号的产品字符串，如 "[产品1,产品2]"

    Returns:
        处理后的产品列表
    """
    # 去除首尾的方括号
    cleaned_str = product_str.strip('[]')

    # 如果字符串为空，返回空列表
    if not cleaned_str:
        return []

    # 分割并清理每个产品名称
    products = [name.strip().strip('"\'') for name in cleaned_str.split(',')]

    # 过滤掉空字符串
    return [p for p in products if p]

def generate_output_message(products: List[str]) -> str:
    """
    根据产品列表生成输出消息

    Args:
        products: 产品列表

    Returns:
        格式化的输出消息
    """
    if not products:
        return "没有找到相关匹配产品！"

    if products[0] == "没有匹配产品":
        return "没有找到相关匹配产品！"

    if len(products) == 1:
        return f"已为您生成【{products[0]}】相关的内容"

    other_products = products[1:]
    return f"已为您生成【{products[0]}】相关的内容，或许您是想选择其他的产品：{other_products}"

async def main(args: Args) -> Output:
    """
    主函数处理产品信息并生成输出

    Args:
        args: 包含输入参数的对象

    Returns:
        包含输出消息的字典
    """
    try:
        # 获取输入字符串
        product_str = args.params.get('input', '[]')

        # 处理产品列表
        products = await process_product_list(product_str)
        chosen = products[0]
        # 生成输出消息
        message = generate_output_message(products)

        # 返回结果
        return {
            "key0": message,
            "chosen": chosen
        }

    except Exception as e:
        # 错误处理
        error_message = f"处理失败：{str(e)}"
        return {
            "key0": error_message,
            "chosen": ""
        }