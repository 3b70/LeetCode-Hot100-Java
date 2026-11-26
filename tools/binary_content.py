from content import add
add(35,'在严格升序数组找target；存在返回下标，否则返回保持有序时应插入的位置，可以等于数组长度。','[1,3,5,6], target=2 → 1',
'顺序找第一个≥target的元素需O(n)。','二分维护半开区间[l,r)，答案是第一个≥target的位置。mid值偏小就令l=mid+1，否则r=mid。l==r时搜索结束，该位置即插入点。r初始n允许返回末尾。',
'[1,3,5,6]找2：l0,r4,m2值5，r2；m1值3，r1；m0值1，l1；收敛到1。',
'O(log n) 时间，每轮剩余区间约减半；O(1) 空间。','半开区间不能混用r=mid-1；插入位置可以是n；中点用l+(r-l)/2。',r'''
class Solution {
    public int searchInsert(int[] nums,int target) {
        int l=0,r=nums.length;
        while(l<r) {
            int m=l+(r-l)/2;
            if(nums[m]<target) l=m+1; else r=m; // 保留第一个不小于target的位置
        }
        return l;
    }
}''','eq(new Solution().searchInsert(new int[]{1,3,5,6},2),1); eq(new Solution().searchInsert(new int[]{1},2),1); eq(new Solution().searchInsert(new int[]{1,3},1),0);')
add(74,'矩阵每行递增，且下一行首元素大于上一行尾元素。判断target是否出现。','[[1,3,5],[7,9,11]], target=9 → true',
'逐格找O(mn)，但整体实际上有序。','把矩阵视为长度m*n的有序一维数组。逻辑下标mid对应行mid/n、列mid%n。用闭区间二分，命中返回true，偏小舍左半，偏大舍右半；区间空返回false。',
'6个元素找9：mid2对应(0,2)=5，左界升3；mid4对应(1,1)=9，命中。',
'O(log(mn)) 时间，每轮减半；O(1) 空间，没有真正展开矩阵。','坐标除数是列数n；只行列各自有序的240题不适用此法；闭区间循环用l<=r。',r'''
class Solution {
    public boolean searchMatrix(int[][] matrix,int target) {
        int n=matrix[0].length,l=0,r=matrix.length*n-1;
        while(l<=r) {
            int mid=l+(r-l)/2,value=matrix[mid/n][mid%n]; // 一维下标映射回行列
            if(value==target) return true;
            if(value<target) l=mid+1; else r=mid-1;
        }
        return false;
    }
}''','eq(new Solution().searchMatrix(new int[][]{{1,3,5},{7,9,11}},9),true); eq(new Solution().searchMatrix(new int[][]{{1}},0),false); eq(new Solution().searchMatrix(new int[][]{{1,3}},2),false);')
add(34,'非递减数组可能有重复，返回target首次和末次出现的下标；不存在返回[-1,-1]。','[5,7,7,8,8,10], target=8 → [3,4]',
'线性扫描能找到，但要求O(log n)。','分别二分求第一个≥target的lower和第一个>target的upper。两个半开区间搜索仅在相等时的移动方向不同。若lower==n或该位置不等target则无解，否则答案[lower,upper-1]。不用target+1，避免最大整数溢出。',
'找8的lower收敛3，upper收敛5；覆盖下标3、4，返回[3,4]。找6时lower为1但nums[1]=7，返回无解。',
'O(log n) 时间，两次二分；O(1) 空间。','先检查lower是否越界；upper是排他位置需减1；不要用target+1实现上界而忽略溢出。',r'''
class Solution {
    public int[] searchRange(int[] nums,int target) {
        int first=bound(nums,target,false);
        if(first==nums.length || nums[first]!=target) return new int[]{-1,-1};
        return new int[]{first,bound(nums,target,true)-1};
    }
    private int bound(int[] a,int target,boolean upper) {
        int l=0,r=a.length;
        while(l<r) {
            int m=l+(r-l)/2;
            // upper为true时，相等元素也要排除到左边
            if(a[m]<target || (upper && a[m]==target)) l=m+1; else r=m;
        }
        return l;
    }
}''','eq(new Solution().searchRange(new int[]{5,7,7,8,8,10},8),new int[]{3,4}); eq(new Solution().searchRange(new int[]{},0),new int[]{-1,-1}); eq(new Solution().searchRange(new int[]{2,2},2),new int[]{0,1});')
add(33,'原本严格递增的数组经一次旋转，返回target下标，不存在返回-1。元素互不相同。','[4,5,6,7,0,1,2], target=0 → 4',
'遍历O(n)，题目要求对数时间。','闭区间二分，每次mid把区间分开，其中至少一半有序。若nums[l]<=nums[mid]则左半有序，判断target是否处于[l,mid)值域；否则右半有序，判断是否位于(mid,r]值域。只保留可能含目标的一半。',
'l0,r6,mid3值7，左半有序但0不在[4,7)，保留右半；l4,r6,mid5值1，0位于左半，r4；命中下标4。',
'O(log n) 时间，每轮减半；O(1) 空间。','有序判断含等号才能覆盖单元素半段；目标区间端点开闭配套；重复值场景不满足本题前提。',r'''
class Solution {
    public int search(int[] nums,int target) {
        int l=0,r=nums.length-1;
        while(l<=r) {
            int m=l+(r-l)/2;
            if(nums[m]==target) return m;
            if(nums[l]<=nums[m]) { // 左半有序
                if(nums[l]<=target && target<nums[m]) r=m-1; else l=m+1;
            } else {
                if(nums[m]<target && target<=nums[r]) l=m+1; else r=m-1;
            }
        }
        return -1;
    }
}''','eq(new Solution().search(new int[]{4,5,6,7,0,1,2},0),4); eq(new Solution().search(new int[]{1},0),-1); eq(new Solution().search(new int[]{1,3},3),1);')
add(153,'在旋转后的严格递增非空数组中求最小值，无重复元素，未旋转也合法。','[3,4,5,1,2] → 1',
'遍历取最小O(n)。','比较mid与当前右端：nums[mid]>nums[r]说明旋转断点在右侧，l=mid+1；否则mid处于有序右段，最小值在左边或就是mid，r=mid。l==r时唯一候选即最小值。',
'[3,4,5,1,2]，mid2值5>右2，l3；mid3值1≤右2，r3；返回nums[3]=1。',
'O(log n) 时间，区间每轮约减半；O(1) 空间。','右界不能写mid-1，mid可能就是最小；以当前nums[r]比较；重复元素需不同处理。',r'''
class Solution {
    public int findMin(int[] nums) {
        int l=0,r=nums.length-1;
        while(l<r) {
            int mid=l+(r-l)/2;
            if(nums[mid]>nums[r]) l=mid+1;
            else r=mid; // mid自身仍是最小值候选
        }
        return nums[l];
    }
}''','eq(new Solution().findMin(new int[]{3,4,5,1,2}),1); eq(new Solution().findMin(new int[]{1}),1); eq(new Solution().findMin(new int[]{1,2,3}),1);')
add(4,'两个各自升序数组，至少一个非空，求合并序列中位数。偶数长度返回中间两数平均值。','[1,3] 与 [2] → 2.0；[1,2]与[3,4] → 2.5',
'真正合并需O(m+n)时间和线性空间，不满足对数时间要求。','在较短数组A二分划分i，B划分j=(m+n+1)/2-i，让左侧总数比右侧相等或多1。需要A左末≤B右首且B左末≤A右首；过界用整数极值作哨兵。若A左末过大则i左移，否则右移。合法后奇数取左侧最大，偶数取左最大与右最小的平均。较短数组保证j不会越界。',
'A=[1,2],B=[3,4]，先i1,j1：B左3>A右2，i右移；i2,j0后左为1,2，右为3,4，跨边界合法，中位数(2+3)/2=2.5。',
'O(log(min(m,n)+1)) 时间，只二分较短数组；O(1) 额外空间，交换参数最多一次递归。','先确保A较短；偶数求和前转double防int溢出；空侧需要边界哨兵。',r'''
class Solution {
    public double findMedianSortedArrays(int[] a,int[] b) {
        if(a.length>b.length) return findMedianSortedArrays(b,a);
        int m=a.length,n=b.length,l=0,r=m;
        while(l<=r) {
            int i=l+(r-l)/2,j=(m+n+1)/2-i;
            int al=i==0?Integer.MIN_VALUE:a[i-1],ar=i==m?Integer.MAX_VALUE:a[i];
            int bl=j==0?Integer.MIN_VALUE:b[j-1],br=j==n?Integer.MAX_VALUE:b[j];
            if(al<=br && bl<=ar) { // 两侧交叉边界都满足整体有序
                if((m+n)%2==1) return Math.max(al,bl);
                return ((double)Math.max(al,bl)+Math.min(ar,br))/2;
            }
            if(al>br) r=i-1; else l=i+1;
        }
        throw new IllegalArgumentException("输入必须为有序数组");
    }
}''','eq(new Solution().findMedianSortedArrays(new int[]{1,3},new int[]{2}),2.0); eq(new Solution().findMedianSortedArrays(new int[]{1,2},new int[]{3,4}),2.5); eq(new Solution().findMedianSortedArrays(new int[]{},new int[]{1}),1.0); eq(new Solution().findMedianSortedArrays(new int[]{Integer.MAX_VALUE},new int[]{Integer.MAX_VALUE}),2147483647.0);')
