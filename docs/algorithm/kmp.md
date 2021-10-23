

# kmp


模式字符串的前缀表：  

长度为n的模式字符串计作str[0:n]， 其对应的前缀表计作pre[0:n], 则pre[i]的含义为字符串sub_str[0:i]的相同前后缀长度

eg： str： aabaaf ，  pre： 010120， pre[4]=2 表示字符串aabaa的相同前后缀长度为2

next 数组含义：  


void getNext(int* next, const string& s){
    int j = -1;
    next[0] = j;
    for(int i = 1; i < s.size(); i++) { // 注意i从1开始
        while (j >= 0 && s[i] != s[j + 1]) { // 前后缀不相同了
            j = next[j]; // 向前回退
        }
        if (s[i] == s[j + 1]) { // 找到相同的前后缀
            j++;
        }
        next[i] = j; // 将j（前缀的长度）赋给next[i]
    }
}