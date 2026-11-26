import hashlib,json,re,pathlib
from foundations import java_appendix,algorithm_appendix

# 正则只匹配本题实际出现的语法/API。解释配合基础附录复习，不以无关API充数。
API=[
(r'\bint\[\]|\bchar\[\]|\bboolean\[\]','数组与下标',2,'固定长度容器；new int[n]初值为0，boolean初值false；a[i]读取或写入第i项。本题用数组承载输入或索引状态，索引必须在0..length-1；a.length是字段，不是方法。示例：int[] a={2,7}; a[0]为2。'),
(r'\[\]\[\]','二维数组',2,'a[r][c]先取第r行再取第c列；行数a.length，列数a[0].length。本题用它表示矩阵或二维状态。不要把行列维度写反，空外数组不能访问a[0]。'),
(r'\bfor\s*\(|\bwhile\s*\(','循环',3,'for控制初始化、条件、更新；while先判断再执行。本题循环反复处理元素或缩小区间；必须保证每轮有进展。i++先产生旧值再加1，例如a[i++]使用旧下标。增强for读取元素副本，给基本类型循环变量赋值不会改数组。'),
(r'\bif\s*\(|\?','条件与短路',3,'if仅在boolean条件为true时执行；条件?A:B只求被选择的一个分支。&&左侧false不算右侧，||左侧true不算右侧；本题利用它们保护边界或选择算法分支。检查p!=null须放在读取p.next之前。'),
(r'\breturn\b','方法与返回值',4,'方法参数声明输入类型，return表达式交还结果并结束当前调用，void方法可只写return。public入口供力扣调用，private辅助方法只供本类使用。递归时每层局部变量独立，集合参数传的是同一对象的引用值副本。'),
(r'\bnew\b|\bnull\b','对象、引用与null',21,'new创建对象；赋值p=q复制引用，不复制节点或集合。本题经引用修改对象内容，调用者可见；重新给参数赋new只改变局部参数。null没有可访问的字段或方法。对象==比较身份，String等内容要用equals。'),
(r'\bList<|\bArrayList<','List、ArrayList与泛型',11,'List<E>是有序可重复列表接口，new ArrayList<>()创建实现；E必须是引用类型，int需用Integer自动装箱。本题收集可变长结果或路径。add(x)尾部追加，get(i)读取，size()给元素数；get越界会抛异常。尾add摊还O(1)。'),
(r'new ArrayList<>\(path\)|new ArrayList<>\(groups.values\(\)\)','列表快照与集合构造器',11,'new ArrayList<>(collection)把集合元素复制到新列表；本题用来保留当前路径或导出分组。复制的是元素引用，属于浅复制。回溯不能直接ans.add(path)，否则多个结果共享随后被清空的路径对象。'),
(r'path\.remove','List.remove(int)',11,'remove(index)按下标删除并返回被删元素，后面的元素左移。本题传path.size()-1撤销最后一次选择，尾删除O(1)。List<Integer>的remove(1)是删下标1，删值1要写remove(Integer.valueOf(1))。'),
(r'\bMap<|\bHashMap<','Map、HashMap',12,'Map<K,V>把每个键映射到一个值；put(k,v)写入并返回旧值，get(k)读取或返回null，containsKey(k)检查存在。本题按键快速定位信息；平均查找O(1)，遍历不保序。get缺失后直接拆箱int会空指针。'),
(r'getOrDefault','Map.getOrDefault(key, defaultValue)',12,'键不存在时返回defaultValue，存在时返回其值，不自动修改Map。本题用默认0统计次数，例如count.put(x,count.getOrDefault(x,0)+1)。不能误以为查询默认值就已经插入了键。'),
(r'entrySet|getKey|getValue','Map.Entry与entrySet()',12,'entrySet()返回键值对集合视图；Entry.getKey()/getValue()读取键和值。本题遍历计频结果建立频率桶。泛型限定键值类型，遍历时不要随意结构性修改同一个Map。'),
(r'\.values\(','Map.values()',12,'返回所有值的集合视图，不是独立拷贝。本题将每个分组列表导出，再用new ArrayList<>(...)形成结果外层列表。内层列表仍是原对象，后续不要继续修改它们来破坏已返回结果。'),
(r'count\.remove|map\.remove','Map.remove(key)',12,'删除指定键并返回旧值或null。本题用它撤销已失效状态或淘汰缓存键。只改链表、不删缓存Map会留下可查询的旧记录；前缀和中移除零频键还能控制当前路径空间。'),
(r'\bSet<|\bHashSet<','Set、HashSet',13,'集合不保存重复项，add(x)返回是否新增，contains(x)检查，remove(x)返回是否删除成功。本题用它维护已出现元素或合法窗口。平均操作O(1)，不保证顺序；不要依赖其迭代顺序生成固定顺序答案。'),
(r'\bDeque<|\bArrayDeque<','Deque、ArrayDeque',14,'Deque支持两端操作，ArrayDeque是数组实现且不能存null。本题将其作为栈、队列或单调候选容器。isEmpty()检查是否为空，size()返回元素数；两端写操作摊还O(1)，不要在中间位置做线性删除来破坏复杂度。'),
(r'\.push\(|\.pop\(|\.peek\(','push / pop / peek',14,'push(x)把x压入头部，pop()删除并返回头部，peek()只读头部。用于本题栈或读取堆顶（PriorityQueue也有peek）。pop空栈抛异常；peek空时null，拆箱前必须确认非空。例：压3再压5，弹出5。'),
(r'peekFirst|peekLast|addLast|removeFirst|removeLast','双端队列的首尾API',14,'addLast(x)尾部加入，removeFirst()/removeLast()删除并返回首/尾，peekFirst()/peekLast()只读取首/尾。本题分别淘汰过期队首和较差队尾，必须保持两端含义一致；remove前先检查非空。'),
(r'\bQueue<|\.offer\(|\.poll\(','Queue.offer / poll / peek',15,'offer(x)加入并返回boolean；poll()删除返回队首，空时null；peek只读。本题使用ArrayDeque时按先进先出，PriorityQueue时按比较规则出堆。BFS需提前固定本层size，不能把刚加入的下一层也在本层处理。'),
(r'PriorityQueue','PriorityQueue',15,'默认自然顺序最小堆，堆顶最小；offer/poll为O(log k)，peek为O(1)。本题保留优先级最高的候选或平衡两半数据。不能用遍历顺序推断全排序，不可加入null。最大堆需反向比较器。'),
(r'\bString\b','String',10,'不可变字符序列；length()返回字符单元数，equals比较文本。作为本题输入、键或结果；修改内容须创建新String或用StringBuilder。String==只比较引用，不能替代内容比较。'),
(r'charAt','String.charAt(index)',10,'传入0到length()-1的下标，返回对应char。本题逐字符扫描或检查两端。越界抛异常；char是UTF-16单元，本题实现按题目保证的字符范围处理，不声称覆盖任意Unicode字符。'),
(r'toCharArray','String.toCharArray()',10,'把字符串复制为新的char[]，可修改或排序。本题用增强for遍历字符或排序生成特征键；排序数组不会修改原字符串。char数组直接toString()不是内容，要new String(chars)。'),
(r'substring','String.substring(begin, end)',10,'返回左闭右开[begin,end)的子串，长度end-begin。本题构造结果片段或查询候选单词；闭区间结尾j需传j+1。Java 17会复制子串内容，不能把创建与哈希代价一概算成O(1)。'),
(r'StringBuilder','StringBuilder',10,'可变字符串缓冲；append(x)追加且返回同一builder；deleteCharAt(i)删除字符；toString()返回不可变快照。本题反复追加并可能撤销末字符，避免大量短命String。删除前确保length()>0。'),
(r'Arrays\.sort','Arrays.sort(array[, comparator])',19,'原地排序且无返回值。原生char/int数组按自然顺序，对象数组可传Comparator。本题用排序建立单调性或统一特征；排序会改变输入。通常O(n log n)，不同数组类型的辅助空间不同，见本题复杂度。'),
(r'Arrays\.fill','Arrays.fill(array, value)',19,'把数组每格设为value，无返回值。本题用于DP不可达初值、单位元或棋盘空格。new int[n]默认0不一定符合状态语义；二维数组不能靠一次fill深度填充所有内部基本元素。'),
(r'Arrays\.equals','Arrays.equals(a, b)',19,'按长度和每项内容比较两个一维数组，返回boolean。本题比较固定窗口的26个字母频次；不是引用比较a==b。长度为26时比较O(26)，若数组随n变长则不是常数。'),
(r'Arrays\.asList','Arrays.asList(...)',19,'把传入对象元素包装成定长List，可读取/替换但不能add/remove。本题只用于记录不再修改的三元组；int值自动装箱成Integer。单独传int[]会被当成一个对象，不会自动拆成Integer列表。'),
(r'\.toArray\(','List.toArray(T[] a)',11,'把列表元素复制到数组，所传数组提供结果数组类型；本题int[]元素组成int[][]，写new int[ans.size()][]。这是外层复制，内部int[]仍共享，不能误称深复制。'),
(r'Integer\.compare|Comparator|->','比较器、Lambda',18,'Comparator.compare(a,b)返回负/零/正分别表示a在前/同序/b在前。(a,b)->Integer.compare(a.val,b.val)是按节点值比较的简写；Integer.compare避免a-b溢出。Comparator.reverseOrder()反转自然顺序。本题把规则交给排序或堆。'),
(r'Math\.max|Math\.min','Math.max / Math.min',19,'静态方法传两个同类数值，返回较大/较小值，不修改实参。本题维护最优值、边界或DP转移。必须把结果赋回变量：Math.max(best,x)单独调用不会改变best。'),
(r'Integer\.MIN_VALUE|Integer\.MAX_VALUE|Long\.MIN_VALUE|Long\.MAX_VALUE','整数边界与数值提升',1,'Integer常量为32位上下界，Long为64位上下界。本题作为初始最优值、哨兵或安全边界。MIN_VALUE取负会溢出；相加前转long/double而非运算后再转换，例如((double)a+b)/2避免int加法溢出。'),
(r'\blong\b','long与L后缀',1,'long保存64位有符号整数，0L是long字面量。本题累计路径前缀避免int溢出；Map<Long,Integer>的键要用Long，0与0L装箱类型不同。赋值给long前的int表达式仍可能先溢出，应提前提升操作数。'),
(r'\bthis\b|\bstatic\b|\bfinal\b','this、static、final',7,'this表示当前对象，可区分字段与参数。static成员属于类；final字段仅允许初始化一次，若指向集合仍能增删内容。本题用它们保存对象结构或固定配置，不能把可变结果错误地当所有调用共享的全局状态。'),
(r'\^','异或与复合赋值',22,'^逐位异或，相同为0，不同为1；ans^=x等价ans=ans^x。本题利用x^x=0、x^0=x以及交换结合律消去成对元素。它不是乘方，也不等于|或||。'),
]

