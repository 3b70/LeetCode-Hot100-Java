# 学习 Hot 100 前需要掌握的 Java 知识

本附录以Java 17语法为准。先学变量、数组、循环和方法，再边刷题边学习集合、对象与递归；不必等整套JavaSE课程结束才开始。代码片段有些需要放在类或方法内，不是每段都能单独提交。

<a id="java-1"></a>
## 1. 基本数据类型和变量

变量像带类型标签的盒子。int保存32位有符号整数，long保存64位整数，boolean只有true/false，char保存一个UTF-16代码单元，double保存浮点数。整数/整数会截断小数。

```java
int count = 0;
long sum = 0L;
boolean found = false;
char letter = 'a';
double average = ((double) 2 + 3) / 2;
```

常用语法与API：Integer.MIN_VALUE/MAX_VALUE是int边界；Long.MIN_VALUE/MAX_VALUE对应long。强转(double)在运算前提升类型。

Hot 100使用场景：437路径总和使用long，4中位数使用double。

初学者注意：int乘法可能先溢出再赋给long，应写(long)a*b；局部变量必须初始化后使用。

<a id="java-2"></a>
## 2. 数组及二维数组

数组长度创建后固定，从下标0开始。int[]是整数数组，int[][]是“数组的数组”，本手册矩阵题使用每行等长的矩形。

```java
int[] nums = {2, 7, 11};
int[] zeros = new int[3];
int[][] grid = {{1, 2}, {3, 4}};
int value = grid[1][0]; // 第二行第一列，值3
```

常用语法与API：a.length是字段，不带括号；a[i]读写元素；a.clone()只复制一层，二维数组深复制要逐行clone。

Hot 100使用场景：283原地移动，73用首行首列标记。

初学者注意：合法下标0..length-1；二维数组的行数grid.length，列数grid[0].length；访问grid[0]前需满足非空约束。

<a id="java-3"></a>
## 3. for、while、增强for

for适合知道遍历范围，while适合按条件反复，增强for适合逐个读取元素。break结束整个当前循环，continue跳过本轮剩余语句。

```java
int[] a = {1, 2, 3};
for (int i = 0; i < a.length; i++) { a[i]++; }
for (int value : a) { System.out.println(value); }
int left = 0, right = a.length - 1;
while (left < right) { left++; right--; }
```

常用语法与API：i++返回旧值再自增，++i先自增再返回；独立语句中两者效果相同。

Hot 100使用场景：1按下标返回答案，239用while清理队列。

初学者注意：增强for中的基本类型变量是副本，对value赋值不会修改数组；需要下标时用普通for。

<a id="java-4"></a>
## 4. 方法、参数和返回值

方法封装一段操作，参数是调用时传入的信息，return返回计算结果并结束当前调用。void表示不返回值。

```java
class Demo {
    int add(int a, int b) { return a + b; }
    void clear(int[] a) { java.util.Arrays.fill(a, 0); }
}
```

常用语法与API：签名由方法名和参数类型等决定；调用add(2,3)得到int 5；void方法可以使用return;提前结束。

Hot 100使用场景：Solution公开方法供力扣调用，private辅助方法拆分算法。

初学者注意：非void方法的正常执行路径必须返回值；参数名只在方法内部有效；题目方法名和参数类型不可随意改动。

<a id="java-5"></a>
## 5. 类与对象

类是描述数据和操作的模板，对象是用new创建的具体实例；两个new一般得到不同对象，即使字段值相同。

```java
class Box { int value; }
// 在方法内部：
// Box a = new Box();
// Box b = new Box();
// a.value = 3; // 不会改变b.value
```

常用语法与API：new分配对象并调用构造器；点号访问字段或方法；引用变量保存对象的引用。

Hot 100使用场景：链表节点和树节点都是对象；160根据对象身份判断相交。

初学者注意：a==b比较引用是否指向同一对象；两个值相同的节点不代表同一个节点。

<a id="java-6"></a>
## 6. 构造方法、成员变量、成员方法

成员变量保存对象状态，构造方法初始化对象，成员方法读取或修改状态。构造方法与类同名且没有返回类型。

```java
class Counter {
    private int value;
    Counter(int start) { this.value = start; }
    int next() { return ++value; }
}
```

常用语法与API：new Counter(3)调用有参构造器；c.next()返回4并保存新状态；对象成员默认初始化，而局部变量不会。

