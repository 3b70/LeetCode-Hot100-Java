class Solution {
    public int majorityElement(int[] nums) {
        int candidate=0,count=0;
        for(int x:nums) {
            if(count==0) candidate=x; // 之前的票已两两抵消
            count+=(x==candidate)?1:-1;
        }
        return candidate;
    }
}
