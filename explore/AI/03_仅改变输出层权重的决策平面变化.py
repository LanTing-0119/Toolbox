import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from mpl_toolkits.mplot3d import Axes3D



# 定义激活函数：sigmoid 和 step
def sigmoid(x):
    return 1 / (1 + np.exp(-x))

def step(x):
    return (x > 0).astype(float)

# 定义一个简单的前馈神经网络
class SimpleNN:
    def __init__(self, n_hidden, activation='sigmoid'):
        self.n_hidden = n_hidden
        # 根据选择的激活函数决定隐藏层的激活
        if activation == 'sigmoid':
            self.hidden_activation = sigmoid
        elif activation == 'step':
            self.hidden_activation = step
        else:
            raise ValueError("只支持'sigmoid'或'step'激活函数")
            
        # 初始化权重与偏置（这里先随机初始化，后面我们手动设置）
        self.W1 = np.random.randn(n_hidden, 2)
        self.b1 = np.random.randn(n_hidden, 1)
        self.W2 = np.random.randn(1, n_hidden)
        self.b2 = np.random.randn(1, 1)
    
    def forward(self, x):
        """
        前向传播：
        x 的形状为 (2, number_of_samples)
        返回输出 a2 的形状为 (1, number_of_samples)
        """
        z1 = np.dot(self.W1, x) + self.b1
        a1 = self.hidden_activation(z1)
        z2 = np.dot(self.W2, a1) + self.b2
        a2 = sigmoid(z2)
        return a2

# 构造一个2个隐藏神经元的网络，并固定隐藏层参数（用于解决 XOR 问题）
n_hidden = 2  
nn = SimpleNN(n_hidden, activation='sigmoid')
# 固定隐藏层参数（XOR 经典设置）
nn.W1 = np.array([[10, 10],
                  [10, 10]])
nn.b1 = np.array([[-5],
                  [-15]])

# 设置初始的输出层参数（后续将在动画中动态变化）
nn.W2 = np.array([[10, -20]])
nn.b2 = np.array([[-5]])

# 定义决策平面绘制函数，接受一个已构造好的 nn
def get_decision_data(nn):
    # 为 XOR 问题我们关注 [0,1] 范围
    x_min, x_max = -0.5, 1.5
    y_min, y_max = -0.5, 1.5
    xx, yy = np.meshgrid(np.linspace(x_min, x_max, 200),
                         np.linspace(y_min, y_max, 200))
    grid = np.c_[xx.ravel(), yy.ravel()].T
    Z = nn.forward(grid)
    Z = Z.reshape(xx.shape)
    return xx, yy, Z

# 设置图形及动画
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

def init():
    ax.clear()
    ax.set_xlim(-0.5, 1.5)
    ax.set_ylim(-0.5, 1.5)
    ax.set_zlim(0, 1)
    ax.set_xlabel('X1')
    ax.set_ylabel('X2')
    ax.set_zlabel('Output')
    ax.set_title('动态决策面 (输出层参数变化)')
    return ax,

def update(frame):
    # 动态更新输出层参数
    # 这里以 frame 作为时间参数 t
    t = frame / 10.0  # 调整速度
    # 令输出层的两个权重和偏置周期性变化
    new_W2_0 = 10 + 5 * np.sin(t)
    new_W2_1 = -20 + 5 * np.cos(t)
    new_b2 = -5 + 2 * np.sin(t/2)
    
    nn.W2 = np.array([[new_W2_0, new_W2_1]])
    nn.b2 = np.array([[new_b2]])
    
    # 获取当前决策面数据
    xx, yy, Z = get_decision_data(nn)
    median_val = 0.5
    
    # 清除之前图像
    ax.clear()
    # 重新设置坐标范围与标签
    ax.set_xlim(-0.5, 1.5)
    ax.set_ylim(-0.5, 1.5)
    ax.set_zlim(0, 1)
    ax.set_xlabel('X1')
    ax.set_ylabel('X2')
    ax.set_zlabel('Output')
    ax.set_title(f'动态决策面 (中位数={median_val:.3f})')
    
    # 绘制决策面
    surf = ax.plot_surface(xx, yy, Z, cmap='viridis', alpha=0.7)
    # 绘制决策边界在 z=0 平面的投影
    cont = ax.contour(xx, yy, Z, levels=[median_val], zdir='z', offset=0, cmap='coolwarm')
    
    return surf, cont

# 创建动画
anim = FuncAnimation(fig, update, frames=200, init_func=init, interval=100, blit=False)

plt.show()
