from content import add
add(121,'每天股价已知，只能先买后卖一次，求最大利润；可以不交易，返回0。','[7,1,5,3,6,4] → 5',
'枚举买卖日期O(n²)。','扫描时low记录当前及之前最低价，best记录最佳利润。每天先更新low再用price-low更新best；使用当前价作为最低价时利润0，对合法答案没有影响。低价是对之前所有买入选择的压缩。',
'读7时low7,best0；读1时low1；读5利润4；读6利润5；最终5。',
'O(n) 时间，一次扫描；O(1) 空间。','不能先卖后买；下跌时答案为0而非负数；只允许一笔交易不能累计多个上涨区间。',r'''
class Solution {
    public int maxProfit(int[] prices) {
        int low=Integer.MAX_VALUE,best=0;
        for(int price:prices) {
            low=Math.min(low,price); // 压缩历史所有买入日
            best=Math.max(best,price-low);
        }
        return best;
    }
}''','eq(new Solution().maxProfit(new int[]{7,1,5,3,6,4}),5); eq(new Solution().maxProfit(new int[]{7,6,4,3,1}),0); eq(new Solution().maxProfit(new int[]{1}),0);')
add(55,'非负数组中nums[i]表示从i最多可向右跳几步，判断能否从0到最后一格。','[2,3,1,1,4] → true',
'递归枚举跳跃距离可能指数级且重复计算。','far表示目前已知可达的最远位置。从左往右扫描，若i>far则此处都不可达，后面也无法越过断层；否则更新far=max(far,i+nums[i])。一旦far覆盖终点即可成功。贪心只保留所有已达位置的最远延伸。',
'i0将far更新2；i1可达并更新4，已覆盖末尾，true。对于[3,2,1,0,4]，far始终3，到i4时4>3失败。',
'O(n) 时间，一次扫描；O(1) 空间。','不能从不可达位置更新far；跳跃长度是最大值并非必须值；单元素数组天然已到终点。',r'''
class Solution {
    public boolean canJump(int[] nums) {
        int far=0;
        for(int i=0;i<nums.length;i++) {
            if(i>far) return false; // 先检查可达，再读取此位置的跳跃贡献
            far=Math.max(far,i+nums[i]);
            if(far>=nums.length-1) return true;
        }
        return true;
    }
}''','eq(new Solution().canJump(new int[]{2,3,1,1,4}),true); eq(new Solution().canJump(new int[]{3,2,1,0,4}),false); eq(new Solution().canJump(new int[]{0}),true);')
add(45,'从数组起点跳到终点，返回最少跳数。每格表示最大可跳距离，题目保证可到达。','[2,3,1,1,4] → 2',
'DP枚举每个位置可跳到哪里可做，但最坏O(n²)。','按跳数分层的贪心：end是当前跳数能覆盖的右边界，far是扫描这一层所有点后下一跳能达到的最远处。扫描到i==end时必须增加一步并把end扩到far。只扫描到倒数第二个位置，避免到终点后多算一步。',
'i0时far2且到旧边界0，steps1,end2；扫描i1可扩far4；i2到边界再steps2,end4；结果2。',
'O(n) 时间，每位置扫描一次；O(1) 空间。','循环不能包含末尾；应从当前层所有点取最远而非只选最大nums值；不可达输入不属于题目保证范围。',r'''
class Solution {
    public int jump(int[] nums) {
        int end=0,far=0,steps=0;
        for(int i=0;i<nums.length-1;i++) {
            far=Math.max(far,i+nums[i]);
            if(i==end) { steps++; end=far; } // 当前层结束，进入下一跳覆盖区间
        }
        return steps;
    }
}''','eq(new Solution().jump(new int[]{2,3,1,1,4}),2); eq(new Solution().jump(new int[]{0}),0); eq(new Solution().jump(new int[]{1,1,1}),2);')
add(763,'把小写字母串切成尽可能多的连续片段，使每个字母只出现在其中一个片段；返回各段长度。','"ababcbacadefegdehijhklij" → [9,7,8]',
'尝试每个切点并检查字符是否跨段，会重复扫描。','先记录每个字母最后出现位置last。扫描当前段时end=max(end,last[c])；当i到达end，当前段内所有字符都不会在后面出现，可以立即切段获得最多段数。记录长度i-start+1并更新start。',
'从a开始end8，b末位5、c末位7不超过8；i8可以切长9；下一段遇d、e、f把end推15，切长7；最后长8。',
'O(n) 时间，两次扫描；O(26)=O(1) 辅助空间，不含输出。','必须看最后一次出现而非首次；长度加1；当前段遇新字母要扩边界。',r'''
import java.util.*;
class Solution {
    public List<Integer> partitionLabels(String s) {
        int[] last=new int[26];
        for(int i=0;i<s.length();i++) last[s.charAt(i)-'a']=i;
        List<Integer> ans=new ArrayList<>(); int start=0,end=0;
        for(int i=0;i<s.length();i++) {
            end=Math.max(end,last[s.charAt(i)-'a']); // 当前段必须覆盖所有已遇字符的最后位置
            if(i==end) { ans.add(i-start+1); start=i+1; }
        }
        return ans;
    }
}''','eq(new Solution().partitionLabels("ababcbacadefegdehijhklij").toString(),"[9, 7, 8]"); eq(new Solution().partitionLabels("aaaa").toString(),"[4]"); eq(new Solution().partitionLabels("abc").toString(),"[1, 1, 1]");')
add(70,'每次爬1或2阶，求到第n阶的不同走法数量，1≤n≤45。','n=3 → 3（1+1+1、1+2、2+1）',
'递归f(n)=f(n-1)+f(n-2)但不缓存会指数重复。','状态f[i]是到第i阶的走法数，最后一步来自i-1或i-2，因此f[i]=f[i-1]+f[i-2]。初始f[0]=1（不走这一个方案）、f[1]=1。i从2递增；仅保存a=f[i-2]、b=f[i-1]滚动更新。',
'a1,b1；i2得到2，更新a1,b2；i3得到3，更新a2,b3，返回3。',
'O(n) 时间，逐阶一次加法；O(1) 空间，滚动两状态。','初始f0不是0；更新先保存和再移动a、b；超过题目范围会int溢出。',r'''
class Solution {
    public int climbStairs(int n) {
        int a=1,b=1;
        for(int i=2;i<=n;i++) { int next=a+b; a=b; b=next; } // 两个旧状态滚动到下一阶
        return b;
    }
}''','eq(new Solution().climbStairs(3),3); eq(new Solution().climbStairs(1),1); eq(new Solution().climbStairs(45),1836311903);')
add(118,'返回杨辉三角前numRows行，首行是[1]，每行边缘为1，中间等于上一行相邻两数之和。','numRows=5 → [[1],[1,1],[1,2,1],[1,3,3,1],[1,4,6,4,1]]',
'按定义逐行生成就是合适算法，不必为每格重新用组合数公式。','状态triangle[i][j]为第i行第j个值。边界j=0或j=i置1；内部值=triangle[i-1][j-1]+triangle[i-1][j]。i从0递增，j从0到i，上一行已完整生成。每行都新建列表。',
'先[1]；下一行两端均1得[1,1]；再下一行中间1+1=2得[1,2,1]；之后内项1+2=3、2+1=3。',
'O(R²) 时间，前R行共R(R+1)/2个元素；含返回值O(R²)空间，单行构建额外O(R)。','每行长度是i+1；两边不要访问上一行越界；不能重复使用同一个可变行列表。',r'''
import java.util.*;
class Solution {
    public List<List<Integer>> generate(int numRows) {
        List<List<Integer>> ans=new ArrayList<>();
        for(int i=0;i<numRows;i++) {
            List<Integer> row=new ArrayList<>();
            for(int j=0;j<=i;j++) {
                if(j==0 || j==i) row.add(1);
                else row.add(ans.get(i-1).get(j-1)+ans.get(i-1).get(j)); // 读取上一行两项
            }
            ans.add(row);
        }
        return ans;
    }
}''','eq(new Solution().generate(5).toString(),"[[1], [1, 1], [1, 2, 1], [1, 3, 3, 1], [1, 4, 6, 4, 1]]"); eq(new Solution().generate(1).toString(),"[[1]]"); eq(new Solution().generate(2).toString(),"[[1], [1, 1]]");')
add(198,'每间房有非负金额，不能偷相邻房屋，求最大总额。','[2,7,9,3,1] → 12',
'对每房枚举偷或不偷，重复子问题指数增长。','dp[i]为前i间房可偷最大额。第i间不偷得到dp[i-1]，偷则前一间不能偷，得到dp[i-2]+nums[i-1]；取最大。dp[0]=0，dp[1]=nums[0]。代码统一以prev2=0、prev1=0从首房扫描，先算next再滚动，兼容空数组。',
'[2,7,9,3,1]逐房最优2、7、11、11、12；第3房9与第1房2组合，第5房1接上得到12。',
'O(n) 时间，每房一次转移；O(1) 空间。','不是只比较奇数房总和与偶数房总和；旧状态不要提前覆盖；金额非负但允许一个也不偷。',r'''
class Solution {
    public int rob(int[] nums) {
        int prev2=0,prev1=0;
        for(int money:nums) {
            int next=Math.max(prev1,prev2+money); // 不偷当前房，或偷当前并跳过前房
            prev2=prev1; prev1=next;
        }
        return prev1;
    }
}''','eq(new Solution().rob(new int[]{2,7,9,3,1}),12); eq(new Solution().rob(new int[]{0}),0); eq(new Solution().rob(new int[]{2,1,1,2}),4);')
add(279,'求正整数n最少能表示为多少个完全平方数之和，平方数可以重复。','n=12 → 3（4+4+4）',
'递归枚举平方数分拆会重复求相同剩余值。','dp[i]为凑出i的最少平方数个数。dp[0]=0，其余先置n+1代表无穷。i从1递增，对所有j²≤i转移dp[i]=min(dp[i],dp[i-j²]+1)。减去正平方后状态下标更小，已计算完成。',
'dp1=1，dp2=2，dp3=3，dp4=1；到dp12，尝试1²、2²、3²，dp8+1=3最优，对应4+4+4。',
'O(n√n) 时间，n个状态各枚举至多√n个平方数；O(n) 空间。','平方数1也必须枚举；dp0=0；j是平方根，转移减j*j不是减j。',r'''
import java.util.*;
class Solution {
    public int numSquares(int n) {
        int[] dp=new int[n+1]; Arrays.fill(dp,n+1); dp[0]=0;
        for(int i=1;i<=n;i++) for(int j=1;j*j<=i;j++) {
            dp[i]=Math.min(dp[i],dp[i-j*j]+1); // 最后选择一个平方数j²
        }
        return dp[n];
    }
}''','eq(new Solution().numSquares(12),3); eq(new Solution().numSquares(13),2); eq(new Solution().numSquares(1),1);')
add(322,'给正整数硬币面额和非负金额，硬币无限使用，求最少枚数；不能凑出返回-1。','coins=[1,2,5], amount=11 → 3',
'总选最大面额的贪心对任意币值不成立，例如[1,3,4]凑6。','dp[a]为凑a的最少枚数。初始化dp[0]=0，其余amount+1作不可达；金额a从1递增，枚举coin≤a，转移min(dp[a],dp[a-coin]+1)。因为coin>0，依赖更小金额；最终仍大于amount则-1。这求最少数，不是方案数。',
'[1,2,5]：dp1=1，dp2=1，dp5=1；dp10=2；dp11由dp10+1或dp9+1或dp6+1得到3。',
'O(A·C) 时间，A为金额、C为面额数；O(A) 空间。','amount0答案0；不可达不能用0初始化；避免用MAX_VALUE再加1导致溢出。',r'''
import java.util.*;
class Solution {
    public int coinChange(int[] coins,int amount) {
        int[] dp=new int[amount+1]; Arrays.fill(dp,amount+1); dp[0]=0;
        for(int a=1;a<=amount;a++) for(int coin:coins) {
            if(coin<=a) dp[a]=Math.min(dp[a],dp[a-coin]+1); // 无次数限制，依赖更小金额
        }
        return dp[amount]>amount?-1:dp[amount];
    }
}''','eq(new Solution().coinChange(new int[]{1,2,5},11),3); eq(new Solution().coinChange(new int[]{2},3),-1); eq(new Solution().coinChange(new int[]{1},0),0); eq(new Solution().coinChange(new int[]{1,3,4},6),2);')
add(139,'判断字符串能否切成词典中的若干单词，同一单词可多次使用。切分必须覆盖全部字符。','s="leetcode", dict=["leet","code"] → true',
'尝试所有切点的递归可能指数级；相同后缀被反复判断。','dp[i]表示前i个字符可以切分；dp[0]=true。i从1到n，枚举最后一词起点j∈[0,i)：若dp[j]且s.substring(j,i)在Set中，则dp[i]=true并停止本状态搜索。答案dp[n]。Set平均查找常数，但创建和哈希子串仍按长度计费。',
'dp0=true；i4时substring(0,4)=leet，dp4=true；i8时dp4且substring(4,8)=code，dp8=true。',
'此Java实现最坏O(n³+M)时间，O(n²)个切分各创建/哈希O(n)子串，M为词典总字符数；O(n+M)持久空间，临时子串最多O(n)。','dp0必须true；substring右边界排他；字典出现某词不代表整串都可切分。',r'''
import java.util.*;
class Solution {
    public boolean wordBreak(String s,List<String> wordDict) {
        Set<String> dict=new HashSet<>(wordDict); boolean[] dp=new boolean[s.length()+1]; dp[0]=true;
        for(int i=1;i<=s.length();i++) for(int j=0;j<i;j++) {
            if(dp[j] && dict.contains(s.substring(j,i))) { dp[i]=true; break; } // 最后一个词合法
        }
        return dp[s.length()];
    }
}''','eq(new Solution().wordBreak("leetcode",Arrays.asList("leet","code")),true); eq(new Solution().wordBreak("catsandog",Arrays.asList("cats","dog","sand","and","cat")),false); eq(new Solution().wordBreak("aaaa",Arrays.asList("aa")),true);')
add(300,'求严格递增子序列最大长度。子序列可跳过元素，但必须保持下标顺序；相等不算递增。','[10,9,2,5,3,7,101,18] → 4',
'枚举全部子序列要O(2^n)。','使用入门DP：dp[i]表示以nums[i]结尾的最长严格递增子序列长度，初始都1。i从左向右，j枚举0..i-1，若nums[j]<nums[i]则dp[i]=max(dp[i],dp[j]+1)。答案取所有dp最大，而非仅最后一项。进阶可用二分维护最小结尾降到O(n log n)。',
'逐项dp为[1,1,1,2,2,3,4,4]；18可接在长度3、结尾7之后，获得长度4。',
'O(n²) 时间，枚举所有j<i的下标对；O(n) 状态空间。','严格比较<而非<=；子序列不是连续子数组；最终取max(dp)不是dp[n-1]。',r'''
import java.util.*;
class Solution {
    public int lengthOfLIS(int[] nums) {
        int[] dp=new int[nums.length]; Arrays.fill(dp,1); int best=0;
        for(int i=0;i<nums.length;i++) {
            for(int j=0;j<i;j++) if(nums[j]<nums[i]) dp[i]=Math.max(dp[i],dp[j]+1);
            best=Math.max(best,dp[i]); // 任意位置都可作为最优序列的结尾
        }
        return best;
    }
}''','eq(new Solution().lengthOfLIS(new int[]{10,9,2,5,3,7,101,18}),4); eq(new Solution().lengthOfLIS(new int[]{7,7,7}),1); eq(new Solution().lengthOfLIS(new int[]{1,2,0}),2);')
add(152,'求非空连续子数组的最大乘积。允许负数和0，题目保证相关乘积在32位范围内。','[2,3,-2,4] → 6',
'枚举每个起点并累计乘积O(n²)。','状态maxEnd/minEnd分别是以当前项结尾的最大、最小乘积，初始nums[0]。负数可能把最小乘积翻成最大，因此新max=max(x,oldMax*x,oldMin*x)，新min同理取最小。先保存旧值，再更新；从下标1递增，答案维护全部maxEnd最大值。',
'初始max=min=2；读3后max6,min3；读-2后max-2,min-12；读4后max4,min-48；全局最大仍6。',
'O(n) 时间，每项常数次乘法比较；O(1) 空间。','不能只维护最大值；两个状态更新需使用同一组旧值；0会自然重置，不需要删除它。',r'''
class Solution {
    public int maxProduct(int[] nums) {
        int max=nums[0],min=nums[0],best=max;
        for(int i=1;i<nums.length;i++) {
            int x=nums[i],a=max*x,b=min*x; // 先保存两个旧状态的乘积
            max=Math.max(x,Math.max(a,b)); min=Math.min(x,Math.min(a,b));
            best=Math.max(best,max);
        }
        return best;
    }
}''','eq(new Solution().maxProduct(new int[]{2,3,-2,4}),6); eq(new Solution().maxProduct(new int[]{-2,0,-1}),0); eq(new Solution().maxProduct(new int[]{-2,3,-4}),24); eq(new Solution().maxProduct(new int[]{-2}),-2);')
add(416,'给正整数数组，判断能否分成两个元素总和相等的子集，每个位置只能使用一次。','[1,5,11,5] → true',
'枚举分组是指数级，可转成是否能凑出总和一半的0/1背包。','总和为奇数直接false；目标T=sum/2。dp[j]表示用已处理元素能否凑出j，初始dp0=true。每个数x处理时j从T倒序到x，dp[j]|=dp[j-x]；倒序确保右侧读取的旧状态没有使用本轮x，避免一个元素被多次选。最后dp[T]即答案。',
'总和22，T11；处理1可达{0,1}；处理5可达{0,1,5,6}；处理11直接令dp11=true，能分为[11]和[1,5,5]。',
'O(nT) 时间，每个数扫描目标区间；O(T) 空间。','内层必须倒序；总和奇数先排除；输入正整数是背包范围成立的条件。',r'''
class Solution {
    public boolean canPartition(int[] nums) {
        int sum=0; for(int x:nums) sum+=x;
        if(sum%2!=0) return false;
        int target=sum/2; boolean[] dp=new boolean[target+1]; dp[0]=true;
        for(int x:nums) for(int j=target;j>=x;j--) dp[j]=dp[j] || dp[j-x]; // 倒序防止同一数复用
        return dp[target];
    }
}''','eq(new Solution().canPartition(new int[]{1,5,11,5}),true); eq(new Solution().canPartition(new int[]{1,2,3,5}),false); eq(new Solution().canPartition(new int[]{1,2,5}),false);')
add(32,'给只含左右括号的字符串，求最长连续合法括号子串长度。空串返回0。','")()())" → 4',
'枚举子串再用栈验证可能O(n³)。','dp[i]表示必须以位置i结尾的最长合法括号长度，初始0，i从1递增。若s[i]是(则为0；若前一个是(，dp[i]=2+dp[i-2]；若前一个是)，令j=i-dp[i-1]-1，尝试匹配前一整段之前的(，若合法则dp[i]=dp[i-1]+2+dp[j-1]。所有越界前段当0。',
'")()())"：i2配位置1，dp2=2；i4配位置3，再接dp2，dp4=4；i5计算j=0但字符是)，无法匹配，保持0。',
'O(n) 时间，每项常数次查状态；O(n) 空间。','j必须先检查非负；嵌套匹配后还要接前面dp[j-1]；结果是最大dp而非最后一个。',r'''
class Solution {
    public int longestValidParentheses(String s) {
        int[] dp=new int[s.length()]; int best=0;
        for(int i=1;i<s.length();i++) {
            if(s.charAt(i)==')') {
                if(s.charAt(i-1)=='(') dp[i]=2+(i>=2?dp[i-2]:0);
                else {
                    int j=i-dp[i-1]-1; // 越过前一段合法串，寻找配对左括号
                    if(j>=0 && s.charAt(j)=='(') dp[i]=dp[i-1]+2+(j>=1?dp[j-1]:0);
                }
                best=Math.max(best,dp[i]);
            }
        }
        return best;
    }
}''','eq(new Solution().longestValidParentheses(")()())"),4); eq(new Solution().longestValidParentheses(""),0); eq(new Solution().longestValidParentheses("()(())"),6);')
