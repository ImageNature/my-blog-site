# -- coding: utf-8 --
import datetime
import os
import re
import subprocess

# 删除当前目录以及所有子目录下的 svg 文件
# 遍历当前目录及所有子目录
for root, dirs, files in os.walk('.'):
  for file in files:
    # 检查文件名是否包含'small', 'large', 'medium'，并且是.svg文件
    if file.endswith('.svg') and ('small' in file or 'large' in file
                                  or 'medium' in file):
      # 获取文件的完整路径
      file_path = os.path.join(root, file)
      # 删除文件
      os.remove(file_path)

small_size = "paperwidth=3.96in"
medium_size = "paperwidth=5.83in"
large_size = "paperwidth=8.7in"

small_filename = "small.tex"
medium_filename = "medium.tex"
large_filename = "large.tex"

with open("main.tex") as f:
  content = f.read()

pattern = r'paperwidth=\d+.?\d*in'

small_content = re.sub(pattern, small_size, content)
with open(small_filename, "w") as f:
  f.write(small_content)

medium_content = re.sub(pattern, medium_size, content)
with open(medium_filename, "w") as f:
  f.write(medium_content)

large_content = re.sub(pattern, large_size, content)
with open(large_filename, "w") as f:
  f.write(large_content)
"""
# 调用系统命令编译 tex 文件并转成 svg
subprocess.call(["xelatex", small_filename])
subprocess.call(['xelatex', small_filename])

small_pdf_file = small_filename.replace('.tex', '.pdf')
crop_pdf = small_pdf_file.replace('.pdf', '-crop.pdf')
subprocess.call(['pdfcrop', small_pdf_file, crop_pdf])

svg_file = crop_pdf.replace('.pdf', '.svg')
subprocess.call(['pdftocairo', '-svg', crop_pdf, svg_file])
"""


def tex_to_svg(tex_file):
  subprocess.call(["xelatex", tex_file])

  pdf_file = tex_file.replace('.tex', '.pdf')
  crop_pdf = pdf_file.replace('.pdf', '-crop.pdf')
  subprocess.call(['pdfcrop', pdf_file, crop_pdf])

  svg_file = crop_pdf.replace('.pdf', '.svg')
  subprocess.call(['pdftocairo', '-svg', crop_pdf, svg_file])

  return svg_file


small_svg = tex_to_svg(small_filename)
medium_svg = tex_to_svg(medium_filename)
large_svg = tex_to_svg(large_filename)


# 以日期时间重命名
def rename_svg(src_name):
  # 去除源文件名中的"-crop"
  name = src_name.replace("-crop", "")
  now = datetime.datetime.now()
  time_str = now.strftime("%Y-%m-%d-%H%M")

  dest_name = time_str + "-" + name
  os.rename(src_name, dest_name)

  return dest_name


small_src = "small-crop.svg"
medium_src = "medium-crop.svg"
large_src = "large-crop.svg"

small_dest = rename_svg(small_src)
medium_dest = rename_svg(medium_src)
large_dest = rename_svg(large_src)

# 存储变量作为 hugo blog 内容
small_hugo_text = small_dest
medium_hugo_text = medium_dest
large_hugo_text = large_dest

# 删除文件

delete_extensions = {'log', 'out', 'aux'}
delete_keywords = ['crop']
delete_tex = {'main-large', 'main-medium', 'main-small'}
delete_files = {
    'small.tex', 'small.pdf', 'large.tex', 'large.pdf', 'medium.tex',
    'medium.pdf'
}

for root, dirs, files in os.walk('.'):

  for filename in files:
    name, ext = os.path.splitext(filename)

    if (ext[1:].lower() in delete_extensions
        or ext.lower() == '.pdf' and delete_keywords[0] in name
        or name in delete_tex or filename in delete_files):

      print('Deleting {}'.format(os.path.join(root, filename)))
      os.remove(os.path.join(root, filename))

print('Files deleted.')

#
#
# new markdown
#
#

from datetime import datetime
import os
import shutil

# 获取当前日期和时间
today = datetime.today().strftime('%Y-%m-%d')
now = datetime.now().strftime('%Y-%m-%dT%H:%M:%S+08:00')

# 创建文件夹
if not os.path.exists('{}/imgs'.format(today)):
  os.makedirs('{}/imgs'.format(today))

# 复制svg文件
for filename in os.listdir('.'):
  if filename.endswith('.svg'):
    shutil.copy(filename, '{}/imgs/{}'.format(today, filename))

# 定义 index.md 中的变量
abstract = "摘要"
categories = "数学"
categories_sub = "代数"
tags = "群论"

# 创建并写入index.md文件
with open('{}/index.md'.format(today), 'w') as f:
  f.write('''---
title: "{today}"
date: {now}
draft: false
toc: true
math: mathjax
categories:
 - {categories}
 - {categories_sub}
tags:
 - {tags}
---

{abstract}

<!--more-->

<picture>
  <source media="(max-width: 630px)" srcset="imgs/{imgs_small}"> 
  <source media="(max-width: 860px)" srcset="imgs/{imgs_medium}">
  <source media="(max-width: 1200px)" srcset="imgs/{imgs_large}">
  <img src="imgs/{imgs_large}" style="width: 100%;">
</picture>
'''.format(
      now=now,
      today=today,
      categories=categories,
      categories_sub=categories_sub,
      tags=tags,
      abstract=abstract,
      imgs_small=small_hugo_text,
      imgs_medium=medium_hugo_text,
      imgs_large=large_hugo_text))

# 遍历当前目录
for file in os.listdir('.'):
  # 检查文件是否是.svg文件
  if file.endswith('.svg'):
    # 删除文件
    os.remove(file)
