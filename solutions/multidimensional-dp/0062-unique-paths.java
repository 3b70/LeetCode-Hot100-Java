import java.util.*;
class Solution {
    public int uniquePaths(int m,int n) {
        int[] dp=new int[n]; Arrays.fill(dp,1); // 第一行都只有沿右走这一条路线
        for(int i=1;i<m;i++) for(int j=1;j<n;j++) dp[j]+=dp[j-1]; // 上方旧状态加左方新状态
        return dp[n-1];
    }
}
