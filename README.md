# ANOVAR
## 背景
使用单因素方差分析，分析一个样本的表型是否与基因型相关
## 使用方法
`sh work_major.sh`
## 其中文件格式
文件: samp_genotype
第一列是样本名，后面每一列是一个位点，位点名字可以更改
| samp | K000754 | K000782 | SNPY3 | SNPY4 | SNPY5 | K000783 |
|------|---------|---------|-------|-------|-------|---------|
| 0    | T:C     | G:G     | C:C   | G:G   | G:G   | A:A     |
| 1    | C:C     | A:A     | T:T   | C:C   | A:A   | T:T     |
| 2    | T:C     | G:A     | C:T   | G:C   | G:A   | A:T     |
| 3    | T:C     | G:A     | C:T   | G:C   | G:A   | A:T     |
| 4    | T:C     | G:A     | C:T   | G:C   | G:A   | A:T     |
| 6    | T:T     | G:G     | C:C   | G:G   | G:G   | A:A     |

<br>

文件: samp_pheno
第一列是样本名，第二列是表型名，一次分析只能一个表型
| samp | leaf_numbers |
|------|--------------|
| 1    | 29           |
| 2    | 31           |
| 3    | 27           |
| 4    | 31           |
| 5    | 30           |
| 6    | 36           |
| 7    | 33           |

<details>                                                                                                          
<summary>所需软件和环境配置</summary>
其中，pipline所需的python模块和R包需要配置，使用conda都能配
</details>

