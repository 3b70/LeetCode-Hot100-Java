import java.util.*;
class Solution {
    public int kthSmallest(TreeNode root,int k) {
        Deque<TreeNode> stack=new ArrayDeque<>(); TreeNode cur=root;
        while(cur!=null || !stack.isEmpty()) {
            while(cur!=null) { stack.push(cur); cur=cur.left; }
            cur=stack.pop();
            if(--k==0) return cur.val; // 中序第k次弹出即第k小
            cur=cur.right;
        }
        throw new IllegalArgumentException("k超出节点数量");
    }
}