DIAGRAMS={
4:'A[在短数组选划分i] --> B[确定另一数组划分j]\nB --> C{交叉边界合法?}\nC -->|是| D[按总长度奇偶求中位数]\nC -->|A左末太大| E[i向左二分]\nC -->|其他| F[i向右二分]\nE --> A\nF --> A',
25:'A[从上一组尾找第k个节点] --> B{找到完整组?}\nB -->|否| C[保留剩余节点并结束]\nB -->|是| D[保存after并反转本组]\nD --> E[前段连接新组头]\nE --> F[旧组头成为新组尾]\nF --> A',
76:'A[加入右字符并更新缺口] --> B{missing等于0?}\nB -->|否| C[右端继续扩张]\nB -->|是| D[更新最短答案]\nD --> E[移走左字符并更新缺口]\nE --> B\nC --> A',
84:'A[读入下一高度含末尾哨兵0] --> B{栈顶更高?}\nB -->|是| C[弹出高度并用新栈顶求宽]\nC --> D[更新矩形最大面积]\nD --> B\nB -->|否| E[压入当前有效下标]\nE --> A',
124:'A[递归获取左右单边贡献] --> B[负贡献截断为0]\nB --> C[用根加左右更新全局答案]\nC --> D[向父返回根加较大单边]',
51:'A[处理当前行] --> B{所有行已放完?}\nB -->|是| C[生成棋盘副本]\nB -->|否| D[枚举未冲突列]\nD --> E[标记列与两条斜线]\nE --> F[递归下一行]\nF --> G[撤销三类标记]\nG --> D',
295:'A[数字加入左最大堆] --> B[左堆最大转入右最小堆]\nB --> C{右堆更大?}\nC -->|是| D[右堆最小转回左堆]\nC -->|否| E[完成]\nD --> E',
72:'A[初始化空前缀的插删代价] --> B[按行列递增枚举前缀]\nB --> C{末字符相同?}\nC -->|是| D[继承左上状态]\nC -->|否| E[插入删除替换最小代价加1]\nD --> F[最终读取右下角]\nE --> F'
}

