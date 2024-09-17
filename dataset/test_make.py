import json
import random
import sys

def select_random_samples(n, input_file):
    # 读取 JSON 文件
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # 随机选择 N 个数据
    selected_data = random.sample(data, n)

    # 输出选择的样本
    output_file = f'selected_{n}_samples.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(selected_data, f, ensure_ascii=False, indent=4)

    print(f"{n} random samples have been saved to {output_file}")

if __name__ == "__main__":
    # 从命令行获取参数
    if len(sys.argv) != 3:
        print("Usage: python a.py <N> <input_file>")
        sys.exit(1)

    # N 是要选择的数据个数，input_file 是输入的 JSON 文件
    N = int(sys.argv[1])
    input_file = sys.argv[2]

    select_random_samples(N, input_file)
