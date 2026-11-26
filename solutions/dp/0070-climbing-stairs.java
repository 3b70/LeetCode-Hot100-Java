class Solution {
    public int climbStairs(int n) {
        int a=1,b=1;
        for(int i=2;i<=n;i++) { int next=a+b; a=b; b=next; } // 两个旧状态滚动到下一阶
        return b;
    }
}
