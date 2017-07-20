#coding: utf-8

'''
xlsxwriter包的Chart类
Chart类实现生成多种xls图形的，通过add_chart方法，通过{type,'图表类型'}字典指定图表类型
chart=workbook.add-chart({type,'column'})创建一个柱形图
更大类型说明
area:创建一个面积样式的图表
bar:创建一个条形样式的图表
column:创建一个柱形样式的图表
line:创建一个线条样式的图表
pie:创建一个饼图样式的图表
stock:创建一个股票样式的图表
radar:创建一个雷达样式的图表
'''
import xlsxwriter


workbook = xlsxwriter.Workbook('chart.xlsx')#创建工作表
worksheet = workbook.add_worksheet()#创建一个工作表对象

chart = workbook.add_chart({'type': 'column'})#创建一个图表对象

#定义表头
title = [u'业务名称',u'星期一',u'星期二',u'星期三',u'星期四',u'星期五',u'星期六',u'星期日',u'平均流量']
buname= [u'业务官网',u'新闻中心',u'购物频道',u'体育频道',u'亲子频道']
#定义五频道一周7天的流量数据列表
data = [
    [150,152,158,149,155,145,148],
    [89,88,95,93,98,100,99],
    [201,200,198,175,170,198,195],
    [75,77,78,78,74,70,79],
    [88,85,87,90,93,88,84],
]
format=workbook.add_format()#定义format格式对象
format.set_border(1)#定义format对象单元格边框加粗（1像素）的格式

format_title=workbook.add_format()#定义format_title格式对象
format_title.set_border(1)#单元格边框加粗
format_title.set_bg_color('#cccccc')
format_title.set_align('center')
format_title.set_bold()#单元格内容加粗的格式

format_ave=workbook.add_format()
format_ave.set_border(1)
format_ave.set_num_format('0.00')

#下面以行列方式将标题，业务名称，流量数据写入起初单元格，同时引用不同的格式对象
worksheet.write_row('A1',title,format_title)
worksheet.write_column('A2', buname,format)
worksheet.write_row('B2', data[0],format)
worksheet.write_row('B3', data[1],format)
worksheet.write_row('B4', data[2],format)
worksheet.write_row('B5', data[3],format)
worksheet.write_row('B6', data[4],format)

#定义图表数据函数
def chart_series(cur_row):
    worksheet.write_formula('I'+cur_row, \
     '=AVERAGE(B'+cur_row+':H'+cur_row+')',format_ave)#计算(AVERAGE函数)频道的周平均流量
    chart.add_series({
        'categories': '=Sheet1!$B$1:$H$1',#将星期一到星期日作为图表X轴
        'values':     '=Sheet1!$B$'+cur_row+':$H$'+cur_row,#频道一周所有数据作为数据区域
        'line':       {'color': 'black'},#线条颜色定义为black（黑色）
        'name':    '=Sheet1!$A$'+cur_row,#引用业务名称为图例项目
    })

for row in range(2, 7):#数据域以第2-6进行图表数据系列函数调用
    chart_series(str(row))

#chart.set_table()#设置X轴表格格式，
#chart.set_style(30)#设置图表样式
chart.set_size({'width': 577, 'height': 287})#设置图表大小
chart.set_title ({'name': u'业务流量周报图表'})#设置图表（上方）大标题
chart.set_y_axis({'name': 'Mb/s'})#设置Y轴（左侧）小标题

worksheet.insert_chart('A8', chart)#在A8单元格插入图表
workbook.close()#关闭文档
