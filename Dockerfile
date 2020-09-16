# 建立python3.7环境
FROM python:3.7

# 镜像作者
MAINTAINER zxy Zengevent@gmail.com

# 设置python 环境变量
ENV PYTHONUNBUDFFERED 1

# 创建project 文件夹
RUN mkdir /projcet

# 将project文件夹设为工作路径
WORKDIR /project

# 将当前目录加入到工作路径
ADD . /project

# 利用pip 安装依赖（ -i 表示指定清华源，默认下载过慢）
RUN pip3 install -r requirement.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

# 设置环境变量
ENV SPIDER=/project