Hot 100使用场景：146缓存保存容量和链表，208节点保存孩子和终点标记。

初学者注意：构造方法不能写void；定义有参构造后不会自动提供无参构造；不要在算法多次调用间遗留旧答案。

<a id="java-7"></a>
## 7. this与static

this指向当前对象；static属于类本身，各实例共享，常用来存不变配置或独立工具方法。实例方法才能直接使用this。

```java
class Demo {
    private int value;
    static final int LIMIT = 100;
    Demo(int value) { this.value = value; }
    static int twice(int x) { return x * 2; }
}
```

常用语法与API：this.value区分字段和同名参数；Demo.twice(3)返回6；final引用不能再指向别处，但指向的数组仍可能被修改。

Hot 100使用场景：17用static final保存字母映射，146用static嵌套节点类。

初学者注意：不要把每题结果列表设为共享static可变状态；static方法不能直接读取非static字段。

<a id="java-8"></a>
## 8. 封装、继承、多态

封装把内部状态藏在private后，通过方法维护规则。继承用extends表达一种更具体的类型；多态让父类型引用调用实际对象的重写实现。

```java
class Animal { String sound() { return "?"; } }
class Cat extends Animal {
    @Override String sound() { return "喵"; }
}
// Animal pet = new Cat(); pet.sound()实际返回“喵”
```

常用语法与API：private限制类内访问，public开放；@Override帮助编译器检查确实在重写；super可调用父类构造或方法。

Hot 100使用场景：List<Integer> list = new ArrayList<>();体现面向抽象类型编程。

初学者注意：Java类只能extends一个类；方法重载看参数列表，方法重写发生在继承实现关系中，二者不同。

<a id="java-9"></a>
## 9. 接口与抽象类

接口描述对象能做什么，抽象类可保存共享状态和部分实现。接口可被多个类实现，抽象类不能直接new。

```java
interface Task { int run(); }
abstract class BaseTask {
    protected int count;
    abstract int run();
}
class SimpleTask implements Task {
    public int run() { return 1; }
}
```

常用语法与API：implements实现接口，extends继承类；抽象方法由具体类实现；接口也可以有default方法。

Hot 100使用场景：List、Map、Set、Queue、Deque是接口，ArrayList、HashMap等是实现类。

初学者注意：不能new List<>()；声明接口类型时只能直接使用该接口暴露的方法。

<a id="java-10"></a>
## 10. String与StringBuilder

String不可变，每次改变文本实际上创建新串；StringBuilder是可变字符缓冲，适合循环拼接或回溯路径。

```java
String s = "abc";
char c = s.charAt(1); // b
String part = s.substring(0, 2); // ab
StringBuilder path = new StringBuilder();
path.append('a');
String snapshot = path.toString();
path.deleteCharAt(path.length() - 1);
```

常用语法与API：length()返回长度；charAt(i)返回char；substring(l,r)左闭右开；toCharArray()创建新char[]；append返回当前builder，toString生成不可变快照。

Hot 100使用场景：17/22回溯生成字符串，394多层解码。

初学者注意：字符串内容比较用equals；下标要小于length()；循环s+=可能制造大量临时对象；char不总等同一个Unicode字符，本题按官方输入字符范围处理。

<a id="java-11"></a>
## 11. ArrayList与List

List是有序可重复列表接口，ArrayList用可扩容数组实现；尾部添加通常快，插入中间或头部需要搬移。

```java
java.util.List<Integer> path = new java.util.ArrayList<>();
path.add(2);
int first = path.get(0);
java.util.List<Integer> copy = new java.util.ArrayList<>(path);
path.remove(path.size() - 1);
```

常用语法与API：add(E)追加并返回true，get(i)读取，set(i,x)替换并返回旧值，remove(int)删下标并返回旧值，size()元素数。get/set O(1)，尾add摊还O(1)，中间remove O(n)。

Hot 100使用场景：回溯结果和路径，102层序二维列表。

初学者注意：remove(1)删除下标1；remove(Integer.valueOf(1))删值1；new ArrayList<>(path)是浅复制，嵌套可变对象仍共享。

<a id="java-12"></a>
## 12. HashMap与Map

Map建立键到值的映射，每个键至多一个当前值。HashMap按equals和hashCode确定键，平均查找O(1)，不保证遍历顺序。

