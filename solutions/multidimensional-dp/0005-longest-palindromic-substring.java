class Solution {
    public String longestPalindrome(String s) {
        int n=s.length(),start=0,best=0; boolean[][] pal=new boolean[n][n];
        for(int i=n-1;i>=0;i--) for(int j=i;j<n;j++) {
            pal[i][j]=s.charAt(i)==s.charAt(j) && (j-i<2 || pal[i+1][j-1]);
            if(pal[i][j] && j-i+1>best) { start=i; best=j-i+1; } // 保存最长区间
        }
        return s.substring(start,start+best);
    }
}
