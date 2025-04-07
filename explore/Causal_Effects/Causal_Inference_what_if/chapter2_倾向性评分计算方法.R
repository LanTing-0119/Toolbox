# 利用倾向性评分计算分层和汇总的因果效应

# 创建数据框
df <- data.frame(
  L = c(0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1),
  A = c(0,0,0,0,1,1,1,1,0,0,0,1,1,1,1,1,1,1,1,1),
  Y = c(0,1,0,0,0,0,0,1,1,1,0,1,1,1,1,1,1,0,0,0)
)

# 估计倾向性评分
fit <- glm(A ~ L, family = binomial(), data = df)  # 估计倾向性评分的模型（依赖于L）
df$pscore_hat <- predict(fit, type = "response")   # 计算倾向性评分

# 计算逆概率权重
df$ipw <- ifelse(df$A == 1, 1 / df$pscore_hat, 1 / (1 - df$pscore_hat))

# 计算在L = 0和L = 1分层下的加权平均处理效应（ATE）
# L = 0 的加权因果效应
df_L0 <- df[df$L == 0, ]
ATE_L0 <- with(df_L0, sum(ipw * (Y - mean(Y))) / sum(ipw))

# L = 1 的加权因果效应
df_L1 <- df[df$L == 1, ]
ATE_L1 <- with(df_L1, sum(ipw * (Y - mean(Y))) / sum(ipw))

# 计算每个分层的样本量
N_L0 <- nrow(df_L0)  # L = 0 组的样本量
N_L1 <- nrow(df_L1)  # L = 1 组的样本量
N_total <- nrow(df)  # 总样本量

# 计算总体加权平均效应
ATE_total <- (N_L0 * ATE_L0 + N_L1 * ATE_L1) / N_total

# 查看结果
cat("ATE for L = 0: ", ATE_L0, "\n")
cat("ATE for L = 1: ", ATE_L1, "\n")
cat("Total ATE: ", ATE_total, "\n")
