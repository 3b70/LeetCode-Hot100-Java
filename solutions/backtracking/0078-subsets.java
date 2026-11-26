import java.util.*;
class Solution {
    public List<List<Integer>> subsets(int[] nums) {
        List<List<Integer>> ans=new ArrayList<>(); dfs(nums,0,new ArrayList<>(),ans); return ans;
    }
    private void dfs(int[] a,int start,List<Integer> path,List<List<Integer>> ans) {
        ans.add(new ArrayList<>(path)); // 每个节点本身就是一个合法子集
        for(int i=start;i<a.length;i++) {
            path.add(a[i]); dfs(a,i+1,path,ans);
            path.remove(path.size()-1); // 回到本层状态，尝试下一个数
        }
    }
}
