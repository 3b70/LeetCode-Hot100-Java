class Solution {
    private int best;
    public int maxPathSum(TreeNode root) { best=Integer.MIN_VALUE; gain(root); return best; }
    private int gain(TreeNode node) {
        if(node==null) return 0;
        int l=Math.max(0,gain(node.left)),r=Math.max(0,gain(node.right));
        best=Math.max(best,node.val+l+r); // 在当前节点把两条分支接起来
        return node.val+Math.max(l,r); // 父节点只能接上一条分支
    }
}
