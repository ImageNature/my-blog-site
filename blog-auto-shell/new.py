import datetime
import os
import random
import subprocess

# 生成随机数
random_num = str(random.randint(1000, 9999))

# 获取当前日期
now = datetime.datetime.now()
date = now.strftime("%Y-%m-%d")

# 构造文件名
filename = f'{date}-filename-{random_num}-zh.md' 

# 构造hugo命令
command = f'hugo new posts/{filename}'

# 执行命令
subprocess.call(command, shell=True)

print(f'Article {filename} created.')
