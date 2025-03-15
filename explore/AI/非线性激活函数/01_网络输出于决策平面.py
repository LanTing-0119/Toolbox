import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']  # 或者使用 ['Microsoft YaHei']
# plt.rcParams['axes.unicode_minus'] = False  # 防止负号显示为方块

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

        # 初始化权重与偏置，采用随机初始化
        # 输入层到隐藏层：输入2维，隐藏层 n_hidden 个神经元
        self.W1 = np.random.randn(n_hidden, 2)
        self.b1 = np.random.randn(n_hidden, 1)
        # 隐藏层到输出层：输出1个神经元
        self.W2 = np.random.randn(1, n_hidden)
        self.b2 = np.random.randn(1, 1)
    
    def forward(self, x):
        """
        前向传播：
        x 的形状为 (2, number_of_samples)
        返回输出 a2 的形状为 (1, number_of_samples)
        """
        # 计算隐藏层
        z1 = np.dot(self.W1, x) + self.b1
        a1 = self.hidden_activation(z1)
        # 输出层使用 sigmoid 保证输出在 0-1 范围
        z2 = np.dot(self.W2, a1) + self.b2
        a2 = sigmoid(z2) # 这一步相当于是为了让输出值落于0-1方便显示和设定阈值，仅此而已
        return a2


def plot_decision_boundary(nn):
    # 定义输入空间范围
    x_min, x_max = -5, 5
    y_min, y_max = -5, 5
    xx, yy = np.meshgrid(np.linspace(x_min, x_max, 200),
                         np.linspace(y_min, y_max, 200))
    # 将网格点整形成2×(num_points)的矩阵
    grid = np.c_[xx.ravel(), yy.ravel()].T
    # 计算每个网格点对应的网络输出
    Z = nn.forward(grid)
    Z = Z.reshape(xx.shape)
    
    # 计算输出的中位数
    median_val = np.median(Z)
    
    # 绘制3D图形
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    
    # 绘制决策面
    ax.plot_surface(xx, yy, Z, cmap='viridis', alpha=0.7)
    # 使用输出中位数作为等高线水平值，将其在 z=0 平面上投影
    ax.contour(xx, yy, Z, levels=[median_val], zdir='z', offset=0, cmap='coolwarm')
    
    # 设置 z 轴显示范围为 0-1
    ax.set_zlim(0, 1)
    
    ax.set_xlabel('X1')
    ax.set_ylabel('X2')
    ax.set_zlabel('Output')
    ax.set_title(f'决策面及其二维投影 (输出中位数 = {median_val:.3f})')
    plt.show()

# 可以修改 activation 参数选择 'sigmoid' 或 'step'
n_hidden = 2  # 隐藏层神经元数量
nn = SimpleNN(n_hidden, activation='sigmoid')
plot_decision_boundary(nn)
