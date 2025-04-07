# 核密度估计通过在每一个观测点上放置一个“光滑的钟形曲线”（核函数，最常见是高斯核），然后对这些小曲线求和，从而得出总体的平滑估计曲线。
# 注意绘制的直方图下面有数据的分布

set.seed(123)
height <- rnorm(100, mean = 170, sd = 10)  # 模拟100个身高数据，均值170，标准差10

hist(height, breaks = 15, probability = TRUE, col = "lightgray", border = "white", main = "身高分布的核密度估计")
lines(density(height), col = "blue", lwd = 2)  # KDE 曲线
rug(height)  # 在X轴添加观测点的小刻度

# 手动调整 KDE 的带宽：
lines(density(height, bw = 5), col = "red", lwd = 2, lty = 2)  # 更平滑
lines(density(height, bw = 2), col = "green", lwd = 2, lty = 2)  # 更平滑
lines(density(height, bw = 0.5), col = "orange", lwd = 2, lty = 2)  # 更平滑
rug(height)  # 在X轴添加观测点的小刻度
