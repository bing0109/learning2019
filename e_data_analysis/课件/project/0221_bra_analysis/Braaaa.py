import pandas as pd
import matplotlib.pyplot as plt
import pymongo

plt.rcParams['font.sans-serif'] = ['SimHei']

MONGO_URL='localhost'
MONGO_DB='jdbra'

client = pymongo.MongoClient(MONGO_URL)
db = client[MONGO_DB]

def get_data():
    '''
    获取数据集
    :return:
    '''
    a=db['BraItem'].find()
    data=pd.DataFrame(list(a))
    data=data.drop(['_id','id'],axis=1)
    # data.to_csv('data/bra.csv',index=False,encoding='gb18030')
    return data

def deal_color(color):
    '''
    提取规范的颜色信息
    :param color: 颜色
    :return:
    '''
    colors = ['肤','红','橙','黄','绿','青','蓝','紫','黑','白','灰','粉']
    for c in colors:
        if c in color:
            return c
    return '其他'

def deal_cup(cup):
    '''
    清洗罩杯数据，将包含罩杯的数据提取出来
    :param cup:
    :return:
    '''
    cups = ['A','B','C','D','E']
    for c in cups:
        if c in cup.upper():
            return c

def get_color_img(series_color):
    '''
    绘制颜色分布
    :param series_color: 包含颜色的Series对象
    :return:
    '''
    color=series_color.value_counts()
    color_main = color[color>100]#超过100数量的颜色
    color_other = color[color <= 100].sum()  # 100数量的颜色
    color_main['其他']=color_main['其他']+color_other
    color_rate = ((color_main/color_main.sum())*100)
    #绘制图片，并进行保存
    plt.figure(figsize=(8,8))
    color_rate.index = color_rate.index+'色'
    plt.pie(color_rate.values,labels=color_rate.index,autopct='%.2f%%')
    plt.title('胸罩不同颜色需求占比',fontsize=15)
    plt.savefig('image/BraColorDistribution.png',dpi=500,bbox_inches='tight')

def get_cup_img(cup_series):
    '''
    绘制罩杯分布
    :param cup_series: 罩杯siries对象
    :return:
    '''
    cups=cup_series.value_counts()
    cups = cups/cups.sum()*100
    cups.index = '罩杯'+cups.index
    #绘制图片，并进行保存
    plt.figure(figsize=(8,8))
    plt.pie(cups.values,labels=cups.index,autopct='%.2f%%')
    plt.title('胸罩不同罩杯需求占比',fontsize=15)
    plt.savefig('image/BraCupDistribution.png',dpi=500,bbox_inches='tight')

#主体函数
def main():
    data=get_data()#从数据库获取数据
    data=data.drop_duplicates()#去重
    data['color']=data['productColor'].apply(deal_color)#清洗颜色数据
    get_color_img(data['color'])#绘制颜色分布图
    data['cup']=data['productSize'].apply(deal_cup)#清洗罩杯数据
    get_cup_img(data['cup'])#绘制罩杯分布

if __name__=='__main__':
    main()