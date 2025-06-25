# ANOVAR
## 背景
使用单因素方差分析，分析一个样本的表型是否与基因型相关
## 使用方法
`sh work_major.sh`
## 其中文件格式
samp_genotype:
| samp | K000754 | K000782 | SNPY3 | SNPY4 | SNPY5 | K000783 |
|------|---------|---------|-------|-------|-------|---------|
| 0    | T:C     | G:G     | C:C   | G:G   | G:G   | A:A     |
| 1    | C:C     | A:A     | T:T   | C:C   | A:A   | T:T     |
| 2    | T:C     | G:A     | C:T   | G:C   | G:A   | A:T     |
| 3    | T:C     | G:A     | C:T   | G:C   | G:A   | A:T     |
| 4    | T:C     | G:A     | C:T   | G:C   | G:A   | A:T     |
| 6    | T:T     | G:G     | C:C   | G:G   | G:G   | A:A     |

samp_pheno:
<details>
<summary>点击展开</summary>
samp_pheno:
samp    leaf_numbers
1       29
2       31
3       27
4       31
5       30
6       36
7       33
.
.
.
</details>

## 所需环境
其中，pipline所需的python模块和R包需要配置，使用conda都能配


