

# 01背包
- 容量C的背包
- 第i件物品体积为v[i], 价值为w[j]，每个物品只有一件

求解： 背包能容纳的最大价值

$ dp[i][j] $: 只在前i件物品中选取，背包容量为j时所能获取的最大价值

```c++
for (int i = 0; i < C; i++) {
    dp[0][i] = i >= v[0] ? w[0] : 0;
}

for (int i = 1; i < n; i++) {
    for (int j = 0; j <= C; j++) {
        if (j < v[i]) {
            dp[i][j] = dp[i-1][j];
        } else {
            dp[i][j] = max(dp[i-1][j], dp[i-1][j - v[i]] + w[j]);
        }
    }
}
```

空间优化(注意内层for循环逆序）：

```c++
for (int i = 0; i < n; i++) {
    for (int j = C; j >= v[i]; j--) {
        dp[j] = max(dp[j], dp[j - v[i]] + w[j];
    }
}
```


> leetcode
- 416. 分割等和子集 https://leetcode-cn.com/problems/partition-equal-subset-sum/


# 完全背包
- 容量V的背包
- 第i件物品体积为v[i], 价值为w[j]，每个物品有无数件


> leetcode
- 322. 零钱兑换 https://leetcode-cn.com/problems/coin-change/