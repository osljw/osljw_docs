
# 面试题 08.11. 硬币

https://leetcode-cn.com/problems/coin-lcci/

给定数量不限的硬币，币值为25分、10分、5分和1分，编写代码计算n分有几种表示法。(结果可能会很大，你需要将结果模上1000000007)

dp[j]: 总额为j有多少种组合方法

```c++
class Solution {
public:
    int waysToChange(int n) {
        vector<int> dp(n+1, 0);
        vector<int> coins = {1, 5, 10, 25};
        dp[0] = 1;
        for(int i = 0; i < 4; i++){
            for(int j = coins[i]; j <= n; j++){
                dp[j] = (dp[j] + dp[j-coins[i]]) % 1000000007;
            }
        }
        return dp[n];
    }
};
```

# 322. 零钱兑换

https://leetcode-cn.com/problems/coin-change/

给定不同面额的硬币 coins 和一个总金额 amount。编写一个函数来计算可以凑成总金额所需的最少的硬币个数。如果没有任何一种硬币组合能组成总金额，返回 -1。


```c++
class Solution {
public:
    int coinChange(vector<int>& coins, int amount) {
        vector<int> dp(amount + 1, amount + 1);
        dp[0] = 0;
        for (int i = 1; i <= amount; i++) {
            for (int j = 0; j < coins.size(); j++) {
                if (coins[j] <= i) {
                    dp[i] = min(dp[i], dp[i - coins[j]] + 1);
                }
            }
        }
        return dp[amount] > amount? -1: dp[amount];
    }
};
```