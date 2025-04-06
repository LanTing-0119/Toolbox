{
  library(ggplot2);library(showtext)
  library(dplyr)
}

# 想证明的核心观点: A → Y ← V，如果试验知道了 A → Y 的因果效应值，此时想知道亚群分析(控制V)时是否会对 A → Y 的因果效应估计产生影响
# 结论是发现如果控制了V，可以在亚族层面得到 A → Y 的因果效应值；而且理论上因为V不影响A对Y的因果效应值，所以两个亚组得到的A → Y 的因果效应值都相同；
# 而且因为总体会存在V的2种取值不一定是 50% vs. 50%, 所以反而会导致计算 A → Y 因果效应时因为认为了亚组的V均匀分布而导致波动
# 注意以上情况还没有纳入存在随机误差ε的情况(添加了还涉及到统计置信区间的问题)

# 开启showtext，自动使用系统字体
showtext_auto()
set.seed(396)

# 情景 1：总体看A对Y效应 ####

# 模拟数据
n <- 1000
V = rbinom(n, 1, 0.5)
A <- rbinom(n, 1, 0.5)  # 干预 A ∈ {0,1}
# Y <- 2 + 3 * A + V + rnorm(n)  # 假设 A对Y的效应值是3
Y <- 2 + 3 * A + V  # 假设 A对Y的效应值是3


# 计算每组的均值
df = data.frame(
  A = A,
  V = V,
  Y = Y
)

plot <- function(df, group='总体') {


  mean_Y_A0 <- df %>% filter(A==0) %>% pull(Y) %>% mean()
  mean_Y_A1 <- df %>% filter(A==1) %>% pull(Y) %>% mean()
  ATE1 <- mean_Y_A1 - mean_Y_A0

  p = ggplot(df, aes(x = factor(A), y = Y)) +
    geom_boxplot() +
    labs(
      title = paste0(group,'看A对Y效应: ',round(ATE1, 5)),
      x = 'A (0/1)',
      y = 'Y'
    )
  p
  return(p)
}

p1 = plot(df, group = '总体')

p1


# 情景 2：控制V在亚组估计A对Y的效应值  ####
df1 = df %>% filter(V==1)
p2 = plot(df1, group = 'V=1')
p2
df2 = df %>% filter(V==0)
p3 = plot(df2, group = 'V=0')
p3


library(patchwork)
p1 + p2 + p3




# 探索是否存在总效应均大于控制修饰因子的情况
effect <- function(df) {
  mean_Y_A0 <- df %>% filter(A==0) %>% pull(Y) %>% mean()
  mean_Y_A1 <- df %>% filter(A==1) %>% pull(Y) %>% mean()
  ATE1 <- mean_Y_A1 - mean_Y_A0
  return (ATE1)
}

for (i in 1:10000){

  set.seed(i)
  # 模拟数据
  n <- 1000
  V = rbinom(n, 1, 0.5)
  A <- rbinom(n, 1, 0.5)  # 干预 A ∈ {0,1}
  # Y <- 2 + 3 * A + V + rnorm(n)  # 假设 A对Y的效应值是3
  Y <- 2 + 3 * A + V  # 假设 A对Y的效应值是3


  # 计算每组的均值
  df = data.frame(
    A = A,
    V = V,
    Y = Y
  )

  effect_v_all = effect(df)

  df1 = df %>% filter(V==1)
  effect_v_1 = effect(df1)
  df2 = df %>% filter(V==0)
  effect_v_0 = effect(df2)

  if (effect_v_all >= (effect_v_1 & effect_v_0)){
    print(i)
  }
}
