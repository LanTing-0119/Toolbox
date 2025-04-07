library(dplyr)

# 手动实现高斯核密度估计
set.seed(123)
# 模拟数据：100个数据点，服从正态分布
data_points <- rnorm(100, mean = 5, sd = 2)

# 定义高斯核函数
gaussian_kernel <- function(u) {
  1 / sqrt(2 * pi) * exp(-0.5 * u^2)
}

# 定义手动核密度估计函数
manual_kde <- function(x, data, h) {
  n <- length(data)
  # 对 x 处的密度估计
  density_est <- sapply(x, function(x0) {
    u <- (x0 - data) / h
    sum(gaussian_kernel(u)) / (n * h)
  })
  return(density_est)
}

# 定义估计范围和带宽
x_vals <- seq(min(data_points) - 1, max(data_points) + 1, length.out = 512)
h <- 0.5  # 带宽参数，可调整

# 计算手动高斯核密度估计
manual_density <- manual_kde(x_vals, data_points, h)

# 绘图比较：手动实现 vs. 内置 density() 函数
par(mfrow = c(1,2))
# 手动估计结果
plot(x_vals, manual_density, type = "l", main = "Manual Gaussian KDE",
     xlab = "Value", ylab = "Density")
# 使用内置 density() 函数
built_in_density <- density(data_points, kernel = "gaussian", bw = h)
plot(built_in_density, main = "Built-in density() KDE",
     xlab = "Value", ylab = "Density")

# 恢复绘图设置
par(mfrow = c(1,1))
