
#!/miniconda3/bin/python
#-*- coding: utf-8 -*-
import argparse
import pandas as pd
import pingouin as pg
from pandas import option_context

# 参数解析
parser = argparse.ArgumentParser(description='基因型与表型关联分析')
parser.add_argument('--infile', help='输入文件路径', default='samp_SNPY4GT_pheno.xls')
parser.add_argument('--mark', type=str, help='分子标记名称', required=True)

parser.add_argument('--seqstrategy', type=str, help='测序策略', 
                   default="WES", choices=["WGS","WES","TR"])
args = parser.parse_args()

# 数据读取和处理
header = None
GT_pheno = {}
with open(args.infile, 'r') as f:
    for line in f:
        if line.startswith('samp') and header is None:
            header = line.strip().split("\t")
            GT_name=header[1]
        else:
            parts = line.strip().split("\t")
            if len(parts) >= 3:
                GT = parts[1].replace(":", "")
                pheno = float(parts[2])
                GT_pheno.setdefault(GT, []).append(pheno)

# 转换为DataFrame
data = pd.DataFrame([(k,v) for k in GT_pheno for v in GT_pheno[k]],
                   columns=['group','value'])

# 设置科学计数法显示
pd.set_option('display.float_format', lambda x: '%.2e' % x)

# 执行ANOVA分析
anova_result = pg.anova(data=data, dv='value', between='group')
print("\nANOVA分析结果:")
print(anova_result[['Source', 'ddof1', 'ddof2', 'F', 'p-unc']])
import pandas as pd
import pingouin as pg
from pandas import ExcelWriter

# 专业导出Excel（保留格式和列名）
#with ExcelWriter(f"{GT_name}_ANOVA.xlsx") as writer:
#    anova_result[['Source', 'ddof1', 'ddof2', 'F', 'p-unc']].to_excel(
#        writer, 
#        sheet_name="ANOVA_Results",
#        float_format="%.3e",  # 确保Excel中也使用科学计数法
#        index=False
#    )



# 事后检验
if len(GT_pheno) > 2:
    print("\n事后检验(Tukey HSD):")
    posthoc = pg.pairwise_tukey(data=data, dv='value', between='group')
    
    # 添加显著性标记
    posthoc['sig'] = posthoc['p-tukey'].apply(
        lambda p: '***' if p < 0.001 else '**' if p < 0.01 else '*' if p < 0.05 else ''
    )
    
    # 打印核心结果
    print(posthoc[['A', 'B', 'mean(A)', 'mean(B)', 'diff', 'p-tukey', 'sig']])
    
    # 专业导出Excel
#    with pd.ExcelWriter(f"{GT_name}_TukeyHSD.xlsx") as writer:
#        posthoc.to_excel(writer, sheet_name="TukeyHSD", index=False)
#
# ANOVA分析导出
anova_result = pg.anova(data=data, dv='value', between='group')
anova_result[['Source', 'ddof1', 'ddof2', 'F', 'p-unc']].to_csv(
    f"{GT_name}_ANOVA.txt",
    sep='\t',
    float_format="%.3e",
    index=False
)

# 事后检验导出
if len(GT_pheno) > 2:
    posthoc = pg.pairwise_tukey(data=data, dv='value', between='group')
    posthoc['sig'] = posthoc['p-tukey'].apply(
        lambda p: '***' if p < 0.001 else '**' if p < 0.01 else '*' if p < 0.05 else ''
    )
    posthoc[['A', 'B', 'mean(A)', 'mean(B)', 'diff', 'p-tukey', 'sig']].to_csv(
        f"{GT_name}_TukeyHSD.txt",
        sep='\t',
        float_format="%.3e",
        index=False
    )


import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.backends.backend_pdf import PdfPages
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np


# 计算统计量
summary = data.groupby('group')['value'].agg(['mean','std','count'])
summary['ci'] = 1.96 * summary['std']/np.sqrt(summary['count'])

# 创建图形
plt.figure(figsize=(8,6))
sns.set_style("ticks")  # 仅保留坐标轴


# 设置X轴范围（增加左右留白）
x_pos = np.arange(len(summary))
x_padding = 1.0  # 两侧留白单位
y_padding = max(summary['mean'])*0.015  # 动态计算Y轴留白


plt.xlim(-x_padding, len(summary)-1 + x_padding)  # 关键调整
plt.xticks(x_pos, summary.index)
plt.ylim(min(summary['mean']-summary['ci'])-y_padding, 
         max(summary['mean']+summary['ci'])+y_padding)


# 绘制点线图
plt.errorbar(x=x_pos, y=summary['mean'],
            yerr=summary['ci'], fmt='o',
            markersize=10, capsize=5,
            color='royalblue', ecolor='darkred')

# 美化样式
plt.xlabel('Genotype Group', fontsize=12)
plt.ylabel('Phenotype Value (Mean±95% CI)', fontsize=12)
plt.title(f'{args.mark}', fontsize=14)  # 添加分子标记名


plt.grid(False)  # 显式关闭网格线

f_value = anova_result.loc[0, 'F']
p_value = anova_result.loc[0, 'p-unc']
stats_text=f"F = {f_value:.2f}, p-unc = {p_value:.2e}"
plt.text(0.95, 0.95, stats_text,
         transform=plt.gca().transAxes,
         ha='right', va='top',
         bbox=dict(facecolor='white', alpha=0.8, edgecolor='none'))

# 双格式保存
with PdfPages(GT_name+'_group_comparison.pdf') as pdf:
    pdf.savefig(bbox_inches='tight')
    plt.savefig(GT_name+'_group_comparison.png', dpi=300, bbox_inches='tight')
    plt.close()

