#!/miniconda3/bin/python
#-*- coding: utf-8 -*-
#File Name    : merge_xls.py
#Author       : liangjifeng
#Mail         : jifeng.liang@biobin.com.cn
#Create Time  : 2025-06-10 11:10
import sys,os,gzip



import pandas as pd
import os

def merge_tsv_to_excel(input_folder, output_file):
    # 创建Excel写入对象
    writer = pd.ExcelWriter(output_file, engine='openpyxl')
    
    # 遍历文件夹中的TSV文件
    for filename in os.listdir(input_folder):
        if filename.endswith('.txt'):
            # 读取TSV文件（制表符分隔）
            filepath = os.path.join(input_folder, filename)
            df = pd.read_csv(filepath, sep='\t')
            
            # 提取文件名作为sheet名（去掉扩展名）
            sheet_name = os.path.splitext(filename)[0][:31]  # Excel限制sheet名长度
            
            # 写入Excel，每个文件一个sheet
            df.to_excel(writer, sheet_name=sheet_name, index=False)
    
    # 保存Excel文件
    writer.close()
    print(f"合并完成，结果已保存到: {output_file}")

# 使用示例
input_folder = sys.argv[1] # 替换为你的TSV文件所在文件夹路径
output_file =  sys.argv[2]      # 输出的Excel文件名
merge_tsv_to_excel(input_folder, output_file)