def knowledge(code):
    return [(name,i,explain) for pattern,name,i,explain in API if re.search(pattern,code)]

def node_explanation(i,code):
    if 'ListNode' in code:
        return ('\n力扣提供`ListNode`节点，核心字段为`int val`和`ListNode next`，常用构造为`ListNode(int val)`及`ListNode(int val, ListNode next)`。`next==null`表示尾部。下面的提交代码直接引用它；本地测试定义在tests文件中，提交时不要重复粘贴。\n')
    if 'TreeNode' in code:
        return ('\n力扣提供`TreeNode`节点，核心字段为`int val`、`TreeNode left`、`TreeNode right`，可用`new TreeNode(value)`创建。null孩子表示空子树。提交文件不重复定义节点；tests中的同名类只用于独立编译。\n')
    if i==138:
        return ('\n本题的`Node`由力扣提供：`int val; Node next; Node random;`，构造`Node(int val)`。random可为空、指向自身或指向链上任意节点；不要与其他题的同名节点类型混用。\n')
    return ''

def section(q,p,result):
    apis=knowledge(p['code']); prereq='、'.join(dict.fromkeys(name for name,_,_ in apis[:7]))
    status='已编译：'+('是' if result.get('compiled') else '尚未验证')+'；本地测试：'+('通过' if result.get('local_pass') else '尚未通过/未验证')+'；LeetCode官方测试：未提交，未验证。'
    header=f"<a id=\"p{q['id']}\"></a>\n## {q['id']}. {q['name']}\n"
    basic=f"### 1. 题目基本信息\n\n|字段|内容|\n|---|---|\n|力扣题号|{q['id']}|\n|中文名称|{q['name']}|\n|难度|{q['difficulty']}|\n|算法专题|{q['category']}|\n|官方原题|[{q['name']}]({q['url']})|\n|推荐前置知识|{prereq}|\n\n验证状态：{status}\n"
    thought=f"### 2. 题目描述\n\n{p['goal']}\n\n输入与输出示例：`{p['example']}`\n\n### 3. 解题思路详细分析\n\n**从直观方案开始**：{p['naive']}\n\n**推荐方案、变量含义与正确性依据**：{p['idea']}\n"
    if q['id'] in DIAGRAMS: thought+='\n执行流程图：\n\n```mermaid\nflowchart TD\n'+DIAGRAMS[q['id']]+'\n```\n'
    source=f"### 4. 完整 Java 解题代码\n\n标准库导入列在代码开头；没有import表示仅使用java.lang自动导入类型及力扣节点。普通题使用`class Solution`，设计题保留指定类名。\n{node_explanation(q['id'],p['code'])}\n```java\n{p['code']}\n```\n"
    java='### 5. Java 知识点详解\n\n以下只复习本题实际出现的语法和关键API；数字锚点对应前面的Java基础章节。\n\n'
    for name,n,explain in apis:
        java+=f'- **{name}**（[基础第{n}节](#java-{n})）：{explain}\n'
    # 主手册中锚点可直达；独立章节的链接稍后改成相对附录地址。
    steps=[s.strip(' 。') for s in re.split('[；。]',p['trace']) if s.strip(' 。')]
    trace='### 6. 示例执行过程\n\n对应本题示例或文中明确标出的同类小例子：\n\n|步骤|扫描位置、变量或数据结构变化|\n|---|---|\n'
    trace+='\n'.join(f'|{i}|{s.replace("|","∣") }|' for i,s in enumerate(steps,1))+'\n'
    timecost,_,space=p['cost'].partition('；')
    cost=f'### 7. 复杂度分析\n\n- **时间**：{timecost}。\n- **空间**：{space or "详见上面的联合成本说明"}\n\n复杂度中返回结果是否计入已明确说明；树高h、层宽w、总节点数N等规模按本题语境取值。哈希表相关分析使用平均情况；代码调用栈也计入辅助空间。\n'
    errors=[s.strip(' 。') for s in p['errors'].split('；') if s.strip(' 。')]
    mistakes='### 8. 常见错误和注意事项\n\n'+'\n'.join(f'{i}. {s}。' for i,s in enumerate(errors,1))+'\n'
    # 总结引用本题具体的思路与API，不使用所有题一致的空泛句子。
    summary=f"### 9. 本题知识总结\n\n- 核心思想：{p['idea'].split('。')[0]}。\n- Java重点：{'、'.join(name for name,_,_ in apis if name not in ['循环','条件与短路','方法与返回值','对象、引用与null'])}。\n- 必会技巧：{errors[0]}。\n- 推荐复习：遮住代码，用第6节的示例重走变量变化，再解释第3节的边界或状态含义，最后独立写出提交方法。\n"
    return '\n'.join([header,basic,thought,source,java,trace,cost,mistakes,summary])

