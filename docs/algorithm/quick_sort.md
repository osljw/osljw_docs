
# 快速排序

```c++
void quickSort(vector<int>& nums, int left, int right) {
    if (left >= right) return;

    int q = partition(nums, left, right);
    quickSort(nums, left, q-1);
    quickSort(nums, q+1, right);
}

int partition(vector<int>& nums, int left, int right) {
    int base = left;
    while(left < right) {
        // 从右往左，寻找比基数小的数
        while(nums[right] >= nums[base] && left < right)
            right--;
        // 从左往右， 寻找比基数大的数
        while(nums[left] <= nums[base] && left < right) 
            left++;
        // 找到一大一小的情况下，交换两个数（只找到一个数，忽略）
        if(left < right) swap(nums[left], nums[right]);
    }
    // 交换基数和最后剩下的数（一定小于等于基数）
    swap(nums[base], nums[right]);
    return right;
}
```

- [left, right] 为闭区间索引
- 