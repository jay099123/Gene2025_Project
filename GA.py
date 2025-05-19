import numpy as np
import pandas as pd

# 讀取原始資料
df = pd.read_csv("total.csv", encoding="utf-8-sig")

# 把 price 欄位的逗號去掉並轉成 int
# df['price'] = df['price'].astype(str).str.replace(',', '').astype(int)

# 取得各欄最大最小值
area_min, area_max = df['area'].min(), df['area'].max()
price_min, price_max = df['price'].min(), df['price'].max()
dis_min, dis_max = df['distance(km)'].min(), df['distance(km)'].max()
# dis_min, dis_max = df['distance_std'].min(), df['distance_std'].max()  # 若 distance 是原始值就用 'dis'，若已經是 std 就用 'distance_std'

# 使用者輸入並自動轉換
while True:
    z1 = input("是否設坪數限制？(y/n): ")
    if z1 == 'y':
        while True:
            area_upper = input("請輸入坪數上限：")
            if area_upper.isdigit() and int(area_upper) >= 0:
                area_upper = int(area_upper)
                area_upper_std = (area_upper - area_min) / (area_max - area_min)
                break
            else:
                print("請輸入非負整數的坪數上限")
        # 坪數下限
        while True:
            area_lower = input("請輸入坪數下限：")
            if area_lower.isdigit() and int(area_lower) >= 0:
                area_lower = int(area_lower)
                area_lower_std = (area_lower - area_min) / (area_max - area_min)
                if area_lower <= area_upper:
                    break
                else:
                    print("坪數下限必須小於或等於上限")
            else:
                print("請輸入非負整數的坪數下限")
        break
    elif z1 == 'n':
        area_upper_std = 1
        area_lower_std = 0
        break
    else:
        print("請輸入y或n")

while True:
    z2 = input("是否設租金限制？(y/n): ")
    if z2 == 'y':
        while True:
            price_upper = input("請輸入租金上限：")
            if price_upper.isdigit() and int(price_upper) >= 0:
                price_upper = int(price_upper)
                price_upper_std = (price_upper - price_min) / (price_max - price_min)
                break
            else:
                print("請輸入非負整數的租金上限")
        # 租金下限
        while True:
            price_lower = input("請輸入租金下限：")
            if price_lower.isdigit() and int(price_lower) >= 0:
                price_lower = int(price_lower)
                price_lower_std = (price_lower - price_min) / (price_max - price_min)
                if price_lower <= price_upper:
                    break
                else:
                    print("租金下限必須小於或等於上限")
            else:
                print("請輸入非負整數的租金下限")
        break
    elif z2 == 'n':
        price_upper_std = 1
        price_lower_std = 0
        break
    else:
        print("請輸入y或n")

while True:
    z3 = input("是否設與學校距離限制？(y/n): ")
    if z3 == 'y':
        while True:
            distance_upper = input("請輸入與學校距離上限：")
            try:
                distance_upper = float(distance_upper)
                if distance_upper >= 0:
                    distance_upper_std = (distance_upper - dis_min) / (dis_max - dis_min)
                    break
                else:
                    print("請輸入非負數的與學校距離上限")
            except ValueError:
                print("請輸入數字的與學校距離上限")
        # 距離下限
        while True:
            distance_lower = input("請輸入與學校距離下限：")
            try:
                distance_lower = float(distance_lower)
                if distance_lower >= 0:
                    distance_lower_std = (distance_lower - dis_min) / (dis_max - dis_min)
                    if distance_lower <= distance_upper:
                        break
                    else:
                        print("與學校距離下限必須小於或等於上限")
                else:
                    print("請輸入非負數的與學校距離下限")
            except ValueError:
                print("請輸入數字的與學校距離下限")
        break
    elif z3 == 'n':
        distance_upper_std = 1
        distance_lower_std = 0
        break
    else:
        print("請輸入y或n")

# 設定給 fitFunc 用的上下限（std值）
area_upper = area_upper_std
area_lower = area_lower_std
price_upper = price_upper_std
price_lower = price_lower_std
distance_upper = distance_upper_std
distance_lower = distance_lower_std


# 輸入權重
print("請輸入權重")
while True:
    a = input("請輸入坪數權重：")
    if a.isdigit() and int(a) >= 0:
        a = int(a)
        break
    else:
        print("請輸入非負整數")
while True:
    p = input("請輸入租金權重：")
    if p.isdigit() and int(p) >= 0:
        p = int(p)
        break
    else:
        print("請輸入非負整數")
while True:
    d = input("請輸入與學校距離權重：")
    if d.isdigit() and int(d) >= 0:
        d = int(d)
        break
    else:
        print("請輸入非負整數")





# 找 x 使得最大化 f(x) = 1024 - x^2
# x 用 6 個 binary bit 編碼

import numpy as np
import pandas as pd
from tabulate import tabulate
# import math

# ==== 參數設定(與演算法相關) ====

NUM_ITERATION = 2000			# 世代數(迴圈數)

NUM_CHROME = 30			# 染色體個數 (一定要偶數)
NUM_BIT = 3					# 染色體長度

Pc = 0.5    					# 交配率 (代表共執行Pc*NUM_CHROME/2次交配)
Pm = 0.01   					# 突變率 (代表共要執行Pm*NUM_CHROME*NUM_BIT次突變)

NUM_PARENT = NUM_CHROME                         # 父母的個數
NUM_CROSSOVER = int(Pc * NUM_CHROME / 2)        # 交配的次數
NUM_CROSSOVER_2 = NUM_CROSSOVER*2               # 上數的兩倍
NUM_MUTATION = int(Pm * NUM_CHROME * NUM_BIT)   # 突變的次數

# np.random.seed(0)          # 若要每次跑得都不一樣的結果，就把這行註解掉

