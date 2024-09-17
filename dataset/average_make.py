import json
import sys
import os

def split_json_data(filename, chunk_size):
    # 读取输入的JSON文件
    with open(filename, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # 计算分块数量
    total = len(data)
    chunk_size = int(chunk_size)
    num_chunks = (total + chunk_size - 1) // chunk_size  # 向上取整
    
    # 创建输出目录
    output_dir = "output_chunks"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # 分割数据并保存成多个文件
    for i in range(num_chunks):
        chunk_data = data[i * chunk_size:(i + 1) * chunk_size]
        output_filename = os.path.join(output_dir, f'data_chunk_{i+1}.json')
        
        with open(output_filename, 'w', encoding='utf-8') as outfile:
            json.dump(chunk_data, outfile, ensure_ascii=False, indent=4)
        
        print(f"Chunk {i+1} saved to {output_filename}")
    
if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python a.py <chunk_size> <filename>")
    else:
        chunk_size = sys.argv[1]
        filename = sys.argv[2]
        split_json_data(filename, chunk_size)
