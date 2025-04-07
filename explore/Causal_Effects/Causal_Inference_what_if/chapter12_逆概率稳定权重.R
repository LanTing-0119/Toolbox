# 1.从零实现逆概率稳定加权
# 2.计算上逆概率稳定加权同样可以计算因果效应且更稳定

# 创建数据框
df <- data.frame(
  L = c(0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1),
  A = c(0,0,0,0,1,1,1,1,0,0,0,1,1,1,1,1,1,1,1,1),
  Y = c(0,1,0,0,0,0,0,1,1,1,0,1,1,1,1,1,1,0,0,0)
)

# 查看数据框
df

# 与上面用倾向性评分计算是等价的
library(dplyr)
df = df %>%
  group_by(L) %>%
  mutate(n_L = n()) %>%
  group_by(L,A) %>%
  mutate(n_A = n()) %>%
  group_by(L,A,Y) %>%
  mutate(n_Y = n()) %>%
  ungroup() %>%
  mutate(weights = n_L / n_A) %>%
  group_by(A) %>%
  mutate(n_A = n()) %>%
  ungroup %>%
  mutate(pr_A = n_A / dim(df)[1]) %>%
  mutate(stable_weights = pr_A * weights)

df$weights
df$stable_weights

# 下面使用倾向性评分的方法计算逆权重加权
# 用逻辑回归估计倾向得分
fit <- glm(A ~ L, family = binomial(), data = df)
df$pscore_hat <- predict(fit, type = "response")

# Step 2: 计算逆概率权重
df$ipw <- ifelse(df$A == 1, 1 / df$pscore_hat, 1 / (1 - df$pscore_hat))


df$ipw
df$weights

df$ipw = df$stable_weights

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

