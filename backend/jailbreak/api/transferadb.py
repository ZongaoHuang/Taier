import sys
import os
import subprocess

# 检查是否传入了正确数量的参数
if len(sys.argv) != 4:
    print("参数错误！需要三个参数：phone_model, test_type, sample_count")
    sys.exit(1)

# 从命令行获取参数
phone_model = sys.argv[1].lower()
test_type = sys.argv[2].lower()
sample_count = sys.argv[3]

# 输出调试信息
print(f"收到的参数: phone_model={phone_model}, test_type={test_type}, sample_count={sample_count}")
print("hello")

# 转换phone_model参数
if phone_model == "oppo":
    phone_model_param = "1"
elif phone_model == "oneplus":
    phone_model_param = "2"
else:
    print("未知的手机型号")
    sys.exit(1)

# 转换test_type参数
if test_type == "security":
    test_type_param = "1"
elif test_type == "accuracy":
    test_type_param = "2"
elif test_type == "privacy":
    test_type_param = "3"
else:
    print("未知的测试类型")
    sys.exit(1)

# 打印参数以确认
print(f"转换后的参数: {phone_model_param}, {test_type_param}, {sample_count}")

# 获取当前脚本所在目录并定位到Taieradb文件夹中的model_test.py
current_directory = os.path.dirname(os.path.abspath(__file__))
target_script = os.path.join(current_directory, 'Taieradb', 'model_test.py')

# 检查目标脚本是否存在
if not os.path.exists(target_script):
    print(f"文件 {target_script} 不存在")
    sys.exit(1)

# 打印即将执行的命令
print(f"执行命令: python {target_script} {phone_model_param} {test_type_param} {sample_count}")

# 传递参数并执行目标脚本
try:
    result = subprocess.run(['python', target_script, phone_model_param, test_type_param, sample_count], 
                            capture_output=True, text=True)

    # 输出结果
    if result.returncode == 0:
        print("脚本执行成功：")
        print(result.stdout)
    else:
        print("脚本执行失败：")
        print(result.stderr)

except Exception as e:
    print(f"调用脚本时出错：{str(e)}")
    sys.exit(1)

