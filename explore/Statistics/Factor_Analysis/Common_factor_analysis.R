# 研究common factor analysis
# 就是假设了观察变量实际上是由未检测得潜在变量决定的；将随机误差归结到了每个样本对该因子产生的独特效应
# 所以common factor analysis实际上是找共有的factor，看每个factor对于观察变量的权重；
# 一个应用是看根据factor能不能用于区分样本(把一个factor当成一个PC)


# 安装和加载必要的包
install.packages("psych")   # 如果尚未安装
install.packages("GPArotation")
library(psych)
library(GPArotation)

# 生成模拟数据（假设3个潜在因子）
set.seed(123)
n <- 500  # 样本量
p <- 9    # 变量数

# 定义因子载荷矩阵
loadings <- matrix(c(
  0.7, 0.5, 0.3, rep(0, 6),  # 因子1影响前3个变量
  rep(0, 3), 0.8, 0.6, 0.4, rep(0, 3),  # 因子2影响中间3个变量
  rep(0, 6), 0.7, 0.5, 0.3   # 因子3影响最后3个变量
), nrow = p, byrow = FALSE)

# 生成相关矩阵并创建数据
sigma <- loadings %*% t(loadings) + diag(p)  # 添加唯一性方差
data <- as.data.frame(MASS::mvrnorm(n, mu = rep(0, p), Sigma = sigma))
colnames(data) <- paste0("V", 1:p)

# 检查数据适合性
KMO(data)  # Kaiser-Meyer-Olkin检验（>0.6可接受）
cortest.bartlett(data)  # 巴特利特球形检验（p<0.05说明适合）

# 确定因子数量
parallel <- fa.parallel(data, fa = "fa")  # 平行分析
nfactors <- parallel$nfact  # 建议因子数

# 进行因子分析（最大似然法 + 斜交旋转）
nfactors = 3 # 可以改成其他数字
fa_result <- fa(data,
                nfactors = nfactors,
                rotate = "oblimin",  # 使用斜交旋转
                fm = "ml",          # 最大似然法
                scores = "regression")

# 查看结果
print(fa_result, digits = 2, sort = TRUE)
fa.diagram(fa_result)  # 绘制因子结构图

# 检查主要指标
fa_result$loadings     # 因子载荷
fa_result$communality  # 共同度
fa_result$TLI          # Tucker-Lewis指数
fa_result$RMSEA        # RMSEA
