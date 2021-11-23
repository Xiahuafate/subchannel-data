from mpl_toolkits.axisartist.parasite_axes import HostAxes, ParasiteAxes
import matplotlib.pyplot as plt
import math
import numpy as np
import pylab
import re
import os
#这是一个用于画图的函数，输出的变量就是你要画图的变量、title（这个会作为这张图的名字保存下来）
def DataPlot(DISTANCE,EQUIL,VOID,MASS_FLUX,W1_13,title):
    fig = plt.figure(dpi=300,figsize=(24,24))#创建一块画布
    ax_void = fig.add_subplot(111)#分割画布
    ax_void = HostAxes(fig, [0, 0, 0.9, 0.9])  #用[left左, bottom下, weight宽, height高]的方式定义axes，
                                              #0 <= l,b,w,h <= 1   
    ax_axial = ParasiteAxes(ax_void, sharex=ax_void)#寄生附加轴，共享x
    ax_cross = ParasiteAxes(ax_void, sharex=ax_void)
    ax_void.parasites.append(ax_axial)#附加轴
    ax_void.parasites.append(ax_cross)
    ax_void.axis['right'].set_visible(False)#ax_void的不可见右轴
    ax_void.axis['top'].set_visible(False)
    ax_axial.axis['right'].set_visible(True)
    ax_axial.axis['right'].major_ticklabels.set_visible(True)
    ax_axial.axis['right'].label.set_visible(True)
    ax_void.set_xlabel('Distance[mm]',fontsize=500)#设置轴的标签及其字体大小
    ax_void.set_ylabel('Void Fraction',fontsize=50)
    ax_axial.set_ylabel('Axial Flow[kg/(m^2·s)]',fontsize=50)
    ax_cross.set_ylabel('Cross Flow[kg/(m·s)]',fontsize=50)
    cross_axisline = ax_cross.get_grid_helper().new_fixed_axis#创建新坐标轴
    ax_cross.axis['right2'] = cross_axisline(loc='right', axes=ax_cross, offset=(80,0))
    fig.add_axes(ax_void)
    
    ax_void.plot(DISTANCE[0],VOID,color="g",linestyle="-",marker=".",label="Void Fraction",linewidth=2)#开始画图,线条颜色、点画线、标记、宽度
    ax_void.plot(DISTANCE[0],EQUIL,color="b",linestyle="-",marker=".",label="Equil Fraction",linewidth=2)
    ax_axial.plot(DISTANCE[0], MASS_FLUX, color='r',linestyle="-",marker=".",label="Axial Flow",linewidth=2)
    ax_cross.plot(DISTANCE[1], W1_13, color='m',linestyle="-",marker=".",label=" Cross Flow between C1-13",linewidth=2)

    ax_void.legend(loc='upper left')  # 绘制图例，plot()中的label值，loc为图例位置，设置在右上方，（右下方为lower right）
    ax_void.legend(fontsize=50)# 设置图例字体大小
    ax_axial.axis['right'].label.set_color('red')#轴名称，刻度值的颜色
    ax_cross.axis['right2'].label.set_color('magenta')
    #这是我修改了的代码
    ax_void.set_xticks(DISTANCE[0][::5],fontsize=50)#设置坐标轴刻度字体大小
    ax_void.set_yticks(VOID[::5],fontsize=50)#VODI[::5]的含义是这个list从第0个数到最后一个数，每隔5个数取一个数出来做坐标轴
    ax_axial.set_yticks(EQUIL[::5],fontsize=50)
    ax_cross.set_yticks(W1_13[::5],fontsize=50)
    #这是我修改的代码，参考来源：https://www.delftstack.com/zh/howto/matplotlib/how-to-set-the-figure-title-and-axes-labels-font-size-in-matplotlib/
    parameters = {'axes.labelsize': 50,'xtick.labelsize':20,"ytick.labelsize":20,
          'axes.titlesize': 50}
    plt.rcParams.update(parameters)
    #通过修改了plt的全局变量来改变尺寸，但是我回答不了，为什么set_xlabel改变不了字体的大小
    ax_void.set_title(title,fontsize=50)#设置标题 
    fig.savefig(title+".jpg",bbox_inches = 'tight')#保存刻度
    plt.close()#关闭画布

#这是一个用来读取你的数据的程序，传入的参数为你的所有数据
def DataGet(lines):
    b='CHANNEL   1'
    c='CHANNEL  24'#第一个查找字符
    chanels =[b,c]
    title = [b,c]#由于title就是图片保存的名字，因此必须不同
    DISTANCE1 = []#为数据创建存储空间
    EQUIL = []
    VOID =[]
    MASS_FLUX =[]
    for i in range(len(chanels)):#还是在创建存储空间
         DISTANCE1.append([])
         EQUIL.append([])
         VOID.append([])
         MASS_FLUX.append([])
    #遍历数据
    #下面当面讲过了，不赘叙
    for i in range(len(lines)):#i为行数，j为列数
        for j in range(len(chanels)):
            if chanels[j] in lines[i]:
                data_line = i+4
                while(1):
                    line =lines[data_line]
                    line =line.strip("\n").split()#去掉换行符、去掉空格
                    DISTANCE1[j].append(float(line[0]))#在列表中添加新值，将参数添加到列表末尾
                    EQUIL[j].append(float(line[5]))
                    VOID[j].append(float(line[6]))
                    MASS_FLUX[j].append(float(line[9])/0.0036)
                    data_line = data_line + 1
                    line = lines[data_line].strip("\n").split()
                    try:
                        temp = float(line[0])#结束标志，若此行第一个元素不是数字，结束迭代
                    except:
                        break                #不用看数据要多少行
    #处理横流数据
    d='W(  1, 13)'
    W =[d]#第二种搜索标签
    DISTANCE2 = []
    W1_13 =[]
    for i in range(len(chanels)):
        DISTANCE2.append([])
        W1_13.append([])
    for i in range(len(lines)):
        for j in range(len(W)):
            if W[j] in lines[i]:
                data_line = i+1
                while(1):
                    line =lines[data_line]
                    line =line.strip("\n").split()
                    DISTANCE2[j].append(float(line[0]))
                    W1_13[j].append(float(line[4+2]))
                    data_line = data_line + 1
                    line = lines[data_line].strip("\n").split()
                    try:
                        temp = float(line[0])
                    except:
                        break
    #因为前面你的x轴有113个数值，下面的w只有112个数值，我删除了最后一个
    # DISTANCE2[0].pop(0)
    #画图
    DISTANCE = [DISTANCE1[0],DISTANCE2[0]]
    for i in range(len(EQUIL)):
        DataPlot(DISTANCE,EQUIL[i],VOID[i],MASS_FLUX[i],W1_13[0],title[i])
#主函数，入口在这里
def main():
    #读文件
    filename = "2.7-2100-22.2-474.txt"
    f = open(filename,"r")
    lines = f.readlines()
    f.close()
    #调用子函数
    DataGet(lines)
#进入主函数
main()

#小知识
# 1.建议打包成exe，然后写脚本运行，如果你的重复性很高，而运行python的脚本不太方便的话
# 2.我去看一下vs code 怎么调试来着，可以学一手调试
# 3.我看你的想法是改变画图的结构，建议改DataPlot子函数，如果觉得画图难看，也在这个子函数里面做修改
# 4.如果我的数据处理错了，建议查看类似于“EQUIL[j].append(float(line[5+2]))”这种代码中line[]中间的那种数字，从左往右，从0开始计数
