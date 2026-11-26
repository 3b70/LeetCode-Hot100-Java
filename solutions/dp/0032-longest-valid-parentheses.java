class Solution {
    public int longestValidParentheses(String s) {
        int[] dp=new int[s.length()]; int best=0;
        for(int i=1;i<s.length();i++) {
            if(s.charAt(i)==')') {
                if(s.charAt(i-1)=='(') dp[i]=2+(i>=2?dp[i-2]:0);
                else {
                    int j=i-dp[i-1]-1; // 越过前一段合法串，寻找配对左括号
                    if(j>=0 && s.charAt(j)=='(') dp[i]=dp[i-1]+2+(j>=1?dp[j-1]:0);
                }
                best=Math.max(best,dp[i]);
            }
        }
        return best;
    }
}
