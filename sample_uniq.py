#!/miniconda3/bin/python
#-*- coding: utf-8 -*-
#File Name    : sample_uniq.py
#Author       : liangjifeng
#Mail         : jifeng.liang@biobin.com.cn
#Create Time  : 2025-06-09 13:58
import sys,os,gzip
import argparse
parser = argparse.ArgumentParser(description='fighting')
parser.add_argument('--inf1_samp_genotype',  help='输入文件路径',required=True )
parser.add_argument('--inf2_samp_pheno',  help='输入文件路径',required=True )

parser.add_argument('--pre',type=str, help='测序策略', default="WES",choices=["WGS","WES","TR"])
args = parser.parse_args()

header = ''
samp_list=[]
samp_mk_GT = {}
for  i in open(args.inf1_samp_genotype,'r').readlines():
    if header == '' and "samp" in i:
        header = i.strip().split("\t")
        site_list = i.strip().split("\t")[1:]
        print("site_list is :")
        print(site_list)
    else:
        
        samp_name=i.strip().split("\t")[0]
        samp_mk_GT[samp_name]={}
        if samp_name in samp_list :
            print("samp name dup")
            continue
        else :
            samp_list.append(samp_name)
            for  mk in  site_list :
                samp_mk_GT[samp_name][mk]=i.strip().split("\t")[header.index(mk)]

header = ''
samp_pheno = {}
for i in open(args.inf2_samp_pheno,'r').readlines():
    if  header=='' and  "samp" in i :
            header = i.strip().split("\t")
    else:
        if len(i.strip().split("\t"))==1:
            continue
        samp_name=i.strip().split("\t")[0]
        pheno = i.strip().split("\t")[1]
        if  samp_name not  in samp_list:
            samp_list.append(samp_name)
        samp_pheno[samp_name] = pheno

for mk in  site_list :
    open("samp_"+mk+"GT_pheno.xls",'w').write('''samp\t{mk}\tpheno\n'''.format(mk=mk,   pheno=pheno ))
    for samp in samp_list :
        if   samp in samp_pheno.keys() and  samp in samp_mk_GT.keys():
            pheno = samp_pheno[samp] 
            #print(samp_mk_GT[samp])
            GT = samp_mk_GT[samp][mk]
            if  GT  in ["?","Uncallable"]:
                continue
            open("samp_"+mk+"GT_pheno.xls",'a').write('''{samp}\t{GT}\t{pheno}\n'''.format(samp=samp,   GT=GT,   pheno=pheno))

