import random
async def main(args: Args) -> Output:
    params = args.params
    advantages = params['input'].split('\n')
    random_advantage = random.choice(advantages)

    # 构建输出对象
    i = len(advantages)
    ret: Output = {
        "key0": random_advantage,
    }
    return ret