from content import add
add(200,'字符矩阵中1是陆地、0是水；只按上下左右连通，求岛屿个数。会把访问过的陆地改为0。','[[1,1,0],[0,1,0],[1,0,1]] → 3',
'每个陆地单独算一座会重复，必须把连通区域整体访问。','逐格扫描，遇未访问1则答案加1，并用显式栈DFS把整个岛清零。入栈时就标记，避免同一格被多个邻居重复加入。使用r*n+c编码位置，弹栈后除以n和取模恢复行列。',
'(0,0)触发第一次DFS，清掉(0,1)、(1,1)；(2,0)触发第二次；(2,2)触发第三次，总计3。',
'O(mn) 时间，每格至多入栈一次且最多检查4个方向；O(mn) 最坏栈空间。','1是字符\'1\'而非整数1；对角线不连通；本解修改输入，需要保留原矩阵时先复制。',r'''
import java.util.*;
class Solution {
    public int numIslands(char[][] grid) {
        int m=grid.length,n=grid[0].length,ans=0;
        int[] dr={1,-1,0,0},dc={0,0,1,-1};
        Deque<Integer> stack=new ArrayDeque<>();
        for(int r=0;r<m;r++) for(int c=0;c<n;c++) {
            if(grid[r][c]!='1') continue;
            ans++; grid[r][c]='0'; stack.push(r*n+c);
            while(!stack.isEmpty()) {
                int p=stack.pop(),x=p/n,y=p%n;
                for(int d=0;d<4;d++) {
                    int a=x+dr[d],b=y+dc[d];
                    if(a>=0 && a<m && b>=0 && b<n && grid[a][b]=='1') {
                        grid[a][b]='0'; stack.push(a*n+b); // 入栈即标记，杜绝重复
                    }
                }
            }
        }
        return ans;
    }
}''','eq(new Solution().numIslands(new char[][]{{\'1\',\'1\',\'0\'},{\'0\',\'1\',\'0\'},{\'1\',\'0\',\'1\'}}),3); eq(new Solution().numIslands(new char[][]{{\'0\'}}),0); eq(new Solution().numIslands(new char[][]{{\'1\'}}),1);')
add(994,'网格0为空、1为新鲜橘子、2为腐烂橘子，每分钟所有腐烂橘子同时感染四邻新鲜橘子。求全部腐烂的最短分钟数，不能全部感染返回-1；本来无新鲜则0。','[[2,1,1],[1,1,0],[0,1,1]] → 4',
'逐分钟扫描整张网格可行，但需区分本分钟与下分钟，否则会瞬间传播。','多源BFS：所有初始腐烂格子入队，统计fresh。每轮固定size，只处理当前这一分钟的腐烂源；新感染即改2并入队，同时fresh减1。完成一层minutes加1。没有新鲜后立即停；队列耗尽还有新鲜说明不可达。',
'初始源(0,0)；第1分钟感染(1,0),(0,1)；第2分钟感染(1,1),(0,2)；第3分钟感染(2,1)；第4分钟感染(2,2)，fresh降0。',
'O(mn) 时间，每个橘子入队一次；O(mn) 队列空间。','全部初始腐烂源同时入队；每层开始固定size；感染时立刻标记，不等出队才标。',r'''
import java.util.*;
class Solution {
    public int orangesRotting(int[][] grid) {
        int m=grid.length,n=grid[0].length,fresh=0,minutes=0;
        Queue<Integer> q=new ArrayDeque<>();
        for(int i=0;i<m;i++) for(int j=0;j<n;j++) {
            if(grid[i][j]==2) q.offer(i*n+j); else if(grid[i][j]==1) fresh++;
        }
        int[] dr={1,-1,0,0},dc={0,0,1,-1};
        while(fresh>0 && !q.isEmpty()) {
            int size=q.size();
            for(int i=0;i<size;i++) {
                int p=q.poll(),r=p/n,c=p%n;
                for(int d=0;d<4;d++) {
                    int x=r+dr[d],y=c+dc[d];
                    if(x>=0 && x<m && y>=0 && y<n && grid[x][y]==1) {
                        grid[x][y]=2; fresh--; q.offer(x*n+y); // 下一分钟的源
                    }
                }
            }
            minutes++;
        }
        return fresh==0?minutes:-1;
    }
}''','eq(new Solution().orangesRotting(new int[][]{{2,1,1},{1,1,0},{0,1,1}}),4); eq(new Solution().orangesRotting(new int[][]{{0,2}}),0); eq(new Solution().orangesRotting(new int[][]{{1}}),-1);')
add(207,'课程编号0..numCourses-1，先修关系[a,b]表示必须先学b再学a。判断能否学完所有课程，允许无依赖。','2门课，[[1,0]] → true；[[1,0],[0,1]] → false',
'尝试所有学习顺序是阶乘级；关键其实是有向图能否拓扑排序。','建边b→a，统计每个节点入度。所有入度0节点入队，逐个学完并将后继入度减1，变0者入队。最终完成数等于总课数才无环；剩余节点无法解除依赖，必然含环。',
'边0→1，入度[0,1]；先学0后令1入度降0；再学1，完成2门。若互相依赖，初始队列为空，完成0门。',
'O(V+E) 时间，每个节点出队一次，每条边处理一次；O(V+E) 邻接表和队列空间。','边方向不能与入度含义冲突；孤立课程也要入队；不是只有从课程0出发的部分需要检查。',r'''
import java.util.*;
class Solution {
    public boolean canFinish(int numCourses,int[][] prerequisites) {
        List<List<Integer>> graph=new ArrayList<>();
        for(int i=0;i<numCourses;i++) graph.add(new ArrayList<>());
        int[] degree=new int[numCourses];
        for(int[] edge:prerequisites) { graph.get(edge[1]).add(edge[0]); degree[edge[0]]++; }
        Queue<Integer> q=new ArrayDeque<>();
        for(int i=0;i<numCourses;i++) if(degree[i]==0) q.offer(i);
        int done=0;
        while(!q.isEmpty()) {
            int u=q.poll(); done++;
            for(int v:graph.get(u)) if(--degree[v]==0) q.offer(v); // 所有前置课已完成
        }
        return done==numCourses;
    }
}''','eq(new Solution().canFinish(2,new int[][]{{1,0}}),true); eq(new Solution().canFinish(2,new int[][]{{1,0},{0,1}}),false); eq(new Solution().canFinish(3,new int[][]{}),true);')
add(208,'实现小写英文字母前缀树：insert插入单词，search检查完整单词，startsWith检查前缀。单词终点必须区别于中间节点。','insert("apple")后search("apple")=true，search("app")=false，startsWith("app")=true',
'列表逐个比较所有单词，查询要随词典规模增加。','每个节点有26个孩子和end标记。沿字符c-\'a\'逐层前进；插入时缺节点就创建，末尾标end。查询共享walk方法，找不到边返回null；search还需end为true，前缀查询只要路径存在。',
'插入apple依次建a→p→p→l→e，只有e标终点；查app能走完路径但p.end=false；插入app后把该p.end设true。',
'每次操作O(L) 时间，L为参数长度；空间O(26S)=O(S)，S为建立的节点数，单次查询O(1)辅助空间。','前缀存在不等于单词存在；数组索引依赖小写输入；重复insert不应破坏现有子树。',r'''
class Trie {
    private final Trie[] children=new Trie[26];
    private boolean end;
    public Trie() {}
    public void insert(String word) {
        Trie node=this;
        for(char c:word.toCharArray()) {
            int i=c-'a';
            if(node.children[i]==null) node.children[i]=new Trie();
            node=node.children[i];
        }
        node.end=true; // 单独标记完整单词的终点
    }
    public boolean search(String word) { Trie node=walk(word); return node!=null && node.end; }
    public boolean startsWith(String prefix) { return walk(prefix)!=null; }
    private Trie walk(String s) {
        Trie node=this;
        for(char c:s.toCharArray()) {
            node=node.children[c-'a'];
            if(node==null) return null; // 某条边不存在就无法匹配
        }
        return node;
    }
}''','Trie t=new Trie(); t.insert("apple"); eq(t.search("apple"),true); eq(t.search("app"),false); eq(t.startsWith("app"),true); t.insert("app"); eq(t.search("app"),true); eq(t.startsWith("b"),false);')

