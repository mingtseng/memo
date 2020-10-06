import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
from pylab import mpl

pd.set_option('display.unicode.ambiguous_as_wide', True)
pd.set_option('display.unicode.east_asian_width', True)
pd.set_option('display.width', 400)  # 设置打印宽度
pd.set_option('expand_frame_repr', False)  # 数据超过总宽度后是否折叠显示
# 导入数据
file_name = '朝阳医院2018年销售数据.xlsx'

# 使用ExcelFile()时需要传入目标excel文件所在路径及文件名称
xls = pd.ExcelFile(file_name)

# 使用parse()可以根据传入的sheet名称来提取对应的表格信息
dataDF = xls.parse('Sheet1', dtype='object')

# 输入前五行数据
print(dataDF.head())

# 使用sheet_names来查看当前表格中包含的所有sheet名称(按顺序)
print('\n', xls.sheet_names)

# 查看数据基本信息
# 查看数据几行几列
print('\n', dataDF.shape)

# 查看索引
print('\n', dataDF.index)

# 查看每一列的列表头内容
print('\n', dataDF.columns)

# 查看每一列数据统计数目
print('\n', dataDF.count())

# 数据清洗: 选择子集、列名重命名、缺失数据处理、数据类型转换、数据排序及异常值处理

# (1) 选择子集

# (2) 列重命名
dataDF.rename(columns={'购药时间': '销售时间'}, inplace=True)
print('\n', dataDF.head())

# (3) 缺失值处理(删除含有缺失数据的记录或者利用算法去补全缺失数据)
print('\n删除缺失值前:', dataDF.shape)

# 使用info查看数据信息
print('\n', dataDF.info())

# 删除缺失值
dataDF = dataDF.dropna(subset=['销售时间', '社保卡号'], how='any')
print('\n删除缺失值后', dataDF.shape)
print(dataDF.info())

# (4) 数据类型转换
dataDF['销售数量'] = dataDF['销售数量'].astype('float')
dataDF['应收金额'] = dataDF['应收金额'].astype('float')
dataDF['实收金额'] = dataDF['实收金额'].astype('float')
print(dataDF.dtypes)

'''
定义函数: 分割销售日期, 提取销售日期'
输入: timeColSer 销售时间这一列, Series数据类型, 例'2018-01-01 星期五'
输出: 分割后的时间, 返回Series数据类型, 例'2018-01-01
'''
def splitSaleTime(timeColSer):
    timeList = []

    for value in timeColSer:
        dateStr = value.split(' ')[0]
        timeList.append(dateStr)
    timeSer = pd.Series(timeList)  # 将列表转换为一维数据Series类型
    return timeSer

# 获取'销售时间'这一列
timeSeries = dataDF.loc[:, '销售时间']

# 对字符串进行分割, 提取销售日期
dateSeries = splitSaleTime(timeSeries)

# 修改销售时间这一列的值
dataDF.loc[:, '销售时间'] = dateSeries
print('\n', dataDF.head())

'''
数据类型转换: 字符串转换为日期, 把切割后的日期转为时间格式, 为后面的数据统计:
'''
# errors='coerce' 如果原始数据不符合日期的格式, 转换后的值为空值NaT
dataDF.loc[:, '销售时间'] = pd.to_datetime(dataDF.loc[:, '销售时间'], format='%Y-%m-%d', errors='coerce')
print('\n', dataDF.dtypes)

# 查看每列有多少行被转换后是空值NaT
print('\n', dataDF.isnull().sum())

'''
转换日期过程中不符合日期格式的数值会被转换为空值
删除含有NaT的空行, 此时dataDF或Series类型的数据不再是连续的索引, 可以使用reset_index()重置索引
'''
dataDF = dataDF.dropna(subset=['销售时间', '社保卡号'], how='any')
dataDF = dataDF.reset_index(drop=True)
print('\n', dataDF.info())

# (5) 数据排序
# 排序之后索引会被打乱, 所以也需要重置一下索引
dataDF = dataDF.sort_values(by='销售时间', ascending=True)
dataDF = dataDF.reset_index(drop=True)
print('\n', dataDF.head())

