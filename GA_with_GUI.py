import numpy as np
import pandas as pd
import random
from tabulate import tabulate
import tkinter as tk
from tkinter import ttk, messagebox
import re
import requests

random.seed(0)  

# 讀取原始資料
df = pd.read_csv("total.csv", encoding="utf-8-sig")

# 取得各欄最大最小值
area_min, area_max = df['area'].min(), df['area'].max()
price_min, price_max = df['price'].min(), df['price'].max()
dis_min, dis_max = df['distance(km)'].min(), df['distance(km)'].max()

# ==== 基因演算法會用到的函式 ====
def initPop():
    pop = []
    for i in range(NUM_CHROME):
        pop.append([random.uniform(0, 1) for i in range(3)])
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
    a_sel = []
    for i in range(NUM_PARENT):
        [j, k] = np.random.choice(NUM_CHROME, 2, replace=False)  # 任選兩個index
        if p_fit[j] > p_fit[k] :                      # 擇優
            a_sel.append(p[j])
        else:
            a_sel.append(p[k])
    return a_sel

def crossover(p):           # 用單點交配來繁衍子代
    a_cross = []
    for i in range(NUM_CROSSOVER) :
        c = np.random.randint(1, NUM_BIT)      		  # 隨機找出單點(不包含0)
        [j, k] = np.random.choice(NUM_PARENT, 2, replace=False)  # 任選兩個index
        a_cross.append(np.concatenate((p[j][0: c], p[k][c: NUM_BIT]), axis=0))
        a_cross.append(np.concatenate((p[k][0: c], p[j][c: NUM_BIT]), axis=0))
    return a_cross

def mutation(p):	           # 突變
    for _ in range(NUM_MUTATION) :
        row = np.random.randint(NUM_CROSSOVER_2)  # 任選一個染色體
        col = np.random.randint(NUM_BIT)          # 任選一個基因
        p[row][col] = (p[row][col] + 1) % 2       # 對應此染色體的此基因01互換

def sortChrome(a, a_fit):	    # a的根據a_fit由大排到小
    a_index = range(len(a))                         
    a_fit, a_index = zip(*sorted(zip(a_fit,a_index), reverse=True)) 
    return [a[i] for i in a_index], a_fit           

def replace(p, p_fit, a, a_fit):            # 適者生存
    b = np.concatenate((p,a), axis=0)               
    b_fit = p_fit + a_fit                           
    b, b_fit = sortChrome(b, b_fit)                 
    return b[:NUM_CHROME], list(b_fit[:NUM_CHROME]) 

# ==== 參數設定(與演算法相關) ====
NUM_ITERATION = 1000		# 世代數(迴圈數)
NUM_CHROME = 800			# 染色體個數 (一定要偶數)
NUM_BIT = 3					# 染色體長度
Pc = 0.6    					# 交配率
Pm = 0.01   					# 突變率
NUM_PARENT = NUM_CHROME                         
NUM_CROSSOVER = int(Pc * NUM_CHROME / 2)        
NUM_CROSSOVER_2 = NUM_CROSSOVER*2               
NUM_MUTATION = int(Pm * NUM_CHROME * NUM_BIT)   
np.random.seed(0)          

