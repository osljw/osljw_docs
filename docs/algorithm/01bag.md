
- [01背包](#01背包)
- [完全背包](#完全背包)
  - [1. 背包能容纳的最大价值](#1-背包能容纳的最大价值)
  - [2. 背包恰好装满, 所能容纳的最小价值](#2-背包恰好装满-所能容纳的最小价值)
  - [3. 背包恰好装满, 所有的方案数](#3-背包恰好装满-所有的方案数)
- [01分组背包](#01分组背包)
- [背包总结](#背包总结)


# 01背包
- 容量C的背包
- 第i件物品体积为v[i], 价值为w[j]，每个物品只有一件

求解： 
- 背包能容纳的最大价值
- 背包恰好装满, 所能容纳的最小价值（特例判断能否装满）
  - （416. 分割等和子集 https://leetcode-cn.com/problems/partition-equal-subset-sum/）
- 背包恰好装满，所有的方案数
  -  （494. 目标和 https://leetcode-cn.com/problems/target-sum/）

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
            dp[i][j] = max(dp[i-1][j], dp[i-1][j - v[i]] + w[i]);
        }
    }
}
```

空间优化(注意内层for循环逆序）：

```c++
for (int i = 0; i < n; i++) {
    for (int j = C; j >= v[i]; j--) {
        dp[j] = max(dp[j], dp[j - v[i]] + w[i];
    }
}
```



# 完全背包
- 容量V的背包
- 第i件物品体积为v[i], 价值为w[j]，每个物品有无数件

求解
- 背包能容纳的最大价值
- 背包恰好装满，所能容纳的最小价值（特例判断能否装满）
  - （322. 零钱兑换 https://leetcode-cn.com/problems/coin-change/）
- 背包恰好装满，所有的方案数
   - （518. 零钱兑换 II https://leetcode-cn.com/problems/coin-change-2/）


## 1. 背包能容纳的最大价值
$dp[i][j]$: 只在前i件物品中选取，背包容量为j时所能获取的最大价值

二维递推
$$ dp[i][j]=max(dp[i−1][j], min_k(dp[i−1][j−k∗v[i]]+k∗w[i])) $$

一维优化
$$ dp[j]=max(dp[j], dp[j-v[i]] + w[i])$$

## 2. 背包恰好装满, 所能容纳的最小价值
$dp[i][j]$: 只在前i件物品中选取，背包装满体积为j时，最少的价值

二维递推
$$ dp[i][j] = min(dp[i-1][j], min_k(dp[i-1][j-k*v[i]] + k * w[i])) $$

一维优化
$$dp[j] = min(dp[j], dp[j-v[i]] + w[i])$$

- 322. 零钱兑换 https://leetcode-cn.com/problems/coin-change/

dp[i][j]: 只在前i件硬币中选取， 硬币的面值作为体积， 每枚硬币的价值为1 => 背包恰好装满，最少的价值

```c++
class Solution {
public:
    int coinChange(vector<int>& coins, int amount) {
        int n = coins.size();

        const int INF = INT_MAX / 2;
        vector<int> dp(amount + 1, INF);
        dp[0] = 0;

        for (int i = 0; i < n; i++) {
            for (int j = coins[i]; j <= amount; j++) {
                dp[j] = min(dp[j], dp[j - coins[i]] + 1);
            }
        }

        return dp[amount] == INF ? -1 : dp[amount];
    }
};
```

## 3. 背包恰好装满, 所有的方案数


- 518. 零钱兑换 II https://leetcode-cn.com/problems/coin-change-2

```c++
class Solution {
public:
    int change(int amount, vector<int>& coins) {
        int n = coins.size();

        vector<vector<int>> dp(n+1, vector<int>(amount+1));

        dp[0][0] = 1;
        for (int i = 1; i <= n; i++) {
            for (int j = 0; j <= amount; j++) {
                dp[i][j] = dp[i-1][j];
                for (int k = 1; k * coins[i-1] <= j; k++) {
                    dp[i][j] += dp[i-1][j-k*coins[i-1]];
                }
            }
        }
        return dp[n][amount];
    }
};
```

一维优化
```c++
class Solution {
public:
    int change(int amount, vector<int>& coins) {
        int n = coins.size();
        vector<int> dp(amount+1);

        dp[0] = 1;
        for (int i = 0; i < n; i++) {
            for (int j = coins[i]; j <= amount; j++) {
                dp[j] += dp[j-coins[i]];
            }
        }
        return dp[amount];
    }
};
```

# 01分组背包
- 容量V的背包
- 有m组物品， 第i组的第j件物品体积为v[i][j], 价值为w[i][j]

$ dp[i][j] $: 只在前i组中选取，背包容量为j时所能获取的最大价值

二维递推
$$ dp[i][j] = max(dp[i][j], max_k(dp[i-1][j-v[i][k]] + w[i][k])) $$




# 背包总结

相同点
1. 01背包和完全背包均用两层循环，外循环为物品， 内循环为价值
2. 01背包和完全背包都能进行一维优化， 求解问题用max（最大价值）， min（最小价值）， +（组合数）

不同点
1. 01背包物品只能选择一次， 完全背包物品选择不限次数
2. 01背包一维优化内层循环用倒序， 完全背包用正序

