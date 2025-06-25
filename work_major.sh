rm -rf  ANOVA_stat
rm -rf  ANOVA_stat.zip
python  sample_uniq.py       --inf1_samp_genotype    samp_genotype   --inf2_samp_pheno  samp_pheno
ls   samp*pheno.xls  |awk -F  "_" '{print$2"\t"$0}' |awk  -F "GT" '{print$1"\t"$0}' |awk -F   "\t"   '{print$3"\t"$1}'    |while read i  ;do 

    array=($i)  ;
    echo  ${array[0]}; 
    cat  ${array[0]}     |cut -f 2  |sort |uniq  -c   ;echo  -e  "\n\n"   ;
    python   ANOVA_statistic.py   --infile   ${array[0]}     --mark   ${array[1]}   ;
done


ls     samp*pheno.xls  |awk -F  "_"  '{print$2}'  |awk -F "GT"   '{print$1}' |while read i   ; do   
    mkdir    -p   ANOVA_stat/${i}  ;
    cp ${i}_group_comparison.png ${i}_group_comparison.pdf ${i}_ANOVA.txt ${i}_TukeyHSD.txt ANOVA_stat/${i} ;
done
cp       ANOVA_readme.txt      ANOVA_stat

mkdir   -p    merge_excel   
cp   *_ANOVA.txt   *_TukeyHSD.txt  merge_excel
cp   ANOVA_readme.txt   merge_excel

python txt2xlsx.py    merge_excel    ANOVA.xlsx

python   Report.py

zip  -r    ANOVA_stat.zip   ANOVA_stat/    ANOVA_report.html
