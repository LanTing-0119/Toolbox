# 加载所需包
library(ggplot2)
library(ggmosaic)
library(dplyr)

set.seed(42)

# 设置样本大小
n <- 100

# 人群 A（比如男性多，吸烟多）
groupA <- data.frame(
  group = "A",
  sex = sample(c("Male", "Female"), size = n , replace = TRUE, prob = c(0.8, 0.2)),
  smoke = sample(c("Yes", "No"), size = n, replace = TRUE, prob = c(0.8, 0.2))
)

# 人群 B（比如女性多，吸烟少）
groupB <- data.frame(
  group = "B",
  sex = sample(c("Male", "Female"), size = n, replace = TRUE, prob = c(0.2, 0.8)),
  smoke = sample(c("Yes", "No"), size = n, replace = TRUE, prob = c(0.2, 0.8))
)

# 合并数据
df <- bind_rows(groupA, groupB)

# 分组作图函数
plot_mosaic <- function(data, title, legend = FALSE) {
  p <- ggplot(data = data) +
    geom_mosaic(aes(x = product(sex, smoke), fill = smoke), na.rm = TRUE) +
    labs(title = title, x = "Smoke", y = "Proportion") +
    theme_minimal()

  # 控制图例显示
  if (!legend) {
    p <- p + theme(legend.position = "none")
  }

  return(p)
}


# 绘制三张图
p1 <- plot_mosaic(groupA, "Group A (Independent)")
p2 <- plot_mosaic(groupB, "Group B (Independent)")
p3 <- plot_mosaic(df, "Combined (Apparent Association)", legend = TRUE)

# 使用 patchwork 拼图
library(patchwork)
p1 + p2 + p3