```java
java.util.Map<Integer, Integer> count = new java.util.HashMap<>();
count.put(7, count.getOrDefault(7, 0) + 1);
boolean exists = count.containsKey(7);
int times = count.get(7);
count.remove(7);
```

常用语法与API：put(k,v)返回旧值或null；get(k)返回对应值或null；getOrDefault(k,d)缺失用默认值d；entrySet()遍历键值对；size()返回键数。

Hot 100使用场景：1数值到下标，560前缀到次数。

初学者注意：get缺失返回null，拆箱成int会空指针；频次必须累加而非覆盖为1；Integer比较值不要依赖==缓存。

<a id="java-13"></a>
## 13. HashSet与Set

Set只保存不重复元素，HashSet平均查找、插入、删除O(1)，顺序未定义。

```java
java.util.Set<Integer> seen = new java.util.HashSet<>();
boolean first = seen.add(2); // true
boolean again = seen.add(2); // false
boolean has = seen.contains(2);
seen.remove(2);
```

常用语法与API：add返回是否真的新增；contains返回是否存在；remove返回是否存在并删除；size是不同元素个数。

Hot 100使用场景：128去重并找前驱，3维护窗口字符。

初学者注意：不要把无序集合当有序数组；自定义可变对象作为键时修改参与哈希的字段会破坏查找；节点默认按身份比较。

<a id="java-14"></a>
## 14. Deque、ArrayDeque和栈

Deque双端队列可在两头操作；ArrayDeque是数组实现。栈是一端进一端出的后进先出结构，优先用Deque而非旧Stack类。

```java
java.util.Deque<Integer> stack = new java.util.ArrayDeque<>();
stack.push(3); stack.push(5);
int top = stack.peek(); // 5，未删除
int popped = stack.pop(); // 5，删除
boolean empty = stack.isEmpty();
```

常用语法与API：push/pop/peek操作头部；addLast/removeLast/peekLast操作尾部；offerLast/pollFirst可作队列。两端操作通常摊还O(1)。

Hot 100使用场景：20括号匹配、84单调栈、239单调双端队列。

初学者注意：ArrayDeque不接受null；pop空栈抛异常，peek空栈返回null，拆箱仍会出错；不要混淆队首队尾。

<a id="java-15"></a>
## 15. Queue与PriorityQueue

普通Queue按先入先出供BFS使用；PriorityQueue按优先级出队，是堆，不按插入顺序。默认最小堆。

```java
java.util.Queue<Integer> queue = new java.util.ArrayDeque<>();
queue.offer(1); queue.offer(2);
int first = queue.poll(); // 1
java.util.PriorityQueue<Integer> heap = new java.util.PriorityQueue<>();
heap.offer(5); heap.offer(2);
int min = heap.peek(); // 2
```

常用语法与API：offer插入，poll取出并删除队首/堆顶，peek只读；空poll/peek返回null。堆offer/poll O(log n)，peek O(1)；遍历堆不保证有序。

Hot 100使用场景：102层序使用队列，215保留前k大，295双堆中位数。

初学者注意：优先队列不能代替BFS队列；最大堆须传反向比较器；不可插入null。

<a id="java-16"></a>
## 16. 泛型

泛型用类型参数表达集合里装什么，让编译器提前发现类型错误。List<Integer>保存整数包装对象，不是原生int。

```java
java.util.List<Integer> numbers = new java.util.ArrayList<>();
numbers.add(3); // int自动装箱为Integer
int x = numbers.get(0); // 自动拆箱
java.util.List<java.util.List<Integer>> groups = new java.util.ArrayList<>();
```

常用语法与API：尖括号中是引用类型；<>菱形语法让右侧类型由上下文推断；List<List<Integer>>是列表的列表。

Hot 100使用场景：回溯二维结果、哈希表键值类型、节点队列。

初学者注意：不能写List<int>；List<Integer>不是List<Number>的子类型；拆箱null会抛NullPointerException。

<a id="java-17"></a>
## 17. Lambda表达式

Lambda是函数式接口的简写实现；函数式接口只有一个抽象方法。参数从目标类型推断，->右侧是执行体。

```java
java.util.List<int[]> rows = new java.util.ArrayList<>();
rows.sort((a, b) -> Integer.compare(a[0], b[0]));
java.util.Map<String, java.util.List<String>> map = new java.util.HashMap<>();
map.computeIfAbsent("key", k -> new java.util.ArrayList<>()).add("value");
```

