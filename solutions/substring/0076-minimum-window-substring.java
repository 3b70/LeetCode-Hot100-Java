class Solution {
    public String minWindow(String s,String t) {
        if(t.isEmpty()) return "";
        int[] need=new int[128];
        for(char c:t.toCharArray()) need[c]++;
        int missing=t.length(),left=0,start=0,best=Integer.MAX_VALUE;
        for(int right=0;right<s.length();right++) {
            char c=s.charAt(right);
            if(need[c]>0) missing--;
            need[c]--; // 负数代表窗口中有富余
            while(missing==0) {
                if(right-left+1<best) { best=right-left+1; start=left; }
                char out=s.charAt(left++);
                need[out]++;
                if(need[out]>0) missing++; // 移出了必要字符，覆盖失效
            }
        }
        return best==Integer.MAX_VALUE ? "" : s.substring(start,start+best);
    }
}
