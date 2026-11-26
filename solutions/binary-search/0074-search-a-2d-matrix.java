class Solution {
    public boolean searchMatrix(int[][] matrix,int target) {
        int n=matrix[0].length,l=0,r=matrix.length*n-1;
        while(l<=r) {
            int mid=l+(r-l)/2,value=matrix[mid/n][mid%n]; // 一维下标映射回行列
            if(value==target) return true;
            if(value<target) l=mid+1; else r=mid-1;
        }
        return false;
    }
}
