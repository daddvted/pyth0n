import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import matplotlib.patches as mp
import numpy as np

# Generate data
data = pd.DataFrame([['第一季度', 80],
                     ['第二季度', 130],
                     ['第三季度', 115],
                     ['第四季度', 180]], columns=["季度","销量"])

main_color = 'green'

# 设置中文字体
# Linux
font = fm.FontProperties(fname="/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc")
# Windows
# font = fm.FontProperties(fname="C:\Windows\Fonts\simhei.ttf")


fig, ax = plt.subplots()

# 季度为 y 轴，销量为 y 轴 
ax.barh(data['季度'], data['销量'], color=main_color)

# 设置 y 轴的标签，并垂直显示
#ax.set_xticklabels(data['季度'], fontproperties=font, rotation='vertical')
ax.set_yticklabels(data['季度'], fontproperties=font)
ax.set_xlabel("单位：万元", fontproperties=font)

# 设置图例名，颜色
red_patch = mp.Patch(color=main_color, label="销量")
ax.legend(handles=[red_patch], prop=font)

fig.tight_layout()
# 显示图片
plt.show()
