# coding:utf-8
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
import pymongo


myfont = matplotlib.font_manager.FontProperties(fname='/home/zelin/bing1/other/simhei.ttf')

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

    color_statistics = pd.concat([color_main.drop('其他色'), pd.Series(color_other, index=['其他'])], axis=0)
    # print(color_statistics)

    # 画饼状图
    plt.figure(figsize=(6, 6))
    lables = ['肤色', '黑色', '灰色', '蓝色', '红色', '粉色', '紫色', '其他']
    colors = ['#FFF68F', 'black', 'grey', 'blue', 'red', 'pink', 'purple', '#E0E0E0']
    # pie,l_text,p_text = plt.pie(color_statistics.values, autopct='%.2f%%', labels=lables, colors=colors, textprops={'fontsize': 16, 'color': 'w'})
    pie, l_text, p_text = plt.pie(color_statistics.values, autopct='%.2f%%', labels=lables, colors=colors)
    '''
    patches, l_texts, p_texts，为饼图的返回值，p_texts饼图内部文本的，l_texts饼图外label的文本
    '''
    for text in l_text:
        print(text)
        text.set_fontproperties(myfont)

    for text in p_text:
        print(text)
        text.set_fontproperties(myfont)

    plt.setp(p_text, size=12, weight="bold", color='black')
    plt.setp(l_text, size=14, weight="bold", color='black')
    # 黑色类的字体颜色也是黑的，可改一下其百分比的字体颜色
    plt.setp(p_text[1], size=14, weight="bold", color='w')

    plt.title('颜色分布图', fontproperties=myfont, fontsize=16)
    # plt.show()
    plt.savefig('image/颜色分布图1.png', dpi=300, bbox_inches='tight')


def clean_CupData(ds):
    cup_list = ['A', 'B', 'C', 'D', 'E']
    for s in cup_list:
        if s in ds.upper():
            return s

    return 'other'


def gen_cup_img(s_cup):
    cup_data = s_cup.value_counts().sort_index()
    plt.figure(figsize=(6.5,5))
    labels = cup_data.index + '罩杯'
    option, l_text, p_text = plt.pie(cup_data.values, autopct='%.2f%%', pctdistance=1.1)

    # plt.setp(l_text, fontproperties=myfont, size=14, weight="bold")
    plt.setp(p_text, fontproperties=myfont, size=14, weight="bold")

    legendarea = plt.legend(option, labels,
                            # title="分类",
                            loc="center left",
                            bbox_to_anchor=(1, 0, 0.5, 1),
                            prop=myfont,
                            # title_fontsize=20,
                            fontsize='large')


    plt.title('罩杯分布图', fontproperties=myfont, fontsize=18)

    plt.savefig('image/罩杯分布图.png', dpi=400,bbox_inches='tight')


def main():
    data = get_data()
    # print(type(data),data.columns)
    # 清洗颜色数据
    data['color'] = data['productColor'].apply(clean_ColorData)
    # 根据颜色画饼状态
    gen_color_img(data['color'])

    # 清洗杯罩数据
    data['cups'] = data['productSize'].apply(clean_CupData)
    # 根据杯罩画饼状图
    gen_cup_img(data['cups'])

    abc=data['cups'].value_counts()
    print(abc)


if __name__ == '__main__':
    main()



