import java.util.*;
class Solution {
    public List<Integer> spiralOrder(int[][] matrix) {
        List<Integer> ans=new ArrayList<>();
        int top=0,bottom=matrix.length-1,left=0,right=matrix[0].length-1;
        while(top<=bottom && left<=right) {
            for(int j=left;j<=right;j++) ans.add(matrix[top][j]); top++;
            for(int i=top;i<=bottom;i++) ans.add(matrix[i][right]); right--;
            // 检查边界，避免最后一行或一列被重复遍历
            if(top<=bottom) { for(int j=right;j>=left;j--) ans.add(matrix[bottom][j]); bottom--; }
            if(left<=right) { for(int i=bottom;i>=top;i--) ans.add(matrix[i][left]); left++; }
        }
        return ans;
    }
}
