# 想证明的观点是个体的比值期望不等于群体比值期望: 因为有部分个体的权重更大(例如样本A因果效应比3，但本身不治疗发生结局概率就低，因此需要校正)
# 从p分布下的个体，要去估计y的平均值。
# 如果我们在一个非均匀分布下进行抽样（比如某些类型的人更容易被抽到），那我们就需要用它来当权重，做一个纠正。

# 模拟三个个体的 Q_Y^0(1) 和 Q_Y^1(1)
Q0 <- c(0.1, 0.4, 0.7)
Q1 <- c(0.3, 0.8, 0.7)

# 个体因果风险比
RR_individual <- Q1 / Q0

# 不加权平均
mean_unweighted <- mean(RR_individual)

# 权重：个体Q0除以人群平均Q0
mean_Q0 <- mean(Q0)
W <- Q0 / mean_Q0

# 加权平均
mean_weighted <- sum(W * RR_individual) / sum(W)

# 输出
cat("不加权平均风险比:", mean_unweighted, "\n")
cat("加权平均风险比:", mean_weighted, "\n")
