"""附录原稿，统一由render写出。"""
JAVA = [
('基本数据类型和变量','变量像带类型标签的盒子。int保存32位有符号整数，long保存64位整数，boolean只有true/false，char保存一个UTF-16代码单元，double保存浮点数。整数/整数会截断小数。',
'int count = 0;\nlong sum = 0L;\nboolean found = false;\nchar letter = \'a\';\ndouble average = ((double) 2 + 3) / 2;',
'Integer.MIN_VALUE/MAX_VALUE是int边界；Long.MIN_VALUE/MAX_VALUE对应long。强转(double)在运算前提升类型。','437路径总和使用long，4中位数使用double。','int乘法可能先溢出再赋给long，应写(long)a*b；局部变量必须初始化后使用。'),
('数组及二维数组','数组长度创建后固定，从下标0开始。int[]是整数数组，int[][]是“数组的数组”，本手册矩阵题使用每行等长的矩形。',
'int[] nums = {2, 7, 11};\nint[] zeros = new int[3];\nint[][] grid = {{1, 2}, {3, 4}};\nint value = grid[1][0]; // 第二行第一列，值3',
'a.length是字段，不带括号；a[i]读写元素；a.clone()只复制一层，二维数组深复制要逐行clone。','283原地移动，73用首行首列标记。','合法下标0..length-1；二维数组的行数grid.length，列数grid[0].length；访问grid[0]前需满足非空约束。'),
('for、while、增强for','for适合知道遍历范围，while适合按条件反复，增强for适合逐个读取元素。break结束整个当前循环，continue跳过本轮剩余语句。',
'int[] a = {1, 2, 3};\nfor (int i = 0; i < a.length; i++) { a[i]++; }\nfor (int value : a) { System.out.println(value); }\nint left = 0, right = a.length - 1;\nwhile (left < right) { left++; right--; }',
'i++返回旧值再自增，++i先自增再返回；独立语句中两者效果相同。','1按下标返回答案，239用while清理队列。','增强for中的基本类型变量是副本，对value赋值不会修改数组；需要下标时用普通for。'),
('方法、参数和返回值','方法封装一段操作，参数是调用时传入的信息，return返回计算结果并结束当前调用。void表示不返回值。',
'class Demo {\n    int add(int a, int b) { return a + b; }\n    void clear(int[] a) { java.util.Arrays.fill(a, 0); }\n}',
'签名由方法名和参数类型等决定；调用add(2,3)得到int 5；void方法可以使用return;提前结束。','Solution公开方法供力扣调用，private辅助方法拆分算法。','非void方法的正常执行路径必须返回值；参数名只在方法内部有效；题目方法名和参数类型不可随意改动。'),
('类与对象','类是描述数据和操作的模板，对象是用new创建的具体实例；两个new一般得到不同对象，即使字段值相同。',
'class Box { int value; }\n// 在方法内部：\n// Box a = new Box();\n// Box b = new Box();\n// a.value = 3; // 不会改变b.value',
'new分配对象并调用构造器；点号访问字段或方法；引用变量保存对象的引用。','链表节点和树节点都是对象；160根据对象身份判断相交。','a==b比较引用是否指向同一对象；两个值相同的节点不代表同一个节点。'),
('构造方法、成员变量、成员方法','成员变量保存对象状态，构造方法初始化对象，成员方法读取或修改状态。构造方法与类同名且没有返回类型。',
'class Counter {\n    private int value;\n    Counter(int start) { this.value = start; }\n    int next() { return ++value; }\n}',
'new Counter(3)调用有参构造器；c.next()返回4并保存新状态；对象成员默认初始化，而局部变量不会。','146缓存保存容量和链表，208节点保存孩子和终点标记。','构造方法不能写void；定义有参构造后不会自动提供无参构造；不要在算法多次调用间遗留旧答案。'),
('this与static','this指向当前对象；static属于类本身，各实例共享，常用来存不变配置或独立工具方法。实例方法才能直接使用this。',
'class Demo {\n    private int value;\n    static final int LIMIT = 100;\n    Demo(int value) { this.value = value; }\n    static int twice(int x) { return x * 2; }\n}',
'this.value区分字段和同名参数；Demo.twice(3)返回6；final引用不能再指向别处，但指向的数组仍可能被修改。','17用static final保存字母映射，146用static嵌套节点类。','不要把每题结果列表设为共享static可变状态；static方法不能直接读取非static字段。'),
('封装、继承、多态','封装把内部状态藏在private后，通过方法维护规则。继承用extends表达一种更具体的类型；多态让父类型引用调用实际对象的重写实现。',
'class Animal { String sound() { return "?"; } }\nclass Cat extends Animal {\n    @Override String sound() { return "喵"; }\n}\n// Animal pet = new Cat(); pet.sound()实际返回“喵”',
'private限制类内访问，public开放；@Override帮助编译器检查确实在重写；super可调用父类构造或方法。','List<Integer> list = new ArrayList<>();体现面向抽象类型编程。','Java类只能extends一个类；方法重载看参数列表，方法重写发生在继承实现关系中，二者不同。'),
('接口与抽象类','接口描述对象能做什么，抽象类可保存共享状态和部分实现。接口可被多个类实现，抽象类不能直接new。',
'interface Task { int run(); }\nabstract class BaseTask {\n    protected int count;\n    abstract int run();\n}\nclass SimpleTask implements Task {\n    public int run() { return 1; }\n}',
'implements实现接口，extends继承类；抽象方法由具体类实现；接口也可以有default方法。','List、Map、Set、Queue、Deque是接口，ArrayList、HashMap等是实现类。','不能new List<>()；声明接口类型时只能直接使用该接口暴露的方法。'),
('String与StringBuilder','String不可变，每次改变文本实际上创建新串；StringBuilder是可变字符缓冲，适合循环拼接或回溯路径。',
'String s = "abc";\nchar c = s.charAt(1); // b\nString part = s.substring(0, 2); // ab\nStringBuilder path = new StringBuilder();\npath.append(\'a\');\nString snapshot = path.toString();\npath.deleteCharAt(path.length() - 1);',
'length()返回长度；charAt(i)返回char；substring(l,r)左闭右开；toCharArray()创建新char[]；append返回当前builder，toString生成不可变快照。','17/22回溯生成字符串，394多层解码。','字符串内容比较用equals；下标要小于length()；循环s+=可能制造大量临时对象；char不总等同一个Unicode字符，本题按官方输入字符范围处理。'),
('ArrayList与List','List是有序可重复列表接口，ArrayList用可扩容数组实现；尾部添加通常快，插入中间或头部需要搬移。',
'java.util.List<Integer> path = new java.util.ArrayList<>();\npath.add(2);\nint first = path.get(0);\njava.util.List<Integer> copy = new java.util.ArrayList<>(path);\npath.remove(path.size() - 1);',
'add(E)追加并返回true，get(i)读取，set(i,x)替换并返回旧值，remove(int)删下标并返回旧值，size()元素数。get/set O(1)，尾add摊还O(1)，中间remove O(n)。','回溯结果和路径，102层序二维列表。','remove(1)删除下标1；remove(Integer.valueOf(1))删值1；new ArrayList<>(path)是浅复制，嵌套可变对象仍共享。'),
('HashMap与Map','Map建立键到值的映射，每个键至多一个当前值。HashMap按equals和hashCode确定键，平均查找O(1)，不保证遍历顺序。',
'java.util.Map<Integer, Integer> count = new java.util.HashMap<>();\ncount.put(7, count.getOrDefault(7, 0) + 1);\nboolean exists = count.containsKey(7);\nint times = count.get(7);\ncount.remove(7);',
'put(k,v)返回旧值或null；get(k)返回对应值或null；getOrDefault(k,d)缺失用默认值d；entrySet()遍历键值对；size()返回键数。','1数值到下标，560前缀到次数。','get缺失返回null，拆箱成int会空指针；频次必须累加而非覆盖为1；Integer比较值不要依赖==缓存。'),
('HashSet与Set','Set只保存不重复元素，HashSet平均查找、插入、删除O(1)，顺序未定义。',
'java.util.Set<Integer> seen = new java.util.HashSet<>();\nboolean first = seen.add(2); // true\nboolean again = seen.add(2); // false\nboolean has = seen.contains(2);\nseen.remove(2);',
'add返回是否真的新增；contains返回是否存在；remove返回是否存在并删除；size是不同元素个数。','128去重并找前驱，3维护窗口字符。','不要把无序集合当有序数组；自定义可变对象作为键时修改参与哈希的字段会破坏查找；节点默认按身份比较。'),
('Deque、ArrayDeque和栈','Deque双端队列可在两头操作；ArrayDeque是数组实现。栈是一端进一端出的后进先出结构，优先用Deque而非旧Stack类。',
'java.util.Deque<Integer> stack = new java.util.ArrayDeque<>();\nstack.push(3); stack.push(5);\nint top = stack.peek(); // 5，未删除\nint popped = stack.pop(); // 5，删除\nboolean empty = stack.isEmpty();',
'push/pop/peek操作头部；addLast/removeLast/peekLast操作尾部；offerLast/pollFirst可作队列。两端操作通常摊还O(1)。','20括号匹配、84单调栈、239单调双端队列。','ArrayDeque不接受null；pop空栈抛异常，peek空栈返回null，拆箱仍会出错；不要混淆队首队尾。'),
('Queue与PriorityQueue','普通Queue按先入先出供BFS使用；PriorityQueue按优先级出队，是堆，不按插入顺序。默认最小堆。',
'java.util.Queue<Integer> queue = new java.util.ArrayDeque<>();\nqueue.offer(1); queue.offer(2);\nint first = queue.poll(); // 1\njava.util.PriorityQueue<Integer> heap = new java.util.PriorityQueue<>();\nheap.offer(5); heap.offer(2);\nint min = heap.peek(); // 2',
'offer插入，poll取出并删除队首/堆顶，peek只读；空poll/peek返回null。堆offer/poll O(log n)，peek O(1)；遍历堆不保证有序。','102层序使用队列，215保留前k大，295双堆中位数。','优先队列不能代替BFS队列；最大堆须传反向比较器；不可插入null。'),
('泛型','泛型用类型参数表达集合里装什么，让编译器提前发现类型错误。List<Integer>保存整数包装对象，不是原生int。',
'java.util.List<Integer> numbers = new java.util.ArrayList<>();\nnumbers.add(3); // int自动装箱为Integer\nint x = numbers.get(0); // 自动拆箱\njava.util.List<java.util.List<Integer>> groups = new java.util.ArrayList<>();',
'尖括号中是引用类型；<>菱形语法让右侧类型由上下文推断；List<List<Integer>>是列表的列表。','回溯二维结果、哈希表键值类型、节点队列。','不能写List<int>；List<Integer>不是List<Number>的子类型；拆箱null会抛NullPointerException。'),
('Lambda表达式','Lambda是函数式接口的简写实现；函数式接口只有一个抽象方法。参数从目标类型推断，->右侧是执行体。',
'java.util.List<int[]> rows = new java.util.ArrayList<>();\nrows.sort((a, b) -> Integer.compare(a[0], b[0]));\njava.util.Map<String, java.util.List<String>> map = new java.util.HashMap<>();\nmap.computeIfAbsent("key", k -> new java.util.ArrayList<>()).add("value");',
'computeIfAbsent(key,fn)在键未关联非null值时调用fn建立值并返回该值；k是传入的键，new ArrayList<>()是新组；返回List后可继续add。传统写法：if(!map.containsKey(key)) map.put(key,new ArrayList<>()); map.get(key).add(value);','56排序区间、23堆按节点值比较；49正文采用更容易读的传统写法。','Lambda参数不是字符串；捕获的局部变量须final或有效final；不要为简短而使用不理解的链式调用。'),
('Comparator与Comparable','Comparable定义类型的自然顺序（compareTo），Comparator是独立比较规则（compare），可为同一类型指定不同排序。',
'java.util.Comparator<Integer> ascending = Integer::compare;\njava.util.PriorityQueue<Integer> maxHeap =\n    new java.util.PriorityQueue<>(java.util.Comparator.reverseOrder());\nint cmp = Integer.compare(2, 5); // 负数，表示2应在5之前',
'compare(a,b)<0表示a在前，=0同序，>0表示b在前；reverseOrder()反转自然顺序；Integer::compare是方法引用，等价(a,b)->Integer.compare(a,b)。','56区间排序，295左侧最大堆。','不要写a-b比较极值，可能溢出；比较器应保持反对称和传递性；原生int[]不能传Comparator逐元素排序。'),
('Arrays、Collections、Math常用API','这些工具类提供静态方法，不需要new；Arrays作用于数组，Collections作用于集合，Math做数学比较。',
'int[] a = {3, 1, 2};\njava.util.Arrays.sort(a);\nboolean same = java.util.Arrays.equals(a, new int[]{1, 2, 3});\njava.util.Arrays.fill(a, 0);\nint larger = Math.max(2, 5);\njava.util.List<Integer> list = new java.util.ArrayList<>(java.util.Arrays.asList(3, 1));\njava.util.Collections.sort(list);',
'sort修改原容器；equals比较一维数组内容，deepEquals比较嵌套对象数组；fill全部赋值；asList返回定长列表；Collections.reverse反转列表；Math.max/min返回较大/小值。','49排序字符，438比较计数数组，DP初始化和最优值更新。','Arrays.asList(int[])会得到只含整个int[]的列表；asList不能add/remove；数组==比较引用而非内容。'),
('递归','方法调用自身处理更小子问题。每层调用有自己的参数与局部变量，通过调用栈保留现场；必须明确终止条件、递归过程、返回含义。',
'class Demo {\n    int sum(int n) {\n        if (n == 0) return 0; // 终止\n        return n + sum(n - 1); // 子问题变小，返回前n项和\n    }\n}',
'sum(3)展开3+sum(2)，再2+sum(1)，最终sum(0)=0，自底向上返回1、3、6。栈深度也占空间。','104返回子树高度，46回溯排列。','没有终止会无限递归；输入退化成长链时Java可能StackOverflowError，需要显式栈；不要把递归栈算成O(1)。'),
('引用、null、对象传参','Java始终按值传参；对象参数传入的是“引用值的副本”。方法能经引用修改同一对象，但给参数重新赋new不会替换调用者变量。null表示没有指向对象。',
'class Demo {\n    void edit(int[] a) { a[0] = 9; } // 调用者可看到\n    void replace(int[] a) { a = new int[]{9}; } // 只改局部参数\n    boolean empty(int[] a) { return a == null; }\n}',
'p.next=null切断链接；p=q只复制引用，不复制对象；&&与||会短路，p!=null && p.next!=null能防止访问空引用。','206必须保存next，138必须new新节点，146维护共享节点引用。','不能调用null的方法或字段；引用副本不是深拷贝；Java没有C++式引用传递。'),
('位运算基础','整数按二进制逐位计算：&两位都1才1，|任一为1即1，^相异为1，~按位取反；<<左移，>>保留符号右移，>>>补0右移。',
'int xor = 5 ^ 3; // 101 ^ 011 = 110，即6\nint lowBit = 6 & -6; // 得最低位的1，值2\nboolean odd = (5 & 1) != 0;\nint doubled = 3 << 1; // 6',
'x^x=0，x^0=x，异或交换结合；移位优先级容易误读，应加括号。int移位距离只使用低5位，1<<32等于1。','136成对抵消；进阶可位掩码枚举78子集。','^不是指数运算；&与&&不同，前者不短路；负数按补码表示，不要把逻辑右移与算术右移混用。'),
]