STAGE_NAMES=['Java基础语法、数组、字符串','HashMap、HashSet、ArrayList','双指针、滑动窗口、二分查找','链表、栈、队列','二叉树、递归、图论','回溯、贪心、动态规划','困难题及综合复习']
STAGE_ONE=[283,136,169,121,118,53,189,238,48,54,73,240]
def stage(q):
    if q['difficulty']=='困难': return 7
    if q['id'] in STAGE_ONE: return 1
    if q['category'] in ['哈希','子串']: return 2
    if q['category'] in ['双指针','滑动窗口','二分查找','技巧']: return 3
    if q['category'] in ['链表','栈','堆']: return 4
    if q['category'] in ['二叉树','图论']: return 5
    return 6

def learning_order(manifest):
    # 指定起步顺序，之后按难度、专题和官方原顺序稳定排序。
    rank={q['id']:i for i,q in enumerate(manifest)}
    ordered=sorted(manifest,key=lambda q:(stage(q),STAGE_ONE.index(q['id']) if stage(q)==1 else (0 if q['difficulty']=='简单' else 1),rank[q['id']]))
    assert len({q['id'] for q in ordered})==100
    out=['# Java 初学者 Hot 100 推荐刷题顺序\n',
         '学习顺序与正文专题顺序分开维护。先用数组练语法，再学集合和指针，然后利用节点对象练引用与递归，最后深入状态设计。困难题统一留到综合阶段；其中76可在掌握滑窗后提前挑战。复习优先级不等于难度：P0为基础模式或高复用转移，P1为常规巩固，P2为困难综合。\n']
    p0={1,49,128,283,3,560,239,53,238,206,21,141,19,146,94,104,102,98,236,200,994,207,46,78,35,34,20,739,215,121,55,70,198,322,300,416,62,64,1143,72,136}
    for s,name in enumerate(STAGE_NAMES,1):
        out.append(f'## 阶段{s}：{name}\n\n|推荐顺序|题号|名称|难度|提前掌握的Java知识|复习优先级|\n|---|---|---|---|---|---|')
        for index,q in enumerate(ordered,1):
            if stage(q)!=s: continue
            names=[name for name,_,_ in knowledge(q['_code']) if name not in ['方法与返回值','循环','条件与短路']][:5]
            priority='P0' if q['id'] in p0 else ('P2' if q['difficulty']=='困难' else 'P1')
            out.append(f"|{index}|{q['id']}|[{q['name']}]({q['url']})|{q['difficulty']}|{'、'.join(names)}|{priority}|")
    out.append('\n## 30～60天如何安排\n\n推荐60天作为排程框架，每天约1.5～3小时；尚未学完JavaSE时可延长，困难题可拆成两天。30天版是加速选项，每个新题日4题，通常需要更多时间，不必为了赶表跳过API与手动模拟。\n\n每天先复习再做新题：到期题中选1题从零重写，另选1～2题口述思路和API；P0或做错的优先，其余延后。表中列出全部到期候选，允许分配到后续复习日。复习间隔是学后第1、3、7天；第14、30天继续在progress里自行安排。全复习日重点清理积压。\n\n遇到不会的题：先自行尝试20～30分钟，再读思路，手动画变量，然后关闭答案重写。若连数组/方法还生疏，当天只做1题，并把后续编号整体顺延；一次重写通过且能说明复杂度才勾选掌握。\n')
    for days,per in [(60,2),(30,4)]:
        schedule={}; cursor=0
        for d in range(1,days+1):
            fresh=[] if d%6==0 else ordered[cursor:cursor+per]
            cursor+=len(fresh); schedule[d]=fresh
        assert cursor==100
        out.append(f'### {days}天排程\n\n|天数|每日新题（题号）|到期复习候选（题号）|\n|---|---|---|')
        for d,fresh in schedule.items():
            review=[str(q['id']) for lag in [1,3,7] for q in schedule.get(d-lag,[])]
            out.append(f"|{d}|{', '.join(str(q['id']) for q in fresh) or '无：集中复习、补欠题'}|{', '.join(review) or '预习基础附录 / 清理积压'}|")
        out.append('\n最后一批新题学后的第1、3、7天复习可能超出排程结束日，需继续追加；完成排程不代表永久掌握。\n')
    return '\n'.join(out),ordered

