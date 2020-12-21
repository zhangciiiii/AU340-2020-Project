import csv
import os 
threshold = 13
length_threshold = 50 #每个梯形的最小长度
tolerate_error = 3
min_threshold = 0.5 #找梯形下降到0的容忍值

file_list = ['Datalog_2019_12_10_14_20_33','Datalog_2019_12_10_14_59_07','Datalog_2019_12_10_15_07_25','Datalog_2019_12_10_15_12_00',
           'Datalog_2019_12_10_15_17_33','Datalog_2019_12_10_15_22_40','Datalog_2019_12_10_15_45_19','Datalog_2019_12_10_16_07_01',
           'Datalog_2019_12_10_16_39_44']
    


def Analysis(file_name):
    nums = len(os.listdir('./Data_Process/'+file_name))
    for num in range(0,nums):
        #读取轴速度
        data = []
        count = 0
        filename =  './Data_Process/' + file_name + '/' + str(num+1) + ".csv"
        with open(filename, 'r') as f:
            reader = csv.reader(f)
            for i in reader:
                count += 1
                if(count==1):
                    continue
                data.append(float(i[4]))

        #取绝对值
        for i in range(len(data)):
            data[i] = abs(data[i])

        #寻找梯形上行
        start_array = []
        end_array = []

        flag = False
        for i in range(len(data)):
            if(flag and data[i]<threshold):
                flag = False
                if(i-start_array[-1]>length_threshold):
                    end_array.append(i-1)
                else:
                    start_array.pop()
            elif(not flag and data[i]>threshold):
                flag = True
                start_array.append(i)
        if(flag):
            start_array.pop()

        #判断梯形的两腰是否完全
        flag = False
        for start, end in zip(start_array, end_array):
            while(start>=0 and data[start]>min_threshold):
                start -= 1
            if(start<0):
                continue
            while(end<len(data) and data[end]>min_threshold):
                end += 1
            if(end>=len(data)):
                continue
            flag = True
            break

        print(filename, ' is ',flag)

for file_name in file_list:
    print("Start to Analyze "+file_name)
    Analysis(file_name)
