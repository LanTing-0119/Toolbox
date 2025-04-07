# 1.从零实现逆权重加权
# 2.证明从零实现逆权重加权可以通过GLM倾向性评分简化计算

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
  mutate(weights = n_L / n_A)

df$weights

# 下面使用倾向性评分的方法计算逆权重加权
# 用逻辑回归估计倾向得分
fit <- glm(A ~ L, family = binomial(), data = df)
df$pscore_hat <- predict(fit, type = "response")

# Step 2: 计算逆概率权重
df$ipw <- ifelse(df$A == 1, 1 / df$pscore_hat, 1 / (1 - df$pscore_hat))

df$ipw
df$weights