常用语法与API：computeIfAbsent(key,fn)在键未关联非null值时调用fn建立值并返回该值；k是传入的键，new ArrayList<>()是新组；返回List后可继续add。传统写法：if(!map.containsKey(key)) map.put(key,new ArrayList<>()); map.get(key).add(value);

Hot 100使用场景：56排序区间、23堆按节点值比较；49正文采用更容易读的传统写法。

初学者注意：Lambda参数不是字符串；捕获的局部变量须final或有效final；不要为简短而使用不理解的链式调用。

<a id="java-18"></a>
## 18. Comparator与Comparable

Comparable定义类型的自然顺序（compareTo），Comparator是独立比较规则（compare），可为同一类型指定不同排序。

```java
java.util.Comparator<Integer> ascending = Integer::compare;
java.util.PriorityQueue<Integer> maxHeap =
    new java.util.PriorityQueue<>(java.util.Comparator.reverseOrder());
int cmp = Integer.compare(2, 5); // 负数，表示2应在5之前
```

常用语法与API：compare(a,b)<0表示a在前，=0同序，>0表示b在前；reverseOrder()反转自然顺序；Integer::compare是方法引用，等价(a,b)->Integer.compare(a,b)。

Hot 100使用场景：56区间排序，295左侧最大堆。

初学者注意：不要写a-b比较极值，可能溢出；比较器应保持反对称和传递性；原生int[]不能传Comparator逐元素排序。

<a id="java-19"></a>
## 19. Arrays、Collections、Math常用API

这些工具类提供静态方法，不需要new；Arrays作用于数组，Collections作用于集合，Math做数学比较。

```java
int[] a = {3, 1, 2};
java.util.Arrays.sort(a);
boolean same = java.util.Arrays.equals(a, new int[]{1, 2, 3});
java.util.Arrays.fill(a, 0);
int larger = Math.max(2, 5);
java.util.List<Integer> list = new java.util.ArrayList<>(java.util.Arrays.asList(3, 1));
java.util.Collections.sort(list);
```

常用语法与API：sort修改原容器；equals比较一维数组内容，deepEquals比较嵌套对象数组；fill全部赋值；asList返回定长列表；Collections.reverse反转列表；Math.max/min返回较大/小值。

Hot 100使用场景：49排序字符，438比较计数数组，DP初始化和最优值更新。

初学者注意：Arrays.asList(int[])会得到只含整个int[]的列表；asList不能add/remove；数组==比较引用而非内容。

<a id="java-20"></a>
## 20. 递归

方法调用自身处理更小子问题。每层调用有自己的参数与局部变量，通过调用栈保留现场；必须明确终止条件、递归过程、返回含义。

```java
class Demo {
    int sum(int n) {
        if (n == 0) return 0; // 终止
        return n + sum(n - 1); // 子问题变小，返回前n项和
    }
}
```

常用语法与API：sum(3)展开3+sum(2)，再2+sum(1)，最终sum(0)=0，自底向上返回1、3、6。栈深度也占空间。

Hot 100使用场景：104返回子树高度，46回溯排列。

初学者注意：没有终止会无限递归；输入退化成长链时Java可能StackOverflowError，需要显式栈；不要把递归栈算成O(1)。

<a id="java-21"></a>
## 21. 引用、null、对象传参

Java始终按值传参；对象参数传入的是“引用值的副本”。方法能经引用修改同一对象，但给参数重新赋new不会替换调用者变量。null表示没有指向对象。

```java
class Demo {
    void edit(int[] a) { a[0] = 9; } // 调用者可看到
    void replace(int[] a) { a = new int[]{9}; } // 只改局部参数
    boolean empty(int[] a) { return a == null; }
}
```

常用语法与API：p.next=null切断链接；p=q只复制引用，不复制对象；&&与||会短路，p!=null && p.next!=null能防止访问空引用。

Hot 100使用场景：206必须保存next，138必须new新节点，146维护共享节点引用。

初学者注意：不能调用null的方法或字段；引用副本不是深拷贝；Java没有C++式引用传递。

<a id="java-22"></a>
## 22. 位运算基础

整数按二进制逐位计算：&两位都1才1，|任一为1即1，^相异为1，~按位取反；<<左移，>>保留符号右移，>>>补0右移。

