*_ANOVA.txt :	 单因素方差分析统计结果表格
	    Source :	变异来源  : 	"group":（组间变异）,"Residual"或"Error":(未被解释的随机变异),"Total":(整体变异)
	    ddof1  :	组间自由度: 	自由度=分组数-1 : 值为2 代表3个分组
	    ddof2  :	组内自由度: 	自由度=组内自由度+组间自由度+1 ：值为845 表示总样本量为845,反映独立信息量
	    F      :	F统计量   : 	组间组内方差比 : 值为58,则表示组间方差是组内方差的58倍
	    p-unc  :	未校正p值 : 	结果是偶然发生的概率(无效假设)，P值远小于常规阈值0.05 : 拒绝假设

*_TukeyHSD.txt : 	Tukey's Honest Significant Difference (HSD): 一种用于多重比较检验的统计方法,通过控制整体第一类错误率,提供组间差异的可靠评估,确保结果的可信度,主要用于方差分析（ANOVA）后确定哪些组间存在显著差异
	    A       : 	第一个比较组名
	    B       : 	第二个比较组名,AB先后顺序无影响
	    mean(A) : 	第一组均值
	    mean(B) : 	第二组均值
	    diff    : 	组间均值差
	    p-tukey : 	校正后P值,通过Tukey方法调整多重比较的显著性
	    sig     : 	显著性标记 p < 0.01（高度显著**）p < 0.05（显著*）

*_group_comparison.png
*_group_comparison.pdf : 	标记位点均值差异, X轴基因型, Y轴表型值均值以及95%置信区间(CI), 添加F统计量和p-unc值

