

# Heap


## 向下调整法

https://leetcode-cn.com/circle/discuss/pxypC8/

```c++

// 大根堆
void down_adjust(vector<int>& nums, int i, int end) {
    int left = 2 * i + 1;
    while (left <= end) {
        if (left + 1 <= end && nums[left] < nums[left + 1]) left++;
        if (nums[i] >= nums[left]) break;
        swap(nums[i], nums[left]);
        i = left;
        left = 2 * i + 1;
    }
}


void build_heap(vector<int>& nums) {
    int n = nums.size();
    for (int i = n - 1; i >= 0; i--) 
        down_adjust(nums, i, n - 1);
}

// 大根堆 -> 从小到大排序
void heap_sort(vector<int>& nums) {
    build_heap(nums);

    int n = nums.size();
    for (int i = n - 1; i >= 0; i--) {
        swap(nums[i], nums[0]);
        down_adjust(nums, 0, i - 1);
    }
}

```


# Tire

https://leetcode-cn.com/problems/longest-word-in-dictionary

```c++
struct TireNode {
public:
    TireNode() {}
    ~TireNode() {
        for (auto ele : child) {
            delete ele.second;
        }
    }

    unordered_map<char, TireNode*> child;
    bool is_word = false;
};

class Tire {
public:
    Tire() {
        root = new TireNode();
    }
    ~Tire() {
        delete root;
    }

    void insert(string& word) {
        TireNode* cur = root;
        for (auto c : word) {
            if (!cur->child[c]) {
                cur->child[c] = new TireNode();
            }
            cur = cur->child[c];            
        }
        cur->is_word = true;
    }

    bool search(string& word) {
        TireNode* cur = root;
        for (auto c : word) {
            cur = cur->child[c];
            if (!cur || !cur->is_word) {
                return false;
            }
        }
        return true;
    }

private:
    TireNode* root;
};



class Solution {
public:

    string longestWord(vector<string>& words) {

        Tire tree;
        for (auto& word : words) {
            tree.insert(word);
        }

        int len = 0;
        string ans;
        for (auto& word : words) {
            if (word.size() >= len && tree.search(word)) {
                //cout << "ans = " << ans << ", word = " << word << endl;
                if (word.size() == len && ans < word) {
                    continue;
                } 
                ans = word;
                len = word.size();
            } 
        }
        return ans;
    }
};
```