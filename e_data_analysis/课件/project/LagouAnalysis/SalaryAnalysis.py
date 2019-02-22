from AreaAnalysis import *

def get_salary(salary_str):
    salary=salary_str.strip().replace('K','').replace('k','').split('-')
    return int(salary[0])+(int(salary[1])-int(salary[0]))*0.4

def get_salary_img(salary_series):
    bins=[0,5,10,15,20,25,30,float('inf')]
    salary=pd.cut(salary_series,bins=bins).value_counts()
    salary=salary.sort_index()
    plt.figure(figsize=(10,8))
    salary.plot(kind='bar')
    plt.xticks(rotation=0)
    plt.xlabel('薪酬区间(k/月)',fontsize=12)
    plt.title('薪酬分布',fontsize=15)
    plt.savefig('img/薪酬分布.png',dpi=400)

def get_city_salary_img(df):
    main_city=['北京','上海','深圳','杭州','广州']
    main_salary=[]
    for city in main_city:
        main_salary.append(df[df['city'].isin([city])]['money'])
    plt.figure(figsize=(10,8))
    plt.boxplot(main_salary,labels=main_city)
    mean_salary=[]
    for a in main_salary:
        mean_salary.append(round(a.mean(),1))
    plt.scatter(range(1,len(main_city)+1),mean_salary,marker='s')
    plt.title('不同城市的薪酬分布',fontsize=15)
    plt.savefig('img/城市薪酬.png',dpi=400,bbox_inches='tight')

def get_education_salary_img(df):
    education_salary=df.groupby('education')['money'].median().round(0)
    education_salary=education_salary[education_salary.index!='博士'].sort_values()
    plt.figure(figsize=(10,8))
    education_salary.plot(kind='bar')
    plt.title('不同教育背景的薪酬分布',fontsize=15)
    plt.xticks(rotation=30,fontsize=12)
    plt.xlabel('')
    for a,b in zip(range(0,len(education_salary)),education_salary.values):
        plt.text(a,b+0.2,str(b),horizontalalignment='center',fontsize=10)
    plt.savefig('img/教育薪酬.png',dpi=400)

def get_workyear_salary_img(df):
    work_salary=df.groupby('workYear')['money'].median().sort_values().round(1)
    plt.figure(figsize=(10, 8))
    work_salary.plot(kind='bar')
    plt.title('不同工作经验的薪酬分布', fontsize=15)
    plt.xticks(rotation=30, fontsize=12)
    plt.xlabel('')
    for a, b in zip(range(0, len(work_salary)), work_salary.values):
        plt.text(a, b + 0.2, str(b), horizontalalignment='center', fontsize=10)
    plt.savefig('img/工作经验薪酬.png', dpi=400)

def main():
    data=pd.read_csv('data/LagouPostion.csv',encoding='gb18030')
    data=data[data['jobNature']=='全职']
    data['money']=data['salary'].apply(get_salary)
    # get_salary_img(data['money'])#薪酬分布
    # get_city_salary_img(data[['money','city']])#城市对应的薪酬分布
    # get_education_salary_img(data[['money','education']])
    get_workyear_salary_img(data[['workYear', 'money']])

if __name__=='__main__':
    main()
