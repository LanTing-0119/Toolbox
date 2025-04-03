{
  library(ggplot2);library(showtext)
  library(dplyr)
}

# 想证明的核心观点: 从数据本身是无法判断谁因谁果的(尤其从情景1、2角度出发)

# 开启showtext，自动使用系统字体
showtext_auto()
set.seed(123)

# 情景 1：干预对结果有影响，基于干预分组计算因果效应 ####


# 模拟数据
n <- 1000
A <- rbinom(n, 1, 0.5)  # 干预 A ∈ {0,1}
Y <- 2 + 3 * A + rnorm(n)  # Y 是受 A 影响的结果

# 计算每组的均值
df = data.frame(
  A = A,
  Y = Y
)
mean_Y_A0 <- mean(Y[A == 0])
mean_Y_A1 <- mean(Y[A == 1])

# 计算因果效应（ATE: average treatment effect）
p1 = ggplot(df, aes(group=A, y=Y)) +
  geom_boxplot() +
  labs(
    title = '基于因分层看效应'
  )

ATE1 <- mean_Y_A1 - mean_Y_A0
print(paste("情景1的平均因果效应（ATE）为:", round(ATE1, 2)))




# 情景 2：结果2受Y影响 ####
Y2 <- 1.5 * Y + rnorm(n)

df = data.frame(
  Y = Y,
  Y2 = Y2
)

# 以中位数分组
threshold <- median(Y2)
df = df %>%
  mutate(group = ifelse(Y2>=threshold, 'high','low'))

p2 = ggplot(df, aes(x=group, y=Y)) +
  geom_boxplot() +
  labs(
    title = '基于果分层看效应'
  )

# 看 Y2 高低组的 Y 差异
Y_high <- Y[Y2 > threshold]
Y_low <- Y[Y2 <= threshold]
effect_Y2_on_Y <- mean(Y_high) - mean(Y_low)
print(paste("情景2中基于Y2分组得到的对Y的影响估计:", round(effect_Y2_on_Y, 2)))


# 情景 3：干预对结果没有影响 ####
Y_null <- 2 + rnorm(n)

# 分组均值
df = data.frame(
  A = A,
  Y_null = Y_null
)

mean_Y_null_A0 <- mean(Y_null[A == 0])
mean_Y_null_A1 <- mean(Y_null[A == 1])

# 计算因果效应（ATE: average treatment effect）
p3 = ggplot(df, aes(group=A, y=Y_null)) +
  geom_boxplot() +
  labs(
    title = '基于无效因分层看效应'
  )

# ATE
ATE3 <- mean_Y_null_A1 - mean_Y_null_A0
print(paste("情景3的平均因果效应（应为接近0）:", round(ATE3, 2)))



library(patchwork)
p1 / p2 / p3
