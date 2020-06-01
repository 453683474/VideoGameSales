import csv
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import leastsq


class Data_pre():
    def __init__(self):
        self.attributes = []  # 存储属性名
        self.column = []  # 按列存储原始数据
        self.length = 0  # 数据条数
        self.result = []  # 按行存储原始数据

        # 各属性按（属性值：[出现次数, 销售总额])存储
        self.gameNameMap = {}
        self.platformMap = {}
        self.yearMap = {}
        self.genreMap = {}
        self.publisherMap = {}

        # 各属性按（属性值：[出现次数, 销售总额])表示，按出现次数降序存储
        self.gameNameMap_count = []
        self.platformMap_count = []
        self.yearMap_count = []
        self.genreMap_count = []
        self.publisherMap_count = []

        # 各属性按（属性值：[出现次数, 销售总额])表示，按销售总额降序存储
        self.gameNameMap_sales = []
        self.platformMap_sales = []
        self.yearMap_sales = []
        self.genreMap_sales = []
        self.publisherMap_sales = []

        # 曲线拟合参数
        self.a = 0
        self.b = 0
        self.c = 0

    # 读取csv文件并初始化
    def read_csv(self, path):
        with open(path, 'r', encoding='mac_roman') as f:
            reader = csv.reader(f)
            self.result = list(reader)
            self.length = len(self.result) - 1
            self.attributes = self.result[0]
            for i in range(len(self.attributes)):
                ss = [row[i] for row in self.result]
                self.column.append(ss[1:])

    # 赋初值
    def init_map(self, tmp, i):
        if i == 1:
            self.gameNameMap = tmp
        elif i == 2:
            self.platformMap = tmp
        elif i == 3:
            self.yearMap = tmp
        elif i == 4:
            self.genreMap = tmp
        elif i == 5:
            self.publisherMap = tmp

    # 初始化，各属性按（属性值：[出现次数, 销售总额])存储
    def init(self, k):
        values = []
        map = {}
        for i in range(self.length):
            if self.column[k][i] not in values:
                values.append(self.column[k][i])
                if self.column[10][i] != "":
                    map[self.column[k][i]] = [1, float(self.column[10][i])]
                else:
                    map[self.column[k][i]] = [1, 0]
            else:
                if self.column[10][i] != "":
                    x = [1, float(self.column[10][i])]
                    map[self.column[k][i]] = [round(m + n, 2) for m, n in zip(map[self.column[k][i]], x)]
                else:
                    x = [1, 0]
                    map[self.column[k][i]] = [round(m + n, 2) for m, n in zip(map[self.column[k][i]], x)]
        return map

    # 各属性按（属性值：[出现次数, 销售总额])表示，按出现次数和总销售额降序排列并存储
    def sort(self):
        self.gameNameMap_count = sorted(self.gameNameMap.items(), key=lambda item: item[1][0], reverse=True)
        self.gameNameMap_sales = sorted(self.gameNameMap.items(), key=lambda item: item[1][1], reverse=True)
        self.platformMap_count = sorted(self.platformMap.items(), key=lambda item: item[1][0], reverse=True)
        self.platformMap_sales = sorted(self.platformMap.items(), key=lambda item: item[1][1], reverse=True)
        self.yearMap_count = sorted(self.yearMap.items(), key=lambda item: item[1][0], reverse=True)
        self.yearMap_sales = sorted(self.yearMap.items(), key=lambda item: item[1][1], reverse=True)
        self.genreMap_count = sorted(self.genreMap.items(), key=lambda item: item[1][0], reverse=True)
        self.genreMap_sales = sorted(self.genreMap.items(), key=lambda item: item[1][1], reverse=True)
        self.publisherMap_count = sorted(self.publisherMap.items(), key=lambda item: item[1][0], reverse=True)
        self.publisherMap_sales = sorted(self.publisherMap.items(), key=lambda item: item[1][1], reverse=True)
        print(self.gameNameMap_count)
        print(self.gameNameMap_sales)
        print(self.platformMap_count)
        print(self.platformMap_sales)
        print(self.yearMap_count)
        print(self.yearMap_sales)
        print(self.genreMap_count)
        print(self.genreMap_sales)
        print(self.publisherMap_count)
        print(self.publisherMap_sales)
        print()
        print()

    # 输出受欢迎的游戏、类型、发布平台、发行人
    def print_result(self):
        print("最受欢迎的游戏top15为：")
        for i, ss in zip(range(15), self.gameNameMap_sales[0:15]):
            print(str(i + 1) + ". " + ss[0] + ":销售额为" + str(ss[1][1]))
        print()

        print("考虑游戏类型出现次数，最受欢迎的游戏类型top10为：")
        for i, ss in zip(range(15), self.genreMap_count[0:10]):
            print(str(i + 1) + ". " + ss[0] + ":出现次数为" + str(ss[1][0]))
        print("考虑游戏类型销售总额，最受欢迎的游戏类型top10为：")
        for i, ss in zip(range(15), self.genreMap_sales[0:10]):
            print(str(i + 1) + ". " + ss[0] + ":销售总额为" + str(ss[1][1]))
        print()

        print("考虑发布平台出现次数，最受欢迎的发布平台top15为：")
        for i, ss in zip(range(15), self.platformMap_count[0:15]):
            print(str(i + 1) + ". " + ss[0] + ":出现次数为" + str(ss[1][0]))
        print("考虑发布平台销售总额，最受欢迎的发布平台top15为：")
        for i, ss in zip(range(15), self.platformMap_sales[0:15]):
            print(str(i + 1) + ". " + ss[0] + ":销售总额为" + str(ss[1][1]))
        print()

        print("考虑发行人出现次数，最受欢迎的发行人top15为：")
        for i, ss in zip(range(15), self.publisherMap_count[0:15]):
            print(str(i + 1) + ". " + ss[0] + ":出现次数为" + str(ss[1][0]))
        print("考虑发行人销售总额，最受欢迎的发行人top15为：")
        for i, ss in zip(range(15), self.publisherMap_sales[0:15]):
            print(str(i + 1) + ". " + ss[0] + ":销售总额为" + str(ss[1][1]))
        print()

    # 二次函数的标准形式
    def func(self, params, x):
        a, b, c = params
        return a * x * x + b * x + c

    def error(self, params, x, y):
        return self.func(params, x) - y

    # 二次曲线拟合
    def matching(self):
        x = []
        y = []
        length = len(self.yearMap_sales)
        for i in range(length - 3):
            if self.yearMap_sales[i][0] != "N/A":
                if 2011 >= int(self.yearMap_sales[i][0]) >= 1980:
                    x.append(int(self.yearMap_sales[i][0]))
                    y.append(self.yearMap_sales[i][1][1])
        X = np.array(x)
        Y = np.array(y)
        p0 = [10, 10, 10]
        Para = leastsq(self.error, p0, args=(X, Y))
        a, b, c = Para[0]
        self.a = a
        self.b = b
        self.c = c
        print("求解的曲线是:")
        print("y=" + str(round(a, 2)) + "x*x+" + str(round(b, 2)) + "x+" + str(c))

        plt.figure(figsize=(8, 6))
        plt.scatter(X, Y, color="green", label="sample data", linewidth=2)

        #   画拟合直线
        x = np.linspace(1980, 2011, 100)
        y = a * x * x + b * x + c
        plt.plot(x, y, color="red", label="solution line", linewidth=2)
        plt.legend()
        plt.show()

    # 预测指定年份电子游戏销售额
    def predict(self, year):
        ans = round(self.a * year *year + self.b * year + self.c, 2)
        print(str(year) + "年的电子游戏销售额为：" + str(ans))

    def autolabel(self, rects):
        for rect in rects:
            height = rect.get_height()
            plt.text(rect.get_x() + rect.get_width() / 2. - 0.2, 1.03 * height, '%s' % float(height))

    # 可视化
    def view(self, p1, p2, k):
        plt.figure(figsize=(20, 11))
        a = plt.bar(np.arange(len(p1)), p2, tick_label=list(p1))
        # plt.legend()
        self.autolabel(a)
        # 销售额最高的20个游戏
        if k == 1:
            plt.xlabel("game_name")
            plt.ylabel('sales')
            plt.title('top20_favorite_games')
        elif k == 2:
            plt.xlabel("platform")
            plt.ylabel('count')
            plt.title('top20_occurrence_platform')
        elif k == 3:
            plt.xlabel("platform")
            plt.ylabel('sales')
            plt.title('top20_highest_sales_platform')
        elif k == 4:
            plt.xlabel("year")
            plt.ylabel('count')
            plt.title('top20_occurrence_year')
        elif k == 5:
            plt.xlabel("year")
            plt.ylabel('sales')
            plt.title('top20_highest_sales_year')
        elif k == 6:
            plt.xlabel("genre")
            plt.ylabel('count')
            plt.title('top10_occurrence_genre')
        elif k == 7:
            plt.xlabel("genre")
            plt.ylabel('sales')
            plt.title('top10_highest_sales_genre')
        elif k == 8:
            plt.xlabel("publisher")
            plt.ylabel('count')
            plt.title('top20_occurrence_publisher')
        elif k == 9:
            plt.xlabel("publisher")
            plt.ylabel('sales')
            plt.title('top20_highest_sales_publisher')

        plt.xticks(rotation=-30)
        plt.show()


