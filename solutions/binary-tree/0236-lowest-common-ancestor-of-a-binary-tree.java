class Solution {
    public TreeNode lowestCommonAncestor(TreeNode root,TreeNode p,TreeNode q) {
        if(root==null || root==p || root==q) return root;
        TreeNode l=lowestCommonAncestor(root.left,p,q),r=lowestCommonAncestor(root.right,p,q);
        if(l!=null && r!=null) return root; // 两侧各找到一个目标
        return l!=null?l:r; // 单侧找到的结果继续向上传递
    }
}
