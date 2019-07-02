---
layout:     post
title:      "jekyll blog"
date:       2018-12-11 19:00:00
author:     "ljw"
header-img: "img/post-bg-2015.jpg"
catalog: true
tags:
    - 算法
---

# 226. Invert Binary Tree
使用栈
```c++
/**
 * Definition for a binary tree node.
 * struct TreeNode {
 *     int val;
 *     TreeNode *left;
 *     TreeNode *right;
 *     TreeNode(int x) : val(x), left(NULL), right(NULL) {}
 * };
 */
class Solution {
public:
    TreeNode* invertTree(TreeNode* root) {
        if(root == nullptr) return nullptr;
        
        stack<TreeNode*> stk;
        stk.push(root);
        while(!stk.empty()) {
            TreeNode* p = stk.top();
            stk.pop();
            if(p) {
                stk.push(p->left);
                stk.push(p->right);
                swap(p->left, p->right);
            }
        }
        return root;
    }
};
```

使用队列
```c++
class Solution {
public:
    TreeNode* invertTree(TreeNode* root) {
        if(root == nullptr) return nullptr;
        
        queue<TreeNode*> q;
        q.push(root);
        while(!q.empty()) {
            TreeNode* p = q.front();
            q.pop();
            if(p->left != nullptr) q.push(p->left);
            if(p->right != nullptr) q.push(p->right);
            
            swap(p->left, p->right);
        }
        return root;
    }
};
```