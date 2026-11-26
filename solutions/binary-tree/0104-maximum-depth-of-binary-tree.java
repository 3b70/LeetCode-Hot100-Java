class Solution {
    public int maxDepth(TreeNode root) {
        if(root==null) return 0; // 递归终点：空树深度为0
        int left=maxDepth(root.left),right=maxDepth(root.right);
        return Math.max(left,right)+1; // 当前根贡献一层
    }
}
