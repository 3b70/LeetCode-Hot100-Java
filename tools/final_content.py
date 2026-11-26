from content import add
add(62,'在m行n列网格从左上走到右下，每步只可向右或向下，求不同路径数，无障碍。','m=3,n=7 → 28',
'枚举每条路线会指数重复到达相同格子的子问题。','dp[i][j]表示到该格的路径数。首行和首列均为1，其余dp[i][j]=dp[i-1][j]+dp[i][j-1]，从上到下、从左到右计算。代码滚动为一维dp[j]：更新前它是上方路径，dp[j-1]已经是本行左方路径。初始所有列置1，代表第一行。',
'3×3初始dp=[1,1,1]；第二行从j1更新到[1,2,3]；第三行变[1,3,6]。3×7按同样规则最终28。',
'O(mn) 时间，每格常数次相加；O(n) 空间，压缩掉行维度。','滚动数组j必须正序；边缘路径只有1；返回dp[n-1]而非整行和。',r'''
import java.util.*;
class Solution {
    public int uniquePaths(int m,int n) {
        int[] dp=new int[n]; Arrays.fill(dp,1); // 第一行都只有沿右走这一条路线
        for(int i=1;i<m;i++) for(int j=1;j<n;j++) dp[j]+=dp[j-1]; // 上方旧状态加左方新状态
        return dp[n-1];
    }
}''','eq(new Solution().uniquePaths(3,7),28); eq(new Solution().uniquePaths(1,1),1); eq(new Solution().uniquePaths(1,5),1);')
add(64,'非负矩阵中从左上走到右下，只能向下或向右，求沿途节点值之和最小值，包含起点和终点。','[[1,3,1],[1,5,1],[4,2,1]] → 7',
'枚举全部路径再求最小会指数增长。','dp[i][j]是到达该格的最小和。起点为grid[0][0]；首行只能来自左，首列只能来自上；内部为min(上,左)+当前值。按行正序滚动到一维数组，dp[j]更新前为上方，dp[j-1]为左方。',
'第一行dp=[1,4,5]；第二行dp=[2,7,6]；第三行dp=[6,8,7]，答案7。对应1→3→1→1→1。',
'O(mn) 时间，每格一次转移；O(n) 空间。','不能默认所有边界为0，否则会从网格外进入；起点只加一次；滚动数组更新方向需从左到右。',r'''
class Solution {
    public int minPathSum(int[][] grid) {
        int m=grid.length,n=grid[0].length; int[] dp=new int[n];
        for(int i=0;i<m;i++) for(int j=0;j<n;j++) {
            if(i==0 && j==0) dp[j]=grid[i][j];
            else if(i==0) dp[j]=dp[j-1]+grid[i][j];
            else if(j==0) dp[j]+=grid[i][j];
            else dp[j]=Math.min(dp[j],dp[j-1])+grid[i][j]; // 两个合法来源中取较小
        }
        return dp[n-1];
    }
}''','eq(new Solution().minPathSum(new int[][]{{1,3,1},{1,5,1},{4,2,1}}),7); eq(new Solution().minPathSum(new int[][]{{5}}),5); eq(new Solution().minPathSum(new int[][]{{1,2,3}}),6);')
add(5,'求字符串最长连续回文子串，多个同长答案可返回任意一个。输入非空。','"babad" → "bab"或"aba"',
'枚举所有区间再逐字符判断需要O(n³)。','区间DP：pal[i][j]表示闭区间回文，当两端相等且(j-i<2或pal[i+1][j-1])时为真。初始由长度1、2的条件直接处理。i倒序、j从i正序，保证内部状态已知；每次真且更长则更新start和best，最后截取。可在后续学习中心扩展以节省空间。',
'babad从靠右区间开始计算，aba的内区间b已为真，首尾a相等，因此长度3；之后bab也成立但只在更长时更新，所以可能保留aba。',
'O(n²) 时间，计算所有i≤j区间；O(n²) 空间保存回文表，返回字符串O(n)。','pal内部区间必须先算；子串而非子序列；同长解不固定，测试可接受两种。',r'''
class Solution {
    public String longestPalindrome(String s) {
        int n=s.length(),start=0,best=0; boolean[][] pal=new boolean[n][n];
        for(int i=n-1;i>=0;i--) for(int j=i;j<n;j++) {
            pal[i][j]=s.charAt(i)==s.charAt(j) && (j-i<2 || pal[i+1][j-1]);
            if(pal[i][j] && j-i+1>best) { start=i; best=j-i+1; } // 保存最长区间
        }
        return s.substring(start,start+best);
    }
}''','String a=new Solution().longestPalindrome("babad"); eq(a.equals("bab") || a.equals("aba"),true); eq(new Solution().longestPalindrome("cbbd"),"bb"); eq(new Solution().longestPalindrome("a"),"a");')
add(1143,'给两个字符串，求最长公共子序列长度，可跳过字符但不能改变相对顺序。没有公共字符返回0。','text1="abcde",text2="ace" → 3',
'尝试所有子序列再判断匹配会指数爆炸。','dp[i][j]为第一个串前i字符和第二个串前j字符的LCS长度。任一前缀为空时为0；末字符相等则dp[i][j]=dp[i-1][j-1]+1，否则取max(dp[i-1][j],dp[i][j-1])。i、j从1正序，所依赖左、上、左上都已完成。',
'abcde与ace：遇a/a得到1；扫描到c/c时左上已有a长度1，转移为2；到e/e时左上已有ac长度2，转移为3。',
'O(mn) 时间，所有前缀对各一次；O(mn) 空间。','dp下标对应前缀长度，字符下标要减1；不相等时不能加1；公共子序列无需连续。',r'''
class Solution {
    public int longestCommonSubsequence(String text1,String text2) {
        int m=text1.length(),n=text2.length(); int[][] dp=new int[m+1][n+1];
        for(int i=1;i<=m;i++) for(int j=1;j<=n;j++) {
            if(text1.charAt(i-1)==text2.charAt(j-1)) dp[i][j]=dp[i-1][j-1]+1;
            else dp[i][j]=Math.max(dp[i-1][j],dp[i][j-1]); // 各舍弃一个末字符，选择较优
        }
        return dp[m][n];
    }
}''','eq(new Solution().longestCommonSubsequence("abcde","ace"),3); eq(new Solution().longestCommonSubsequence("abc","def"),0); eq(new Solution().longestCommonSubsequence("abc","abc"),3);')
add(72,'把word1转换成word2，每次可插入、删除或替换一个字符，求最少操作次数。字符串可以为空。','"horse" → "ros"，最少3次',
'直接枚举编辑序列有大量重复状态，还可能在插删之间循环。','dp[i][j]为word1前i个字符变为word2前j个字符的最少代价。dp[i][0]=i是删除全部，dp[0][j]=j是插入全部；字符相同直接继承左上，否则取上方删除、左方插入、左上替换三者最小+1。i,j从1递增，答案dp[m][n]。',
'horse到ros可先h替换r得到rorse，删第二个r得到rose，删e得到ros，共3。DP每个前缀都取三种操作最小，最后dp[5][3]=3。',
'O(mn) 时间，(m+1)(n+1)状态各常数操作；O(mn) 空间。','空前缀要初始化；相同字符不额外付费；三种操作不是交换相邻字符。',r'''
class Solution {
    public int minDistance(String word1,String word2) {
        int m=word1.length(),n=word2.length(); int[][] dp=new int[m+1][n+1];
        for(int i=0;i<=m;i++) dp[i][0]=i;
        for(int j=0;j<=n;j++) dp[0][j]=j;
        for(int i=1;i<=m;i++) for(int j=1;j<=n;j++) {
            if(word1.charAt(i-1)==word2.charAt(j-1)) dp[i][j]=dp[i-1][j-1];
            else dp[i][j]=1+Math.min(dp[i-1][j-1],Math.min(dp[i-1][j],dp[i][j-1])); // 替换、删除、插入
        }
        return dp[m][n];
    }
}''','eq(new Solution().minDistance("horse","ros"),3); eq(new Solution().minDistance("","abc"),3); eq(new Solution().minDistance("same","same"),0); eq(new Solution().minDistance("intention","execution"),5);')
add(136,'除一个整数只出现一次外，其余每个整数都出现两次，找出单独数。要求线性时间常量空间。','[4,1,2,1,2] → 4',
'用Map计频可行但需O(n)空间。','利用异或：a^a=0，a^0=a，且异或满足交换结合律。把全部数异或，成对数相互抵消，只剩单独数。负数也能按其二进制补码正确抵消。',
'0^4=4；^1=5；^2=7；^1=6；^2=4。也可重新分组为4^(1^1)^(2^2)=4。',
'O(n) 时间，每元素一次异或；O(1) 空间。','^是异或不是乘方；前提是其他数恰好两次；不能用按位或|代替。',r'''
class Solution {
    public int singleNumber(int[] nums) {
        int ans=0;
        for(int x:nums) ans^=x; // 相同位模式出现两次后抵消
        return ans;
    }
}''','eq(new Solution().singleNumber(new int[]{4,1,2,1,2}),4); eq(new Solution().singleNumber(new int[]{-1,2,2}),-1); eq(new Solution().singleNumber(new int[]{0}),0);')
add(169,'非空数组保证某数出现次数严格超过一半，返回这个多数元素。','[2,2,1,1,1,2,2] → 2',
'计频表O(n)空间；排序取中间元素O(n log n)。','Boyer-Moore投票：count为0时更换candidate；遇同值加1，异值减1，相当于不断删除一对不同元素。多数元素比其他所有数总数还多，删除异值对后仍不可能被彻底消除。保证存在多数，因此无需第二遍验证。',
'[2,2,1,1,1,2,2]：候选2计数1、2、1、0；改候选1计数1，遇2抵消到0；最后候选2计数1，答案2。',
'O(n) 时间，每元素一次投票；O(1) 空间。','严格超过一半不同于出现最多；没有存在性保证时要再计数验证；count归零后下一元素才重设候选。',r'''
class Solution {
    public int majorityElement(int[] nums) {
        int candidate=0,count=0;
        for(int x:nums) {
            if(count==0) candidate=x; // 之前的票已两两抵消
            count+=(x==candidate)?1:-1;
        }
        return candidate;
    }
}''','eq(new Solution().majorityElement(new int[]{2,2,1,1,1,2,2}),2); eq(new Solution().majorityElement(new int[]{3}),3); eq(new Solution().majorityElement(new int[]{-1,-1,2}),-1);')
add(75,'数组只含0、1、2，把它原地排成0在前、1居中、2在后。','[2,0,2,1,1,0] → [0,0,1,1,2,2]',
'计数后覆盖需两遍且可行；三指针能一次划分未知区间。','zero左边全是0，two右边全是2，i扫描，区间[zero,i)全是1，[i,two]未知。遇0与zero交换，两者前进；遇2与two交换，只减two，不增i，因为换来的值未知；遇1仅i++。i>two终止。',
'初始i0值2，和末0换得[0,0,2,1,1,2]，i仍0；处理两个0后i2；再次遇2换入1，随后扫完两1，得到有序。',
'O(n) 时间，每轮未知区间缩小一格；O(1) 空间。','交换2后i不能立即前进；未知区间是闭区间要i<=two；值域仅0、1、2。',r'''
class Solution {
    public void sortColors(int[] nums) {
        int zero=0,i=0,two=nums.length-1;
        while(i<=two) {
            if(nums[i]==0) { swap(nums,i,zero); i++; zero++; }
            else if(nums[i]==2) { swap(nums,i,two); two--; } // 换来的元素仍须检查
            else i++;
        }
    }
    private void swap(int[] a,int i,int j) { int t=a[i]; a[i]=a[j]; a[j]=t; }
}''','int[] a={2,0,2,1,1,0}; new Solution().sortColors(a); eq(a,new int[]{0,0,1,1,2,2}); int[] b={2,0,1}; new Solution().sortColors(b); eq(b,new int[]{0,1,2}); int[] c={0}; new Solution().sortColors(c); eq(c,new int[]{0});')
add(31,'原地把数组改成字典序紧邻的下一个排列。如果当前已经最大，就改成最小（升序）。允许重复值。','[1,2,3] → [1,3,2]；[3,2,1] → [1,2,3]',
'生成所有排列再排序不可行，复杂度阶乘。','从右找第一个nums[i]<nums[i+1]的支点，其右侧必为非递增后缀。若存在支点，从右找第一个比它大的值交换，取得最小可能增幅；随后反转后缀变升序，使新前缀下整体最小。没有支点说明全局最大，反转全部。',
'[1,2,3]支点2，与右侧3交换得[1,3,2]，长度1后缀不用动；[1,3,2]支点1，与右侧2交换[2,3,1]，反转后缀得[2,1,3]。',
'O(n) 时间，两次逆向扫描和一次反转；O(1) 空间。','找支点用>=继续跳过重复；寻找交换值要严格大于；交换后还要反转后缀。',r'''
class Solution {
    public void nextPermutation(int[] nums) {
        int i=nums.length-2;
        while(i>=0 && nums[i]>=nums[i+1]) i--;
        if(i>=0) {
            int j=nums.length-1;
            while(nums[j]<=nums[i]) j--;
            swap(nums,i,j); // 右侧第一个更大值带来最小增幅
        }
        for(int l=i+1,r=nums.length-1;l<r;l++,r--) swap(nums,l,r); // 后缀恢复最小顺序
    }
    private void swap(int[] a,int i,int j) { int t=a[i]; a[i]=a[j]; a[j]=t; }
}''','int[] a={1,2,3}; new Solution().nextPermutation(a); eq(a,new int[]{1,3,2}); int[] b={3,2,1}; new Solution().nextPermutation(b); eq(b,new int[]{1,2,3}); int[] c={1,1,5}; new Solution().nextPermutation(c); eq(c,new int[]{1,5,1});')
add(287,'长度n+1数组的值都在1..n，只有一种数重复，可能出现多次。返回重复数，不改数组且只用常量额外空间。','[1,3,4,2,2] → 2',
'集合占O(n)空间，排序会修改输入。','把下标i到nums[i]看成函数边，从0沿函数前进。因为值只在1..n，0无入边，有限节点必进入环；入口有从前链和环内来的两条入边，对应重复数。Floyd第一阶段slow一步fast两步找相遇；第二阶段p回0并与slow同速，返回再相遇下标即重复数。',
'[1,3,4,2,2]形成0→1→3→2→4→2；快慢在环2、4内相遇；一个从0重新走，同速后在2相遇，返回2。',
'O(n) 时间，函数图的入环距离和环长均不超过n+1；O(1) 空间。','不能把nums[0]当必然重复；do-while确保先走再判相遇；值域是安全用值作下标的前提。',r'''
class Solution {
    public int findDuplicate(int[] nums) {
        int slow=0,fast=0;
        do { slow=nums[slow]; fast=nums[nums[fast]]; } while(slow!=fast);
        int p=0;
        while(p!=slow) { p=nums[p]; slow=nums[slow]; } // 回起点后同速找环入口
        return p;
    }
}''','eq(new Solution().findDuplicate(new int[]{1,3,4,2,2}),2); eq(new Solution().findDuplicate(new int[]{1,1}),1); eq(new Solution().findDuplicate(new int[]{3,3,3,3,3}),3);')