# ==== GUI 互動 ====
def run_with_gui():
    def highlight_links(text):
            text_box.tag_remove("link", "1.0", tk.END)
            for i, match in enumerate(re.finditer(r"https?://\S+", text)):
                start = f"1.0+{match.start()}c"
                end = f"1.0+{match.end()}c"
                url = match.group()
                tag_name = f"link_{i}"

                def callback(event, url=url):
                    import webbrowser
                    webbrowser.open_new(url)

                text_box.tag_add(tag_name, start, end)
                text_box.tag_config(tag_name, foreground="blue", underline=True)
                text_box.tag_bind(tag_name, "<Button-1>", callback)

    def on_run():
        try:
            # 取得上下限（Entry物件名稱加_entry，避免與全域變數衝突）
            area_on = area_var.get()
            price_on = price_var.get()
            dis_on = dis_var.get()
            area_l = float(area_lower_entry.get()) if area_lower_entry.get() else 0
            area_u = float(area_upper_entry.get()) if area_upper_entry.get() else 0
            price_l = float(price_lower_entry.get()) if price_lower_entry.get() else 0
            price_u = float(price_upper_entry.get()) if price_upper_entry.get() else 0
            dis_l = float(dis_lower_entry.get()) if dis_lower_entry.get() else 0
            dis_u = float(dis_upper_entry.get()) if dis_upper_entry.get() else 0

            # 權重
            a_val = int(area_weight_entry.get())
            p_val = int(price_weight_entry.get())
            d_val = int(dis_weight_entry.get())
            if a_val < 0 or p_val < 0 or d_val < 0:
                raise ValueError("權重請輸入非負整數")
            if a_val + p_val + d_val != 100:
                messagebox.showwarning("權重錯誤", "請確認三個權重加總為 100")
                return

            # 設定全域變數
            global area_upper, area_lower, price_upper, price_lower, distance_upper, distance_lower, a, p, d
            area_upper = (area_u - area_min) / (area_max - area_min) if area_on else 1
            area_lower = (area_l - area_min) / (area_max - area_min) if area_on else 0
            price_upper = (price_u - price_min) / (price_max - price_min) if price_on else 1
            price_lower = (price_l - price_min) / (price_max - price_min) if price_on else 0
            distance_upper = (dis_u - dis_min) / (dis_max - dis_min) if dis_on else 1
            distance_lower = (dis_l - dis_min) / (dis_max - dis_min) if dis_on else 0
            a, p, d = a_val, p_val, d_val

            # 執行原本主程式
            
            exec_main()
        except Exception as e:
            messagebox.showerror("錯誤", str(e))

    def exec_main():
        pop = initPop()
        pop_fit = evaluatePop(pop)
        best_outputs = []
        best_outputs.append(np.max(pop_fit))
        mean_outputs = []
        mean_outputs.append(np.average(pop_fit))
        for i in range(NUM_ITERATION):
            parent = selection(pop, pop_fit)
            offspring = crossover(parent)
            mutation(offspring)
            offspring_fit = evaluatePop(offspring)
            pop, pop_fit = replace(pop, pop_fit, offspring, offspring_fit)
        best_index = np.argmax(pop_fit)
        best_solution = pop[best_index]
        epsilon = 1e-6
        filtered = df[
            (df['area_std'] <= area_upper + epsilon) & (df['area_std'] >= area_lower - epsilon) &
            (df['price_std'] <= price_upper + epsilon) & (df['price_std'] >= price_lower - epsilon) &
            (df['distance_std'] <= distance_upper + epsilon) & (df['distance_std'] >= distance_lower - epsilon)
        ]
        if filtered.empty:
            text_box.delete("1.0", tk.END)
            text_box.insert(tk.END, "找不到符合條件的房屋。")
        else:
            fields = []
            if a != 0:
                fields.append(('area_std', best_solution[0]))
            if p != 0:
                fields.append(('price_std', best_solution[1]))
            if d != 0:
                fields.append(('distance_std', best_solution[2]))
            def calc_eu_distance(row):
                return sum((row[field] - value) ** 2 for field, value in fields)
            filtered['EU_distance'] = filtered.apply(calc_eu_distance, axis=1)
            
            top3 = filtered.nsmallest(3, 'EU_distance')
            text_box.delete("1.0", tk.END)
            result = "最符合需求的前三間房屋資訊：\n"
            for idx, row in top3.iterrows():
                result += f"\n🏠 房屋 {idx + 1}\n"
                result += f"標題：{row['title']}\n"
                result += f"地址：{row['address']}\n"
                result += f"坪數：{row['area']} 坪\n"
                result += f"租金：{row['price']} $\n"
                result += f"距離：{row['distance(km)']:.1f} km\n"
                result += f"連結：{row['url']}\n"
                result += "-" * 50 + "\n"
            text_box.insert(tk.END, result)
            highlight_links(result)

           # 其他操作...

    # --- GUI 介面 ---
    root = tk.Tk()
    root.title("租屋神助手")
    root.geometry("800x600")

    frame = ttk.LabelFrame(root, text="請輸入篩選條件")
    frame.pack(padx=10, pady=10, fill="x")

    # 坪數
    area_var = tk.BooleanVar()
    ttk.Checkbutton(frame, text="是否限制坪數", variable=area_var).grid(row=0, column=0, sticky='w')
    ttk.Label(frame, text="下限").grid(row=0, column=1)
    area_lower_entry = ttk.Entry(frame, width=10)
    area_lower_entry.grid(row=0, column=2)
    ttk.Label(frame, text="上限").grid(row=0, column=3)
    area_upper_entry = ttk.Entry(frame, width=10)
    area_upper_entry.grid(row=0, column=4)
    ttk.Label(frame, text="坪").grid(row=0, column=5, sticky='w')

    # 租金
    price_var = tk.BooleanVar()
    ttk.Checkbutton(frame, text="是否限制租金", variable=price_var).grid(row=1, column=0, sticky='w')
    ttk.Label(frame, text="下限").grid(row=1, column=1)
    price_lower_entry = ttk.Entry(frame, width=10)
    price_lower_entry.grid(row=1, column=2)
    ttk.Label(frame, text="上限").grid(row=1, column=3)
    price_upper_entry = ttk.Entry(frame, width=10)
    price_upper_entry.grid(row=1, column=4)
    ttk.Label(frame, text="元").grid(row=1, column=5, sticky='w')

    # 距離
    dis_var = tk.BooleanVar()
    ttk.Checkbutton(frame, text="是否限制距離", variable=dis_var).grid(row=2, column=0, sticky='w')
    ttk.Label(frame, text="下限").grid(row=2, column=1)
    dis_lower_entry = ttk.Entry(frame, width=10)
    dis_lower_entry.grid(row=2, column=2)
    ttk.Label(frame, text="上限").grid(row=2, column=3)
    dis_upper_entry = ttk.Entry(frame, width=10)
    dis_upper_entry.grid(row=2, column=4)
    ttk.Label(frame, text="公里").grid(row=2, column=5, sticky='w')

    # 權重
    ttk.Label(frame, text="請輸入權重 (總和需為100):").grid(row=3, column=0, columnspan=6, sticky='w', pady=(10, 0))
    ttk.Label(frame, text="坪數").grid(row=4, column=0)
    area_weight_entry = ttk.Entry(frame, width=5)
    area_weight_entry.grid(row=4, column=1)
    ttk.Label(frame, text="租金").grid(row=4, column=2)
    price_weight_entry = ttk.Entry(frame, width=5)
    price_weight_entry.grid(row=4, column=3)
    ttk.Label(frame, text="距離").grid(row=4, column=4)
    dis_weight_entry = ttk.Entry(frame, width=5)
    dis_weight_entry.grid(row=4, column=5)

    # 結果顯示
    text_box = tk.Text(root, height=20, width=100)
    text_box.pack(padx=10, pady=10)

    # 按鈕
    start_btn = ttk.Button(root, text="開始篩選與推薦", command=on_run)
    start_btn.pack(pady=5)

    # 進度條
    progress = ttk.Progressbar(root, mode='indeterminate')
    progress.pack(pady=5)
    progress.pack_forget()  # 預設隱藏

    import threading
    def on_run_with_progress():
        progress.pack(pady=5)
        progress.start()
        root.update_idletasks()
        def task():
            try:
                on_run()
            finally:
                progress.stop()
                progress.pack_forget()
        threading.Thread(target=task).start()

    # 修改按鈕 command
    start_btn.config(command=on_run_with_progress)

    root.mainloop()

# 執行 GUI
if __name__ == "__main__":
    run_with_gui()