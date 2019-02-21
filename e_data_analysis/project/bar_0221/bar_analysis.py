# coding:utf-8
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
import pymongo


myfont = matplotlib.font_manager.FontProperties(fname='/usr/share/fonts/truetype/arphic/uming.ttc',size=15)



# # 从mongodb里面取数据
# MONGO_URL = 'localhost'
# MONGO_DB = 'pachong'
# mongo_client = pymongo.MongoClient(MONGO_URL)
# db = mongo_client[MONGO_DB]


def get_data():
    data = pd.read_csv('data/bra.csv', encoding='gb18030')
    # print(data)
    return data


def clean_ColorData(series_color):
    color_temp = ['肤','红','灰','蓝','绿','粉','黑','黄','紫','白']
    for color in color_temp:
        if color in series_color:
            return color

    return '其他'


def gen_color_img(series_color):
    color_stc = series_color.value_counts()
    color_main = color_stc[color_stc > 100]
    color_main.index = color_main.index + '色'
    color_other = color_stc[color_stc <= 100].sum() + color_stc['其他']

    # print(color_main,'----',color_other)
    # print(pd.Series(color_other,index=['其他']),'+++++++')
    color_statistics = pd.concat([color_main.drop('其他色'), pd.Series(color_other, index=['其他'])], axis=0)
    print(color_statistics)

    # 画饼状图
    plt.figure(figsize=(8, 8))
    lables = ['肤色','黑色', '灰色', '蓝色', '红色', '粉色', '紫色', '其他']
    colors = ['#FFF68F', 'black', 'gray', 'blue', 'red', 'pink', 'purple', 'white']
    # pie,l_text,p_text = plt.pie(color_statistics.values,autopct='%.2f%%',labels=lables,colors=colors,textprops={'fontsize': 16, 'color': 'w'})
    pie, l_text, p_text = plt.pie(color_statistics.values,autopct='%.2f%%',labels=lables)
    '''
    patches, l_texts, p_texts，为了得到饼图的返回值，p_texts饼图内部文本的，l_texts饼图外label的文本
    '''
    for text in l_text:
        print(text)
        text.set_fontproperties(myfont)

    for text in p_text:
        print(text)
        text.set_fontproperties(myfont)

    # 黑色类的字体颜色也是黑的，想改一下百分比的字体颜色，暂时没成功
    # p_text[2].set_fontproperties(matplotlib.font_manager.FontProperties(textprops={'fontsize': 16, 'color': 'w'}))
    plt.title('颜色分布图', fontproperties=myfont, fontsize=15)
    # plt.show()
    plt.savefig('image/颜色分布图.png', dpi=500, bbox_inches='tight')

def main():
    data = get_data()
    # print(type(data),data.columns)
    # 清洗颜色数据
    data['color'] = data['productColor'].apply(clean_ColorData)
    # print(data['productColor'].unique())
    # print(data['color'].value_counts())
    # 根据颜色画饼状态
    gen_color_img(data['color'])


if __name__ == '__main__':
    main()



