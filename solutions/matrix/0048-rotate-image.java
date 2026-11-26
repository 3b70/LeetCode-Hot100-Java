class Solution {
    public void rotate(int[][] matrix) {
        int n=matrix.length;
        for(int i=0;i<n;i++) for(int j=i+1;j<n;j++) {
            int t=matrix[i][j]; matrix[i][j]=matrix[j][i]; matrix[j][i]=t; // 主对角线转置
        }
        for(int[] row:matrix) {
            for(int l=0,r=n-1;l<r;l++,r--) {
                int t=row[l]; row[l]=row[r]; row[r]=t; // 行内镜像
            }
        }
    }
}
