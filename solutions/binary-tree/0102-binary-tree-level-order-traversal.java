import java.util.*;
class Solution {
    public List<List<Integer>> levelOrder(TreeNode root) {
        List<List<Integer>> ans=new ArrayList<>();
        if(root==null) return ans;
        Queue<TreeNode> q=new ArrayDeque<>(); q.offer(root);
        while(!q.isEmpty()) {
            int size=q.size(); List<Integer> row=new ArrayList<>();
            for(int i=0;i<size;i++) {
                TreeNode node=q.poll(); row.add(node.val);
                if(node.left!=null) q.offer(node.left);
                if(node.right!=null) q.offer(node.right);
            }
            ans.add(row); // 本层完成，队列只剩下一层
        }
        return ans;
    }
}
