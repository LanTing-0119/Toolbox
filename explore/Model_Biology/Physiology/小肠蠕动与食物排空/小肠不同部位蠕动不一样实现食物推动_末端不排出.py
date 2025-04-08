import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# 初始化参数方程
def setting(n=10, food_amount=100):
    food_position = 0  # 食物初始位置
    intestinal = np.zeros(n)  # 小肠，每个位置的食物量初始化为 0
    intestinal[food_position] = food_amount  # 将食物放置在第一个位置
    return intestinal

# 初始化参数
n=30
food_amount=1000
intestinal = setting(n, food_amount)

# 设置不同位置的蠕动频率（范围从 0.1 到 0.5）
movement_frequency = np.sort(np.random.uniform(0.1, 0.8, n))[::-1]  # 按递减排序

# 绘制设置
fig, ax = plt.subplots(figsize=(10, 6))
bar = ax.bar(range(n), intestinal)

ax.set_title("小肠不同部位食物分布")
ax.set_xlabel("小肠位置")
ax.set_ylabel("食物量")
ax.set_ylim(0, food_amount)

# 动画更新函数
def update(frame):

    intestinal = setting(n, food_amount)
    
    # 模拟食物的前进
    t = frame  # 当前循环时间

    for i in list(range(t)):
        # 偶数位置的食物移动
        if i % 2 == 0:
            for j in range(1, n, 2):  # 只考虑偶数位置
                move_prob = np.random.rand()  # 随机生成一个值决定是否移动
                if move_prob < movement_frequency[j]:
                    if j == n - 1:
                        move_amount = intestinal[j] / 2  # 确保不会越界
                        intestinal[j - 1] += move_amount
                        intestinal[j] = move_amount
                    else:
                        # 向前后移动
                        move_amount = intestinal[j] / 2
                        intestinal[j - 1] += move_amount
                        intestinal[j + 1] += move_amount
                        intestinal[j] = 0

        # 奇数位置的食物移动
        elif i % 2 == 1:
            for j in range(0, n, 2):  # 只考虑奇数位置
                move_prob = np.random.rand()  # 随机生成一个值决定是否移动
                if move_prob <= movement_frequency[j]:
                    if j == 0:
                        # 向前后移动
                        move_amount = intestinal[j] / 2
                        intestinal[j + 1] += move_amount
                        intestinal[j] = move_amount
                    else:
                        # 向前后移动
                        move_amount = intestinal[j] / 2
                        intestinal[j - 1] += move_amount
                        intestinal[j + 1] += move_amount
                        intestinal[j] = 0

    # 更新条形图
    for rect, h in zip(bar, intestinal):
        rect.set_height(h)

    ax.set_title(f"小肠不同部位食物分布 (t = {t})")
    return bar,

# 创建动画
ani = animation.FuncAnimation(fig, update, frames=np.arange(1, 20001, 200), interval=100, blit=False)

# 显示动画
plt.show()
