import java.util.*;
class Solution {
    private int index;
    private Map<Integer,Integer> positions;
    public TreeNode buildTree(int[] preorder,int[] inorder) {
        index=0; positions=new HashMap<>();
        for(int i=0;i<inorder.length;i++) positions.put(inorder[i],i);
        return build(preorder,0,inorder.length-1);
    }
    private TreeNode build(int[] pre,int l,int r) {
        if(l>r) return null;
        TreeNode node=new TreeNode(pre[index++]); int mid=positions.get(node.val);
        node.left=build(pre,l,mid-1); // 先序游标先消费完整左树
        node.right=build(pre,mid+1,r);
        return node;
    }
}
