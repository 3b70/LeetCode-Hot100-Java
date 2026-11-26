import java.util.*;
class Solution {
    public List<List<Integer>> permute(int[] nums) {
        List<List<Integer>> ans=new ArrayList<>();
        dfs(nums,new boolean[nums.length],new ArrayList<>(),ans); return ans;
    }
    private void dfs(int[] a,boolean[] used,List<Integer> path,List<List<Integer>> ans) {
        if(path.size()==a.length) { ans.add(new ArrayList<>(path)); return; }
        for(int i=0;i<a.length;i++) {
            if(used[i]) continue;
            used[i]=true; path.add(a[i]); // 做选择
            dfs(a,used,path,ans);
            path.remove(path.size()-1); used[i]=false; // 撤销选择
        }
    }
}
