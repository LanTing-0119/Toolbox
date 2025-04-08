library(showtext)

# 自动使用系统字体
showtext_auto()

# 设置随机种子，确保结果可复现
set.seed(123)

# 1. 初始化
n <- 10  # 小肠长度
food_position <- 1  # 食物初始位置
food_amount <- 100  # 初始食物量
intestinal <- rep(0, n)  # 小肠，每个位置的食物量初始化为 0
intestinal[food_position] <- food_amount  # 将食物放置在第一个位置

library(dplyr)

# 2. 设置不同位置的蠕动频率（假设为随机分布，范围在 0.01 到 0.1 之间）
movement_frequency <- sort(runif(n, 0.1, 0.5) , decreasing = TRUE) # 每个位置的蠕动频率
movement_frequency <- rep(0.5, n) # 每个位置的蠕动频率

# 3. 模拟食物的前进后退 ####
## 3.1 末端不再返回 ####
t <- 1000  # 设置循环次数，模拟时间
for (i in 1:t) {

  # 偶数位置的食物移动
  if (i %% 2 == 0){
    for (j in seq(2, n, by = 2)) {  # 只考虑偶数位置
        move_prob <- runif(1)  # 随机生成一个值决定是否移动
        if (move_prob < movement_frequency[j]) {
          if (j == n) {next} # 确保不会越界
          else {
          # 向前移动
          intestinal[j-1] <- intestinal[j-1] + intestinal[j]/2
          intestinal[j+1] <- intestinal[j+1] + intestinal[j]/2
          intestinal[j] = 0
           }
       }
     }
  }

  # 奇数位置的食物移动
  if (i %% 2 == 1){
    for (j in seq(1, n, by = 2)) {  # 只考虑奇数位置
      move_prob <- runif(1)  # 随机生成一个值决定是否移动
      if (move_prob <= movement_frequency[j]) {
        if (j == 1) {
          intestinal[j+1] <- intestinal[j+1] + intestinal[j]/2
          intestinal[j] = intestinal[j]/2
        } # 确保不会越界
        else {
          # 向前移动
          intestinal[j-1] <- intestinal[j-1] + intestinal[j]/2
          intestinal[j+1] <- intestinal[j+1] + intestinal[j]/2
          intestinal[j] = 0
        }
      }
    }
  }
}

# 4. 绘制结果
# barplot(intestinal, main="小肠不同部位食物分布", xlab="小肠位置", ylab="食物量")


## 3.2 末端返回 ####
t <- 10003  # 设置循环次数，模拟时间
for (i in 1:t) {

  # 偶数位置的食物移动
  if (i %% 2 == 0){
    for (j in seq(2, n, by = 2)) {  # 只考虑偶数位置
      move_prob <- runif(1)  # 随机生成一个值决定是否移动
      if (move_prob < movement_frequency[j]) {
        if (j == n) {
          intestinal[j-1] <- intestinal[j-1] + intestinal[j]/2
          intestinal[j] = intestinal[j]/2
        } # 确保不会越界
        else {
          # 向前移动
          intestinal[j-1] <- intestinal[j-1] + intestinal[j]/2
          intestinal[j+1] <- intestinal[j+1] + intestinal[j]/2
          intestinal[j] = 0
        }
      }
    }
  }

  # 奇数位置的食物移动
  if (i %% 2 == 1){
    for (j in seq(1, n, by = 2)) {  # 只考虑奇数位置
      move_prob <- runif(1)  # 随机生成一个值决定是否移动
      if (move_prob <= movement_frequency[j]) {
        if (j == 1) {
          intestinal[j+1] <- intestinal[j+1] + intestinal[j]/2
          intestinal[j] = intestinal[j]/2
        } # 确保不会越界
        else {
          # 向前移动
          intestinal[j-1] <- intestinal[j-1] + intestinal[j]/2
          intestinal[j+1] <- intestinal[j+1] + intestinal[j]/2
          intestinal[j] = 0
        }
      }
    }
  }
}

# 4. 绘制结果
barplot(intestinal, main="小肠不同部位食物分布", xlab="小肠位置", ylab="食物量")