ALGORITHMS=[
('哈希表','把键映射到值或存在性，适合补数、去重、频次、前缀状态查询。','Map<Integer,Integer> count = new HashMap<>();\nfor (int x : nums) count.put(x, count.getOrDefault(x, 0) + 1);','平均查找/插入O(1)，总计O(n)时间、O(n)空间；碰撞严重时不能保证简单常数。','1、49、128、560；区分映射的值是下标还是次数。'),
('双指针','两个位置协调扫描，把不可能的候选整体排除，适合有序配对、原地压缩、快慢链表。','int l = 0, r = a.length - 1;\nwhile (l < r) {\n    int sum = a[l] + a[r];\n    if (sum < target) l++; else if (sum > target) r--; else break;\n}','有序两数配对O(n)时间O(1)空间，若先排序另计O(n log n)。','11、15、283、141；先证明为什么某一侧可被舍弃。'),
('滑动窗口','维护连续区间及其统计量，通过扩张和收缩避免重复扫描。适合不重复字符、固定窗口频次、最小覆盖。','Set<Character> window = new HashSet<>();\nint left = 0, best = 0;\nfor (int right = 0; right < s.length(); right++) {\n    char c = s.charAt(right);\n    while (window.contains(c)) window.remove(s.charAt(left++));\n    window.add(c);\n    best = Math.max(best, right - left + 1);\n}','两端各移动至多n次且维护O(1)时，总O(n)时间；空间取决于频次数组或集合。','3、438、76；模板演示无重复字符窗口；其他问题需要重设合法条件和更新答案时机。含负数的和不具简单单调性，560改用前缀。'),
('前缀和','前缀累计把区间和转为两个前缀之差，适合区间查询与统计目标和区间。','long[] pre = new long[nums.length + 1];\nfor (int i = 0; i < nums.length; i++) pre[i + 1] = pre[i] + nums[i];\nlong sum = pre[r + 1] - pre[l]; // 闭区间[l,r]','预处理O(n)，每次区间查询O(1)，数组空间O(n)。','560、437；历史前缀计数初始0出现一次，查完再登记。'),
('链表','节点保存值和后继，按引用连接；访问中间项需从头走，已知前驱时插删O(1)。','ListNode prev = null, cur = head;\nwhile (cur != null) {\n    ListNode next = cur.next;\n    cur.next = prev; prev = cur; cur = next;\n}\nreturn prev;','反转O(n)时间O(1)空间；随机定位O(n)。','206、21、19、25；先保存后继再改next，dummy统一处理头部。'),
('栈和队列','栈后进先出管理嵌套和待处理状态，队列先进先出管理距离层次。','Deque<Integer> stack = new ArrayDeque<>();\nstack.push(1); int top = stack.pop();\nQueue<Integer> q = new ArrayDeque<>();\nq.offer(1); int first = q.poll();','两端操作摊还O(1)，处理n个元素O(n)时间，最坏O(n)空间。','20、155、102、994；不要混淆栈顶和队首。'),
('二叉树','每节点至多两个孩子，递归结构适合分治；BST额外具有左小右大的全子树约束。','int height(TreeNode node) {\n    if (node == null) return 0;\n    return Math.max(height(node.left), height(node.right)) + 1;\n}','遍历O(n)，递归O(h)空间；平衡BST查找O(log n)，退化树O(n)。','94、98、104、236、124；说明递归返回值，是高度、布尔还是路径贡献。'),
('DFS与BFS','DFS先走深处再回退，适合连通块和路径；BFS按边数逐层扩展，适合无权图最短距离。','Queue<TreeNode> q = new ArrayDeque<>();\nif (root != null) q.offer(root);\nwhile (!q.isEmpty()) {\n    int size = q.size();\n    for (int i = 0; i < size; i++) {\n        TreeNode node = q.poll();\n        if (node.left != null) q.offer(node.left);\n        if (node.right != null) q.offer(node.right);\n    }\n}','图遍历O(V+E)时间O(V)辅助空间（不含图存储），网格O(mn)。','200、994、207、102；一般图必须标记访问，BFS在入队时标记。'),
('回溯','在决策树逐步构造路径，失败或收集后撤销选择。用于穷举解集及约束搜索。','void dfs(int[] a, int start, List<Integer> path, List<List<Integer>> ans) {\n    ans.add(new ArrayList<>(path));\n    for (int i = start; i < a.length; i++) {\n        path.add(a[i]);\n        dfs(a, i + 1, path, ans);\n        path.remove(path.size() - 1);\n    }\n}','复杂度由搜索树和输出决定，子集O(n2^n)，排列O(n·n!)；辅助空间一般O(深度)。','46、78、39、51；明确路径、选择列表、结束条件、撤销动作；结果需要快照。'),
('二分查找','在有单调判断的候选区间不断排除一半，适合有序查找、上下界、答案划分。','int l = 0, r = a.length;\nwhile (l < r) {\n    int mid = l + (r - l) / 2;\n    if (a[mid] < target) l = mid + 1; else r = mid;\n}\nreturn l; // 第一个>=target的位置，可等于n','O(log n)时间O(1)空间；前提是每步能保持不变量并缩短区间。','35、34、33、153、4；闭区间与半开区间模板不能随意拼接。'),
('堆','堆是局部有序结构，可快速取最小或最大；不保证内部遍历完整有序。适合Top K和多路归并。','PriorityQueue<Integer> heap = new PriorityQueue<>();\nfor (int x : nums) {\n    heap.offer(x);\n    if (heap.size() > k) heap.poll();\n}\nreturn heap.peek();','入出堆O(log k)，读顶O(1)，保留k大O(n log(k+1))时间O(k)空间。','215、23、295；保留最大的k个通常用最小堆淘汰小值。'),
('贪心','每步做有证明的局部最优，压缩搜索空间；必须解释为什么不会丢掉全局最优。','int far = 0;\nfor (int i = 0; i < nums.length; i++) {\n    if (i > far) return false;\n    far = Math.max(far, i + nums[i]);\n}\nreturn true;','取决于问题；跳跃O(n)时间O(1)空间，若先排序则常为O(n log n)。','55、45、763、121；322任意币值不能直接最大币优先，反例[1,3,4]凑6。'),
('动态规划','把重复子问题抽成状态，按依赖顺序计算，每个状态只求一次。适合计数、最优值、可行性。','int[] dp = new int[amount + 1];\nArrays.fill(dp, amount + 1); dp[0] = 0;\nfor (int a = 1; a <= amount; a++) {\n    for (int coin : coins) if (coin <= a) {\n        dp[a] = Math.min(dp[a], dp[a - coin] + 1);\n    }\n}','通常为状态数×每状态转移数；322为O(A·C)时间O(A)空间，不能一概说O(n)。','70、198、322、300、416、72；写清状态、转移、初始化、遍历顺序，最后才考虑压缩空间。'),
('单调栈','栈内对应值保持单调，利用新元素结算旧元素的第一个更大/更小边界。','Deque<Integer> stack = new ArrayDeque<>();\nfor (int i = 0; i < a.length; i++) {\n    while (!stack.isEmpty() && a[i] > a[stack.peek()]) {\n        int j = stack.pop();\n        answer[j] = i - j;\n    }\n    stack.push(i);\n}','每元素入出一次，O(n)时间O(n)空间；双层while并不自动代表O(n²)。','739、84；相等时弹不弹依题意决定，84弹出后算宽度。'),
('位运算','按位规律可压缩状态或抵消成对元素；需要明确整数表示及输入结构。','int answer = 0;\nfor (int x : nums) answer ^= x;\nreturn answer;','136为O(n)时间O(1)空间；位掩码枚举子集仍有2^n个状态。','136；技巧专题169使用投票而非位运算，287使用函数图。'),
]

