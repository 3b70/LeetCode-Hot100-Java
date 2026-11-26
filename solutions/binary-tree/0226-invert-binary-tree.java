class Solution {
    public TreeNode invertTree(TreeNode root) {
        if(root==null) return null;
        TreeNode left=invertTree(root.left),right=invertTree(root.right);
        root.left=right; root.right=left; // 保存完两侧后再交换
        return root;
    }
}
