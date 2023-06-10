# -*- coding: utf-8 -*-
import pandas as pd
import numpy as ny
import re
import json
#from pyecharts.charts import Map
from pyecharts.globals import ThemeType
import streamlit as st
from streamlit_echarts import st_echarts
from pyecharts import options as opts
from pyecharts.charts import Bar
from streamlit_echarts import st_pyecharts
from PIL import Image
st.set_page_config(page_title="猎聘", layout="wide")
#st.markdown(" <style>iframe{ height: 300px !important } ", unsafe_allow_html=True)
st.markdown("<h1 style='text-align: center; color: white;'>猎聘招聘数据分析</h1>", unsafe_allow_html=True)
bi=pd.read_excel(r'.//lieping.xlsx')#,encoding='gb18030')
import base64
def get_base64(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

def set_background(png_file):
    bin_str = get_base64(png_file)
    page_bg_img = '''
    <style>
    .stApp {
    background-image: url("data:image/png;base64,%s");
    background-size: cover;
    }
    </style>
    ''' % bin_str
    st.markdown(page_bg_img, unsafe_allow_html=True)

set_background('.//ceLSL3NHSblIM.jpg')
bg_img="""
<style>
.stApp{{
  width: 100%;
  height: 100%;
  background-size: cover;
  background-position: center center;
  background-repeat: repeat;
  background-image: url(./app/ceLSL3NHSblIM.jpg)}}
[data-testid="stHeader"]{
    background-color:rgba(0, 0, 0, 0)
    }
[data-testid="metric-container"] {
   background-color: rgba(128, 128, 128, 0.4);
   border: 2px solid rgba(28, 131, 225, 0.4);
   padding: 5% 5% 5% 10%;
   border-radius: 5px;
   color: rgb(30, 103, 119);
   overflow-wrap: break-word;
   white-space: break-spaces;
   color:white;
}
[data-testid="stMarkdownContainer"]{
    color: white;
    }
</style>
 """
#background-image: url(./背景2.png)
st.markdown(bg_img, unsafe_allow_html=True)
list1=[]
list2=[]
list3=[]
list4=[]
list5=[]
#薪水
for i in range(len(bi)):
    if '-' in bi['薪水'][i] :        
        temp=bi['薪水'][i].split('-')        
        #list1.append(temp[0])
        if '·' in temp[1]:
            temp1=temp[1].split('·')
            temp2=temp1[1].split('薪')[0]
            temp3=temp1[0].split('k')[0]
            list1.append((int(temp[0])*int(temp2))/12)
            list2.append((int(temp3)*int(temp2))/12)
        else:
            list1.append(temp[0])
            list2.append(temp[1][0:-1])
    else:
        list1.append(0)
        list2.append(0)
bi['salary_min']=pd.Series(list1)
bi['salary_max']=pd.Series(list2)
bi.salary_min=bi.salary_min.astype('float')
bi.salary_max=bi.salary_max.astype('float')
bi['salary_mean']=(bi.salary_min+bi.salary_max)/2
#地点
for i in range(len(bi)):
    if '-' in bi['地点'][i] : 
        tem=bi['地点'][i].split('-')[1].split('\n')
        list3.append(tem[0])
    else:
        list3.append('none')
bi['具体地点']=pd.Series(list3)
a=bi.groupby('具体地点',as_index=False).mean('salary_mean').drop(index=0)
dd_smean=a[['具体地点', 'salary_mean']].values.tolist()
#dd_smean
data_city=[]
for i in range(len(dd_smean)):
    data_city.append({"name":dd_smean[i][0],"value":dd_smean[i][1]})
for i in range(len(bi)):
    if '\n' in str(bi['要求'][i]) :    
        tempnian=str(bi['要求'][i]).split('\n',2)[1]
        list5.append(tempnian)
    else:
        list5.append('none')
bi['学历要求']=pd.Series(list5)
b=bi.groupby('学历要求',as_index=False).mean('salary_mean').drop(index=0).sort_values(axis = 0, ascending = True,by=['salary_mean'])
print(b['salary_min'])
r=bi.groupby('公司名',as_index=False).mean('salary_mean').drop(index=0).sort_values(axis = 0, ascending = True,by=['salary_mean']).iloc[223:233]
rsm=[int(value) for value in r['salary_mean'].values]
rgs=[str(value) for value in r['公司名'].values]
from pyecharts import options as opts
from pyecharts.commons.utils import JsCode
from streamlit_echarts import Map
with open(r".//500000.json", "r",encoding="utf-8") as f:
    map = Map(
        "chongqing", 
        json.loads(f.read())) 
options = {"title": {"text": "平均工资地域分布 ", "left": "left"},
           "backgroundColor": 'rgba(128, 128, 128, 0.5)',
"tooltip": {
      "trigger": 'item',
      "showDelay": 0,
      "transitionDuration": 0.2,
    },
"visualMap": {
    "show": True,
    "left": "right",
    "min": 0,
    "max": 20,
    "inRange": {
        "color": [
            "#313695",
            "#4575b4",
            "#74add1",
            "#abd9e9",
            "#e0f3f8",
            "#ffffbf",
            "#fee090",
            "#fdae61",
            "#f46d43",
            "#d73027",
            "#a50026",
        ]
    },
    "text": ["High", "Low"],
    "calculable": True,
},
"series": [
    {
        "name": "平均工资地域分布",
        "type": "map",
        "roam": True,
        "map": "chongqing",
        "emphasis": {"label": {"show": True}},
       
        "data": data_city,
    }
],
}    
events = {
"click": "function(params) {return params.name }",
}


import pyecharts.options as opts
from pyecharts.charts import Line
from pyecharts.commons.utils import JsCode
from  pyecharts.charts import  *
from pyecharts.globals import ThemeType
for i in range(len(bi)):
    if '\n' in str(bi['要求'][i]) :    
        tempnian=str(bi['要求'][i]).split('\n',2)[1]
        list5.append(tempnian)
    else:
        list5.append('none')
bi['学历要求']=pd.Series(list5)
b=bi.groupby('学历要求',as_index=False).mean('salary_mean').drop(index=0).sort_values(axis = 0, ascending = True,by=['salary_mean'])
bsmin=[int(value) for value in b['salary_min'].values]
bsmax=[int(value) for value in b['salary_max'].values]
bxuel=[str(value) for value in b['学历要求'].values]
bsmean=[int(value) for value in b['salary_mean'].values]
from pyecharts.charts import Bar
bar = (
    Bar(init_opts=opts.InitOpts(width='400px', height='500px'
                               ))
    .add_xaxis(bxuel)
    .add_yaxis("最低工资", bsmin,bar_width = 20 )
    .add_yaxis("最高工资", bsmax,bar_width = 20)
    .set_series_opts(label_opts=opts.LabelOpts(is_show=False,position= "Right"))
    .set_global_opts(title_opts=opts.TitleOpts(title='学历与工资柱状图',title_textstyle_opts=(opts.TextStyleOpts(color='white')),),
                     xaxis_opts=opts.AxisOpts(name='学历'),       
                     yaxis_opts=opts.AxisOpts(name='工资（k）'),
                    legend_opts=opts.LegendOpts(type_="scroll", pos_right=10, orient="horizontal",background_color = "#CBCBCB")
                    )
)
line = (
    Line(init_opts=opts.InitOpts(width='400px', height='500px'
                               ))
    .add_xaxis(bxuel)
    .add_yaxis('平均工资',bsmean,z_level=100)
    .set_series_opts(label_opts=opts.LabelOpts(is_show=True,position= "Right"),# 不显示标签
                   linestyle_opts=opts.LineStyleOpts(width=3), # 线例设置宽度
                    )
    .set_global_opts(xaxis_opts=opts.AxisOpts(), # 设置x轴标签旋转角度
                     yaxis_opts=opts.AxisOpts(name='平均工资', min_=3), 
                     title_opts=opts.TitleOpts(title=''))        
    )
bar.overlap(line)
grid = Grid(init_opts=opts.InitOpts(bg_color='rgba(128, 128, 128, 0.5)'))
grid.add(bar,is_control_axis_index=True, grid_opts=opts.GridOpts(pos_left="5%", pos_right="5%", background_color='rgba(21, 1, 87, 0.5)'))
grid.render_notebook()
r=bi.groupby('公司名',as_index=False).mean('salary_mean').drop(index=0).sort_values(axis = 0, ascending = True,by=['salary_mean']).iloc[223:233]
rsm=[int(value) for value in r['salary_mean'].values]
rgs=[str(value) for value in r['公司名'].values]
bar = (
    Bar(init_opts=opts.InitOpts(width='800px', height='500px',bg_color='rgba(128, 128, 128, 0.5)',
                               theme=ThemeType.DARK))
    .add_xaxis(rgs)
    .add_yaxis("平均工资", rsm)
    .set_series_opts(label_opts=opts.LabelOpts(
                is_show=True,
                position="right",
                font_style='oblique',
                font_weight='bolder',
                font_size='13'),
                    itemstyle_opts={
                "normal": {
                    "color": {
                "type": 'linear',
                "x": 0,
                "y": 0,
                "x2": 0,
                "y2": 1,
                "colorStops": [{
                    "offset": 0, "color": '#0781C3' # 蓝色（头部）
                }, {
                    "offset": 1, "color": '#06F6F8' # 青色（底部）
                }],
            },  # 调整柱子颜色渐变
                    'shadowBlur': 8,  # 光影大小
                    "barBorderRadius": [100, 100, 100, 100],  # 调整柱子圆角弧度
                    "shadowColor": "#0EEEF9",  # 调整阴影颜色
                    'shadowOffsetY': 6,
                    'shadowOffsetX': 6,  # 偏移量
                }
            }

                    )
    .set_global_opts(title_opts=opts.TitleOpts(title='平均工资top10'),
                     xaxis_opts=opts.AxisOpts(name='公司名'),       
                     yaxis_opts=opts.AxisOpts(name='工资（k）'))
    
    .reversal_axis()
)
bar.render('平均工资top10.html')
list7=[]
for i in range(len(bi)):
    if '/' in str(bi['公司信息'][i]) :    
        gsmeg=str(bi['公司信息'][i]).split('/')[0]
        list4.append(gsmeg)
    else:
        list4.append(None)
list4 = list(filter(None, list4)) 
list6=[1]*len(list4)
dic={'企业业务': pd.Series(list4),
        '值': pd.Series(list6)}
cy=pd.DataFrame(dic)
c=cy.groupby('企业业务',as_index=False).count()
cysm=[int(value) for value in c['值'].values]
cygs=[str(value) for value in c['企业业务'].values]
list7 = c.values.tolist()
def wordcloud_base() -> WordCloud:
    c = (
        WordCloud(init_opts=opts.InitOpts(width='800px', height='500px',bg_color='rgba(128, 128, 128, 0.5)',
                               ))
        .add('' ,list7, word_size_range=[20,50],shape='diamond')
        .set_global_opts(title_opts=opts.TitleOpts(title='企业主营业务'))
    )
    return c
wordcloud_base().render_notebook()
import pandas as pd
from pyecharts.charts import Bar
from pyecharts.charts import Pie
from pyecharts import options as opts
from pyecharts.globals import ThemeType
bi=pd.read_excel(r'.//lieping.xlsx')#,encoding='gb18030')
part_interval = ["5K以下", "5K-10K", "10K-15K", "15K-20K", "20K-30K", "30K-50K", "50K以上"]
level1, level2, level3, level4, level5, level6, level7 = 0, 0, 0, 0, 0, 0, 0
#遍历salary，然后对数据进行划分，取中值为标准，薪资单位为 K
for i in bi['薪水']:
    if str(i) == 'nan' or "面议" in i:  # 面议的则不考虑
        pass
    elif i[-1] == "薪":    # 数据中的格式为：6-8k·13薪
        x = i.split("·")
        month = x[1][:-1]
        money = x[0].split("-")
        salary = (float(money[0]) + float(money[1][:-1])) / 2 * float(month) / 12
    else:
        # 正常单位的数据，格式为：10-20k
        x = i.split("-")
        salary = (float(x[0]) + float(x[1][:-1])) / 2

    if salary <= 5:
        level1 += 1
    if 5 < salary <= 10:
        level2 += 1
    elif 10 < salary <= 15:
        level3 += 1
    elif 15 < salary <= 20:
        level4 += 1
    elif 20 < salary <= 30:
        level5 += 1
    elif 30 < salary <= 50:
        level6 += 1
x_data = ["5K以下", "5K-10K", "10K-15K", "15K-20K", "20K-30K", "30K-50K"]
y_data = level1, level2, level3, level4, level5, level6
pie = (
    Pie(init_opts=opts.InitOpts(width='800px', height='500px',bg_color='rgba(128, 128, 128, 0.5)',
                               theme=ThemeType.DARK))  # 设置大小 
        .add(
        series_name="猎聘数据",
        data_pair=[list(z) for z in zip(x_data, y_data)],
        center=["50%", "55%"],   # 设置圆心所在位置
        radius=["30%", "70%"],   # 设置饼图的内圈和外圈差
                rosetype = True,    # 南丁格尔
        label_opts=opts.LabelOpts(
            position="outside",
            formatter=" {b|{b}: }{c}  {per|{d}%} ",  # 格式为：  {b|{b}: }{c}  {per|{d}%}      {b}:{d}%
            background_color="#aaa",  
            border_color="#aaa",
            border_width=1,
            border_radius=4,
            rich={
                "a": {"color": "#999", "lineHeight": 12, "align": "center"},
                "abg": {
                    "backgroundColor": "#e3e3e3",
                    "width": "100%",
                    "align": "right",
                    "height": 12,
                    "borderRadius": [4, 4, 0, 0],
                },
                "hr": {
                    "borderColor": "#aaa",
                    "width": "100%",
                    "borderWidth": 0.5,
                    "height": 0,
                },
                "b": {"fontSize": 12, "lineHeight": 15},
                "per": {
                    "color": "#eee",
                    "backgroundColor": "#334455",
                    "padding": [2, 4],
                    "borderRadius": 2,
                },
            },
        ),
    )
        .set_global_opts(
            title_opts=opts.TitleOpts(title="招聘岗位的薪酬分布", pos_left='left',title_textstyle_opts=(opts.TextStyleOpts(color='white')),),  # 设置title的位置
            legend_opts=opts.LegendOpts(pos_top="10%", orient="horizontal",type_ = 'scroll', background_color = "#CBCBCB")   # 设置「各薪水类别」所在位置
    )
        .set_series_opts(
            tooltip_opts=opts.TooltipOpts(
                trigger="item", formatter="{b}: {c} ({d}%)", # 设置鼠标悬停的提示信息
            )
    )
)
#pie.render("招聘岗位的薪酬分布.html")
pie.render_notebook()
#make_snapshot(snapshot, pie.render(), "薪酬分布.png", pixel_ratio=10

c41,c42,c43,c44=st.columns(4)
c31,c32,c33=st.columns([1.1,1,1.1])
#c21,c22=st.columns(2)
c41.metric("公司总数",len(bi))
c42.metric("平均工资",9000)
c43.metric("最高工资",60000)
c44.metric("最低工资",1000)

with c31:
    st_pyecharts(pie, theme='macarons',height='500px')
    st_pyecharts(wordcloud_base(),theme='dark', height='450px')

with c32:
    #option_province, map_province0,events_province=m3()
    st_echarts(options,map=map,events=events, height=1000,theme='dark')
with c33:
    st_pyecharts(grid,theme='dark', height='500px')
    st_pyecharts(bar,theme='dark', height='450px')

# with c21:
#     st_echarts(paleituo(nick_xse,nick_xse_cum),theme='dark')
# with c22:
#     st_echarts(price_sales(data1,data2),theme='dark')
