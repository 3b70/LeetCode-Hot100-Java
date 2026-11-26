import java.util.*;
class Solution {
    public int subarraySum(int[] nums,int k) {
        Map<Integer,Integer> count=new HashMap<>();
        count.put(0,1); // 空前缀用于匹配从下标0开始的子数组
        int sum=0,ans=0;
        for(int x:nums) {
            sum+=x;
            ans+=count.getOrDefault(sum-k,0); // 统计所有匹配的历史前缀
            count.put(sum,count.getOrDefault(sum,0)+1);
        }
        return ans;
    }
}