def java_appendix():
    out=['# 学习 Hot 100 前需要掌握的 Java 知识\n',
         '本附录以Java 17语法为准。先学变量、数组、循环和方法，再边刷题边学习集合、对象与递归；不必等整套JavaSE课程结束才开始。代码片段有些需要放在类或方法内，不是每段都能单独提交。\n']
    for i,(name,explain,code,apis,scene,pitfall) in enumerate(JAVA,1):
        out.append(f'<a id="java-{i}"></a>\n## {i}. {name}\n\n{explain}\n\n```java\n{code}\n```\n\n常用语法与API：{apis}\n\nHot 100使用场景：{scene}\n\n初学者注意：{pitfall}\n')
    out.append('## Java 常用 API 速查表\n\n|语法/API|作用与返回值|注意|\n|---|---|---|')
    rows=[('a.length / s.length() / list.size()','数组长度 / 字符串长度 / 集合元素数','只有数组length不带括号'),('Arrays.sort(a)','原地排序，无返回值','原生数组排序通常O(n log n)，对象数组额外空间需另计'),('Arrays.fill(a,v)','所有元素设v，无返回值','DP不可达状态初始化'),('Arrays.equals(a,b)','一维数组内容相等返回true','二维int数组用Arrays.deepEquals'),('Arrays.asList(a,b)','返回定长列表','不能add/remove，int[]单参数会成为一个元素'),('Collections.sort(list)','原地自然顺序排序，无返回值','列表必须支持替换'),('Math.max(a,b) / min(a,b)','返回较大/小值','不修改参数'),('Integer.compare(a,b)','负/零/正表示比较结果','优于a-b防溢出'),('String.charAt(i)','返回位置i的char','0≤i<length()'),('String.substring(l,r)','新字符串，范围[l,r)','l≤r≤length()'),('String.toCharArray()','创建char[]副本','可排序副本而不改String'),('StringBuilder.append(x)','追加，返回同一builder','可链式调用'),('StringBuilder.deleteCharAt(i)','删除一字符，返回builder','回溯常删length()-1'),('StringBuilder.toString()','当前内容的String快照','builder之后更改不会改旧String'),('List.add(x) / get(i)','追加返回true / 获取元素','尾add摊还O(1)，get O(1)适用于ArrayList'),('List.remove(i) / remove(obj)','删下标返回元素 / 删对象返回boolean','Integer列表的重载要小心'),('new ArrayList<>(path)','浅复制列表','对二维可变对象不等于深拷贝'),('Map.put(k,v) / get(k)','写入返回旧值 / 读取或null','null拆箱有风险'),('Map.getOrDefault(k,d)','存在时返回值，否则d','默认值不会自动写进Map'),('Map.containsKey(k)','是否含该键，boolean','区别于值是否null'),('Map.entrySet() / values()','键值对视图 / 值视图','视图通常与原Map关联'),('Map.computeIfAbsent(k,fn)','缺值时创建并返回映射值','fn参数为键，不要误写成值'),('Set.add(x) / contains(x) / remove(x)','是否新增 / 存在 / 删除成功','平均O(1)，不保序'),('Deque.push/pop/peek','栈顶压入/删除返回/只读返回','peek空为null，pop空抛异常'),('Deque.addLast/removeFirst/peekLast','尾入/头出/读尾','先isEmpty避免非法读取'),('Queue.offer/poll/peek','入队/出队/只读队首','ArrayDeque作BFS，PriorityQueue按优先级'),('PriorityQueue(Comparator.reverseOrder())','创建最大堆','默认构造是最小堆'),('Map.Entry.getKey/getValue','返回键/值','遍历entrySet时常用'),('== / equals','基本值或引用身份 / 对象内容规则','String用equals，节点身份用==')]
    out.extend(f'|`{a}`|{b}|{c}|' for a,b,c in rows)
    out.append('\n## 力扣提交与本地运行\n\n普通题复制对应.java全部内容（含import与class Solution）。设计题使用题目指定类名：LRUCache、Trie、MinStack、MedianFinder。链表、树的节点由力扣提供，不要把本地测试桩一起粘进去。各题都叫Solution，因此不能把全部源码放同一默认包一起编译；验证工具按题号隔离编译目录。\n\n本地验证命令见README。递归在极深输入时可能受JVM栈限制；局部用例通过不代表完整覆盖所有合法输入，也不等于官方判题通过。\n')
    return '\n'.join(out)