add(46,'给互不相同的整数，返回所有排列，每个元素恰好用一次。','[1,2,3] → 6个排列，如[1,2,3]、[1,3,2]等',
'硬写n重循环不适用于变化的n。','回溯路径path保存已选顺序，used标记每个下标是否已用；选择列表是所有未用元素。路径长度等于n时复制入结果并返回；否则依次选择，递归后删除末项并恢复used。递归返回void，结果参数收集所有叶子。',
'path=[]选1→[1]；再选2→[1,2]；选3→完整[1,2,3]并复制；撤销3、2，改选3再选2得到[1,3,2]；最终撤销1换2开头。',
'O(n·n!) 时间，共n!个结果且每次复制n项；O(n) 递归与路径辅助空间，不含O(n·n!)输出。','必须复制path，不能把可变对象直接加入；used按下标；递归返回必须撤销选择。',r'''
import java.util.*;
class Solution {
    public List<List<Integer>> permute(int[] nums) {
        List<List<Integer>> ans=new ArrayList<>();
        dfs(nums,new boolean[nums.length],new ArrayList<>(),ans); return ans;
    }
    private void dfs(int[] a,boolean[] used,List<Integer> path,List<List<Integer>> ans) {
        if(path.size()==a.length) { ans.add(new ArrayList<>(path)); return; }
        for(int i=0;i<a.length;i++) {
            if(used[i]) continue;
            used[i]=true; path.add(a[i]); // 做选择
            dfs(a,used,path,ans);
            path.remove(path.size()-1); used[i]=false; // 撤销选择
        }
    }
}''','eq(norm(new Solution().permute(new int[]{1,2,3})),"[[1, 2, 3], [1, 3, 2], [2, 1, 3], [2, 3, 1], [3, 1, 2], [3, 2, 1]]"); eq(new Solution().permute(new int[]{0,1}).size(),2); eq(new Solution().permute(new int[]{1}).toString(),"[[1]]");')
add(78,'给互不相同整数，返回全部子集，含空集与全集；元素顺序不必变化。','[1,2] → [[],[1],[1,2],[2]]（顺序不限）',
'用二进制掩码枚举也可以；回溯便于理解如何避免重复。','path是当前子集，start是下一次可选的最小下标。每到一个递归节点就复制当前path入答案；选择列表为[start,n)。选i后递归i+1，结束返回后删除末项。start=n时循环不执行，自然终止。',
'[]先入答案；选1记录[1]；再选2记录[1,2]；退回[]后选2记录[2]。严格递增下标避免[2,1]重复表示同一集合。',
'O(n·2^n) 时间，2^n个子集各复制至多n项；O(n) 辅助空间，输出O(n·2^n)。','空集不能遗漏；递归参数是i+1不是start+1；加入答案时必须复制。',r'''
import java.util.*;
class Solution {
    public List<List<Integer>> subsets(int[] nums) {
        List<List<Integer>> ans=new ArrayList<>(); dfs(nums,0,new ArrayList<>(),ans); return ans;
    }
    private void dfs(int[] a,int start,List<Integer> path,List<List<Integer>> ans) {
        ans.add(new ArrayList<>(path)); // 每个节点本身就是一个合法子集
        for(int i=start;i<a.length;i++) {
            path.add(a[i]); dfs(a,i+1,path,ans);
            path.remove(path.size()-1); // 回到本层状态，尝试下一个数
        }
    }
}''','eq(norm(new Solution().subsets(new int[]{1,2})),"[[1, 2], [1], [2], []]"); eq(new Solution().subsets(new int[]{0}).size(),2); eq(new Solution().subsets(new int[]{1,2,3}).size(),8);')
add(17,'输入只含2..9的数字串，返回电话键盘对应的全部字母组合。空输入返回空列表。','"23" → ["ad","ae","af","bd","be","bf","cd","ce","cf"]',
'逐层列表拼接可行，但反复创建中间字符串。','回溯路径使用StringBuilder；index表示当前要处理的数字，选择列表是该数字映射的3或4个字母。选一个append，递归index+1；返回后删末字符。index==digits.length时toString保存完整结果。',
'先给2选a，再为3依次选d、e、f，得到ad、ae、af；撤销a，换b得到bd、be、bf；最后c开头三组。',
'O(L·4^L) 最坏时间，L为数字数，结果复制长L；O(L) 辅助空间，不含输出。','空串应返回空列表而非包含空串；数字字符减\'0\'转索引；StringBuilder共享要撤销。',r'''
import java.util.*;
class Solution {
    private static final String[] LETTERS={"","","abc","def","ghi","jkl","mno","pqrs","tuv","wxyz"};
    public List<String> letterCombinations(String digits) {
        List<String> ans=new ArrayList<>();
        if(!digits.isEmpty()) dfs(digits,0,new StringBuilder(),ans);
        return ans;
    }
    private void dfs(String s,int index,StringBuilder path,List<String> ans) {
        if(index==s.length()) { ans.add(path.toString()); return; }
        for(char c:LETTERS[s.charAt(index)-'0'].toCharArray()) {
            path.append(c); dfs(s,index+1,path,ans);
            path.deleteCharAt(path.length()-1); // 删除本层选择，保留前缀
        }
    }
}''','eq(new Solution().letterCombinations("23").toString(),"[ad, ae, af, bd, be, bf, cd, ce, cf]"); eq(new Solution().letterCombinations("").size(),0); eq(new Solution().letterCombinations("7").size(),4);')
add(39,'给不重复正整数candidates和正目标值，返回和为目标的所有组合。每个候选数可重复使用，组合不考虑顺序。','[2,3,6,7], target=7 → [[2,2,3],[7]]',
'任意挑选会生成同一组合的许多排列，还可能无限尝试。','排序后回溯。path为已选组合，remain为还差的和，选择列表从start开始，保证非递减下标。remain=0复制并返回；候选值大于remain时后面更大，直接break剪枝。选i后仍传i允许复用，返回删除末项。正数保证remain严格减少。',
'remain7先选2剩5，再选2剩3，再选2剩1无解退回；换3剩0得到[2,2,3]；根分支选7直接得[7]。',
'设T为target、c为最小候选、N为候选数，深度D=⌊T/c⌋；O((N+1)^(D+1)·(D+1)) 为宽松搜索及复制上界，另有排序O(N log N)；辅助O(D+log N)，输出另计。','允许复用时递归传i；候选必须为正才终止；去重依靠递增下标而不是结果contains。',r'''
import java.util.*;
class Solution {
    public List<List<Integer>> combinationSum(int[] candidates,int target) {
        Arrays.sort(candidates); List<List<Integer>> ans=new ArrayList<>();
        dfs(candidates,0,target,new ArrayList<>(),ans); return ans;
    }
    private void dfs(int[] a,int start,int remain,List<Integer> path,List<List<Integer>> ans) {
        if(remain==0) { ans.add(new ArrayList<>(path)); return; }
        for(int i=start;i<a.length;i++) {
            if(a[i]>remain) break; // 后续更大，不可能补足
            path.add(a[i]); dfs(a,i,remain-a[i],path,ans);
            path.remove(path.size()-1); // 撤销当前数
        }
    }
}''','eq(norm(new Solution().combinationSum(new int[]{2,3,6,7},7)),"[[2, 2, 3], [7]]"); eq(new Solution().combinationSum(new int[]{2},1).size(),0); eq(new Solution().combinationSum(new int[]{1},2).toString(),"[[1, 1]]");')
add(22,'给n对括号，生成所有完整且合法的括号字符串。任何前缀的右括号数不能超过左括号数。','n=3 → ["((()))","(()())","(())()","()(())","()()()"]',
'枚举所有2^(2n)字符串再判合法，浪费大量非法前缀。','回溯path、已用左括号left、右括号right。left<n可以选左括号，right<left才可选右括号。路径长2n即结束并复制。每次append后递归再删末字符。前缀始终合法，避免生成后再过滤。',
'n=2：[]只能选(；之后可选(形成((，只能补))得到(())；退回第一个(后选)得()，再补()得到()()。',
'O(n·C_n) 时间，C_n为第n个卡特兰数，保存每个长2n的结果；O(n) 辅助栈和路径，输出另计。','right<n并不足以合法；必须right<left；两条分支都需要撤销；终点应复制字符串。',r'''
import java.util.*;
class Solution {
    public List<String> generateParenthesis(int n) {
        List<String> ans=new ArrayList<>(); dfs(n,0,0,new StringBuilder(),ans); return ans;
    }
    private void dfs(int n,int left,int right,StringBuilder path,List<String> ans) {
        if(path.length()==2*n) { ans.add(path.toString()); return; }
        if(left<n) {
            path.append('('); dfs(n,left+1,right,path,ans); path.deleteCharAt(path.length()-1);
        }
        if(right<left) { // 只允许用已有的左括号来匹配
            path.append(')'); dfs(n,left,right+1,path,ans); path.deleteCharAt(path.length()-1);
        }
    }
}''','eq(new Solution().generateParenthesis(3).toString(),"[((())), (()()), (())(), ()(()), ()()()]"); eq(new Solution().generateParenthesis(1).toString(),"[()]"); eq(new Solution().generateParenthesis(2).size(),2);')
add(79,'在字符矩阵中沿上下左右寻找单词路径，同一格在一条路径中不可重复使用。返回是否存在，单词非空。','[[A,B,C,E],[S,F,C,S],[A,D,E,E]], word="ABCCED" → true',
'从每格尝试所有邻接路线是基本搜索；用访问标记剪掉重复使用。','从每格启动dfs(r,c,k)，表示要匹配word[k]。越界或字符不符返回false；匹配最后一个字符返回true。否则保存字符，把当前格临时标成#，尝试四邻匹配k+1，再恢复原字符。路径是被标记的格子，选择列表是未使用四邻，返回值表示存在一条成功分支。即使成功也先恢复再返回。',
'从(0,0)A走右B、右C、下C、下E、左D，逐个匹配ABCCED；沿途格子临时禁用，函数退出时逐个恢复。',
'宽松O(mn·4^L) 时间，L为单词长度，每格作起点、每层至多4分支；O(L) 递归栈，实际深度不超过mn。','每个起点尝试后须恢复；不能对角走；不能用同一格多次，标记字符须不在输入字母集。',r'''
class Solution {
    public boolean exist(char[][] board,String word) {
        for(int r=0;r<board.length;r++) for(int c=0;c<board[0].length;c++) {
            if(dfs(board,word,r,c,0)) return true;
        }
        return false;
    }
    private boolean dfs(char[][] b,String s,int r,int c,int k) {
        if(r<0 || r>=b.length || c<0 || c>=b[0].length || b[r][c]!=s.charAt(k)) return false;
        if(k==s.length()-1) return true;
        char saved=b[r][c]; b[r][c]='#'; // 本路径禁止重复使用当前格
        boolean ok=dfs(b,s,r+1,c,k+1)||dfs(b,s,r-1,c,k+1)||dfs(b,s,r,c+1,k+1)||dfs(b,s,r,c-1,k+1);
        b[r][c]=saved; // 无论成功失败，都恢复供其他分支使用
        return ok;
    }
}''','eq(new Solution().exist(new char[][]{{\'A\',\'B\',\'C\',\'E\'},{\'S\',\'F\',\'C\',\'S\'},{\'A\',\'D\',\'E\',\'E\'}},"ABCCED"),true); eq(new Solution().exist(new char[][]{{\'A\',\'B\'}},"ABA"),false); eq(new Solution().exist(new char[][]{{\'A\'}},"A"),true);')
add(131,'把字符串切成若干连续片段，每片都必须回文，返回所有切法。','"aab" → [["a","a","b"],["aa","b"]]',
'枚举所有切点再逐段判断回文，会重复判断同一片段。','先预计算pal[i][j]表示闭区间回文：首尾相等且长度≤2或pal[i+1][j-1]为真。i倒序、j正序以保证内区间已知。回溯路径是已切片段，start为剩余串开头，选择所有pal[start][end]为真的end；start到串尾复制结果，否则选substring后递归end+1，再删除末片。',
'pal[0][1]=true因为aa；从start0先选a，再选a、b得[a,a,b]；回根选aa，再选b得[aa,b]。',
'O(n²+n·2^n) 时间，预处理加全部切分与字符串复制的上界；O(n²) 回文表加O(n)栈，输出另计。','substring右端要end+1；表的i倒序；只复制path还要注意其中字符串不可变，所以浅复制足够。',r'''
import java.util.*;
class Solution {
    public List<List<String>> partition(String s) {
        int n=s.length(); boolean[][] pal=new boolean[n][n];
        for(int i=n-1;i>=0;i--) for(int j=i;j<n;j++) {
            pal[i][j]=s.charAt(i)==s.charAt(j) && (j-i<2 || pal[i+1][j-1]);
        }
        List<List<String>> ans=new ArrayList<>(); dfs(s,0,pal,new ArrayList<>(),ans); return ans;
    }
    private void dfs(String s,int start,boolean[][] pal,List<String> path,List<List<String>> ans) {
        if(start==s.length()) { ans.add(new ArrayList<>(path)); return; }
        for(int end=start;end<s.length();end++) if(pal[start][end]) {
            path.add(s.substring(start,end+1)); dfs(s,end+1,pal,path,ans);
            path.remove(path.size()-1); // 撤销本次切片
        }
    }
}''','eq(norm(new Solution().partition("aab")),"[[a, a, b], [aa, b]]"); eq(new Solution().partition("a").toString(),"[[a]]"); eq(new Solution().partition("abc").toString(),"[[a, b, c]]");')
add(51,'在n×n棋盘放n个皇后，任意两个不同行、列或斜线。返回全部棋盘，Q为皇后、.为空位。','n=4 → 2种棋盘，其中一种为[".Q..","...Q","Q...","..Q."]',
'枚举n²个格子任意放置后检查，空间分支巨大。','逐行回溯，path由每行皇后列号pos组成。选择列表是当前行未被占列及两条斜线攻击的列。列用col[c]，主斜线用diag1[r-c+n-1]，副斜线用diag2[r+c]。放下后标记，递归下一行，返回全部撤销；r=n时按pos创建字符串棋盘。',
'n=4时从第0行列0出发均失败；改列1，第1行可列3，第2行列0，第3行列2，得到第一解；恢复标记后继续找到镜像解。',
'宽松O(n·n!+n²S) 时间，每层至多检查n列，S为解数且每棋盘构建n²字符；O(n) 标记、路径、栈辅助空间，输出O(n²S)。','r-c可能负须平移n-1；每次返回恢复三类标记；棋盘每行都要独立创建。',r'''
import java.util.*;
class Solution {
    public List<List<String>> solveNQueens(int n) {
        List<List<String>> ans=new ArrayList<>();
        dfs(0,n,new int[n],new boolean[n],new boolean[2*n-1],new boolean[2*n-1],ans); return ans;
    }
    private void dfs(int r,int n,int[] pos,boolean[] col,boolean[] d1,boolean[] d2,List<List<String>> ans) {
        if(r==n) {
            List<String> board=new ArrayList<>();
            for(int c:pos) { char[] row=new char[n]; Arrays.fill(row,'.'); row[c]='Q'; board.add(new String(row)); }
            ans.add(board); return;
        }
        for(int c=0;c<n;c++) {
            int a=r-c+n-1,b=r+c;
            if(col[c] || d1[a] || d2[b]) continue;
            pos[r]=c; col[c]=d1[a]=d2[b]=true;
            dfs(r+1,n,pos,col,d1,d2,ans);
            col[c]=d1[a]=d2[b]=false; // 离开当前放置，撤销所有占用标记
        }
    }
}''','List<List<String>> a=new Solution().solveNQueens(4); eq(a.size(),2); queens(a,4); eq(new Solution().solveNQueens(1).toString(),"[[Q]]"); eq(new Solution().solveNQueens(2).size(),0);')
