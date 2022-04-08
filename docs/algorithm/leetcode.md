

- [leetcode](#leetcode)
- [二分法](#二分法)
- [链表类](#链表类)
- [字符串类](#字符串类)
  - [字符串前缀hash](#字符串前缀hash)
  - [双指针滑动窗口](#双指针滑动窗口)
  - [kmp](#kmp)
- [排列， 组合， 子集](#排列-组合-子集)
  - [下一个排列](#下一个排列)
  - [全排列， 子集](#全排列-子集)
- [排序](#排序)
- [位运算](#位运算)
- [单调栈](#单调栈)
- [数学](#数学)
  - [最大公约数gcd](#最大公约数gcd)
  - [最小公倍数lcm](#最小公倍数lcm)


# leetcode

# 二分法

技巧
- 取mid防止溢出 int mid = left + (right - left) / 2
- left, right取闭区间


旋转数组和二分法
- 求最小，最大（while使用left < right比较，返回left）
- 搜索特定值存在 （while 使用left <= right比较， while中等于时return）
- 搜索特定值的最小索引
- 旋转数组是否有重复元素

旋转数组最小值
153. 寻找旋转排序数组中的最小值 https://leetcode-cn.com/problems/find-minimum-in-rotated-sorted-array/
154. 寻找旋转排序数组中的最小值 II https://leetcode-cn.com/problems/find-minimum-in-rotated-sorted-array-ii/

旋转数组搜索， 判断存在

旋转数组搜索， 返回索引
面试题 10.03. 搜索旋转数组 https://leetcode-cn.com/problems/search-rotate-array-lcci/

```c++
class Solution {
public:
    int search(vector<int>& arr, int target) {
        int left = 0;
        int right = arr.size() - 1;

        while (left <= right) {
            
            if (arr[left] == target) {
                return left;
            }

            // 去除两端的重复值后， 才能保证arr[mid] >= arr[0]时， [0:mid]是有序的
            while(left + 1 <= right && arr[left + 1] == arr[left]) left++;
            while(right - 1 >= left && arr[right - 1] == arr[right]) right--;

            int mid = left + (right - left) / 2;

            if (arr[mid] == target) {
                right = mid;
            } else if (arr[mid] >= arr[0]) {
                if (target >= arr[0] && target < arr[mid]) {
                    right = mid - 1;
                } else {
                    left = mid + 1;
                }
            } else {
                if (target > arr[mid] && target <= arr[arr.size() - 1]) {
                    left = mid + 1;
                } else {
                    right = mid - 1;
                }
            }
        }

        return -1;
    }
};
```

# 链表类

技巧
- 设置辅助头节点： 头节点会被破坏的场景
- 快慢指针


# 字符串类

技巧
- 字符串前缀hash
- 字母异位词， 排序后字母相同，可以作为map的key
- 双指针滑动窗口
- 字符串翻倍


## 字符串前缀hash

```c++
string s;

int mod = 1e9 + 7;
int base = 31;
vector<int> prefix(n + 1);
vector<int> pow(n + 1);
pow[0] = 1;

for (int i = 1; i <= n; i++) {
    pow[i] = pow[i-1] * base % mod;
    prefix[i] = (prefix[i-1]*base + s[i-1] - 'a') % mod;
}

// 字符串s[i:j], 闭区间[i, j]的hash值为 
prefix[j + 1] - prefix[i] * pow[j - i + 1]

// pow[j - i + 1]中（j-i+1)的含义为字符串长度
// s[0:j] 对应的是 prefix[j + 1]
// s[0:i-1] 对应的是 prefix[i]
// s[i:j] 对应的是 prefix[j + 1] - prefix[i] * pow[j - i + 1]


((prefix[j + 1] - prefix[i] * pow[j - i + 1]) % mod + mod) % mod
```

## 双指针滑动窗口
- 给定窗口长度求解符合要求的窗口， 求解最大/小连续时一般滑动窗口
- [left, right] 闭区间维护窗口， while (right < n) 窗口向右移动
当right - left + 1 大于窗口长度时， 收缩左侧窗口


2024. 考试的最大困扰度 https://leetcode-cn.com/problems/maximize-the-confusion-of-an-exam/


## kmp
- PMT部分匹配表(Partial Match Table)： 字符串的前缀集合与后缀集合的交集中最长元素的长度  -> next数组
PMT右移一位

1392. 最长快乐前缀 https://leetcode-cn.com/problems/longest-happy-prefix/
```c++
class Solution {
public:
    string longestPrefix(string s) {
        int n = s.size();
        vector<int> next(n+1);

        int j = 0, k = -1;
        next[0] = -1;
        while (j < n){
            if (k == -1 || s[j] == s[k]) {
                j++;
                k++;
                next[j] = k;
            } else {
                k = next[k];
            }
        }

        return s.substr(0, next[n]);
    }
};
```

# 排列， 组合， 子集

技巧
- 子集问题， 可以用回溯法和枚举法， 
- 排列问题回溯时使用for循环， 子集问题不用for循环， 子集问题回溯两次， 放入和不放入



## 下一个排列 

下一个大的排列 eg:  47632
- 双指针
- 从右往左找到升序nums[left]（eg. 47632中的4）， 从右往左找第一个大于nums[left]的数（eg.47632中的6）， 交换nums[left]和nums[right], 对left+1之后进行逆序

题目
- 556. 下一个更大元素 III https://leetcode-cn.com/problems/next-greater-element-iii/



## 全排列， 子集

- 回溯法， 返回结果， for循环模拟树层， 递归模拟树深， 
- 全排列的一条结果是根节点到叶子节点， 子集的一条结果是根节点到叶子节点的前缀
- 有重复元素
  - for循环都从start开始， 
    - 全排列需要swap， 下一次从start+1开始
    - 子集从i+1开始， 需要提前排序
  - for循环时使用unordered_set进行树层去重

1.  全排列 https://leetcode-cn.com/problems/permutations/
2.  全排列 II https://leetcode-cn.com/problems/permutations-ii/

```c++
// 全排列 II
class Solution {
public:
    vector<vector<int>> permuteUnique(vector<int>& nums) {
        vector<vector<int>> ans;
        vector<int> path;

        backtrace(nums, 0, path, ans);
        return ans;
    }

    void backtrace(vector<int>& nums, int start, vector<int>& path, vector<vector<int>>& ans) {
        if (nums.size() == path.size()) {
            ans.push_back(path);
            return;
        }

        unordered_set<int> uniq;
        for (int i = start; i < nums.size(); i++) {
            // 树层去重
            if (uniq.count(nums[i])) continue;
            uniq.insert(nums[i]);

            // swap后，始终放入第start位置上的数
            // note1: swap
            swap(nums[start], nums[i]);
            path.push_back(nums[start]);
            // note2: start + 1 开始
            backtrace(nums, start + 1, path, ans);
            path.pop_back();
            swap(nums[start], nums[i]);
        }
    }
};
```


90. 子集 II https://leetcode-cn.com/problems/subsets-ii/

```c++
// 子集 II
class Solution {
public:
    vector<vector<int>> subsetsWithDup(vector<int>& nums) {
        // note1: 预排序
        sort(nums.begin(), nums.end());
        vector<vector<int>> ans;
        vector<int> path;
        backtrace(nums, 0, path, ans);
        return ans;
    }

    void backtrace(vector<int>& nums, int start, vector<int>& path, vector<vector<int>>& ans) {
        ans.push_back(path);

        unordered_set<int> uniq;
        for (int i = start; i < nums.size(); i++) {
            if (uniq.count(nums[i])) continue;
            uniq.insert(nums[i]);

            path.push_back(nums[i]);
            // note2: 从i+1开始
            backtrace(nums, i+1, path, ans);
            path.pop_back();
        }
    }
};
```



# 排序

技巧
- 逆序对的数量， 归并排序， 当合并有序左区间和有序右区间时， 从左区间选择最小元素时， 该元素对应的逆序对数量为p2 - (mid + 1) （mid+1为右区间的起始索引， p2为右区间下一个待归并的索引）
- 临位交换的最小次数等于逆序对数量


题目
- 剑指 Offer 51. 数组中的逆序对 https://leetcode-cn.com/problems/shu-zu-zhong-de-ni-xu-dui-lcof/



# 位运算

技巧
- 取最低位 n & 1
- 移除最低位的1 n & (n - 1)
- __builtin_popcount(val) 统计val的二进制中1的个数
- 长度为m， 从中选取n个进行判断， 可以进行枚举
```c++
for (int mask = 0;  mask < (1 << m); mask++) {
    for (int i = 0; i < m; i++) {
        if (mask & (1 << i)) {

        }
    }
}
```

剑指 Offer 56 - II. 数组中数字出现的次数 II https://leetcode-cn.com/problems/shu-zu-zhong-shu-zi-chu-xian-de-ci-shu-ii-lcof/



# 单调栈

技巧
- 在一维数组中对每一个数找到第一个比自己小/大的元素


# 数学

## 最大公约数gcd
```c++
// 辗转相除法
int gcd(int a, int b) {
    while (b != 0) {
        int t = b;
        b = a % b;
        a = t;
    }
    return a;
}
```
gcd(a,0)=a
gcd(a,1)=1
因此当两个数中有一个为0时，gcd是不为0的那个整数

## 最小公倍数lcm
```
int lcm(int a, int b) {
    return a * b / gcd(a, b);
}
```