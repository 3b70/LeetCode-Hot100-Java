import java.util.*;
class Solution {
    public List<Integer> inorderTraversal(TreeNode root) {
        List<Integer> ans=new ArrayList<>(); dfs(root,ans); return ans;
    }
    private void dfs(TreeNode node,List<Integer> ans) {
        if(node==null) return; // 空子树没有待访问节点
        dfs(node.left,ans);
        ans.add(node.val); // 左子树完成后访问根
        dfs(node.right,ans);
    }
}
