# csv_app/models.py
import datetime

from django.db import models

# 每一个测试集有多个测试问题，每一个测试集对应一种测试类型
# 测试类型包括逻辑错误测试、事实错误测试、偏见与歧视测试

# 测试问题
class Question(models.Model):
    goal = models.CharField(max_length=255)
    target = models.CharField(max_length=255)
    behavior = models.CharField(max_length=255, blank=True)
    category = models.CharField(max_length=255)
    methods = models.CharField(max_length=50, default='无增强')

# 测试类型
class Suite(models.Model):
    name = models.CharField(max_length=50, unique=True)
    time = models.DateTimeField(default=datetime.datetime.now)
    state = models.CharField(max_length=50)

# 测试集
class Set(models.Model):
    name = models.CharField(max_length=50, unique=True)
    # 使用relation将测试集与测试问题对应
    relation = models.ManyToManyField(Question)
    # 使用cate区分模型：幻觉或者越狱
    cate = models.CharField(max_length=50, default='jailbreak')
    # 使用suite将测试集与测试类型对应
    suite = models.ForeignKey(Suite, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=datetime.datetime.now)



# 测试
class Test(models.Model):
    name = models.CharField(max_length=50, unique=True)
    # collection对应Set的ID
    collection = models.ForeignKey(Set, on_delete=models.CASCADE)
    model = models.CharField(max_length=50)
    evaluator = models.CharField(max_length=50)
    suite = models.ForeignKey(Suite, on_delete=models.CASCADE, null=True)
    state = models.CharField(max_length=50, default='starting')
    escape_rate = models.CharField(max_length=50)
    created_at = models.DateTimeField(default=datetime.datetime.now)

# 任务（弃用）
class Task(models.Model):
    name = models.CharField(max_length=50, unique=True)
    state = models.CharField(max_length=50, default='starting')
    escape_rate = models.CharField(max_length=50)
    test = models.ForeignKey(Test, on_delete=models.CASCADE, null=True)