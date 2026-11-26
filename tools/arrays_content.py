from content import add

add(53,'求非空整数数组中，连续非空子数组的最大和。全负数时也必须选至少一个数。','[-2,1,-3,4,-1,2,1,-5,4] → 6',
'枚举所有区间并累计求和，O(n²)。','设end为必须以当前元素结尾的最大和。前一个end若为负，接上它反而变差，应从当前值重新开始；因此end=max(x,end+x)。初始end=nums[0]，从下标1向右遍历，每步更新全局best。',
'end从-2开始；读1重新开始为1；读-3为-2；读4重新开始为4；接-1、2、1得到3、5、6，全局最好6。',
'O(n) 时间，每个元素一次转移；O(1) 空间，只保留前一状态。','best初始化0会导致全负数出错；子数组必须连续；不能把所有正数直接相加。',r'''
class Solution {
    public int maxSubArray(int[] nums) {
        int end=nums[0],best=end;
        for(int i=1;i<nums.length;i++) {
            end=Math.max(nums[i],end+nums[i]); // 延长旧区间或从当前位置重启
            best=Math.max(best,end);
        }
        return best;
    }
}''','eq(new Solution().maxSubArray(new int[]{-2,1,-3,4,-1,2,1,-5,4}),6); eq(new Solution().maxSubArray(new int[]{-3,-1}),-1); eq(new Solution().maxSubArray(new int[]{5}),5);')
add(56,'合并所有重叠闭区间，返回互不重叠的区间。端点相等也算重叠。','[[1,3],[2,6],[8,10],[15,18]] → [[1,6],[8,10],[15,18]]',
'不断两两寻找重叠区间，合并后可能又要重新扫描。','按左端点排序。结果列表最后一个区间是唯一可能与当前区间重叠的区间；若当前起点大于其终点就新建，否则扩大最后终点。排序保证后续不可能再影响更早的已封闭区间。',
'先放[1,3]；[2,6]的2≤3，扩大为[1,6]；8>6，新建[8,10]；15>10，新建[15,18]。',
'O(n log n) 时间，由排序决定；O(n) 空间存结果引用及新区间，排序也需要辅助空间。','闭区间接触必须合并；比较器用Integer.compare避免相减溢出；排序改变输入排列。',r'''
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
}''','eq(new Solution().merge(new int[][]{{1,3},{2,6},{8,10},{15,18}}),new int[][]{{1,6},{8,10},{15,18}}); eq(new Solution().merge(new int[][]{{1,4},{4,5}}),new int[][]{{1,5}}); eq(new Solution().merge(new int[][]{{1,4},{2,3}}),new int[][]{{1,4}});')
add(189,'将数组原地向右轮转k步。k是非负数，超过数组长度时按长度取模。','nums=[1,2,3,4,5,6,7], k=3 → [5,6,7,1,2,3,4]',
'每轮搬移最后一个数到开头，O(nk)。','把数组看成前段A和长度k的后段B，目标BA。整体翻转得到reverse(B)reverse(A)，再分别翻转前k个和后n-k个即可。辅助reverse使用左右交换直到相遇。',
'整体翻转得[7,6,5,4,3,2,1]；前3个翻转得[5,6,7,4,3,2,1]；后4个翻转得到目标。',
'O(n) 时间，三次翻转总计线性次交换；O(1) 空间。','先k%=n避免越界；辅助区间是闭区间；k=0时前段为空，不应交换。',r'''
class Solution {
    public void rotate(int[] nums,int k) {
        if(nums.length==0) return;
        k%=nums.length;
        reverse(nums,0,nums.length-1); // 先交换前后两段的整体位置
        reverse(nums,0,k-1);
        reverse(nums,k,nums.length-1); // 恢复各段内部次序
    }
    private void reverse(int[] a,int l,int r) {
        while(l<r) { int t=a[l]; a[l++]=a[r]; a[r--]=t; }
    }
}''','int[] a={1,2,3,4,5,6,7}; new Solution().rotate(a,3); eq(a,new int[]{5,6,7,1,2,3,4}); int[] b={1}; new Solution().rotate(b,100); eq(b,new int[]{1}); int[] c={1,2}; new Solution().rotate(c,0); eq(c,new int[]{1,2});')
add(238,'返回数组，使答案第i项等于输入中除第i项以外所有数的乘积。不能用除法，允许存在0；题目保证所需乘积在32位范围。','[1,2,3,4] → [24,12,8,6]',
'每个位置重新遍历其他数，O(n²)；总乘积除以当前值无法直接处理0。','第一次从左向右，把当前位置左边所有数的乘积写到ans[i]，初始乘积1。第二次从右向左维护右侧乘积并乘进ans[i]。两部分都不包含当前位置，因此合并后恰好满足要求。',
'前缀写入[1,1,2,6]；右乘积初始1，从右依次乘入1、4、12、24，得到[24,12,8,6]。',
'O(n) 时间，两次扫描；不计返回数组为 O(1) 额外空间，计入输出则 O(n)。','乘完当前值再写前缀会错误包含自身；乘法单位元是1；存在两个0时所有答案均为0。',r'''
class Solution {
    public int[] productExceptSelf(int[] nums) {
        int[] ans=new int[nums.length];
        int product=1;
        for(int i=0;i<nums.length;i++) {
            ans[i]=product; // 先写左侧乘积，再纳入当前元素
            product*=nums[i];
        }
        product=1;
        for(int i=nums.length-1;i>=0;i--) {
            ans[i]*=product;
            product*=nums[i]; // 留给左边位置使用的右侧乘积
        }
        return ans;
    }
}''','eq(new Solution().productExceptSelf(new int[]{1,2,3,4}),new int[]{24,12,8,6}); eq(new Solution().productExceptSelf(new int[]{0,2,3}),new int[]{6,0,0}); eq(new Solution().productExceptSelf(new int[]{0,0}),new int[]{0,0});')
add(41,'在线性时间和常量额外空间内，返回数组没有出现的最小正整数。可修改数组，忽略0和负数。','[3,4,-1,1] → 2',
'集合保存所有正整数再从1找起，时间合适但空间O(n)。','长度n的数组答案必在1..n+1。把值x放到下标x-1：仅当x在1..n且目标位置尚非x时交换，并重新检查换回来的值。最后从左找第一个nums[i]!=i+1的位置，返回i+1；全部正确则返回n+1。',
'[3,4,-1,1]先把3放下标2得[-1,4,3,1]；把4放下标3得[-1,1,3,4]；把1放下标0得[1,-1,3,4]；下标1不等2，返回2。',
'O(n) 时间，每次有效交换至少把一个正数放入最终位置，总交换数至多n；O(1) 空间。','范围检查须先于索引访问；重复数要用目标值相等判断停止；必须while而非只交换一次。',r'''
class Solution {
    public int firstMissingPositive(int[] nums) {
        int n=nums.length;
        for(int i=0;i<n;i++) {
            // 重复值已就位时停止，避免无限交换
            while(nums[i]>=1 && nums[i]<=n && nums[nums[i]-1]!=nums[i]) {
                int target=nums[i]-1;
                int t=nums[target]; nums[target]=nums[i]; nums[i]=t;
            }
        }
        for(int i=0;i<n;i++) if(nums[i]!=i+1) return i+1;
        return n+1;
    }
}''','eq(new Solution().firstMissingPositive(new int[]{3,4,-1,1}),2); eq(new Solution().firstMissingPositive(new int[]{1,1}),2); eq(new Solution().firstMissingPositive(new int[]{1,2,3}),4);')
add(73,'原地修改二维矩阵：原矩阵中含0的行和列都变为0。不能把修改产生的0继续作为新标记扩散。','[[1,1,1],[1,0,1],[1,1,1]] → [[1,0,1],[0,0,0],[1,0,1]]',
'另存需要清零的行列集合，空间O(m+n)。','用第一行、第一列记录内部格子的清零标记，另外两个布尔值保存原第一行和第一列是否含0。先扫描并标记，再清内部，最后按布尔值清第一行、列；顺序保证标记不被提前破坏。',
'中心(1,1)为0，标记(1,0)和(0,1)；内部所有位于第1行或第1列的格子清零；第一行列按标记保留相应0。',
'O(mn) 时间，常数轮矩阵扫描；O(1) 空间，借输入的首行首列存标记。','必须先单独保存首行首列状态；不能边发现边直接清整行；不要提前覆盖用于判断的标记。',r'''
class Solution {
    public void setZeroes(int[][] matrix) {
        int m=matrix.length,n=matrix[0].length;
        boolean row=false,col=false;
        for(int j=0;j<n;j++) if(matrix[0][j]==0) row=true;
        for(int i=0;i<m;i++) if(matrix[i][0]==0) col=true;
        for(int i=1;i<m;i++) for(int j=1;j<n;j++) {
            if(matrix[i][j]==0) { matrix[i][0]=0; matrix[0][j]=0; } // 借首行列标记
        }
        for(int i=1;i<m;i++) for(int j=1;j<n;j++) {
            if(matrix[i][0]==0 || matrix[0][j]==0) matrix[i][j]=0;
        }
        // 内部处理完，再处理首行首列，避免破坏标记
        if(row) for(int j=0;j<n;j++) matrix[0][j]=0;
        if(col) for(int i=0;i<m;i++) matrix[i][0]=0;
    }
}''','int[][] a={{1,1,1},{1,0,1},{1,1,1}}; new Solution().setZeroes(a); eq(a,new int[][]{{1,0,1},{0,0,0},{1,0,1}}); int[][] b={{0,1}}; new Solution().setZeroes(b); eq(b,new int[][]{{0,0}}); int[][] c={{1}}; new Solution().setZeroes(c); eq(c,new int[][]{{1}});')
add(54,'按顺时针螺旋次序访问矩形矩阵全部元素，返回列表。只有一行或一列也要各访问一次。','[[1,2,3],[4,5,6],[7,8,9]] → [1,2,3,6,9,8,7,4,5]',
'维护方向和访问矩阵可以模拟，但额外空间O(mn)。','维护top、bottom、left、right四条未访问边界。依次走上边、右边、下边、左边，每走完一边缩小对应边界；走下边和左边前重新检查边界，避免单行单列重复。',
'先取上边1,2,3，top变1；右边6,9，right变1；下边8,7，bottom变1；左边4，left变1；下一轮只取中心5。',
'O(mn) 时间，每格恰好输出一次；O(1) 额外空间，不含 O(mn) 返回列表。','下边、左边需额外检查剩余区域；收缩方向不要写反；矩阵不一定是方阵。',r'''
import java.util.*;
class Solution {
    public List<Integer> spiralOrder(int[][] matrix) {
        List<Integer> ans=new ArrayList<>();
        int top=0,bottom=matrix.length-1,left=0,right=matrix[0].length-1;
        while(top<=bottom && left<=right) {
            for(int j=left;j<=right;j++) ans.add(matrix[top][j]); top++;
            for(int i=top;i<=bottom;i++) ans.add(matrix[i][right]); right--;
            // 检查边界，避免最后一行或一列被重复遍历
            if(top<=bottom) { for(int j=right;j>=left;j--) ans.add(matrix[bottom][j]); bottom--; }
            if(left<=right) { for(int i=bottom;i>=top;i--) ans.add(matrix[i][left]); left++; }
        }
        return ans;
    }
}''','eq(new Solution().spiralOrder(new int[][]{{1,2,3},{4,5,6},{7,8,9}}).toString(),"[1, 2, 3, 6, 9, 8, 7, 4, 5]"); eq(new Solution().spiralOrder(new int[][]{{1,2}}).toString(),"[1, 2]"); eq(new Solution().spiralOrder(new int[][]{{1},{2}}).toString(),"[1, 2]");')
add(48,'把n×n方阵原地顺时针旋转90度，不能创建另一个同尺寸矩阵。','[[1,2],[3,4]] → [[3,1],[4,2]]',
'新建矩阵并令new[j][n-1-i]=old[i][j]，但违反原地要求。','先沿主对角线转置，再对每一行左右翻转。原(i,j)转置后到(j,i)，行内翻转后到(j,n-1-i)，恰好是顺时针旋转坐标。只交换上三角与下三角，防止抵消。',
'[[1,2],[3,4]]转置为[[1,3],[2,4]]；各行反转后为[[3,1],[4,2]]。',
'O(n²) 时间，每格参与常数次交换；O(1) 空间。','转置时j必须从i+1开始；只能用于方阵；先行反转再转置会变成逆时针。',r'''
class Solution {
    public void rotate(int[][] matrix) {
        int n=matrix.length;
        for(int i=0;i<n;i++) for(int j=i+1;j<n;j++) {
            int t=matrix[i][j]; matrix[i][j]=matrix[j][i]; matrix[j][i]=t; // 主对角线转置
        }
        for(int[] row:matrix) {
            for(int l=0,r=n-1;l<r;l++,r--) {
                int t=row[l]; row[l]=row[r]; row[r]=t; // 行内镜像
            }
        }
    }
}''','int[][] a={{1,2},{3,4}}; new Solution().rotate(a); eq(a,new int[][]{{3,1},{4,2}}); int[][] b={{1}}; new Solution().rotate(b); eq(b,new int[][]{{1}}); int[][] c={{1,2,3},{4,5,6},{7,8,9}}; new Solution().rotate(c); eq(c,new int[][]{{7,4,1},{8,5,2},{9,6,3}});')
add(240,'矩阵每行从左到右递增，每列从上到下递增，判断目标值是否存在。行间不保证整体有序。','[[1,4,7],[2,5,8],[3,6,9]], target=6 → true',
'逐格扫描 O(mn)，或每行二分 O(m log n)。','从右上角开始。如果当前值比目标大，当前列以下更大，整列可排除，向左；当前值比目标小，当前行左侧更小，整行可排除，向下。剩余区域始终是左下方矩形。',
'从7开始找6，7>6向左到4；4<6向下到5；5<6向下到6，命中。',
'O(m+n) 时间，每次排除一行或一列；O(1) 空间。','不能把整个矩阵当一维有序数组；从左上角不能单步排除一整行列；下标边界两侧都要检查。',r'''
class Solution {
    public boolean searchMatrix(int[][] matrix,int target) {
        int i=0,j=matrix[0].length-1;
        while(i<matrix.length && j>=0) {
            if(matrix[i][j]==target) return true;
            if(matrix[i][j]>target) j--; // 当前列全部过大
            else i++; // 当前行全部过小
        }
        return false;
    }
}''','eq(new Solution().searchMatrix(new int[][]{{1,4,7},{2,5,8},{3,6,9}},6),true); eq(new Solution().searchMatrix(new int[][]{{1}},2),false); eq(new Solution().searchMatrix(new int[][]{{1,3}},1),true);')
