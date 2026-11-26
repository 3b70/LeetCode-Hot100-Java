"""题解内容唯一数据源；每题：题意、示例、直观思路、推荐算法、执行过程、复杂度、易错点、代码、测试。"""
P = {}
def add(i, goal, example, naive, idea, trace, cost, errors, code, tests):
    assert i not in P
    P[i] = dict(goal=goal, example=example, naive=naive, idea=idea, trace=trace,
                cost=cost, errors=errors, code=code.strip(), tests=tests.strip())

add(1,'输入整数数组和目标值，返回两个不同位置的下标，使对应数字之和等于目标。题目保证恰有一组解；同一元素不能使用两次。',
'nums=[2,7,11,15], target=9 → [0,1]', '枚举所有下标对需要 O(n²) 次比较。',
'从左往右扫描，用哈希表保存已经见过的数及下标。当前值 x 需要 target-x；先查找补数，再存当前值，保证不会配对自己。找到后立即返回。表只保存扫描位置左边的元素，这是循环不变量。',
'i=0，x=2，补数7不在表中，存{2:0}；i=1，x=7，补数2命中下标0，返回[0,1]。',
'O(n) 平均时间，最多扫描 n 个元素且哈希查找平均 O(1)；O(n) 额外空间，保存至多 n 个键。',
'先存后查会把同一个位置用两次；返回数值而非下标；重复值仍可能组成答案，例如[3,3]。',r'''
import java.util.HashMap;
import java.util.Map;
class Solution {
    public int[] twoSum(int[] nums, int target) {
        Map<Integer, Integer> seen = new HashMap<>();
        for (int i = 0; i < nums.length; i++) {
            int need = target - nums[i];
            // 先查左侧元素，避免使用当前下标两次
            if (seen.containsKey(need)) return new int[]{seen.get(need), i};
            seen.put(nums[i], i); // 数值映射到已扫描的下标
        }
        return new int[0];
    }
}''', 'eq(new Solution().twoSum(new int[]{2,7,11,15},9), new int[]{0,1}); eq(new Solution().twoSum(new int[]{3,3},6),new int[]{0,1}); eq(new Solution().twoSum(new int[]{-3,4,3},0),new int[]{0,2});')
add(49,'输入字符串数组，将字母出现次数完全相同的字符串放进同一组。组与组以及组内顺序不限；空字符串也要归组。',
'["eat","tea","tan","ate","nat","bat"] → [["eat","tea","ate"],["tan","nat"],["bat"]]（顺序可不同）',
'逐对比较字符频率会重复比较很多次。',
'异位词排序后得到同一个字符串。把排序结果作为 Map 的键，把原字符串列表作为值。遍历时复制字符数组再排序，原字符串不改变；若键不存在先创建空组，再追加原字符串。',
'eat排序成aet，新建aet组[eat]；tea也得到aet，追加成[eat,tea]；tan得到ant，建立另一组。',
'O(n k log k) 时间，n 是字符串数，k 是最大长度，每个字符串排序；O(nk) 空间，保存分组及键（含返回结果）。',
'不能直接用char[]作按内容比较的键；输出顺序不固定，测试应规范化；空字符串的排序键是空串。',r'''
import java.util.*;
class Solution {
    public List<List<String>> groupAnagrams(String[] strs) {
        Map<String, List<String>> groups = new HashMap<>();
        for (String s : strs) {
            char[] chars = s.toCharArray(); // 新数组可以排序，String 本身不可变
            Arrays.sort(chars);
            String key = new String(chars);
            if (!groups.containsKey(key)) groups.put(key, new ArrayList<>());
            groups.get(key).add(s); // 同一个排序键对应同一组
        }
        return new ArrayList<>(groups.values());
    }
}''','eq(norm(new Solution().groupAnagrams(new String[]{"eat","tea","tan","ate","nat","bat"})),"[[ate, eat, tea], [bat], [nat, tan]]"); eq(norm(new Solution().groupAnagrams(new String[]{""})),"[[]]"); eq(norm(new Solution().groupAnagrams(new String[]{"a","a"})),"[[a, a]]");')
add(128,'输入无序整数数组，求其中数值连续的最长序列长度，不要求在原数组位置连续。重复数字只算一次；空数组返回0。',
'[100,4,200,1,3,2] → 4（1,2,3,4）','排序后扫描可以完成，但需要 O(n log n) 时间。',
'把所有数加入集合去重。只有找不到 x-1 的 x 才可能是序列起点；从起点不断查找 x+1。每个不同数字最多被一次向右扩展访问，因此不是二次复杂度。额外检查整数边界，避免 MAX_VALUE+1 回绕。',
'集合{100,4,200,1,3,2}中，1没有前驱，从1连续走到4，长度4；2、3、4有前驱，跳过；100和200各长1。',
'O(n) 平均时间，建集合加上每条连续链的一次遍历；O(n) 空间。哈希操作按平均 O(1) 计算。',
'从每个数字都向右扩展会退化；要对集合而非含重复值的原数组枚举起点；加减1注意整数边界。',r'''
import java.util.*;
class Solution {
    public int longestConsecutive(int[] nums) {
        Set<Integer> set = new HashSet<>();
        for (int x : nums) set.add(x);
        int best = 0;
        for (int x : set) {
            // 只从没有前驱的数字开始，避免重复扫描整条序列
            if (x != Integer.MIN_VALUE && set.contains(x - 1)) continue;
            int y = x, length = 1;
            while (y != Integer.MAX_VALUE && set.contains(y + 1)) { y++; length++; }
            best = Math.max(best, length);
        }
        return best;
    }
}''','eq(new Solution().longestConsecutive(new int[]{100,4,200,1,3,2}),4); eq(new Solution().longestConsecutive(new int[]{}),0); eq(new Solution().longestConsecutive(new int[]{1,2,0,1}),3);')
add(283,'原地把数组中的0移到末尾，非零数字保持原相对顺序。没有返回数组，直接修改输入。',
'[0,1,0,3,12] → [1,3,12,0,0]','借助新数组收集非零数字可行，但额外占用 O(n) 空间。',
'write 表示下一个非零元素应写入的位置。扫描时把非零元素依次写入前段，扫描完从 write 到末尾补0。始终有 write 不超过当前扫描位置，所以覆盖不会破坏尚未读取的数据。',
'扫描0不写；读1写到下标0，write=1；读3写到1；读12写到2；最后下标3、4补0。',
'O(n) 时间，每个位置至多读写常数次；O(1) 额外空间，只使用下标。',
'非零元素必须稳定保序；不要边遍历边删除数组元素；全零时write保持0。',r'''
class Solution {
    public void moveZeroes(int[] nums) {
        int write = 0;
        for (int x : nums) {
            if (x != 0) nums[write++] = x; // 稳定地压紧非零元素
        }
        while (write < nums.length) nums[write++] = 0; // 剩余位置补零
    }
}''','int[] a={0,1,0,3,12}; new Solution().moveZeroes(a); eq(a,new int[]{1,3,12,0,0}); int[] b={0,0}; new Solution().moveZeroes(b); eq(b,new int[]{0,0}); int[] c={1}; new Solution().moveZeroes(c); eq(c,new int[]{1});')
add(11,'输入各位置竖线高度，选两条与横轴围出最大水量。容积为下标距离乘较矮高度；数组至少有两个元素。',
'[1,8,6,2,5,4,8,3,7] → 49','枚举每对边界，O(n²) 计算面积。',
'左右指针从两端开始。当前面积取宽度乘短板；移动短板一侧。若只移动长板，宽度减少且短板不增加，不可能改善当前面积；因此可以安全舍弃当前短板。每一步更新最大面积。',
'l=0,r=8面积8，左短板移动；l=1,r=8面积7×7=49；右侧7较短，右移入；后续宽度缩小，没有超过49。',
'O(n) 时间，每步至少一个指针靠近且总步数至多 n-1；O(1) 空间。',
'宽度是r-l而非r-l+1；不能移动较高边来保证优化；最大值要在移动前计算。',r'''
class Solution {
    public int maxArea(int[] height) {
        int left=0, right=height.length-1, best=0;
        while (left < right) {
            best=Math.max(best,(right-left)*Math.min(height[left],height[right]));
            // 舍弃短板，才可能提高下一次的限制高度
            if (height[left] < height[right]) left++; else right--;
        }
        return best;
    }
}''','eq(new Solution().maxArea(new int[]{1,8,6,2,5,4,8,3,7}),49); eq(new Solution().maxArea(new int[]{1,1}),1); eq(new Solution().maxArea(new int[]{0,0}),0);')
add(15,'返回数组中和为0的所有不同数值三元组。三个位置必须不同，结果不能包含重复组合；不足三个数返回空列表。',
'[-1,0,1,2,-1,-4] → [[-1,-1,2],[-1,0,1]]','三重循环 O(n³)，还需要额外处理重复结果。',
'先排序。固定第一个数 i，在右侧用左右指针找两数之和。总和小于0就增大左值，大于0就减小右值；等于0记录并同时跳过重复值。固定值也必须去重。排序后 nums[i]>0 时，后续不可能再凑出0。',
'排序[-4,-1,-1,0,1,2]；固定-4无解；固定第一个-1，配-1和2得到0，再配0和1得到0；第二个-1作为固定值跳过。',
'O(n²) 时间，排序 O(n log n) 后每个固定值扫描至多 n 步；排序栈 O(log n) 额外空间，不含最多 O(n²) 的输出。',
'去重不能在记录答案前错误跳过合法元素；左右指针不能越过数组边界；排序会修改输入。',r'''
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
}''','eq(norm(new Solution().threeSum(new int[]{-1,0,1,2,-1,-4})),"[[-1, -1, 2], [-1, 0, 1]]"); eq(new Solution().threeSum(new int[]{1,2}).size(),0); eq(new Solution().threeSum(new int[]{0,0,0,0}).size(),1);')
add(42,'非负数组表示柱高，求下雨后柱间可以存下的总水量。每格宽1；不足三根柱子不能积水。',
'[4,2,0,3,2,5] → 9','对每格分别向左右找最高柱，O(n²)；预处理两侧最大高度可降到 O(n)，但占 O(n) 空间。',
'两个指针维护尚未处理区间，leftMax/rightMax记录已遇到的最高边界。更新两侧最高值后，哪侧上界较小，就可以确定那格水量：另一侧已有足够高的墙。加上该侧最高值减当前高度，再向内移动。',
'[4,2,0,3,2,5]：左最高4小于右最高5，依次结算左侧水量0、2、4、1、2；最后两指针相遇，总和9。',
'O(n) 时间，每个位置处理一次；O(1) 额外空间，用两侧最大值代替辅助数组。',
'水量使用较低的两侧最高墙；更新最高值后再相减，避免负数；相遇位置无需重复结算。',r'''
class Solution {
    public int trap(int[] height) {
        int l=0,r=height.length-1,lm=0,rm=0,water=0;
        while(l<r) {
            lm=Math.max(lm,height[l]); rm=Math.max(rm,height[r]);
            // 较低的已知最高墙足以确定本侧水位
            if(lm<=rm) { water+=lm-height[l]; l++; }
            else { water+=rm-height[r]; r--; }
        }
        return water;
    }
}''','eq(new Solution().trap(new int[]{4,2,0,3,2,5}),9); eq(new Solution().trap(new int[]{1}),0); eq(new Solution().trap(new int[]{3,0,3}),3);')
add(3,'求字符串中不含重复字符的最长连续子串长度。子串必须连续；空串返回0。本实现按题目字符范围处理Java char。',
'"abcabcbb" → 3','从每个起点重新检查重复，可能 O(n²)。',
'用集合维护窗口[left,right]的字符。加入右字符前，如果它已经存在，就持续删除左端字符并右移left，直到窗口合法。加入当前字符后更新长度。两个端点都只向右走。',
'读a、b、c，窗口增长到abc长度3；再读a，先删左端a，left变1，再加入a，窗口bca仍长3；最终答案3。',
'O(n) 平均时间，每个字符各入集合、出集合至多一次；O(min(n,Σ)) 空间，Σ为字符集大小。',
'遇到重复时只移一次左指针可能仍重复；窗口长度是right-left+1；子序列不能当子串。',r'''
import java.util.*;
class Solution {
    public int lengthOfLongestSubstring(String s) {
        Set<Character> window=new HashSet<>();
        int left=0,best=0;
        for(int right=0;right<s.length();right++) {
            char c=s.charAt(right);
            // 不断收缩，直到当前字符可以安全加入
            while(window.contains(c)) window.remove(s.charAt(left++));
            window.add(c);
            best=Math.max(best,right-left+1);
        }
        return best;
    }
}''','eq(new Solution().lengthOfLongestSubstring("abcabcbb"),3); eq(new Solution().lengthOfLongestSubstring(""),0); eq(new Solution().lengthOfLongestSubstring("abba"),2);')
add(438,'在小写字母串 s 中找出所有长度等于 p 且字母计数与 p 相同的子串，返回起点列表；p比s长时无解。',
's="cbaebabacd", p="abc" → [0,6]','每个子串排序比较会重复工作。',
'维护长度为 p.length 的固定窗口，用26格计数数组描述窗口和目标。右侧加入字符，若窗口超长则移走左侧；达到长度后用 Arrays.equals 比较频率。由于字符集固定，比较是常数开销。',
'right=2时窗口cba，频率a1b1c1，记录0；继续右移时加入新字符并移走最旧字符；right=8时窗口bac，记录6。',
'O(26n)=O(n) 时间，每个位置比较26个计数；O(26)=O(1) 额外空间，不含答案。',
'只有窗口长度足够才比较；移出位置是right-m；该26格实现仅适用于小写英文字母。',r'''
import java.util.*;
class Solution {
    public List<Integer> findAnagrams(String s,String p) {
        List<Integer> ans=new ArrayList<>();
        int[] target=new int[26],window=new int[26];
        for(char c:p.toCharArray()) target[c-'a']++;
        int m=p.length();
        for(int r=0;r<s.length();r++) {
            window[s.charAt(r)-'a']++;
            if(r>=m) window[s.charAt(r-m)-'a']--; // 保持固定长度
            if(r>=m-1 && Arrays.equals(window,target)) ans.add(r-m+1);
        }
        return ans;
    }
}''','eq(new Solution().findAnagrams("cbaebabacd","abc").toString(),"[0, 6]"); eq(new Solution().findAnagrams("ab","abc").size(),0); eq(new Solution().findAnagrams("aaaa","aa").toString(),"[0, 1, 2]");')
add(560,'统计整数数组中和恰好等于k的连续子数组个数。允许负数和0；子数组非空。',
'nums=[1,1,1], k=2 → 2','枚举每个起点并累加到各终点，O(n²)。负数存在时不能使用普通伸缩窗口。',
'前缀和sum表示当前之前所有数的总和。若历史前缀为sum-k，两者之间的子数组和就是k。Map保存各历史前缀出现次数，先查询再登记当前前缀；最初前缀0出现一次，以便统计从下标0开始的答案。',
'初始{0:1}；第一个1，sum=1查-1无，存1；第二个1，sum=2查0有1个，ans=1；第三个1，sum=3查1有1个，ans=2。',
'O(n) 平均时间，单次遍历加平均 O(1) 哈希操作；O(n) 空间保存前缀和频次。',
'忘记初始0前缀；Map必须存次数而非仅存是否出现；先登记会在k=0时统计空子数组。',r'''
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
}''','eq(new Solution().subarraySum(new int[]{1,1,1},2),2); eq(new Solution().subarraySum(new int[]{0,0},0),3); eq(new Solution().subarraySum(new int[]{1,-1,1},1),3);')
add(239,'窗口长度k每次右移一格，返回每个完整窗口的最大值。1≤k≤数组长度。',
'[1,3,-1,-3,5,3,6,7], k=3 → [3,3,5,5,6,7]','每个窗口重新扫描 O(nk)。',
'双端队列存下标，并让对应值从队首到队尾递减。队首过期就弹出；新值比队尾大或相等时，旧队尾既更小又更早过期，可以永久删除。当前下标入队，窗口形成后队首就是最大值。',
'i=0队列[0]；i=1值3淘汰值1，队列[1]；i=2队列[1,2]，输出3；i=4值5淘汰所有较小尾部，输出5。',
'O(n) 时间，每个下标入队一次、出队至多一次；O(k) 空间保存窗口候选，不含输出。',
'必须保存下标才能判断过期；过期条件是下标≤i-k；结果从i=k-1开始写。',r'''
import java.util.*;
class Solution {
    public int[] maxSlidingWindow(int[] nums,int k) {
        int[] ans=new int[nums.length-k+1];
        Deque<Integer> q=new ArrayDeque<>();
        for(int i=0;i<nums.length;i++) {
            while(!q.isEmpty() && q.peekFirst()<=i-k) q.removeFirst(); // 去掉过期下标
            while(!q.isEmpty() && nums[q.peekLast()]<=nums[i]) q.removeLast();
            q.addLast(i); // 保留从大到小的候选
            if(i>=k-1) ans[i-k+1]=nums[q.peekFirst()];
        }
        return ans;
    }
}''','eq(new Solution().maxSlidingWindow(new int[]{1,3,-1,-3,5,3,6,7},3),new int[]{3,3,5,5,6,7}); eq(new Solution().maxSlidingWindow(new int[]{1},1),new int[]{1}); eq(new Solution().maxSlidingWindow(new int[]{2,2},2),new int[]{2});')
add(76,'在s中找最短连续子串，覆盖t中的全部字符及其重复次数。无解返回空串；字符按题目英文字母范围计数。',
's="ADOBECODEBANC", t="ABC" → "BANC"','枚举所有子串再检查覆盖，代价很高。',
'need[c]记录还缺多少个字符c，missing记录缺少字符总数。扩张右端时，若need[c]>0就满足一个缺口，然后递减need[c]。missing为0时窗口覆盖成功，循环收缩左端并更新最短答案；移出字符后need变正，说明丢失了必要字符，停止收缩。负计数代表多余字符。',
'右端到C时ADOBEC首次覆盖ABC，记录长度6；收缩丢掉A后不再覆盖；后面补A再次收缩；最终BANC长度4，继续收缩会丢B。',
'O(|s|+|t|) 时间，每个字符进出窗口至多一次；O(128)=O(1) 空间，依赖英文字母输入约束。',
'不能只比较不同字符种类，t可重复；收缩须使用while；返回substring的右端是排他下标。',r'''
class Solution {
    public String minWindow(String s,String t) {
        if(t.isEmpty()) return "";
        int[] need=new int[128];
        for(char c:t.toCharArray()) need[c]++;
        int missing=t.length(),left=0,start=0,best=Integer.MAX_VALUE;
        for(int right=0;right<s.length();right++) {
            char c=s.charAt(right);
            if(need[c]>0) missing--;
            need[c]--; // 负数代表窗口中有富余
            while(missing==0) {
                if(right-left+1<best) { best=right-left+1; start=left; }
                char out=s.charAt(left++);
                need[out]++;
                if(need[out]>0) missing++; // 移出了必要字符，覆盖失效
            }
        }
        return best==Integer.MAX_VALUE ? "" : s.substring(start,start+best);
    }
}''','eq(new Solution().minWindow("ADOBECODEBANC","ABC"),"BANC"); eq(new Solution().minWindow("a","aa"),""); eq(new Solution().minWindow("aa","aa"),"aa");')
