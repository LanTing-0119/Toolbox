# 倾向性评分是如何通过匹配倾向性评分值实现组间均匀分布的
# 不同的匹配方式会完全造成不同的结果匹配后结果
# 匹配后两组间变得更加一致是因为没有匹配的样本会被忽略掉

library(MatchIt)
library(ggplot2)
library(gridExtra)
library(showtext)

# 自动使用系统字体
showtext_auto()
# 设置随机种子
set.seed(123)

# 1. 模拟数据
n <- 1000
age <- rnorm(n, mean = 50, sd = 10)
gender <- rbinom(n, 1, 0.5)  # 0: 女, 1: 男
exercise <- rbinom(n, 1, prob = plogis((age - 50)/10))
logit_p <- -3 + 0.05 * age + 0.8 * gender + 1.2 * exercise
p <- plogis(logit_p)
A <- rbinom(n, 1, p)
df <- data.frame(A = factor(A), age, gender = factor(gender), exercise = factor(exercise))

# 2. 倾向性评分匹配(不同的匹配方案结果不同)

# 方法1
match_model <- matchit(A ~ age + gender + exercise, data = df, method = "nearest", distance = "logit")

# 方法2 提升匹配质量
match_model <- matchit(
  A ~ age + gender + exercise,
  data = df,
  method = "nearest",
  distance = "logit",
  caliper = 0.2,   # 一般取 0.1 ~ 0.25 SD
  replace = FALSE
)

# 方法3 更稳健的匹配算法
match_model <- matchit(
  A ~ age + gender + exercise,
  data = df,
  method = "optimal",
  distance = "logit"
)

# 方法4 Mahalanobis 距离匹配（如果变量是定量的
match_model <- matchit(
  A ~ age + gender + exercise,
  data = df,
  method = "nearest",
  distance = "mahalanobis"
)

matched_data <- match.data(match_model)

# 3. 变量分布图函数
plot_density <- function(data, var, title) {
  ggplot(data, aes_string(x = var, fill = "A")) +
    geom_density(alpha = 0.5) +
    labs(title = title, fill = "治疗组 (A)") +
    theme_minimal()
}

plot_bar <- function(data, var, title) {
  ggplot(data, aes_string(x = var, fill = "A")) +
    geom_bar(position = "fill") +
    labs(title = title, y = "比例", fill = "治疗组 (A)") +
    theme_minimal()
}

# 4. 匹配前图
p1_pre <- plot_density(df, "age", "匹配前：年龄分布")
p2_pre <- plot_bar(df, "gender", "匹配前：性别分布")
p3_pre <- plot_bar(df, "exercise", "匹配前：锻炼频率分布")

# 5. 匹配后图
p1_post <- plot_density(matched_data, "age", "匹配后：年龄分布")
p2_post <- plot_bar(matched_data, "gender", "匹配后：性别分布")
p3_post <- plot_bar(matched_data, "exercise", "匹配后：锻炼频率分布")

# 6. 用 gridExtra 展示
grid.arrange(p1_pre, p1_post,
             p2_pre, p2_post,
             p3_pre, p3_post,
             ncol = 2)
