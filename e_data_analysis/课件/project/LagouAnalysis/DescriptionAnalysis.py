import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import jieba
import os
from wordcloud import WordCloud
import re
from SalaryAnalysis import get_salary

def get_stopword():
    '''
    获取停用词
    :return:
    '''
    stopwords=[]
    with open('data/中文停用词库.txt','r') as f:
        for line in f:
            stopwords.append(line.strip())
    return stopwords

def get_description(desc_str):
    '''
    获取职位描述相关词汇：用结巴进行分词，去除相关词汇（停用词、空白字符等）
    :param desc_str:
    :return:
    '''
    useness_word=['/','.','数据分析','）','（','，','数据','分析']
    desc_str=desc_str.replace('职位描述','').replace('：','').strip()
    seg_list=jieba.cut(desc_str)#分词
    stopwords = get_stopword()
    words=[]
    for word in seg_list:
        word=word.strip()
        if word != '' and word not in stopwords and word not in useness_word:
            words.append(word)
    return words

def get_skill(desc_str):
    skills=re.findall(r'[a-zA-Z]+',desc_str,re.S)
    ss=[]
    for s in skills:
        s=s.upper()
        if 'EXC' in s:
            s='EXCEL'
        if 'POWERPOINT' in s:
            s='PPT'
        ss.append(s)
    return ss

def word_freq(words_series):
    '''
    统计词频
    :param words_series:
    :return:
    '''
    word_dict={}
    for i in range(0,len(words_series)):
        for word in words_series.iloc[i]:
            if word in word_dict:
                word_dict[word]+=1
            else:
                word_dict[word]=1
    return word_dict

#wordcloud应用参考：https://blog.csdn.net/fly910905/article/details/77763086
#wordcloud参数：https://blog.csdn.net/yaochuyi/article/details/80094659
#色系选择：https://matplotlib.org/examples/color/colormaps_reference.html
def get_word_img(word_dict,name):
    '''
    绘制词云图
    :param word_dict: 关于职位描述的词频
    :return:
    '''
    backgroud_Image=plt.imread('data/back.jpg')#读取背景图
    wc = WordCloud(
        background_color='white',#背景色
        mask=backgroud_Image,#背景图
        font_path='data/simhei.ttf',#字体路径
        max_words=1000,#限制最大词数
        max_font_size=100,#
        colormap='hsv'
    )
    wc.generate_from_frequencies(word_dict)#生成词云图
    plt.imshow(wc)
    plt.axis('off')#去掉坐标轴
    plt.savefig('img/'+name,dpi=400,bbox_inches='tight')#保存图片

def func(description,skill):
    if skill in description:
        return True
    else:
        return False

def get_skill_salary(df):
    main_skill=['EXCEL','PPT','SQL','统计','PYTHON','SAS','SPSS','R','机器学习','HADOOP','SPARK','HIVE']
    df.loc[:,'description'] = df['description'].str.upper().str.replace('EXC', 'EXCEL').str.replace('POWERPOINT', 'PPT')
    skill_salary=[]
    for skill in main_skill:
        skill_salary.append(round(df[df['description'].apply(func,skill=skill)]['money'].mean(),1))
    plt.figure(figsize=(10,8))
    series_skill=pd.Series(skill_salary,index=main_skill)
    series_skill.plot(kind='bar')
    plt.xticks(rotation=0,fontsize=12)
    plt.title('不能技能的薪资情况',fontsize=15)
    for a,b in zip(range(0,len(series_skill)),series_skill.values):
        plt.text(a,b+0.2,str(b),horizontalalignment='center',fontsize=10)
    plt.savefig('img/技能薪资.png',dpi=400)

def main():
    data = pd.read_csv('data/LagouPosition1234.csv', encoding='gb18030')
    data = data[data['jobNature'] == '全职']
    data['words']=data['description'].apply(get_description)#提取职位描述信息
    word_dict=word_freq(data['words'])#统计词频
    # pd.Series(word_dict).sort_values(ascending=False).to_csv('data/aaa.csv',encoding='gb18030')
    get_word_img(word_dict,name='职责描述.png')#绘制技能和职责的词云图
    data['skill']=data['description'].apply(get_skill)
    skill_dict = word_freq(data['skill'])#统计技能频率
    get_word_img(skill_dict,name='技能要求.png')
    data['money']=data['salary'].apply(get_salary)
    get_skill_salary(data[['money','description']])


if __name__=='__main__':
    main()