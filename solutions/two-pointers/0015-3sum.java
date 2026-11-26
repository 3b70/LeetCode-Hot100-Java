import java.util.*;
class Solution {
    public List<List<Integer>> threeSum(int[] nums) {
        Arrays.sort(nums);
        List<List<Integer>> ans=new ArrayList<>();
        for(int i=0;i<nums.length-2;i++) {
            if(i>0 && nums[i]==nums[i-1]) continue; // 固定值去重
            if(nums[i]>0) break;
            int l=i+1,r=nums.length-1;
            while(l<r) {
                int sum=nums[i]+nums[l]+nums[r];
                if(sum<0) l++;
                else if(sum>0) r--;
                else {
                    ans.add(Arrays.asList(nums[i],nums[l],nums[r]));
                    int a=nums[l],b=nums[r];
                    // 同一固定值下，跳过重复的左右值
                    while(l<r && nums[l]==a) l++;
                    while(l<r && nums[r]==b) r--;
                }
            }
        }
        return ans;
    }
}