def algorithm_appendix():
    out=['# Hot 100 算法与数据结构附录\n','下列模板服务于理解，涉及nums、target、节点等外部变量的片段需放入相应题目方法。通用框架中的注释条件需要按具体问题实现；完整可提交代码始终以每题源码为准。\n']
    for i,(name,meaning,code,cost,ids) in enumerate(ALGORITHMS,1):
        out.append(f'## {i}. {name}\n\n含义与适用问题：{meaning}\n\n```java\n{code}\n```\n\n常见复杂度：{cost}\n\n代表题与复习重点：{ids}\n')
    out.append('## 如何自己推复杂度\n\n先定输入规模：数组n，字符串m和n，图V和E，树高h，结果数量S。顺序执行的循环相加，嵌套且范围独立时相乘；单调栈、滑窗要数每个元素实际入出次数。递归既要算调用总数，也要算最大同时存活的栈深度。必须区分辅助空间与返回结果空间，并把排序、子串创建、复制路径的代价算进去。\n\n## 从基础到后端\n\nHashMap与LRU有助于理解缓存，但本题LRU不是线程安全生产缓存；队列与拓扑排序帮助理解任务依赖；二分与树帮助建立索引直觉，但MySQL索引要另学B+树。完成题目后再将集合、异常、IO、多线程知识与Spring Boot、MySQL、Redis项目结合，不把刷题等同于后端开发。\n')
    return '\n'.join(out)
