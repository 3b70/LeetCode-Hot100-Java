import java.util.*;
class Solution {
    public int[][] merge(int[][] intervals) {
        Arrays.sort(intervals,(a,b)->Integer.compare(a[0],b[0]));
        List<int[]> ans=new ArrayList<>();
        for(int[] cur:intervals) {
            if(ans.isEmpty() || ans.get(ans.size()-1)[1]<cur[0]) {
                ans.add(new int[]{cur[0],cur[1]}); // 复制端点，避免改写原区间内容
            } else {
                int[] last=ans.get(ans.size()-1);
                last[1]=Math.max(last[1],cur[1]); // 只扩大最后区间的右端点
            }
        }
        return ans.toArray(new int[ans.size()][]);
    }
}