data = Data_pre()
path = "D:/data/vgsales.csv"
data.read_csv(path)
for i in range(1, 6):
    tmp = data.init(i)
    data.init_map(tmp, i)
data.sort()
# print(data.yearMap_count)
# # print(len(data.yearMap_sales))
data.print_result()
data.matching()
for i in range(1980, 2021):
    data.predict(i)

x1 = [ss[0] for ss in data.gameNameMap_sales[0:20]]
y1 = [ss[1][1] for ss in data.gameNameMap_sales[0:20]]
x2 = [ss[0] for ss in data.platformMap_sales[0:20]]
y2_1 = [ss[1][0] for ss in data.gameNameMap_count[0:20]]
y2_2 = [ss[1][1] for ss in data.gameNameMap_sales[0:20]]
x3 = [ss[0] for ss in data.platformMap_sales[0:20]]
y3_1 = [ss[1][0] for ss in data.yearMap_count[0:20]]
y3_2 = [ss[1][1] for ss in data.yearMap_sales[0:20]]
x4 = [ss[0] for ss in data.genreMap_sales[0:10]]
y4_1 = [ss[1][0] for ss in data.genreMap_count[0:10]]
y4_2 = [ss[1][1] for ss in data.genreMap_sales[0:10]]
x5 = [ss[0] for ss in data.publisherMap_sales[0:20]]
y5_1 = [ss[1][0] for ss in data.publisherMap_count[0:20]]
y5_2 = [ss[1][1] for ss in data.publisherMap_sales[0:20]]
data.view(x1, y1, 1)
data.view(x2, y2_1, 2)
data.view(x2, y2_2, 3)
data.view(x3, y3_1, 4)
data.view(x3, y3_2, 5)
data.view(x4, y4_1, 6)
data.view(x4, y4_2, 7)
data.view(x5, y5_1, 8)
data.view(x5, y5_2, 9)
