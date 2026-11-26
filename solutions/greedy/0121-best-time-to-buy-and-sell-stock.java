class Solution {
    public int maxProfit(int[] prices) {
        int low=Integer.MAX_VALUE,best=0;
        for(int price:prices) {
            low=Math.min(low,price); // 压缩历史所有买入日
            best=Math.max(best,price-low);
        }
        return best;
    }
}
