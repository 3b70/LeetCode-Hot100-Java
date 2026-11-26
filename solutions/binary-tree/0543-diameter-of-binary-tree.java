class Solution {
    private int best;
    public int diameterOfBinaryTree(TreeNode root) { best=0; height(root); return best; }
    private int height(TreeNode node) {
        if(node==null) return 0;
        int l=height(node.left),r=height(node.right);
        best=Math.max(best,l+r); // 当前节点连接左右分支的路径
        return Math.max(l,r)+1; // 向父节点只返回一条分支
    }
}
