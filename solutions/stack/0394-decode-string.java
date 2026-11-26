import java.util.*;
class Solution {
    public String decodeString(String s) {
        Deque<Integer> counts=new ArrayDeque<>();
        Deque<StringBuilder> parents=new ArrayDeque<>();
        StringBuilder cur=new StringBuilder(); int count=0;
        for(char c:s.toCharArray()) {
            if(c>='0' && c<='9') count=count*10+c-'0';
            else if(c=='[') {
                counts.push(count); parents.push(cur); count=0; cur=new StringBuilder();
            } else if(c==']') {
                int times=counts.pop(); StringBuilder parent=parents.pop();
                for(int i=0;i<times;i++) parent.append(cur); // 把本层展开结果接回父层
                cur=parent;
            } else cur.append(c);
        }
        return cur.toString();
    }
}