# (6) 异常值处理

# 查看描述统计信息
print('\n', dataDF.describe())

# 将'销售数量'这一列小于0的数据排除掉
pop = dataDF.loc[:, '销售数量'] > 0
print('\n', pop)
dataDF = dataDF.loc[pop, :]
print('\n', dataDF.describe())


# 计算相应的业务指标, 并用可视化的方式呈现结果

# (1) 业务指标1: 月均消费次数
# 月均消费次数 = 总消费次数/月份数 (同一天内, 同一个人所有消费算作一次消费)
# 计算总消费次数
# 删除重复数据
kpil_Df = dataDF.drop_duplicates(subset=['销售时间', '社保卡号'])
print('\n', kpil_Df.shape)
totalI = kpil_Df.shape[0]
print('\n总消费次数 =', totalI)

# 计算月份数
# 按销售时间升序排序
kpil_Df = kpil_Df.sort_values(by='销售时间', ascending=True)
# 重置索引
kpil_Df = kpil_Df.reset_index(drop=True)
# 获取时间范围
startTime = kpil_Df.loc[0, '销售时间']
endTime = kpil_Df.loc[totalI-1, '销售时间']
# 计算月份
# 天数
daysI = (endTime - startTime).days
mounthI = daysI // 30
print('月份数 = ', mounthI)

# 月平均消费次数
kpil_1 = totalI // mounthI
print('业务指标1: 月均消费次数 =', kpil_1)

# (2) 月均消费金额
# 客单价 = 总消费金额 / 月份数
totalMoneyF = dataDF.loc[:, '实收金额'].sum()
mounthMoney = totalMoneyF // mounthI
print('\n业务指标2: 月均消费金额 =', mounthMoney)

# (3) 客单价
# 客单价 = 总消费金额 / 总消费次数
pct = totalMoneyF / totalI
print('\n业务指标3: 客单价 =', pct)

# (4) 消费趋势

# a. 分析日消费金额趋势

# 画圈时用于显示中文字符
mpl.rcParams['font.sans-serif'] = ['SimHei']

# 在操作之前先复制一份数据, 防止影响清洗后的数据
groupDF = dataDF

# 将'销售时间'设置为index
groupDF.index = groupDF['销售时间']
print('\n', groupDF.head())

# 按'销售时间'分组对'销售数量'、'应收金额'、'实收金额'求和
gb = groupDF.groupby(groupDF.index)
print('\n', gb)
dayDF = gb.sum()
print('\n', dayDF)

# 画图
plt.plot(dayDF['实收金额'])
plt.title('日消费金额')
plt.xlabel('时间')
plt.ylabel('实收金额')
a = plt.show()
print(a)

# b. 分析月消费金额
# 将销售时间聚合按月分组
gb = groupDF.groupby(groupDF.index.month)
print('\n', gb)
monthDF = gb.sum()
print('\n', monthDF)

# 画图
plt.plot(monthDF['实收金额'])
plt.title('月消费金额')
plt.xlabel('时间')
plt.ylabel('实收金额')
b = plt.show()
print(b)

# c. 分析药品销售情况
# 聚合统计各种药品数量
medicine = groupDF[['商品名称', '销售数量']]
bk = medicine.groupby('商品名称')[['销售数量']].sum()
print('\n', bk)

# 对销售药品数量按降序排序
bk = bk.sort_values(by='销售数量', ascending=False)
print('\n', bk.head())

# 截取销售数量最多的前十种药品, 并用条形图展示结果
top_medcine = bk.iloc[:10, :]
print('\n', top_medcine)

# 画图
top_medcine.plot(kind='bar')
plt.title('销售前十的药品')
plt.xlabel('药品')
plt.ylabel('数量')
c = plt.show()
print(c)

# d. 每天的消费金额分布情况

# 横轴为时间, 纵轴为实收金额, 画散点图
plt.scatter(dataDF['销售时间'], dataDF['实收金额'])
plt.title('日销售金额')
plt.xlabel('时间')
plt.ylabel('实收金额')
d = plt.show()
print(d)