# ==== 基因演算法會用到的函式 ====
def initPop():
    df = pd.read_csv("total.csv", encoding="utf-8-sig")
    pop = df[['area_std', 'price_std', 'distance_std']].astype(float).values
    return pop

def fitFunc(x):            
    obj = a * x[0] - p * x[1] - d * x[2]   # 坪數加分，租金/距離扣分
    pen = 100000000
    pencount = 0  
    
    if (x[0] > area_upper or x[0] < area_lower):
        pencount += 1
    if (x[1] > price_upper or x[1] < price_lower):
        pencount += 1
    if (x[2] > distance_upper or x[2] < distance_lower):
        pencount += 1

    denominator = obj - pen * pencount
    if denominator == 0:
        return 0
    return denominator   # 直接回傳 obj 越大越好

def evaluatePop(p):        # 評估群體之適應度
    return [fitFunc(p[i]) for i in range(len(p))]

def selection(p, p_fit):   # 用二元競爭式選擇法來挑父母
	a = []

	for i in range(NUM_PARENT):
		[j, k] = np.random.choice(NUM_CHROME, 2, replace=False)  # 任選兩個index
		if p_fit[j] > p_fit[k] :                      # 擇優
			a.append(p[j])
		else:
			a.append(p[k])

	return a

def crossover(p):           # 用單點交配來繁衍子代
	a = []

	for i in range(NUM_CROSSOVER) :
		c = np.random.randint(1, NUM_BIT)      		  # 隨機找出單點(不包含0)
		[j, k] = np.random.choice(NUM_PARENT, 2, replace=False)  # 任選兩個index
       
		a.append(np.concatenate((p[j][0: c], p[k][c: NUM_BIT]), axis=0))
		a.append(np.concatenate((p[k][0: c], p[j][c: NUM_BIT]), axis=0))

	return a

def mutation(p):	           # 突變
	for _ in range(NUM_MUTATION) :
		row = np.random.randint(NUM_CROSSOVER_2)  # 任選一個染色體
		col = np.random.randint(NUM_BIT)          # 任選一個基因
      
		p[row][col] = (p[row][col] + 1) % 2       # 對應此染色體的此基因01互換
        

def sortChrome(a, a_fit):	    # a的根據a_fit由大排到小
    a_index = range(len(a))                         # 產生 0, 1, 2, ..., |a|-1 的 list
    
    a_fit, a_index = zip(*sorted(zip(a_fit,a_index), reverse=True)) # a_index 根據 a_fit 的大小由大到小連動的排序
   
    return [a[i] for i in a_index], a_fit           # 根據 a_index 的次序來回傳 a，並把對應的 fit 回傳

def replace(p, p_fit, a, a_fit):            # 適者生存
    b = np.concatenate((p,a), axis=0)               # 把本代 p 和子代 a 合併成 b
    b_fit = p_fit + a_fit                           # 把上述兩代的 fitness 合併成 b_fit
    
    b, b_fit = sortChrome(b, b_fit)                 # b 和 b_fit 連動的排序
    
    return b[:NUM_CHROME], list(b_fit[:NUM_CHROME]) # 回傳 NUM_CHROME 個為新的一個世代


# ==== 主程式 ====

pop = initPop()             # 初始化 pop
pop_fit = evaluatePop(pop)  # 算 pop 的 fit

best_outputs = []                           # 用此變數來紀錄每一個迴圈的最佳解 (new)
best_outputs.append(np.max(pop_fit))        # 存下初始群體的最佳解 (new)

mean_outputs = []                           # 用此變數來紀錄每一個迴圈的平均解 (new)
mean_outputs.append(np.average(pop_fit))        # 存下初始群體的最佳解 (new)

for i in range(NUM_ITERATION) :
    parent = selection(pop, pop_fit)            # 挑父母
    offspring = crossover(parent)               # 交配
    mutation(offspring)                         # 突變
    offspring_fit = evaluatePop(offspring)      # 算子代的 fit
    pop, pop_fit = replace(pop, pop_fit, offspring, offspring_fit)    # 取代
    
    best_outputs.append(np.max(pop_fit))        # 存下這次的最佳解 (new)
    mean_outputs.append(np.average(pop_fit))    # 存下這次的平均解 (new)

    print('iteration %d: x = %s, y = %f'	%(i, pop[0], pop_fit[0]))

# 取得最佳解的 index
best_index = np.argmax(pop_fit)  # 改成 argmax

# 取得最佳解的特徵值
best_solution = pop[best_index]

# 讀取原始資料
df = pd.read_csv("total.csv", encoding="utf-8-sig")

# 先篩選符合上下限的資料
epsilon = 1e-6
filtered = df[
    (df['area_std'] <= area_upper + epsilon) & (df['area_std'] >= area_lower - epsilon) &
    (df['price_std'] <= price_upper + epsilon) & (df['price_std'] >= price_lower - epsilon) &
    (df['distance_std'] <= distance_upper + epsilon) & (df['distance_std'] >= distance_lower - epsilon)
]

if filtered.empty:
    print("找不到符合條件的房屋。")
else:
    # 計算距離並取最接近的三筆
    filtered['EU_distance'] = (
        (filtered['area_std'] - best_solution[0])**2 +
        (filtered['price_std'] - best_solution[1])**2 +
        (filtered['distance_std'] - best_solution[2])**2
    )
    top3 = filtered.nsmallest(3, 'EU_distance')
    print("最符合需求的前三間房屋資訊：")
    print(tabulate(top3[['title', 'address', "price", "distance(km)", "url"]], headers='keys', tablefmt='psql'))
    # print(tabulate(top3[['title',  "distance(km)", "distance_std"]], headers='keys', tablefmt='psql'))