```java
int xor = 5 ^ 3; // 101 ^ 011 = 110，即6
int lowBit = 6 & -6; // 得最低位的1，值2
boolean odd = (5 & 1) != 0;
int doubled = 3 << 1; // 6
```

常用语法与API：x^x=0，x^0=x，异或交换结合；移位优先级容易误读，应加括号。int移位距离只使用低5位，1<<32等于1。

Hot 100使用场景：136成对抵消；进阶可位掩码枚举78子集。

初学者注意：^不是指数运算；&与&&不同，前者不短路；负数按补码表示，不要把逻辑右移与算术右移混用。

## Java 常用 API 速查表

|语法/API|作用与返回值|注意|
|---|---|---|
|`a.length / s.length() / list.size()`|数组长度 / 字符串长度 / 集合元素数|只有数组length不带括号|
|`Arrays.sort(a)`|原地排序，无返回值|原生数组排序通常O(n log n)，对象数组额外空间需另计|
|`Arrays.fill(a,v)`|所有元素设v，无返回值|DP不可达状态初始化|
|`Arrays.equals(a,b)`|一维数组内容相等返回true|二维int数组用Arrays.deepEquals|
|`Arrays.asList(a,b)`|返回定长列表|不能add/remove，int[]单参数会成为一个元素|
|`Collections.sort(list)`|原地自然顺序排序，无返回值|列表必须支持替换|
|`Math.max(a,b) / min(a,b)`|返回较大/小值|不修改参数|
|`Integer.compare(a,b)`|负/零/正表示比较结果|优于a-b防溢出|
|`String.charAt(i)`|返回位置i的char|0≤i<length()|
|`String.substring(l,r)`|新字符串，范围[l,r)|l≤r≤length()|
|`String.toCharArray()`|创建char[]副本|可排序副本而不改String|
|`StringBuilder.append(x)`|追加，返回同一builder|可链式调用|
|`StringBuilder.deleteCharAt(i)`|删除一字符，返回builder|回溯常删length()-1|
|`StringBuilder.toString()`|当前内容的String快照|builder之后更改不会改旧String|
|`List.add(x) / get(i)`|追加返回true / 获取元素|尾add摊还O(1)，get O(1)适用于ArrayList|
|`List.remove(i) / remove(obj)`|删下标返回元素 / 删对象返回boolean|Integer列表的重载要小心|
|`new ArrayList<>(path)`|浅复制列表|对二维可变对象不等于深拷贝|
|`Map.put(k,v) / get(k)`|写入返回旧值 / 读取或null|null拆箱有风险|
|`Map.getOrDefault(k,d)`|存在时返回值，否则d|默认值不会自动写进Map|
|`Map.containsKey(k)`|是否含该键，boolean|区别于值是否null|
|`Map.entrySet() / values()`|键值对视图 / 值视图|视图通常与原Map关联|
|`Map.computeIfAbsent(k,fn)`|缺值时创建并返回映射值|fn参数为键，不要误写成值|
|`Set.add(x) / contains(x) / remove(x)`|是否新增 / 存在 / 删除成功|平均O(1)，不保序|
|`Deque.push/pop/peek`|栈顶压入/删除返回/只读返回|peek空为null，pop空抛异常|
|`Deque.addLast/removeFirst/peekLast`|尾入/头出/读尾|先isEmpty避免非法读取|
|`Queue.offer/poll/peek`|入队/出队/只读队首|ArrayDeque作BFS，PriorityQueue按优先级|
|`PriorityQueue(Comparator.reverseOrder())`|创建最大堆|默认构造是最小堆|
|`Map.Entry.getKey/getValue`|返回键/值|遍历entrySet时常用|
|`== / equals`|基本值或引用身份 / 对象内容规则|String用equals，节点身份用==|

## 力扣提交与本地运行

普通题复制对应.java全部内容（含import与class Solution）。设计题使用题目指定类名：LRUCache、Trie、MinStack、MedianFinder。链表、树的节点由力扣提供，不要把本地测试桩一起粘进去。各题都叫Solution，因此不能把全部源码放同一默认包一起编译；验证工具按题号隔离编译目录。

本地验证命令见README。递归在极深输入时可能受JVM栈限制；局部用例通过不代表完整覆盖所有合法输入，也不等于官方判题通过。
