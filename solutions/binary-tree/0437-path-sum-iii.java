import java.util.*;
class Solution {
    public int pathSum(TreeNode root,int targetSum) {
        Map<Long,Integer> count=new HashMap<>(); count.put(0L,1);
        return dfs(root,0L,targetSum,count);
    }
    private int dfs(TreeNode node,long sum,int target,Map<Long,Integer> count) {
        if(node==null) return 0;
        sum+=node.val;
        int ans=count.getOrDefault(sum-target,0);
        count.put(sum,count.getOrDefault(sum,0)+1); // 只记录当前祖先路径
        ans+=dfs(node.left,sum,target,count)+dfs(node.right,sum,target,count);
        int remaining=count.get(sum)-1;
        if(remaining==0) count.remove(sum); else count.put(sum,remaining); // 撤销当前节点
        return ans;
    }
}
