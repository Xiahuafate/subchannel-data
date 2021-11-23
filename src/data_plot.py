import matplotlib.pyplot as plt
import math
import numpy as np
import pylab
import re
import os
#这是一个用于画图的函数，输出的变量就是你要画图的变量还有x、y轴的名字、你图的title（这个会作为这张图的名字保存下来）
def DataPlot(DISTANCE,EQUIL,VOID,MASS_FLUX,title,x_label,y1_label,y2_label):
    fig = plt.figure()#创建一块画布
    ax1 = fig.add_subplot(111)#分割画布
    ax1.plot(DISTANCE,EQUIL,"b")#开始画图
    ax1.plot(DISTANCE,VOID,"g")
    ax1.set_ylabel(y1_label)#设置第一个y的y标签
    ax1.set_title(title)#设置标题
    ax2 = ax1.twinx() #第二个y轴
    ax2.plot(DISTANCE, MASS_FLUX, 'r')
    ax2.set_ylabel(y2_label)#设置第二个y的y标签
    ax2.set_xlabel(x_label)#设置x标签
    fig.savefig(title+".jpg")#保存
    plt.close()#关闭画布

#这是一个用来读取你的数据的程序，传入的参数为你的所有数据
def DataGet(lines):
    b='CHANNEL   1'
    c='CHANNEL  24'#第一个查找字符
    chanels =[b,c]
    title = [b,c]#由于title就是图片保存的名字，因此必须不同
    x_label = [b,c]#x轴的标签,要画多少图写多少个
    y1_label = [b,c]#y1轴标签
    y2_label = [b,c]#y2轴标签
    DISTANCE = []#为数据创建存储空间
    EQUIL = []
    VOID =[]
    MASS_FLUX =[]
    for i in range(len(chanels)):#还是在创建存储空间
         DISTANCE.append([])
         EQUIL.append([])
         VOID.append([])
         MASS_FLUX.append([])
    #遍历数据
    #下面当面讲过了，不赘叙
    for i in range(len(lines)):
        for j in range(len(chanels)):
            if chanels[j] in lines[i]:
                data_line = i+4
                while(1):
                    line =lines[data_line]
                    line =line.strip("\n").split()
                    DISTANCE[j].append(float(line[0]))
                    EQUIL[j].append(float(line[5]))
                    VOID[j].append(float(line[6]))
                    MASS_FLUX[j].append(float(line[9])/0.0036)
                    data_line = data_line + 1
                    line = lines[data_line].strip("\n").split()
                    try:
                        temp = float(line[0])
                    except:
                        break
    #画图
    for i in range(len(DISTANCE)):
        DataPlot(DISTANCE[i],EQUIL[i],VOID[i],MASS_FLUX[i],title[i],x_label[i],y1_label[i],y2_label[i])
    
    d='W(  1,  2)'
    e='W(  1, 13)'
    f='W( 13, 14)'
    W =[d,f]#第二种搜索标签
    title = [d,"aaaa"]
    x_label = [b,c]
    y1_label = [b,c]
    y2_label = [b,c]
    temp_distance = DISTANCE[0]
    DISTANCE = []
    EQUIL = []
    VOID =[]
    MASS_FLUX =[]
    for i in range(len(chanels)):
        DISTANCE.append(temp_distance)
        EQUIL.append([])
        VOID.append([])
        MASS_FLUX.append([])
    for i in range(len(lines)):
        for j in range(len(W)):
            if W[j] in lines[i]:
                data_line = i+1
                while(1):
                    line =lines[data_line]
                    line =line.strip("\n").split()
                    EQUIL[j].append(float(line[5+2]))
                    VOID[j].append(float(line[6+2]))
                    MASS_FLUX[j].append(float(line[9+2])/0.0036)
                    data_line = data_line + 1
                    line = lines[data_line].strip("\n").split()
                    try:
                        temp = float(line[0])
                    except:
                        break
    #因为前面你的x轴有113个数值，下面的w只有112个数值，我删除了最后一个
    DISTANCE[0].pop(0)
    #画图
    for i in range(len(DISTANCE)):
        DataPlot(DISTANCE[i],EQUIL[i],VOID[i],MASS_FLUX[i],title[i],x_label[i],y1_label[i],y2_label[i])
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
