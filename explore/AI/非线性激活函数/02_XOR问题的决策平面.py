import numpy as np
import matplotlib.pyplot as plt
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
        # 根据选择的激活函数决定隐藏层的激活
        if activation == 'sigmoid':
            self.hidden_activation = sigmoid
        elif activation == 'step':
            self.hidden_activation = step
        else:
            raise ValueError("只支持'sigmoid'或'step'激活函数")
            
        # 这里先随机初始化，后面我们会手动设置权重
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
        a2 = sigmoid(z2)  # 保证输出在 0-1 范围
        return a2

def plot_decision_boundary(nn):
    # 定义输入空间范围
    x_min, x_max = -0.5, 1.5
    y_min, y_max = -0.5, 1.5
    xx, yy = np.meshgrid(np.linspace(x_min, x_max, 200),
                         np.linspace(y_min, y_max, 200))
    grid = np.c_[xx.ravel(), yy.ravel()].T
    Z = nn.forward(grid)
    Z = Z.reshape(xx.shape)
    
    # 计算输出的中位数
    median_val = np.median(Z)
    
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    
    # 绘制决策面
    ax.plot_surface(xx, yy, Z, cmap='viridis', alpha=0.7)
    ax.contour(xx, yy, Z, levels=[median_val], zdir='z', offset=0, cmap='coolwarm')
    ax.set_zlim(0, 1)
    
    ax.set_xlabel('X1')
    ax.set_ylabel('X2')
    ax.set_zlabel('Output')
    ax.set_title(f'决策面及其二维投影 (输出中位数 = {median_val:.3f})')
    plt.show()

# 构造一个2个隐藏神经元的网络
n_hidden = 2  
nn = SimpleNN(n_hidden, activation='sigmoid')

# 手动设置网络权重以解决 XOR 问题
# 隐藏层 neuron1: 用于捕捉 (x1 OR x2) 的信息
# 当两个隐藏层权重一样或呈倍数关系时，实际上网络输出只依赖于一个方程，而偏置b决定了两条平行线的距离程度
nn.W1 = np.array([[10, 10],
                  [10, 10]])
# nn.W1 = np.array([[20, 20],
#                   [10, 10]])
# 当两个隐藏层权重不一样时，就会得到真正复杂的非线性决策边界
# nn.W1 = np.array([[40, 5],
#                   [10, 10]])
nn.b1 = np.array([[-5],
                  [-15]])

# 输出层：结合两个隐藏神经元的输出
nn.W2 = np.array([[10, -20]])
nn.b2 = np.array([[-5]])

# 打印几个测试点的输出验证 XOR
test_inputs = np.array([[0, 0, 1, 1],
                        [0, 1, 0, 1]])
outputs = nn.forward(test_inputs)

# 绘制决策面
plot_decision_boundary(nn)


