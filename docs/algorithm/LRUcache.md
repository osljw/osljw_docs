
# LRUCache

```c++
class LRUCache {
public:
    LRUCache(int capacity): capacity(capacity) {
        
    }
    
    int get(int key) {
        auto it = hmap.find(key);
        if(it != hmap.end()) {
            put(key, it->second->second);
            return it->second->second;
        }
        return -1;
    }
    
    void put(int key, int value) {
        auto it = hmap.find(key);
        if(it != hmap.end()) {
            l.erase(it->second);
        } else if (hmap.size() >= capacity) {
            // 超过缓存， 移除双向链表末尾的数据
            hmap.erase(l.back().first);
			l.pop_back();
        }
        l.push_front({key, value});
        hmap[key] = l.begin();
    }
    
private:
    int capacity;
    std::list<std::pair<int, int>> l;
    std::unordered_map<int, std::list<std::pair<int, int>>::iterator> hmap;
};
```

- std::list 双向链表， 最近存储的移动到表头