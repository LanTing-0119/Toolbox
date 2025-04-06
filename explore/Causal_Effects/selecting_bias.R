
# 情景: 人群中开展随机对照试验研究吃芥末是否影响其生存率；入组假设总体人群中有2/3的人都有心脏病，1/3没有；而有心脏病的人吃了芥末可能更容易死亡；死亡的患者更容易失访
# 想证明的观点: 在数据设计的时候假设吃芥末不会造成提高死亡率(图1的无心脏病列)；失访由于不具有可互换性因此会导致偏倚 → 如果只分析未失访的患者的生存率会发现汇总的话吃芥末会增加死亡率(图1的总体列)


set.seed(1234)

n <- 100000  # 总样本数

# 1. 基线特征
heart_disease <- rbinom(n, 1, 2/3)  # 2/3 有心脏病
mustard <- rbinom(n, 1, 0.5)        # 随机分配吃芥末

# 2. 生存概率模型（logit 模型）
# 假设：吃芥末对无心脏病者无影响，但对有心脏病者有负效应
linear_pred <- -1 +
  0.5 * (1 - heart_disease) +       # 无心脏病的人生存率更高
  (-1.5) * (heart_disease * mustard) # 心脏病 + 吃芥末 → 更高死亡风险

prob_survival <- plogis(linear_pred)
survived <- rbinom(n, 1, prob_survival)

# 3. 加入失访（失访与心脏病 & 芥末有关）
# 假设有心脏病并吃芥末的人更可能失访
prob_missing <- plogis(-2 + 1.5 * heart_disease * mustard)
missing <- rbinom(n, 1, prob_missing)

# 设置死亡状态为 NA（失访）
outcome <- ifelse(missing == 1, NA, survived)

# 4. 构建数据框
df <- data.frame(
  heart_disease = heart_disease,
  mustard = mustard,
  linear_pred = linear_pred,
  prob_survival = prob_survival,
  survived = survived,
  prob_missing = prob_missing,
  missing = missing,
  outcome = outcome
)

# 查看前几行
head(df)

# 统计检验吃芥末和心脏病分布无关联
# 四格表：吃芥末 vs 心脏病
table_mh <- table(df$mustard, df$heart_disease)
colnames(table_mh) <- c("无心脏病", "有心脏病")
rownames(table_mh) <- c("不吃芥末", "吃芥末")
table_mh

# 卡方检验：检验是否独立
chisq_test <- chisq.test(table_mh)
chisq_test

library(dplyr)
library(ggplot2)

# ---- 公共数据准备 ----
df_clean <- na.omit(df)

# 为比例图准备 group 字段（去除 NA）
df_prop_clean <- bind_rows(
  df_clean %>% mutate(group = "总体"),
  df_clean %>% mutate(group = ifelse(heart_disease == 1, "有心脏病", "无心脏病"))
)

# 为比例图准备 group 字段（保留 NA）
df_prop_full <- bind_rows(
  df %>% mutate(group = "总体"),
  df %>% mutate(group = ifelse(heart_disease == 1, "有心脏病", "无心脏病"))
)

# ---- 百分比数据准备函数 ----
prep_label_data <- function(df_plot) {
  df_plot %>%
    group_by(group, mustard, outcome) %>%
    summarise(n = n(), .groups = "drop") %>%
    group_by(group, mustard) %>%
    mutate(
      prop = n / sum(n),
      label = paste0(round(prop * 100,1), "%")
    )
}

# 标注数据
label_p1 <- prep_label_data(df_prop_clean)
label_p2 <- prep_label_data(df_prop_full)

# ---- 图1：按比例（失访已剔除） ----
p1 <- ggplot(df_prop_clean, aes(x = factor(mustard), fill = factor(outcome))) +
  geom_bar(position = "fill") +
  geom_text(data = label_p1,
            aes(x = factor(mustard), y = prop, label = label, group = outcome),
            position = position_stack(vjust = 0.5),
            color = "white", size = 4) +
  facet_wrap(~ group) +
  labs(
    x = "是否吃芥末",
    fill = "生存状态 \n (1=存活, 0=死亡)",
    y = "比例",
    title = "【1】按比例（失访已剔除）"
  )

# ---- 图2：按比例（包含失访） ----
p2 <- ggplot(df_prop_full, aes(x = factor(mustard), fill = factor(outcome))) +
  geom_bar(position = "fill") +
  geom_text(data = label_p2,
            aes(x = factor(mustard), y = prop, label = label, group = outcome),
            position = position_stack(vjust = 0.5),
            color = "white", size = 4) +
  facet_wrap(~ group) +
  labs(
    x = "是否吃芥末",
    fill = "生存状态 \n (1=存活, 0=死亡/失访)",
    y = "比例",
    title = "【2】按比例（包含失访）"
  )

# 5. 构建频数数据（去除 NA）
df_freq_clean <- df_prop_clean %>%
  group_by(group, mustard, outcome) %>%
  summarise(n = n(), .groups = "drop")

p3 <- ggplot(df_freq_clean, aes(x = factor(mustard), y = n, fill = factor(outcome))) +
  geom_bar(stat = "identity", position = "stack") +
  geom_text(aes(label = n),
            position = position_stack(vjust = 0.5),
            color = "white", size = 4) +
  facet_wrap(~ group) +
  labs(
    x = "是否吃芥末",
    y = "人数",
    fill = "生存状态 \n (1=存活, 0=死亡)",
    title = "【3】按人数（失访已剔除）"
  )

# 6. 构建频数数据（保留 NA）
df_freq_full <- df_prop_full %>%
  group_by(group, mustard, outcome) %>%
  summarise(n = n(), .groups = "drop")

p4 <- ggplot(df_freq_full, aes(x = factor(mustard), y = n, fill = factor(outcome))) +
  geom_bar(stat = "identity", position = "stack") +
  geom_text(aes(label = n),
            position = position_stack(vjust = 0.5),
            color = "white", size = 4) +
  facet_wrap(~ group) +
  labs(
    x = "是否吃芥末",
    y = "人数",
    fill = "生存状态 \n (1=存活, 0=死亡/失访)",
    title = "【4】按人数（包含失访）"
  )

# 如果你要一起展示，使用 patchwork 包
library(patchwork)
(p1 | p2) / (p3 | p4)
