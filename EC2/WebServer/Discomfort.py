import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

#matplotlib.pyplot.figure(figsize=(横インチ, 縦インチ), dpi=解像度, facecolor=グラフの余白色, edgecolor=’k’)
plt.figure(figsize=(10, 6))
#plt = fig.add_subplot()

# csvを出力。最終行からn列まで。
df = pd.read_csv('/home/ec2-user/S3/environment_data.csv')
df1 = df.tail(144)

data_x = df1[df1.columns[0]]
data_y = df1[df1.columns[3]]

plt.xlabel('Date', fontsize=16)
plt.ylabel('Discomfort', fontsize=16)

plt.plot(data_x, data_y, color = 'green', linestyle='solid', label = 'Discomfort')

# プロット数指定
plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=14))

#x軸ラベルの角度
plt.xticks(rotation=45)

#plt.show()
# ここにグラフを描画してファイルに保存する処理
plt.tight_layout()
plt.savefig("/home/ec2-user/WebServer/templates/images/Discomfort.jpg") # この行を追記
