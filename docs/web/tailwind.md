
# tailwind 布局


## 同一行， 一个组件位于最左侧， 一个组件位于最右侧
```jsx
<div className="flex justify-between items-center">
  <div className="flex items-center">
    {/* 左侧组件 */}
    {/* 在这里放置您的左侧组件代码 */}
  </div>
  
  <div className="flex items-center">
    {/* 右侧组件 */}
    {/* 在这里放置您的右侧组件代码 */}
  </div>
</div>
```
