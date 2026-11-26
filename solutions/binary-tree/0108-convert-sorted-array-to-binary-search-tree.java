class Solution {
    public TreeNode sortedArrayToBST(int[] nums) { return build(nums,0,nums.length-1); }
    private TreeNode build(int[] a,int l,int r) {
        if(l>r) return null; // 空区间对应空子树
        int m=l+(r-l)/2;
        TreeNode node=new TreeNode(a[m]);
        node.left=build(a,l,m-1); node.right=build(a,m+1,r);
        return node; // 返回构造好的子树根
    }
}
