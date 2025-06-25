#!/miniconda3/bin/python
#-*- coding: utf-8 -*-
#File Name    : Report.py
#Author       : liangjifeng
#Mail         : jifeng.liang@biobin.com.cn
#Create Time  : 2025-06-10 11:51
import sys,os,gzip
import argparse
#parser = argparse.ArgumentParser(description='fighting')
#parser.add_argument('--infile',  help='输入文件路径',required=True )
#parser.add_argument('--seqstrategy',type=str, help='测序策略', default="WES",choices=["WGS","WES","TR"])
#args = parser.parse_args()


#!/miniconda3/bin/python
#-*- coding: utf-8 -*-
import os
import glob

def read_table(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        return [line.strip().split('\t') for line in f if line.strip()]

def find_samples(base_dir="ANOVA_stat"):
    samples = {}
    for dir_path in glob.glob(f"{base_dir}/*"):
        sample_id = os.path.basename(dir_path)
        files = {
            'anova': f"{dir_path}/{sample_id}_ANOVA.txt",
            'tukey': f"{dir_path}/{sample_id}_TukeyHSD.txt",
            'image': f"{dir_path}/{sample_id}_group_comparison.png"
        }
        if all(os.path.exists(f) for f in files.values()):
            samples[sample_id] = {
                **files,
                'anova_data': read_table(files['anova']),
                'tukey_data': read_table(files['tukey'])
            }
    return samples

def generate_html(output_path, samples):
    sample_options = ''.join(
        f'<option value="{sid}">{sid}</option>'
        for sid in samples.keys()
    )

    sample_contents = []
    for sid, data in samples.items():
        content = f"""
        <div id="{sid}-content" class="sample-content" style="display:none">
            <div class="table-section">
                <h3>ANOVA分析结果 - {sid}</h3>
                <table>                                                                                                                {' '.join(f'<tr>{"".join(f"<td>{cell}</td>" for cell in row)}</tr>'                                                for row in data['anova_data'])}                                                                                </table>                                    
                <div class="caption">
                    <p><strong>表1：单因素方差分析结果</strong></p>
                    <p style="white-space: pre-line">Source :变异来源  : "group":（组间变异）,"Residual"或"Error":(未被解释的随机变异),"Total":(整体变异)
    ddof1  :组间自由度: 自由度=分组数-1 : 值为2 代表3个分组
    ddof2  :组内自由度: 自由度=组内自由度+组间自由度+1 ：值为845 表示总样本量为845,反映独立信息量
    F      :F统计量   : 组间组内方差比 : 值为58,则表示组间方差是组内方差的58倍
    p-unc  :未校正p值 : 结果是偶然发生的概率(无效假设)，P值远小于常规阈值0.05 : 拒绝假设
</p>
                </div>
            </div>

            <div class="table-section">
                <h3>TukeyHSD检验结果 - {sid}</h3>
                <table>
                    {' '.join(f'<tr>{"".join(f"<td>{cell}</td>" for cell in row)}</tr>'
                    for row in data['tukey_data'])}
                </table>
                <div class="caption">
                    <p><strong>表2：多重比较检验结果</strong></p>
                    <p style="white-space: pre-line">A       : 第一个比较组名
    B       : 第二个比较组名,AB先后顺序无影响
    mean(A) : 第一组均值
    mean(B) : 第二组均值
    diff    : 组间均值差
    p-tukey : 校正后P值,通过Tukey方法调整多重比较的显著性
    sig     : 显著性标记 p < 0.01（高度显著**）p < 0.05（显著*）</p>
                </div>
            </div>

            <div class="img-section">

                <h3>组间比较图 - {sid}</h3>
                <img src="{data['image']}" style="max-width:600px">
                <div class="caption">
                    <p><strong>图1：组间均值比较</strong></p>
                    <p style="white-space: pre-line">X轴：分组类别；Y轴：表型值均值；误差线：95%置信区间；图中标注F统计量和p值</p>
                </div>
            </div>
        </div>"""
        sample_contents.append(content)

    html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>分子标记分析报告</title>
    <style>
        body {{
            font-family: Arial;
            max-width: 800px;
            margin: 0 auto;
            padding: 15px;
            line-height: 1.6;
        }}
        .control-panel {{
            margin: 15px 0;
            padding: 15px;
            background: #f5f7fa;
            border-radius: 5px;
        }}
        select {{
            padding: 8px 12px;
            border: 1px solid #ddd;
        }}
        .section {{
            margin: 25px 0;
            padding: 15px;
            border: 1px solid #e1e4e8;
            border-radius: 5px;
            background: #fff;
        }}
        .caption {{
            background: #f8f9fa;
            padding: 12px;
            margin-bottom: 15px;
            border-left: 4px solid #4285f4;
            font-size: 14px;
        }}
        .caption p {{
            margin: 5px 0;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 10px 0;
            font-size: 14px;
        }}
        th, td {{
            border: 1px solid #ddd;
            padding: 10px;
            text-align: left;
        }}
        th {{
            background-color: #f2f6ff;
        }}
        img {{
            display: block;
            max-width: 100%;
            height: auto;
            margin: 15px auto;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        h3 {{
            color: #202124;
            border-bottom: 1px solid #eee;
            padding-bottom: 8px;
        }}
    </style>
</head>
<body>
    <h1>分子标记统计分析报告</h1>
<!-- 新增正文区域 -->
    <section class="report-intro">
        <ul>
            <li>单因素方差分析是一种用于比较三个或更多组的均值是否存在显著差异的统计方法，适用于单一分类变量（自变量）对连续型因变量的影响分析。</li>
            <li>Tukey HSD（Honestly Significant Difference，真实显著差异）检验是用于<200c>多重比较<200c>的统计方法>，专门解决ANOVA（方差分析）后多组间两两比较的假阳性问题。</li>
        </ul>
    </section>
<!-- 其余代码保持不变 -->
    
    <div class="control-panel">
        <select id="sample-select" onchange="switchSample()">
            <option value="">-- 请选择分子标记名称 --</option>
            {sample_options}
        </select>
    </div>

    {''.join(sample_contents)}

    <script>
        function switchSample() {{
            const sel = document.getElementById('sample-select');
            document.querySelectorAll('.sample-content').forEach(el => {{
                el.style.display = 'none';
            }});
            if (sel.value) {{
                document.getElementById(sel.value + '-content').style.display = 'block';
            }}
        }}
        document.addEventListener('DOMContentLoaded', () => {{
            const first = document.querySelector('.sample-content');
            if (first) {{
                first.style.display = 'block';
                document.getElementById('sample-select').value = first.id.replace('-content', '');
            }}
        }});
    </script>
</body>
</html>"""
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html)

if __name__ == "__main__":
    samples = find_samples()
    if not samples:
        print("未找到有效样本数据")
        exit()
    output_file = "ANOVA_report.html"
    generate_html(output_file, samples)
    print(f"报告已生成: {os.path.abspath(output_file)}")


