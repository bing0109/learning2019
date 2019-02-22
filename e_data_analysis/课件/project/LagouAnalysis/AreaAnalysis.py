import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['SimHei']

def get_field(field_str):
    '''
    清洗行业数据
    :param field_str: 关于行业的字符串
    :return:
    '''
    fields=field_str.strip().replace(' ',',').replace('、',',').replace('，',',').split(',')[0]
    return fields

def get_pie_img(city_series,title,filename,num=100):
    '''
    统计频数，并进行图片绘制和保存
    :param city_series: 需要统计的数据series对象
    :param title: 图片标题的名字
    :param filename: 保存的文件名
    :param num: 划分其他类的数量
    :return:
    '''
    city_num=city_series.value_counts()#统计频数
    #将低于num数量的数量变为其他类
    if num>0:
        city_main = city_num[city_num>num]
        city_other = pd.Series(city_num[city_num<=num].sum(),index=['其他'])
        city_num=pd.concat([city_main,city_other],axis=0)
    city_rate = city_num/city_num.sum()*100#转化为总数为100
    #画图
    plt.figure(figsize=(10,10))
    plt.pie(city_rate.values,labels=city_rate.index,autopct='%.1f%%')
    plt.title(title,fontsize=15)
    plt.savefig('img/'+filename,dpi=400,bbox_inches='tight')#保存

def main():
    data=pd.read_csv('data/LagouPostion.csv',encoding='gb18030')#读取数据
    data = data[data['jobNature'] == '全职']
    get_pie_img(data['city'],title='不同城市的需求分布',filename='城市分布.png')#城市需求分布
    data['field']=data['industryField'].apply(get_field)#清洗行业数据
    get_pie_img(data['field'], title='不同行业的需求分布', filename='行业分布.png',num=40)#行业需求分布
    # print(data['Field'].value_counts())
    get_pie_img(data['workYear'],title='经验需求分布',filename='经验需求分布.png',num=0)

if __name__=='__main__':
    main()