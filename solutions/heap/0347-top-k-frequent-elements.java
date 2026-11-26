import java.util.*;
class Solution {
    public int[] topKFrequent(int[] nums,int k) {
        Map<Integer,Integer> count=new HashMap<>();
        for(int x:nums) count.put(x,count.getOrDefault(x,0)+1);
        List<List<Integer>> buckets=new ArrayList<>();
        for(int i=0;i<=nums.length;i++) buckets.add(new ArrayList<>());
        for(Map.Entry<Integer,Integer> e:count.entrySet()) buckets.get(e.getValue()).add(e.getKey());
        int[] ans=new int[k]; int index=0;
        for(int f=nums.length;f>=1 && index<k;f--) {
            for(int x:buckets.get(f)) {
                ans[index++]=x;
                if(index==k) break; // 收满k种后不再写入
            }
        }
        return ans;
    }
}
