import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from mpl_toolkits.mplot3d import Axes3D

# plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']
# plt.rcParams['axes.unicode_minus'] = False

# 定义激活函数：sigmoid 和 step
def sigmoid(x):
    return 1 / (1 + np.exp(-x))

def step(x):
    return (x > 0).astype(float)

# 定义一个简单的前馈神经网络
class SimpleNN:
    def __init__(self, n_hidden, activation='sigmoid'):
        self.n_hidden = n_hidden
        if activation == 'sigmoid':
            self.hidden_activation = sigmoid
        elif activation == 'step':
            self.hidden_activation = step
        else:
            raise ValueError("只支持'sigmoid'或'step'激活函数")
        
        # 初始化参数（稍后我们会手动设置隐藏层参数）
        self.W1 = np.random.randn(n_hidden, 2)
        self.b1 = np.random.randn(n_hidden, 1)
        self.W2 = np.random.randn(1, n_hidden)
        self.b2 = np.random.randn(1, 1)
    
    def forward(self, x):
        z1 = np.dot(self.W1, x) + self.b1
        a1 = z1
        # a1 = self.hidden_activation(z1)
        z2 = np.dot(self.W2, a1) + self.b2
        a2 = sigmoid(z2)
        return a2

def get_decision_data(nn):
    # 因为 XOR 输入在 [0,1] 范围，所以设置该范围
    x_min, x_max = -0.5,1.5
    y_min, y_max = -0.5,1.5
    xx, yy = np.meshgrid(np.linspace(x_min, x_max, 200),
                         np.linspace(y_min, y_max, 200))
    grid = np.c_[xx.ravel(), yy.ravel()].T
    Z = nn.forward(grid)
    Z = Z.reshape(xx.shape)
    return xx, yy, Z

# 构造一个2个隐藏神经元的网络
n_hidden = 2  
nn = SimpleNN(n_hidden, activation='sigmoid')

# 固定输出层参数（保持 XOR 处理能力）
nn.W2 = np.array([[10, -20]])
nn.b2 = np.array([[-5]])

# 固定隐藏层偏置，初始隐藏层权重（经典设置用于 XOR）
nn.b1 = np.array([[-5],
                  [-15]])
# 初始隐藏层权重，将在动画中动态更新
nn.W1 = np.array([[10, 10],
                  [10, 10]])

# 设置动画图形
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

def init():
    ax.clear()
    ax.set_xlim(-10, 30)
    ax.set_ylim(-10, 30)
    ax.set_zlim(-1, 2)
    ax.set_xlabel('X1')
    ax.set_ylabel('X2')
    ax.set_zlabel('Output')
    ax.set_title('动态决策面 (隐藏层参数变化)')
    return ax,

def update(frame):
    t = frame / 10.0  # 时间参数，用于调节动画速度
    # 动态更新隐藏层权重：每个元素周期性变化
    # 两个隐藏层权重都变化
    # new_W1 = np.array([[10 + 5 * np.sin(t), 10 + 5 * np.cos(t)],
    #                    [10 + 5 * np.cos(t), 10 + 5 * np.sin(t)]])
    # 只变化一个隐藏层权重
    new_W1 = np.array([[10, 10],
                       [10 + 5 * np.cos(t), 10 + 5 * np.sin(t)]])
    nn.W1 = new_W1  # 更新隐藏层权重，隐藏层偏置保持不变
    
    # 获取决策面数据
    xx, yy, Z = get_decision_data(nn)
    median_val = 0.5
    
    # 清除当前坐标轴，并重新设置
    ax.clear()
    ax.set_xlim(-1, 3)
    ax.set_ylim(-1, 3)
    ax.set_zlim(-1, 2)
    ax.set_xlabel('X1')
    ax.set_ylabel('X2')
    ax.set_zlabel('Output')
    # ax.set_title(f'动态决策面 (中位数={median_val:.3f})')
    
    # 绘制决策面
    surf = ax.plot_surface(xx, yy, Z, cmap='viridis', alpha=0.7)
    cont = ax.contour(xx, yy, Z, levels=[median_val], zdir='z', offset=0, cmap='coolwarm')
    
    # 在右上角显示当前隐藏层权重矩阵
    weight_text = "W1 =\n" + np.array2string(nn.W1, formatter={'float_kind':lambda x: f"{x:6.2f}"})
    # 使用 text2D 显示在 Axes 坐标中，右上角位置 (0.65, 0.95)
    ax.text2D(0.65, 0.95, weight_text, transform=ax.transAxes, fontsize=10,
              bbox=dict(facecolor='white', alpha=0.6))
    
    return surf, cont

# 创建动画: 200帧，间隔100ms
anim = FuncAnimation(fig, update, frames=200, init_func=init, interval=100, blit=False)

# 在动画生成后调用 save 方法导出动画
# anim.save('decision_boundary.gif', writer='pillow', fps=10)

plt.show()

