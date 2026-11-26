class Solution {
    public boolean isSymmetric(TreeNode root) { return root==null || mirror(root.left,root.right); }
    private boolean mirror(TreeNode a,TreeNode b) {
        if(a==null || b==null) return a==b; // 只有同时为空才匹配
        return a.val==b.val && mirror(a.left,b.right) && mirror(a.right,b.left);
    }
}