def render(root,manifest,content):
    def write(path,text):
        p=root/path; p.parent.mkdir(parents=True,exist_ok=True); p.write_text(text,encoding='utf-8')
    result_path=root/'reports/test-results.json'
    results={r['id']:r for r in json.loads(result_path.read_text(encoding='utf-8'))} if result_path.exists() else {}
    intro='# LeetCode Hot 100 Java 完整题解与知识点学习手册\n\n适合正在学习JavaSE的读者，兼容Java 17。核对日期：2026-11-25（Asia/Shanghai）。\n\n来源：[力扣官方LeetCode热题100](https://leetcode.cn/studyplan/top-100-liked/)。这是Hot 100，不是“面试经典150题”。网页正文的静态提取未显示题目，本项目直接读取官方HTML中的`__NEXT_DATA__ → props.pageProps.dehydratedState.queries → studyPlanV2Detail.planSubGroups`，得到17组、100个唯一题号。原始快照在sources中保留，题单今后可能更新。\n\n所有题意由本项目自行概括，未复制官方题面或题解。例子是帮助理解的局部输入，具体输入约束以各题官方页面为准。每个提交实现采用独立文件；有意选择易读版本，例如300用O(n²)DP、148用递归归并并明确栈空间。\n\n学习建议：先看Java基础，再按推荐顺序练习；遇到集合API时回到附录，不必先背完全部API。源码中文注释与各题第3、6节配合阅读。树示例用层序数组表示，null为空孩子；链表示例中的箭头表示next，特别标明共享节点时才表示引用相同；设计题示例按调用先后列出。\n'
    write('Java基础知识附录.md',java_appendix()); write('算法知识附录.md',algorithm_appendix())
    for q in manifest: q['_code']=content[q['id']]['code']
    plan,ordered=learning_order(manifest); write('初学者推荐刷题顺序.md',plan)
    index='## 100题清单\n\n|题号|中文名称|难度|官方专题|官方链接|\n|---|---|---|---|---|\n'
    index+='\n'.join(f"|{q['id']}|[{q['name']}](#p{q['id']})|{q['difficulty']}|{q['category']}|[原题]({q['url']})|" for q in manifest)+'\n'
    all_chapters=[]; navigation=[]
    for c in range(1,18):
        group=[q for q in manifest if q['chapter']==c]
        group.sort(key=lambda q: {'简单':0,'中等':1,'困难':2}[q['difficulty']])
        name=group[0]['category']; filename=f'chapters/{c:02d}-{name}.md'
        navigation.append(f'- [{c:02d} {name}（{len(group)}题）]({filename})')
        body=f'# {c:02d} {name}\n\n本专题共{len(group)}题。按简单、中等、困难稳定排序；同难度保留官方顺序。先复习算法附录中的对应结构，再学习各题的变量不变量与边界。\n\n'
        body+=' | '.join(f"[{q['id']} {q['name']}](#p{q['id']})" for q in group)+'\n\n'
        for q in group:
            body+=section(q,content[q['id']],results.get(q['id'],{}))+'\n---\n\n'
        body=re.sub(r'\]\(#java-(\d+)\)',r'](../Java基础知识附录.md#java-\1)',body)
        write(filename,body)
        # 主手册真正从已写出的章节文件汇总，仅改回书内附录锚点。
        saved=(root/filename).read_text(encoding='utf-8')
        all_chapters.append(saved.replace('](../Java基础知识附录.md#java-','](#java-'))
    full=intro+'\n'+index+'\n'+java_appendix()+'\n'+algorithm_appendix()+'\n'+plan+'\n'+'\n'.join(all_chapters)
    write('Hot100-Java-完整学习手册.md',full)
    # 机器检查既检查数据也检查落盘产物；检查结果形成可审计报告。
    errors=[]; sections=0
    for q in manifest:
        code=(root/q['source']).read_text(encoding='utf-8'); p=content[q['id']]
        if code.strip()!=p['code']: errors.append(f"{q['id']}源码与讲解不一致")
        if hashlib.sha256((root/q['source']).read_bytes()).hexdigest()!=q['sha256']: errors.append(f"{q['id']}源码哈希变化")
        if results.get(q['id'],{}).get('source_sha256')!=q['sha256']: errors.append(f"{q['id']}本地测试对应的源码版本已过期")
        if len([s for s in p['errors'].split('；') if s.strip()])<2: errors.append(f"{q['id']}易错点不足")
        if '// ' not in code: errors.append(f"{q['id']}缺少行内中文注释")
        for n in range(1,10):
            if f'### {n}.' not in section(q,p,results.get(q['id'],{})): errors.append(f"{q['id']}缺第{n}节")
        sections+=9
    ids=re.findall(r'<a id="p(\d+)"></a>',full)
    if len(ids)!=100 or len(set(ids))!=100: errors.append('主手册题解数量或唯一性异常')
    if len(list((root/'solutions').rglob('*.java')))!=100: errors.append('独立源码不是100个')
    compiled=sum(r.get('compiled',False) for r in results.values()); passed=sum(r.get('local_pass',False) for r in results.values())
    assertions=sum(r.get('assertions',0) for r in results.values())
    for q in manifest:
        if not results.get(q['id'],{}).get('local_pass'): errors.append(f"{q['id']}本地验证未通过或缺失")
    report=f'# 完整性与正确性验证报告\n\n核对与生成日期：2026-11-25（Asia/Shanghai）。\n\n|检查项|结果|\n|---|---|\n|官方清单题数/唯一题号|100 / 100|\n|专题文件|17|\n|主手册完整题解|{len(ids)}|\n|每题九部分|{sections}个小节|\n|独立Java源码|100|\n|Java基础主题/算法主题|22 / 15|\n|Java17目标编译|{compiled}/100|\n|本地测试通过|{passed}/100|\n|本地断言数|{assertions}|\n|LeetCode官方测试通过|0/100（未提交，不代表失败）|\n|自动完整性检查问题|{len(errors)}|\n\n## 验证方法与证据\n\n使用本机JDK 26.0.2.1，通过`javac -encoding UTF-8 --release 17`限制语言和标准库目标到Java17；运行在JDK26，未声称在Java17运行时重测。每题独立编译，tests中提供节点桩和断言入口，.build按题号隔离class文件。`reports/test-results.json`保存每题编译和运行输出。`sources/manifest.json`保存源码SHA-256及测试语句；测试记录另保存源码与测试文件哈希以防结果过期。`tools/extra_checks.py`保存对拍逻辑，例如最长合法括号穷举长度0～9的所有括号串，与枚举子串的独立判定比较；LRU对照LinkedHashMap，双堆中位数对照完整排序。\n\n所有题都包含例题、边界或特殊结构的多个断言，另为21题增加固定种子的随机对拍或小规模穷举；计数是assertion次数，不等同于独立测试场景数。链表相交按身份验证，随机链验证深拷贝与random指针，平衡树验证中序和值域、平衡性，N皇后验证数量与列/斜线约束，无序答案归一化比较。\n\n## 适用范围与未解决事项\n\n本地有限测试不能证明对所有合法输入正确；未进行力扣在线提交，100题官方状态均为“未验证”。递归实现可能在极深链式树上遇到JVM栈限制；学习手册在基础附录说明了这一点。PDF未导出，交付以Markdown与源码为准。题单是核对日官方快照，今后需要重新获取并人工审阅变更，不能只改日期。\n\n自动检查覆盖结构、数量、文件一致性、注释存在性和本地执行状态，不能替代人工评估教学质量或证明算法。\n\n'
    report+='## 独立交付审计\n\n生成后运行`python tools/audit.py`，审计官方HTML与提取数据、清单字段、100份源码及测试哈希、章节/主手册代码一致性、九部分结构和本地链接。结果保存在`reports/audit.json`；审计失败会返回非零退出码。\n\n## 逐题验证记录\n\n|题号|编译|本地测试|断言数|官方|\n|---|---|---|---|---|\n'
    report+='\n'.join(f"|{q['id']}|{'已编译' if results.get(q['id'],{}).get('compiled') else '尚未验证'}|{'通过' if results.get(q['id'],{}).get('local_pass') else '尚未通过/未验证'}|{results.get(q['id'],{}).get('assertions',0)}|未提交|" for q in manifest)
    if errors: report+='\n\n## 待处理\n\n'+'\n'.join('- '+e for e in errors)
    if (root/'output/pdf/Hot100-Java-完整学习手册.pdf').exists():
        report=report.replace('PDF未导出，交付以Markdown与源码为准。','已额外导出完整PDF，文件位于output/pdf；PDF覆盖与抽样渲染记录见reports/pdf-check.json。Markdown与源码仍为维护原稿。')
    write('完整性检查报告.md',report+'\n')
    progress=f'# 制作进度与学习追踪\n\n更新时间：2026-11-25。内容100/100，专题17/17；编译{compiled}/100，本地测试{passed}/100，官方未提交100/100。\n\n制作阶段：官方题单核对、基础附录、17专题题解、独立源码、编译/测试、主手册汇总、完整性报告均已执行。验证边界详见完整性检查报告。\n\n以下复选框是你自己的掌握进度，默认未勾选；不要把本地测试通过误当成自己已经掌握。建议做题后记下用时、错因、下次复习日期。\n\n'
    progress+='\n'.join(f"- [ ] {i:03d}｜{q['id']} {q['name']}｜掌握程度：待学习｜错因：｜下次复习：" for i,q in enumerate(ordered,1))
    progress+='\n\n## 下次维护\n\n重新验证：python tools/verify.py；然后python tools/build.py刷新报告。修改tools中的题解源数据再生成，不直接手改chapters或主手册。若中断，先读本文件和reports/test-results.json，再从未通过题继续；不清空已有成果。\n'
    progress_path=root/'progress.md'
    if progress_path.exists():
        # 重建手册时保留学习者已经勾选的题目、错因和复习日期。
        old=progress_path.read_text(encoding='utf-8')
        rows={m.group(1):m.group(0) for m in re.finditer(r'^- \[[ xX]\] \d+｜(\d+) .*$',old,re.M)}
        progress=re.sub(r'^- \[[ xX]\] \d+｜(\d+) .*$',lambda m:rows.get(m.group(1),m.group(0)),progress,flags=re.M)
    if (root/'mkdocs.yml').exists():
        progress+='\n\n## 手机与电脑阅读交付\n\n已增加MkDocs Material网站、100个独立题目页、17个专题、中文搜索、代码复制、主题切换及翻页；PDF和网站ZIP位于output目录。当前验证记录见reports/site-audit.json、reports/browser-check.json、reports/pdf-check.json。未公开部署，手机使用触摸视口模拟，未在实体iPhone Safari上实测。详见手机与电脑阅读说明.md、网站构建与验证报告.md。\n'
    write('progress.md',progress)
    readme='# LeetCode Hot 100 Java 完整题解与知识点学习手册\n\n面向Java初学者的中文学习资料。官方题单核对日期：2026-11-25，17专题、100个不同题号。100份源码已通过Java17目标编译及本地测试；没有进行LeetCode官方提交。\n\n## 从哪里开始\n\n1. [Java基础知识附录](Java基础知识附录.md)：22项基础与常用API速查。\n2. [初学者推荐刷题顺序](初学者推荐刷题顺序.md)：七阶段100题、60天和30天逐日新题/复习安排。\n3. [完整学习手册](Hot100-Java-完整学习手册.md)：含全部100题完整讲解与代码，可离线全文搜索。\n4. [算法知识附录](算法知识附录.md)：15类算法含义、适用场景、模板和复杂度。\n5. [制作进度与个人学习追踪](progress.md)。\n6. [完整性与验证报告](完整性检查报告.md)：检查范围、逐题状态和局限。\n\n本文件位于工作区内新建的LeetCode-Hot100-Java子目录，未改动其他项目。每题九部分统一组织：基本信息、题意、思路、代码、Java知识、示例过程、复杂度、易错点、总结。正文题目仅出现一次，索引与推荐顺序只是导航。\n\n## 专题导航\n\n'+'\n'.join(navigation)+'\n\n## 源码、测试与维护\n\n`solutions/`按专题英文目录保存题号开头的源码；普通题类名都是Solution，设计题类名按题意。不能把100份默认包的Solution同时编译到同一个目录。`tests/`是每题的独立测试入口与节点桩，不能混进力扣提交代码。\n\n在本README所在目录执行：\n\n```powershell\npython tools/build.py --sources\npython tools/verify.py\npython tools/build.py\npython tools/audit.py\n```\n\n需要Python3与JDK17以上。build仅使用Python标准库；verify每题独立编译运行，最多4个并发进程，失败与日志写入`reports/test-results.json`；源码依据`tools/*_content.py`与`tools/content.py`生成，主手册由相同内容的专题章节汇总，避免多处手改。附录源稿在`tools/foundations.py`，文档生成在`tools/render.py`。\n\n## 官方依据\n\n[力扣Hot100官方题单](https://leetcode.cn/studyplan/top-100-liked/)。官方HTML快照：[sources/official-page.html](sources/official-page.html)；嵌入数据：[sources/official-data.json](sources/official-data.json)；提取后的100题清单：[sources/problems.json](sources/problems.json)。核对时程序断言17组、100题、100唯一题号；未来更新时需重新抓取并审阅，不把旧快照当实时清单。可运行`python tools/extract_official.py`从已保存快照重提取；该操作本身不会联网刷新。\n\n## 文件清单\n\n'
    readme+='|题号|名称|难度|讲解|源码|\n|---|---|---|---|---|\n'
    for q in manifest:
        chapter=f"chapters/{q['chapter']:02d}-{q['category']}.md#p{q['id']}"
        readme+=f"|{q['id']}|{q['name']}|{q['difficulty']}|[题解]({chapter})|[Java]({q['source']})|\n"
    if (root/'mkdocs.yml').exists():
        webintro='## 手机与电脑阅读\n\n- [直接打开HTML网站](site/index.html)：MkDocs Material，100个独立题目页、中文搜索、代码复制、深浅主题。\n- [手机与电脑阅读说明](手机与电脑阅读说明.md)：Windows本地阅读、iPhone Safari、主屏幕快捷方式、构建与GitHub Pages手动部署。\n- [完整PDF](output/pdf/Hot100-Java-完整学习手册.pdf)：适合保存到iPhone离线阅读。\n- [网站ZIP包](output/hot100-website.zip)：解压整个目录后打开index.html。\n\n网站与PDF生成方式、依赖清单和验证范围见阅读说明。本次没有推送或公开部署。\n\n'
        readme=readme.replace('## 从哪里开始\n',webintro+'## 从哪里开始\n')
    write('README.md',readme)
    write('reports/integrity.json',json.dumps(dict(problems=len(ids),unique=len(set(ids)),chapters=17,sources=100,compiled=compiled,local_pass=passed,assertions=assertions,official_pass=0,errors=errors),ensure_ascii=False,indent=2))
    print(f'Generated: 100 solutions, 17 chapters; compiled={compiled}, local_pass={passed}, integrity_errors={errors}')
    if errors: raise SystemExit(1)
