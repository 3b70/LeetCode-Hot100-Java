from content import add
add(20,'只含三类括号的字符串，判断是否按类型及嵌套顺序完全配对。','"([])" → true；"([)]" → false',
'统计左右括号数量相同不能保证嵌套合法。','栈保存尚未闭合的左括号。遇左括号入栈；遇右括号必须与栈顶类型匹配，否则false；匹配则弹栈。最后栈为空才合法。栈的后进先出恰好对应最内层先闭合。',
'(入栈，再[入栈；]弹出[；)弹出(；结束空栈，true。([)]在遇)时栈顶是[，立即false。',
'O(n) 时间，每字符入出栈至多一次；O(n) 最坏栈空间。','弹栈前检查空；数量一致不够；结束还要检查剩余左括号。',r'''
import java.util.*;
class Solution {
    public boolean isValid(String s) {
        Deque<Character> stack=new ArrayDeque<>();
        for(char c:s.toCharArray()) {
            if(c=='(' || c=='[' || c=='{') stack.push(c);
            else {
                if(stack.isEmpty()) return false;
                char open=stack.pop();
                if((c==')' && open!='(')||(c==']' && open!='[')||(c=='}' && open!='{')) return false;
            }
        }
        return stack.isEmpty(); // 不能遗留未闭合的左括号
    }
}''','eq(new Solution().isValid("([])"),true); eq(new Solution().isValid("([)]"),false); eq(new Solution().isValid(")"),false); eq(new Solution().isValid("("),false);')
add(155,'设计栈，支持push、pop、top、getMin，每个操作常数时间。题目保证后三类操作调用时非空。','push(-2),push(0),push(-3),getMin()=-3,pop(),getMin()=-2',
'每次getMin遍历全栈要O(n)。','数据栈保存实际值，辅助栈在每一层保存从底到这一层的最小值。push时把min(新值,原最小)压入辅助栈；pop时两栈同步弹出。这样重复最小值也能正确恢复。',
'压-2后min栈[-2]；压0后顶部仍-2；压-3后顶部-3；弹一次后两个栈回退，最小恢复-2。',
'push/pop摊还O(1)时间（ArrayDeque扩容偶尔O(n)），getMin/top最坏O(1)；O(n)总空间，两个栈各保存n层状态。','重复最小值也必须有一层记录；两栈同步pop；空栈操作不在题目合法输入内。',r'''
import java.util.*;
class MinStack {
    private final Deque<Integer> data=new ArrayDeque<>(),mins=new ArrayDeque<>();
    public MinStack() {}
    public void push(int val) {
        data.push(val);
        mins.push(mins.isEmpty()?val:Math.min(val,mins.peek())); // 为本层保存最小值
    }
    public void pop() { data.pop(); mins.pop(); }
    public int top() { return data.peek(); }
    public int getMin() { return mins.peek(); }
}''','MinStack s=new MinStack(); s.push(-2); s.push(0); s.push(-3); eq(s.getMin(),-3); s.pop(); eq(s.top(),0); eq(s.getMin(),-2); s.push(-2); s.pop(); eq(s.getMin(),-2);')
add(394,'解码形如k[子串]的嵌套字符串，表示子串重复k次。输入合法，数字只代表重复次数。','"3[a2[c]]" → "accaccacc"',
'不断找最内层括号替换可以做，但频繁复制难以管理。','遇数字累积多位count；遇[把当前前缀和重复次数分别压栈，然后清空当前层；遇]弹出父层，重复追加当前层，再把父层设为当前字符串。普通字母直接追加。两栈对应一层嵌套上下文。',
'读3[保存次数3和空前缀；读a2[保存次数2和前缀a；读c]得到acc；外层]把acc重复3次，得到目标。',
'设L为最终长度、D为最大嵌套深度，保守O(n+LD)时间，字符可能跨多层复制；O(n+LD)保守空间上界（含各层缓冲与输出），不能简单宣称仅O(n)。','多位数用count*10+digit；进入新层count清0；嵌套时必须保留父层前缀。',r'''
import java.util.*;
class Solution {
    public String decodeString(String s) {
        Deque<Integer> counts=new ArrayDeque<>();
        Deque<StringBuilder> parents=new ArrayDeque<>();
        StringBuilder cur=new StringBuilder(); int count=0;
        for(char c:s.toCharArray()) {
            if(c>='0' && c<='9') count=count*10+c-'0';
            else if(c=='[') {
                counts.push(count); parents.push(cur); count=0; cur=new StringBuilder();
            } else if(c==']') {
                int times=counts.pop(); StringBuilder parent=parents.pop();
                for(int i=0;i<times;i++) parent.append(cur); // 把本层展开结果接回父层
                cur=parent;
            } else cur.append(c);
        }
        return cur.toString();
    }
}''','eq(new Solution().decodeString("3[a2[c]]"),"accaccacc"); eq(new Solution().decodeString("10[a]"),"aaaaaaaaaa"); eq(new Solution().decodeString("abc3[cd]xyz"),"abccdcdcdxyz");')
add(739,'对每天温度，求还要等待多少天才出现严格更高的温度；之后没有更高则0。','[73,74,75,71,69,72,76,73] → [1,1,4,2,1,1,0,0]',
'每个位置往后找第一个更大，最坏O(n²)。','单调栈存还未找到答案的日期下标，对应温度从底到顶非递增。当前温度严格高于栈顶时弹出旧日期p，答案i-p；循环处理所有被当前温度解决的日期，最后当前下标入栈。',
'第1天74解决第0天73，等待1；第5天72依次解决69、71，等待1和2；第6天76解决72、75，等待1和4。',
'O(n) 时间，每个下标入出栈一次；O(n) 栈空间，另有O(n)输出。','相等温度不算更暖；栈存下标不是温度；未弹出的答案保留默认0。',r'''
import java.util.*;
class Solution {
    public int[] dailyTemperatures(int[] temperatures) {
        int[] ans=new int[temperatures.length]; Deque<Integer> stack=new ArrayDeque<>();
        for(int i=0;i<temperatures.length;i++) {
            while(!stack.isEmpty() && temperatures[i]>temperatures[stack.peek()]) {
                int p=stack.pop(); ans[p]=i-p; // 当前日是旧日期遇到的第一个更暖日
            }
            stack.push(i);
        }
        return ans;
    }
}''','eq(new Solution().dailyTemperatures(new int[]{73,74,75,71,69,72,76,73}),new int[]{1,1,4,2,1,1,0,0}); eq(new Solution().dailyTemperatures(new int[]{30,30}),new int[]{0,0}); eq(new Solution().dailyTemperatures(new int[]{50}),new int[]{0});')
add(84,'柱状图每根宽1，找连续若干柱可围成的最大矩形面积。高度非负。','[2,1,5,6,2,3] → 10',
'对每段枚举最低高度，O(n²)；需要快速确定每根柱的左右更矮边界。','单调栈存高度非递减的下标。遇更矮柱时，弹出高度h，它的右边界是i，左边界是弹出后的栈顶，宽度i-left-1。末尾额外处理虚拟高度0清栈。相等高度允许留栈，较早的相等柱最终获得完整宽度。',
'读到下标4高度2时，弹出6，宽1面积6；再弹5，此时栈顶下标1，宽4-1-1=2，面积10；最后哨兵清栈，没有超过10。',
'O(n) 时间，每个下标入出栈至多一次；O(n) 栈空间。','宽度要减1；弹出后再读左边界；末尾须清栈，否则递增数组答案缺失。',r'''
import java.util.*;
class Solution {
    public int largestRectangleArea(int[] heights) {
        Deque<Integer> stack=new ArrayDeque<>(); int best=0,n=heights.length;
        for(int i=0;i<=n;i++) {
            int h=i==n?0:heights[i]; // 末尾虚拟0触发所有正高度结算
            while(!stack.isEmpty() && heights[stack.peek()]>h) {
                int height=heights[stack.pop()];
                int left=stack.isEmpty()?-1:stack.peek();
                best=Math.max(best,height*(i-left-1));
            }
            if(i<n) stack.push(i); // 不把虚拟下标压栈
        }
        return best;
    }
}''','eq(new Solution().largestRectangleArea(new int[]{2,1,5,6,2,3}),10); eq(new Solution().largestRectangleArea(new int[]{2,2}),4); eq(new Solution().largestRectangleArea(new int[]{0}),0); eq(new Solution().largestRectangleArea(new int[]{1,2,3}),4);')
add(215,'返回数组按降序排列的第k个元素，重复元素分别计数，1≤k≤n。','[3,2,1,5,6,4], k=2 → 5',
'排序后取nums[n-k]，O(n log n)。','维护容量至多k的最小堆。每个元素入堆，若超k就弹出最小值；这样堆始终保留目前最大的k个数。扫描完堆顶就是第k大。此版比随机快速选择更易理解，但时间O(n log k)。',
'k2：读3、2，堆保留2,3；读1后弹1；读5后弹2，保留3,5；读6后弹3，保留5,6；读4后弹4，堆顶5。',
'O(n log(k+1)) 时间，每元素入堆并可能出堆；O(k) 空间。','第k大不是第k个不同值；Java默认最小堆恰好适用；不要提前读取空堆。',r'''
import java.util.*;
class Solution {
    public int findKthLargest(int[] nums,int k) {
        PriorityQueue<Integer> heap=new PriorityQueue<>();
        for(int x:nums) {
            heap.offer(x);
            if(heap.size()>k) heap.poll(); // 丢弃较小数，只留下最大的k个
        }
        return heap.peek();
    }
}''','eq(new Solution().findKthLargest(new int[]{3,2,1,5,6,4},2),5); eq(new Solution().findKthLargest(new int[]{2,2,1},2),2); eq(new Solution().findKthLargest(new int[]{-1},1),-1);')
add(347,'返回出现频率最高的k种整数，保证答案唯一，结果顺序不限。k不超过不同整数个数。','[1,1,1,2,2,3], k=2 → [1,2]',
'统计后对所有不同数字按频率排序，O(n+u log u)。','先用Map计频，再建大小n+1的桶，bucket[f]存出现f次的数字。频率范围只在1..n，因此从高频桶向低频桶收集，满k即结束。这是桶方法，满足比O(n log n)更好的题目要求；堆解法可作后续练习。',
'频次{1:3,2:2,3:1}；桶3放1，桶2放2，桶1放3；从桶6往下扫，取到1和2，结束。',
'O(n) 平均时间，计频、入桶、扫描桶均线性；O(n) 空间。','桶下标是频率而非数值；k是种类数；输出无序，测试先排序再比较。',r'''
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
}''','int[] a=new Solution().topKFrequent(new int[]{1,1,1,2,2,3},2); Arrays.sort(a); eq(a,new int[]{1,2}); eq(new Solution().topKFrequent(new int[]{1},1),new int[]{1}); eq(new Solution().topKFrequent(new int[]{-1,-1,2},1),new int[]{-1});')
add(295,'维护整数数据流，支持addNum加入数字与findMedian查询当前中位数。保证查询时至少有一个数。','加入1、2后中位数1.5；再加入3后2.0',
'每次加入排序数组成本O(n)，每次查询再排序也慢。','左半用最大堆low，右半用最小堆high。保持low大小等于high或多1，且low最大≤high最小。每次先放low，再把low最大转入high，若high更大再转回最小值。奇数取low堆顶，偶数求两堆顶平均。',
'加1：low=[1],high=[]；加2：low=[1],high=[2]，平均1.5；加3：low含1,2，high含3，中位数2。',
'addNum为O(log n)时间，常数次堆调整，findMedian为O(1)时间；总空间O(n)，两个堆合计保存全部已加入数字。','low必须是最大堆；两堆大小差不超过1且low不小；求平均先转double避免整数溢出。',r'''
import java.util.*;
class MedianFinder {
    private final PriorityQueue<Integer> low=new PriorityQueue<>(Comparator.reverseOrder());
    private final PriorityQueue<Integer> high=new PriorityQueue<>();
    public MedianFinder() {}
    public void addNum(int num) {
        low.offer(num); high.offer(low.poll()); // 把左半最大值交给右半
        if(high.size()>low.size()) low.offer(high.poll()); // 恢复大小不变量
    }
    public double findMedian() {
        if(low.size()>high.size()) return low.peek();
        return ((double)low.peek()+high.peek())/2;
    }
}''','MedianFinder f=new MedianFinder(); f.addNum(1); f.addNum(2); eq(f.findMedian(),1.5); f.addNum(3); eq(f.findMedian(),2.0); MedianFinder g=new MedianFinder(); g.addNum(Integer.MAX_VALUE); g.addNum(Integer.MAX_VALUE); eq(g.findMedian(),2147483647.0); MedianFinder h=new MedianFinder(); h.addNum(-1); eq(h.findMedian(),-1.0);')
