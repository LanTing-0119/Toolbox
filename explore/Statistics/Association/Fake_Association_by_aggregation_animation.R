# 安装必要包（如未安装）
# install.packages(c("ggmosaic", "ggplot2", "dplyr", "patchwork", "magick"))

library(ggplot2)
library(ggmosaic)
library(dplyr)
library(patchwork)
library(magick)

set.seed(42)

# 自定义绘图函数（和你的一样）
plot_mosaic <- function(data, title, legend = FALSE) {
  p <- ggplot(data = data) +
    geom_mosaic(aes(x = product(sex, smoke), fill = smoke), na.rm = TRUE) +
    labs(title = title, x = "Smoke", y = "Proportion") +
    theme_minimal()

  if (!legend) {
    p <- p + theme(legend.position = "none")
  }

  return(p)
}

# 创建保存帧的临时目录
dir.create("mosaic_frames", showWarnings = FALSE)

# 动画每帧对应的 Group A 样本数量
n_B <- 1000
n_A_seq <- seq(20, 200, by = 1)

# 生成每一帧图像
for (n_A in n_A_seq) {
  print(paste0(which(n_A==n_A_seq),' / ',length(n_A_seq)))
  # 生成 Group A（男性多、吸烟多）
  groupA <- data.frame(
    group = "A",
    sex = sample(c("Male", "Female"), size = n_A, replace = TRUE, prob = c(0.8, 0.2)),
    smoke = sample(c("Yes", "No"), size = n_A, replace = TRUE, prob = c(0.8, 0.2))
  )

  # 生成 Group B（女性多、吸烟少）
  groupB <- data.frame(
    group = "B",
    sex = sample(c("Male", "Female"), size = n_B, replace = TRUE, prob = c(0.2, 0.8)),
    smoke = sample(c("Yes", "No"), size = n_B, replace = TRUE, prob = c(0.2, 0.8))
  )

  # 合并数据
  combined <- bind_rows(groupA, groupB)

  # 三个子图
  p1 <- plot_mosaic(groupA, paste0("Group A (n = ", n_A, ")"))
  p2 <- plot_mosaic(groupB, "Group B (n = 100)")
  p3 <- plot_mosaic(combined, "Combined (A + B)", legend = TRUE)

  # 拼图
  full_plot <- p1 + p2 + p3

  # 保存帧
  ggsave(filename = sprintf("mosaic_frames/frame_%03d.png", n_A),
         plot = full_plot, width = 12, height = 4)
}

# 合成 GIF 动图
img_list <- list.files("mosaic_frames", pattern = "*.png", full.names = TRUE)
animation <- image_read(img_list) %>%
  image_animate(fps = 100)

# 保存动图
image_write(animation, "mosaic_combined_animation.gif")
