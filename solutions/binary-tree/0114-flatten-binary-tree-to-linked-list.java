class Solution {
    public void flatten(TreeNode root) {
        for(TreeNode cur=root;cur!=null;cur=cur.right) {
            if(cur.left!=null) {
                TreeNode pre=cur.left;
                while(pre.right!=null) pre=pre.right;
                pre.right=cur.right; // 原右树接到左树末端
                cur.right=cur.left; cur.left=null;
            }
        }
    }
}
