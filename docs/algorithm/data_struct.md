

# Heap 堆


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


# Tire 字典树

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


# 并查集 UnionFind

- 路径压缩， Find时将节点尽可能直接挂到顶级父节点下
- 按秩合并， Union时将节点数少的树挂到节点数多的树下

代码模板
```c++
class UnionFind {
public:
    UnionFind(int len):parent(len), size(len), group_size(len) {
        for (int i = 0; i < len; i++) {
            parent[i] = i;
        }
    }

    int Find(int x) {
        // 路径压缩
        if (x != parent[x]) {
            parent[x] = Find(parent[x]);
        }
        return parent[x];
    }

    // void Union(int x, int y) {
    //     int px = Find(x);
    //     int py = Find(y);

    //     if (px == py) return;
    //     parent[px] = py;
    //     group_size--;
    // }

    int Union(int x, int y) {
        int px = Find(x);
        int py = Find(y);
        if (px == py) return 1;

        // 按秩合并，节点小的树合并到节点多的树
        if (size[px] > size[py]) {
            swap(px, py);
        }
        parent[px] = py;
        size[py] += size[px];
        group_size--;
        return 0;
    }

    int GroupSize() {
        return group_size;
    }

private:
    vector<int> parent;
    vector<int> size;
    int group_size;
};
```

剑指 Offer II 116. 省份数量 https://leetcode-cn.com/problems/bLyHh0/

```c++
class Solution {
public:
    int findCircleNum(vector<vector<int>>& isConnected) {
        int n = isConnected.size();

        UnionFind uf(n);

        for (int i = 0; i < n; i++) {
            for (int j = i + 1; j < n; j++) {
                if (isConnected[i][j]) {
                    uf.Union(i, j);
                }
            }
        }

        return uf.GroupSize();
    }
};
```


# DFA 确定有限自动机

- 有穷状态集合Q， 有穷结束状态集合F($F \in Q$)
- 有穷输入集合I
- 转移函数： 输入为当前状态和输入符号，输出为下一个状态

