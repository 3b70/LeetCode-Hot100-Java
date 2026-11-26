class Solution {
    public boolean searchMatrix(int[][] matrix,int target) {
        int i=0,j=matrix[0].length-1;
        while(i<matrix.length && j>=0) {
            if(matrix[i][j]==target) return true;
            if(matrix[i][j]>target) j--; // 当前列全部过大
            else i++; // 当前行全部过小
        }
        return false;
    }
}
