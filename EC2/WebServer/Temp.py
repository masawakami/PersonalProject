import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

#matplotlib.pyplot.figure(figsize=(横インチ, 縦インチ), dpi=解像度, facecolor=グラフの余白色, edgecolor=’k’)
fig = plt.figure(figsize=(10, 6))
plt1 = fig.add_subplot()

# csvを出力。最終行からn列まで。
df = pd.read_csv('/home/ec2-user/S3/environment_data.csv')
df1 = df.tail(144)

# Date,Temperature,Humidity列の値を抽出
data_x = df1[df1.columns[0]]
data_y1 = df1[df1.columns[1]]
data_y2 = df1[df1.columns[2]]

# pltにplt2を関連付ける
plt2 = plt.twinx()

# x,y1,y2軸のラベルを指定
plt1.set_xlabel('Date', fontsize=16)
plt1.set_ylabel('Temperture(C)', fontsize=16)
plt2.set_ylabel('Humidity(%)', fontsize=16)

plt1.plot(data_x, data_y1, color = 'red', linestyle='solid', label = 'Temperture(C)')
plt2.plot(data_x, data_y2, color = 'blue', linestyle='solid', label = 'Humidity(%)')

# プロット数
locator = mdates.DayLocator(interval=14)
plt1.xaxis.set_major_locator(locator)

#x軸ラベルの角度
#plt1.autofmt_xdate(rotation=45)
#plt1.set_xticklabels(data_x, rotation=45, ha='right')
plt1.xaxis.set_tick_params(rotation=45)

#凡例
h1, l1 = plt1.get_legend_handles_labels()
h2, l2 = plt2.get_legend_handles_labels()
plt1.legend(h1+h2, l1+l2 ,loc='upper left')

#plt.show()
# ここにグラフを描画してファイルに保存する処理
plt.tight_layout()
plt.savefig("/home/ec2-user/WebServer/templates/images/Temp.jpg") # この行を追記
