from content import add
add(94,'返回二叉树按左子树、根、右子树访问得到的值列表。空树返回空列表。','根1，右孩子2，2的左孩子3 → [1,3,2]',
'直接照访问定义递归即可；无需先转为其他结构。','dfs(node)向同一个结果列表追加中序序列；node为null时返回，不追加；先递归左子树，再加入node.val，最后递归右子树。递归方法返回void，结果通过参数列表累积。',
'访问1先处理空左树；加入1；递归2前先递归3并加入3；再加入2，结果[1,3,2]。',
'O(n) 时间，每节点访问一次；O(h) 栈空间，h为树高，最坏O(n)，另有O(n)输出。','空节点不可读取val；顺序不能混成根左右；每次调用新建结果列表，避免累积旧答案。',r'''
import java.util.*;
class Solution {
    public List<Integer> inorderTraversal(TreeNode root) {
        List<Integer> ans=new ArrayList<>(); dfs(root,ans); return ans;
    }
    private void dfs(TreeNode node,List<Integer> ans) {
        if(node==null) return; // 空子树没有待访问节点
        dfs(node.left,ans);
        ans.add(node.val); // 左子树完成后访问根
        dfs(node.right,ans);
    }
}''','eq(new Solution().inorderTraversal(tree(1,null,2,3)).toString(),"[1, 3, 2]"); eq(new Solution().inorderTraversal(null).size(),0); eq(new Solution().inorderTraversal(tree(1)).toString(),"[1]");')
add(104,'求从根到最深叶子的节点数。空树深度0，单节点深度1。','[3,9,20,null,null,15,7] → 3',
'按层遍历并数层也可以；递归更直接对应深度定义。','maxDepth(node)返回该节点为根的子树高度。null返回0；递归获得左右高度，较大值加1。子问题沿子树缩小，最终到达空节点。',
'叶子9、15、7的左右深度都是0，因此各为1；20高度2；根3取max(1,2)+1=3。',
'O(n) 时间，每个节点一次；O(h) 递归栈，平衡树O(log n)，退化链O(n)。','深度按节点数不是边数；空树返回0；不能把左右高度相加。',r'''
class Solution {
    public int maxDepth(TreeNode root) {
        if(root==null) return 0; // 递归终点：空树深度为0
        int left=maxDepth(root.left),right=maxDepth(root.right);
        return Math.max(left,right)+1; // 当前根贡献一层
    }
}''','eq(new Solution().maxDepth(tree(3,9,20,null,null,15,7)),3); eq(new Solution().maxDepth(null),0); eq(new Solution().maxDepth(tree(1)),1);')
add(226,'把二叉树每个节点的左右孩子互换，返回镜像树根。空树仍为空。','[4,2,7,1,3,6,9] → [4,7,2,9,6,3,1]',
'逐层交换也可行；不能只交换根的一对孩子。','递归函数返回已经翻转的子树根。null直接返回null；保存左右子树各自的翻转结果，再交换赋给root.left和root.right。每个子树递归执行相同规则。',
'先将2的孩子1、3交换，将7的孩子6、9交换；最后根4的左右交换，得到左7(9,6)、右2(3,1)。',
'O(n) 时间，每节点交换一次；O(h) 栈空间，最坏O(n)。','赋值前保存两侧结果避免引用覆盖；必须遍历整树；该实现原地修改树。',r'''
class Solution {
    public TreeNode invertTree(TreeNode root) {
        if(root==null) return null;
        TreeNode left=invertTree(root.left),right=invertTree(root.right);
        root.left=right; root.right=left; // 保存完两侧后再交换
        return root;
    }
}''','eq(level(new Solution().invertTree(tree(4,2,7,1,3,6,9))),"[4, 7, 2, 9, 6, 3, 1]"); eq(new Solution().invertTree(null)==null,true); eq(level(new Solution().invertTree(tree(1,2))),"[1, null, 2]");')
add(101,'判断二叉树是否关于根左右镜像对称。对应位置结构和值都要相同。','[1,2,2,3,4,4,3] → true',
'只比较每层值的集合会丢失左右位置和空节点信息。','mirror(a,b)判断两棵子树互为镜像：都空返回true，仅一个空返回false；值相同且a.left对b.right、a.right对b.left都镜像才成功。入口比较root.left和root.right。',
'比较左右2；再比较外侧3与3、内侧4与4；叶子下的空节点成对匹配，因此true。',
'O(n) 时间，每节点参与一次配对；O(h) 栈空间，最坏O(n)。','两个空与一个空分开处理；不是同侧孩子配对；相同值但结构不同仍不对称。',r'''
class Solution {
    public boolean isSymmetric(TreeNode root) { return root==null || mirror(root.left,root.right); }
    private boolean mirror(TreeNode a,TreeNode b) {
        if(a==null || b==null) return a==b; // 只有同时为空才匹配
        return a.val==b.val && mirror(a.left,b.right) && mirror(a.right,b.left);
    }
}''','eq(new Solution().isSymmetric(tree(1,2,2,3,4,4,3)),true); eq(new Solution().isSymmetric(tree(1,2,2,null,3,null,3)),false); eq(new Solution().isSymmetric(null),true);')
add(543,'求树中任意两节点之间最长路径的边数，路径不一定经过根；空树返回0。','[1,2,3,4,5] → 3（4→2→1→3）',
'对每个节点重新计算左右深度，会重复访问子树，最坏O(n²)。','后序递归height(node)返回子树高度，空树0。获得左右高度l、r后，经过当前节点的最长路径边数为l+r，更新全局best；向父节点返回max(l,r)+1，因为延伸路径只能选一个分支。每次公开调用重置best。',
'叶4、5高度1；节点2有l=r=1，候选直径2，高度2；根1有l=2,r=1，候选3，答案3。',
'O(n) 时间，同一后序同时算高度和直径；O(h) 栈，最坏O(n)。','返回给父节点的高度不能是l+r；直径按边数；不能只计算经过根的路径。',r'''
class Solution {
    private int best;
    public int diameterOfBinaryTree(TreeNode root) { best=0; height(root); return best; }
    private int height(TreeNode node) {
        if(node==null) return 0;
        int l=height(node.left),r=height(node.right);
        best=Math.max(best,l+r); // 当前节点连接左右分支的路径
        return Math.max(l,r)+1; // 向父节点只返回一条分支
    }
}''','eq(new Solution().diameterOfBinaryTree(tree(1,2,3,4,5)),3); eq(new Solution().diameterOfBinaryTree(tree(1)),0); eq(new Solution().diameterOfBinaryTree(null),0);')
add(102,'按从上到下、同层从左到右返回节点值的二维列表。空树返回空列表。','[3,9,20,null,null,15,7] → [[3],[9,20],[15,7]]',
'DFS记录深度也可以；队列更自然对应逐层访问。','BFS队列保存待处理节点。每轮开始固定size=q.size()，只弹出这size个作为本层；把其非空左右孩子加入队尾，留给下一轮。队列不存null。',
'队列[3]，size1输出[3]并入9、20；下一层size2输出[9,20]并入15、7；下一层输出[15,7]。',
'O(n) 时间，每节点入出队各一次；O(w) 队列空间，w是最大层宽，另有O(n)输出。','本层size必须提前固定；ArrayDeque不允许null；左右入队顺序决定层内顺序。',r'''
import java.util.*;
class Solution {
    public List<List<Integer>> levelOrder(TreeNode root) {
        List<List<Integer>> ans=new ArrayList<>();
        if(root==null) return ans;
        Queue<TreeNode> q=new ArrayDeque<>(); q.offer(root);
        while(!q.isEmpty()) {
            int size=q.size(); List<Integer> row=new ArrayList<>();
            for(int i=0;i<size;i++) {
                TreeNode node=q.poll(); row.add(node.val);
                if(node.left!=null) q.offer(node.left);
                if(node.right!=null) q.offer(node.right);
            }
            ans.add(row); // 本层完成，队列只剩下一层
        }
        return ans;
    }
}''','eq(new Solution().levelOrder(tree(3,9,20,null,null,15,7)).toString(),"[[3], [9, 20], [15, 7]]"); eq(new Solution().levelOrder(null).size(),0); eq(new Solution().levelOrder(tree(1)).toString(),"[[1]]");')
add(108,'把严格递增数组转换为高度平衡的二叉搜索树。返回任意合法树，空数组返回null。','[-10,-3,0,5,9] → 可取根0，左右分别由[-10,-3]和[5,9]构造',
'依次按搜索树插入递增值会得到链，不能保证平衡。','build(l,r)处理闭区间；l>r返回null。取中点m作根，递归[l,m-1]构造左树、[m+1,r]构造右树。数组有序保证搜索树性质，两段大小至多差1保证平衡。返回当前根。',
'区间[0,4]取m=2根0；左[0,1]取-10并把-3放其右；右[3,4]取5并把9放其右，所有子树高度差≤1。',
'O(n) 时间，每个元素创建一个节点；O(log n) 递归栈，另有O(n)输出树。','不能把中点再次包含进子区间；有序中序序列是验证依据；树形答案不唯一。',r'''
class Solution {
    public TreeNode sortedArrayToBST(int[] nums) { return build(nums,0,nums.length-1); }
    private TreeNode build(int[] a,int l,int r) {
        if(l>r) return null; // 空区间对应空子树
        int m=l+(r-l)/2;
        TreeNode node=new TreeNode(a[m]);
        node.left=build(a,l,m-1); node.right=build(a,m+1,r);
        return node; // 返回构造好的子树根
    }
}''','TreeNode a=new Solution().sortedArrayToBST(new int[]{-10,-3,0,5,9}); eq(inorder(a),"[-10, -3, 0, 5, 9]"); balanced(a); eq(new Solution().sortedArrayToBST(new int[]{})==null,true); eq(new Solution().sortedArrayToBST(new int[]{1}).val,1);')
add(98,'判断树是否为严格二叉搜索树：每个节点的整个左子树都小于它，整个右子树都大于它，不允许相等。','[5,1,4,null,null,3,6] → false',
'只比较直接孩子不够，远端后代也受祖先边界限制。','递归传开区间(low,high)。空节点返回true；当前值不在区间立即false；左树上界缩到当前值，右树下界升到当前值。用long上下界涵盖Integer极值。返回两侧判断的逻辑与。',
'根5允许(-∞,+∞)；右节点4应处于(5,+∞)，4≤5直接失败，即使它与自己的孩子关系正确也无效。',
'O(n) 时间，每个节点一次检查；O(h) 栈空间，最坏O(n)。','必须传祖先约束；严格不等不接受重复；初始int极值边界会错误排除合法极值节点。',r'''
class Solution {
    public boolean isValidBST(TreeNode root) { return valid(root,Long.MIN_VALUE,Long.MAX_VALUE); }
    private boolean valid(TreeNode node,long low,long high) {
        if(node==null) return true;
        if(node.val<=low || node.val>=high) return false;
        // 当前值成为两侧子树的新边界
        return valid(node.left,low,node.val) && valid(node.right,node.val,high);
    }
}''','eq(new Solution().isValidBST(tree(2,1,3)),true); eq(new Solution().isValidBST(tree(5,1,4,null,null,3,6)),false); eq(new Solution().isValidBST(tree(Integer.MIN_VALUE)),true); eq(new Solution().isValidBST(tree(2,2)),false);')
add(230,'在有n个节点的二叉搜索树中求第k小的值，保证1≤k≤n。','[3,1,4,null,2], k=1 → 1',
'把所有值排序可以得到答案，但没利用BST已有顺序。','BST中序遍历严格递增。用显式栈模拟递归：不断沿左孩子入栈，弹出最左未处理节点，k减1；若为0返回值，再转向右子树。栈保存回溯时还要访问的祖先。',
'根3入栈，左1入栈；1的左为空，弹1，k从1降0，返回1，无需访问剩余节点。',
'O(h+k) 时间，沿左链并访问前k个节点，最坏O(n)；O(h) 栈空间。','k从1计数；弹栈后再转右子树；必须是BST才能利用中序排序性质。',r'''
import java.util.*;
class Solution {
    public int kthSmallest(TreeNode root,int k) {
        Deque<TreeNode> stack=new ArrayDeque<>(); TreeNode cur=root;
        while(cur!=null || !stack.isEmpty()) {
            while(cur!=null) { stack.push(cur); cur=cur.left; }
            cur=stack.pop();
            if(--k==0) return cur.val; // 中序第k次弹出即第k小
            cur=cur.right;
        }
        throw new IllegalArgumentException("k超出节点数量");
    }
}''','eq(new Solution().kthSmallest(tree(3,1,4,null,2),1),1); eq(new Solution().kthSmallest(tree(3,1,4,null,2),4),4); eq(new Solution().kthSmallest(tree(1),1),1);')
add(199,'从树的右侧观察，每层只看到最右边存在的节点，按层返回其值。','[1,2,3,null,5,null,4] → [1,3,4]',
'层序遍历保留每层全部值，再取最后一个；可在遍历时直接收集。','BFS从左到右入队，固定本层size；处理本层最后一个节点（i=size-1）时加入答案。右侧缺失时，左子树的更深节点也可能出现在视图里，所以不能只沿right走。',
'层1只输出1；层2队列2、3，最后输出3；层3队列5、4，最后输出4。',
'O(n) 时间，每节点一次；O(w) 队列空间，另有O(h)答案。','不能仅走右孩子；固定每层size；没有右节点时左侧节点可见。',r'''
import java.util.*;
class Solution {
    public List<Integer> rightSideView(TreeNode root) {
        List<Integer> ans=new ArrayList<>();
        if(root==null) return ans;
        Queue<TreeNode> q=new ArrayDeque<>(); q.offer(root);
        while(!q.isEmpty()) {
            int size=q.size();
            for(int i=0;i<size;i++) {
                TreeNode node=q.poll();
                if(i==size-1) ans.add(node.val); // 本层最右节点
                if(node.left!=null) q.offer(node.left);
                if(node.right!=null) q.offer(node.right);
            }
        }
        return ans;
    }
}''','eq(new Solution().rightSideView(tree(1,2,3,null,5,null,4)).toString(),"[1, 3, 4]"); eq(new Solution().rightSideView(tree(1,2,null,3)).toString(),"[1, 2, 3]"); eq(new Solution().rightSideView(null).size(),0);')
add(114,'原地把树按先序（根左右）展开为只使用right的链，所有left置null。','[1,2,5,3,4,null,6] → 1→2→3→4→5→6',
'先序收集节点再重连可行，但额外空间O(n)。','若当前节点有左树，找到左树最右节点pre，把原右树接到pre.right；再把整个左树搬到cur.right并将cur.left置空。然后沿right前进。左树在原右树之前，保持先序；最右节点提供安全连接位置。',
'根1的左树最右为4，把5→6接到4后；把2接到1右边；处理2时把其右4接到左3后，形成1→2→3→4→5→6。',
'O(n) 时间，外层沿最终链走一次，找前驱的右边路径总计线性；O(1) 空间。','搬左树前保存并接好原右树；left必须清空；不能复制节点代替原地展开。',r'''
class Solution {
    public void flatten(TreeNode root) {
        for(TreeNode cur=root;cur!=null;cur=cur.right) {
            if(cur.left!=null) {
                TreeNode pre=cur.left;
                while(pre.right!=null) pre=pre.right;
                pre.right=cur.right; // 原右树接到左树末端
                cur.right=cur.left; cur.left=null;
            }
        }
    }
}''','TreeNode a=tree(1,2,5,3,4,null,6); new Solution().flatten(a); eq(chain(a),"[1, 2, 3, 4, 5, 6]"); TreeNode b=tree(1); new Solution().flatten(b); eq(chain(b),"[1]"); new Solution().flatten(null);')
add(105,'由无重复值的先序和中序序列重建二叉树。保证两个序列合法且描述同一棵树。','pre=[3,9,20,15,7], in=[9,3,15,20,7] → [3,9,20,null,null,15,7]',
'每次线性搜索根在中序的位置，最坏O(n²)。','Map预存中序值到下标。递归build(l,r)处理一段中序区间，空区间返回null；先序游标取当前根并前进，在中序下标mid处分割；必须先构造左树再右树，保持先序消费顺序。返回当前根。',
'先序取3，中序中3在1：左区间只含9，右含15,20,7；先造9，再取20，分出15和7，连接回3。',
'O(n) 平均时间，索引查找平均O(1)，每节点创建一次；O(n) Map加最坏O(n)栈。','游标每次公开调用重置；先左后右不可颠倒；重复值会让单一下标映射失效，题目排除了重复。',r'''
import java.util.*;
class Solution {
    private int index;
    private Map<Integer,Integer> positions;
    public TreeNode buildTree(int[] preorder,int[] inorder) {
        index=0; positions=new HashMap<>();
        for(int i=0;i<inorder.length;i++) positions.put(inorder[i],i);
        return build(preorder,0,inorder.length-1);
    }
    private TreeNode build(int[] pre,int l,int r) {
        if(l>r) return null;
        TreeNode node=new TreeNode(pre[index++]); int mid=positions.get(node.val);
        node.left=build(pre,l,mid-1); // 先序游标先消费完整左树
        node.right=build(pre,mid+1,r);
        return node;
    }
}''','eq(level(new Solution().buildTree(new int[]{3,9,20,15,7},new int[]{9,3,15,20,7})),"[3, 9, 20, null, null, 15, 7]"); eq(level(new Solution().buildTree(new int[]{-1},new int[]{-1})),"[-1]"); eq(new Solution().buildTree(new int[]{},new int[]{})==null,true);')
add(437,'统计树中自上而下、节点连续且和为targetSum的非空路径数。起点不必是根，终点不必是叶。','[10,5,-3,3,2,null,11,3,-2,null,1], target=8 → 3',
'从每个节点出发DFS累加，最坏O(n²)。','在根到当前节点的路径上维护前缀和频次。当前和sum出现后，历史sum-target的次数就是以当前节点结尾的答案数。加入当前sum，递归左右树，返回前将频次减1撤销，防止把不同分支拼成路径。空树返回0，递归返回子树内匹配总数；前缀用long防溢出。',
'根前缀0；到10前缀10；到5前缀15；到3前缀18，查18-8=10存在，得到路径5→3；退回5后撤销18；右支2→1也匹配一条。另一条-3→11。',
'O(n) 平均时间，每节点常数次哈希操作；O(h) 路径频次与递归栈，代码删除零频键，最坏O(n)。','递归返回时一定撤销频次；sum用long；初始0频次为1，路径不能跨兄弟子树。',r'''
import java.util.*;
class Solution {
    public int pathSum(TreeNode root,int targetSum) {
        Map<Long,Integer> count=new HashMap<>(); count.put(0L,1);
        return dfs(root,0L,targetSum,count);
    }
    private int dfs(TreeNode node,long sum,int target,Map<Long,Integer> count) {
        if(node==null) return 0;
        sum+=node.val;
        int ans=count.getOrDefault(sum-target,0);
        count.put(sum,count.getOrDefault(sum,0)+1); // 只记录当前祖先路径
        ans+=dfs(node.left,sum,target,count)+dfs(node.right,sum,target,count);
        int remaining=count.get(sum)-1;
        if(remaining==0) count.remove(sum); else count.put(sum,remaining); // 撤销当前节点
        return ans;
    }
}''','eq(new Solution().pathSum(tree(10,5,-3,3,2,null,11,3,-2,null,1),8),3); eq(new Solution().pathSum(tree(0,0,0),0),5); eq(new Solution().pathSum(null,0),0); eq(new Solution().pathSum(tree(1000000000,1000000000,null,1000000000,null,1000000000,null,1000000000),0),0);')
add(236,'在普通二叉树中找给定两个不同节点p、q的最近公共祖先。保证两个节点都在树中；节点自己也可作为祖先。','[3,5,1,6,2,0,8,null,null,7,4]，p=5,q=4 → 节点5',
'记录每个节点父指针后求祖先交集可行，但要额外Map。','递归返回在当前子树找到的目标节点或共同祖先。null、p、q直接返回自身；递归左右，若都非空，说明两目标分居两侧，返回当前根；仅一侧非空就向上传该侧。两个目标保证存在，使该返回语义成立。',
'5是目标之一，递归到5立即返回5；另一个目标4在它内部，所以5本身即祖先；根3右树无目标，向上传回5。',
'O(n) 时间，每节点至多一次；O(h) 栈，最坏O(n)。','比较节点引用；普通树不能按大小找方向；若不保证节点存在，需要额外存在性检查。',r'''
class Solution {
    public TreeNode lowestCommonAncestor(TreeNode root,TreeNode p,TreeNode q) {
        if(root==null || root==p || root==q) return root;
        TreeNode l=lowestCommonAncestor(root.left,p,q),r=lowestCommonAncestor(root.right,p,q);
        if(l!=null && r!=null) return root; // 两侧各找到一个目标
        return l!=null?l:r; // 单侧找到的结果继续向上传递
    }
}''','TreeNode a=tree(3,5,1,6,2,0,8,null,null,7,4); eq(new Solution().lowestCommonAncestor(a,a.left,a.left.right.right)==a.left,true); eq(new Solution().lowestCommonAncestor(a,a.left,a.right)==a,true); TreeNode b=tree(1,2); eq(new Solution().lowestCommonAncestor(b,b,b.left)==b,true);')
add(124,'求非空二叉树任意两节点之间非空路径的最大节点和。路径不能重复节点，也不能分叉成三条。全负树必须选择一个节点。','[-10,9,20,null,null,15,7] → 42（15→20→7）',
'从每个节点枚举所有路径会重复计算。','gain(node)返回从该节点向下只选一边的最大贡献；空节点贡献0。左右贡献若为负就舍弃为0，用node.val+l+r更新全局best；向父节点返回node.val+max(l,r)。全局best从最小整数开始，确保全负也取节点。',
'15和7贡献分别15、7；20处候选42，向上返回35；根-10候选-10+9+35=34，无法超过42。',
'O(n) 时间，一次后序；O(h) 栈，最坏O(n)。','向上传递不能带两条分支；全局答案不能初始化0；负贡献要截断，节点自身不能整体舍弃导致空路径。',r'''
class Solution {
    private int best;
    public int maxPathSum(TreeNode root) { best=Integer.MIN_VALUE; gain(root); return best; }
    private int gain(TreeNode node) {
        if(node==null) return 0;
        int l=Math.max(0,gain(node.left)),r=Math.max(0,gain(node.right));
        best=Math.max(best,node.val+l+r); // 在当前节点把两条分支接起来
        return node.val+Math.max(l,r); // 父节点只能接上一条分支
    }
}''','eq(new Solution().maxPathSum(tree(-10,9,20,null,null,15,7)),42); eq(new Solution().maxPathSum(tree(-3)),-3); eq(new Solution().maxPathSum(tree(2,-1)),2);')
