import java.util.*;
class Solution {
    public List<List<Integer>> combinationSum(int[] candidates,int target) {
        Arrays.sort(candidates); List<List<Integer>> ans=new ArrayList<>();
        dfs(candidates,0,target,new ArrayList<>(),ans); return ans;
    }
    private void dfs(int[] a,int start,int remain,List<Integer> path,List<List<Integer>> ans) {
        if(remain==0) { ans.add(new ArrayList<>(path)); return; }
        for(int i=start;i<a.length;i++) {
            if(a[i]>remain) break; // 后续更大，不可能补足
            path.add(a[i]); dfs(a,i,remain-a[i],path,ans);
            path.remove(path.size()-1); // 撤销当前数
        }
    }
}
