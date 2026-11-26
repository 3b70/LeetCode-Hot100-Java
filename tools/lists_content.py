from content import add
add(160,'给两个无环单链表，返回第一个公共节点对象；没有交点返回null。公共指的是同一对象，不只是值相等。','A=1→8→9，B=2→3→8→9，其中8节点共享 → 返回共享8节点',
'用集合存A的节点，再扫描B，额外空间O(m)。','指针p走完A后改走B，q走完B后改走A。两人走过总长度相同，前段长度差被抵消；有交点时在公共后缀入口相遇，无交点时最终同时为null。循环比较节点引用。',
'A独有1个节点，B独有2个；p先经过公共8、9再切B，q走完B再切A；第二轮进入共享8时同步，返回该对象。',
'O(m+n) 时间，每个指针至多走两条链；O(1) 空间。','用==比较对象引用而非val；切换应发生在指针为null时；题目要求链表无环。',r'''
class Solution {
    public ListNode getIntersectionNode(ListNode headA,ListNode headB) {
        ListNode p=headA,q=headB;
        while(p!=q) {
            p=(p==null)?headB:p.next; // 走完自己的链后换另一条链
            q=(q==null)?headA:q.next;
        }
        return p; // 无交点时两者都为null
    }
}''','ListNode shared=list(8,9); ListNode a=new ListNode(1,shared), b=new ListNode(2,new ListNode(3,shared)); eq(new Solution().getIntersectionNode(a,b)==shared,true); eq(new Solution().getIntersectionNode(list(1),list(1))==null,true); eq(new Solution().getIntersectionNode(null,null)==null,true);')
add(206,'反转单链表，返回新头节点；空链表返回null。节点对象沿用原链表。','1→2→3 → 3→2→1',
'把节点放栈后重新连接可行，但多用O(n)空间。','prev是已经反转的前段头，cur是未处理后段头。先保存next，再令cur.next指向prev，最后一起向前推进。终止时cur为null，prev就是新头。',
'初始prev=null,cur=1；处理1后1→null；处理2后2→1；处理3后3→2→1，cur=null返回3。',
'O(n) 时间，每个节点修改一次next；O(1) 空间，只存三个引用。','必须先保存next否则丢失后半段；返回prev而非旧head；尾节点next要最终变为null。',r'''
class Solution {
    public ListNode reverseList(ListNode head) {
        ListNode prev=null,cur=head;
        while(cur!=null) {
            ListNode next=cur.next; // 修改链接前保存后继
            cur.next=prev;
            prev=cur; cur=next; // 已反转区域向右扩展一个节点
        }
        return prev;
    }
}''','eq(vals(new Solution().reverseList(list(1,2,3))),"[3, 2, 1]"); eq(new Solution().reverseList(null)==null,true); eq(vals(new Solution().reverseList(list(1))),"[1]");')
add(234,'判断单链表的值序列是否回文。返回布尔值，空链表也视为回文。','1→2→2→1 → true',
'复制值到数组再双指针比较，空间O(n)。','快慢指针找前半段尾节点；反转后半段，用左右指针逐个比较；无论相等与否都把后半段再反转接回，恢复输入。只比较后半段长度，奇数链表中点自然忽略。',
'1→2→2→1中slow停前一个2；后半段2→1反转成1→2；比较1=1、2=2；反转回来，返回true。',
'O(n) 时间，找中点、两次反转和比较均线性；O(1) 额外空间。','奇数中点不参与配对；不能反转前丢失后半段入口；提前return会跳过恢复操作。',r'''
class Solution {
    public boolean isPalindrome(ListNode head) {
        if(head==null || head.next==null) return true;
        ListNode slow=head,fast=head;
        while(fast.next!=null && fast.next.next!=null) { slow=slow.next; fast=fast.next.next; }
        ListNode right=reverse(slow.next),p=head,q=right;
        boolean ok=true;
        while(q!=null) {
            if(p.val!=q.val) ok=false;
            p=p.next; q=q.next;
        }
        slow.next=reverse(right); // 判断后恢复原链表
        return ok;
    }
    private ListNode reverse(ListNode cur) {
        ListNode prev=null;
        while(cur!=null) { ListNode next=cur.next; cur.next=prev; prev=cur; cur=next; }
        return prev;
    }
}''','ListNode a=list(1,2,2,1); eq(new Solution().isPalindrome(a),true); eq(vals(a),"[1, 2, 2, 1]"); eq(new Solution().isPalindrome(list(1,2)),false); eq(new Solution().isPalindrome(list(1,2,1)),true); eq(new Solution().isPalindrome(null),true);')
add(141,'判断单链表是否有环。环指沿next最终回到之前的同一节点。不能根据重复值判断。','1→2→3，3.next指向2 → true',
'集合记录访问过的节点，空间O(n)。','慢指针每次一步，快指针两步。若没有环，快指针先到null；若有环，两者在环内的相对距离每轮缩小一格，必然相遇。先移动再比较，避免初始都在头部被误判。',
'环2→3→2：第一轮slow=2,fast=3；第二轮slow=3,fast=3，相遇返回true。',
'O(n) 时间，入环及追赶均线性；O(1) 空间。','先检查fast及fast.next再走两步；比较引用；初始相同不代表有环。',r'''
class Solution {
    public boolean hasCycle(ListNode head) {
        ListNode slow=head,fast=head;
        while(fast!=null && fast.next!=null) {
            slow=slow.next; fast=fast.next.next;
            if(slow==fast) return true; // 移动后才判断是否相遇
        }
        return false;
    }
}''','ListNode a=list(1,2,3); a.next.next.next=a.next; eq(new Solution().hasCycle(a),true); eq(new Solution().hasCycle(list(1,2)),false); eq(new Solution().hasCycle(null),false);')
add(142,'有环则返回环的入口节点，无环返回null；不允许修改链表结构。','1→2→3→4，4.next指向2 → 返回节点2',
'用集合找到第一次重复访问的节点，空间O(n)。','第一阶段快慢指针相遇；第二阶段把一个指针放回head，另一个留在相遇点，两者每次走一步，再次相遇处是入口。若入口前距离a、相遇点到入口沿环剩余距离c，则快慢步数关系推出a与c模环长同余，因此同步走到入口。无环时直接返回null。',
'1→2→3→4→2，快慢在4相遇；p回1，slow留4；同时一步后均到2，因此返回2。',
'O(n) 时间，两次有限追赶；O(1) 空间。','第二阶段两者都走一步；必须先确认有环；入口是对象引用而非入口值。',r'''
class Solution {
    public ListNode detectCycle(ListNode head) {
        ListNode slow=head,fast=head;
        while(fast!=null && fast.next!=null) {
            slow=slow.next; fast=fast.next.next;
            if(slow==fast) {
                ListNode p=head;
                while(p!=slow) { p=p.next; slow=slow.next; } // 同速定位入口
                return p;
            }
        }
        return null;
    }
}''','ListNode a=list(1,2,3,4); a.next.next.next.next=a.next; eq(new Solution().detectCycle(a)==a.next,true); eq(new Solution().detectCycle(list(1))==null,true); ListNode b=list(1); b.next=b; eq(new Solution().detectCycle(b)==b,true);')
add(21,'合并两条升序链表并返回升序新链的头。可以重连原节点；任一输入可为空。','1→2→4 与 1→3→4 → 1→1→2→3→4→4',
'把所有值收集排序再建链，额外成本更高。','使用虚拟头dummy和尾指针tail，每轮比较两条链的头，把较小者接到tail后并推进该链；tail向后移。某条链为空后，剩余链本来有序，直接整体接上。',
'先取第一条的1，再取第二条的1，再2、3、4；剩余4直接接尾，dummy.next指向第一个1。',
'O(m+n) 时间，每个节点至多被比较连接一次；O(1) 额外空间，复用节点。','返回dummy.next；接节点后要推进来源链；输入应是两条独立无环链。',r'''
class Solution {
    public ListNode mergeTwoLists(ListNode list1,ListNode list2) {
        ListNode dummy=new ListNode(0),tail=dummy;
        while(list1!=null && list2!=null) {
            if(list1.val<=list2.val) { tail.next=list1; list1=list1.next; }
            else { tail.next=list2; list2=list2.next; }
            tail=tail.next; // 保持tail为已经合并部分的尾
        }
        tail.next=(list1!=null)?list1:list2;
        return dummy.next;
    }
}''','eq(vals(new Solution().mergeTwoLists(list(1,2,4),list(1,3,4))),"[1, 1, 2, 3, 4, 4]"); eq(new Solution().mergeTwoLists(null,null)==null,true); eq(vals(new Solution().mergeTwoLists(null,list(0))),"[0]");')
add(2,'两条链表按低位在前保存两个非负整数，返回同样格式的和。每节点是一位0..9，输入至少有一个节点。','2→4→3 与 5→6→4 → 7→0→8（342+465=807）',
'转成int后相加可能溢出，链表长度不受int位数限制。','模拟竖式。循环条件包含任一链未结束或还有进位；把存在的位相加，加上carry，结果位为sum%10，新进位为sum/10。构造全新节点并连接。',
'2+5=7写7进位0；4+6=10写0进位1；3+4+1=8写8；结束，返回7→0→8。',
'O(max(m,n)) 时间，逐位加法；O(max(m,n)) 输出空间，除输出外O(1)。','最后一位进位不能丢；链长可能不同；整数不能代替任意长数字链表。',r'''
class Solution {
    public ListNode addTwoNumbers(ListNode l1,ListNode l2) {
        ListNode dummy=new ListNode(0),tail=dummy;
        int carry=0;
        while(l1!=null || l2!=null || carry!=0) {
            int sum=carry;
            if(l1!=null) { sum+=l1.val; l1=l1.next; }
            if(l2!=null) { sum+=l2.val; l2=l2.next; }
            tail.next=new ListNode(sum%10); // 当前十进制位
            tail=tail.next; carry=sum/10; // 进位传给下一轮
        }
        return dummy.next;
    }
}''','eq(vals(new Solution().addTwoNumbers(list(2,4,3),list(5,6,4))),"[7, 0, 8]"); eq(vals(new Solution().addTwoNumbers(list(9,9),list(1))),"[0, 0, 1]"); eq(vals(new Solution().addTwoNumbers(list(0),list(0))),"[0]");')
add(19,'删除单链表倒数第n个节点并返回头部，保证1≤n≤链表长度。可能删除原头节点。','1→2→3→4→5, n=2 → 1→2→3→5',
'先数长度，再定位正数第length-n+1个节点，需要两次遍历。','建立dummy，fast和slow从dummy出发。fast先走n步，然后两个指针同时前进，直到fast位于尾节点；此时slow是待删节点的前驱。令slow.next跳过下一个节点。',
'n=2，fast先到2；同步三步后fast=5，slow=3；令3.next=5，删除4。',
'O(n链长) 时间，fast总共走完整条链；O(1) 空间。','虚拟头解决删除头节点；快慢间隔与循环终点需配套；n按倒数计数从1开始。',r'''
class Solution {
    public ListNode removeNthFromEnd(ListNode head,int n) {
        ListNode dummy=new ListNode(0,head),fast=dummy,slow=dummy;
        for(int i=0;i<n;i++) fast=fast.next; // 保持n个节点的间隔
        while(fast.next!=null) { fast=fast.next; slow=slow.next; }
        slow.next=slow.next.next; // slow指向被删除节点的前驱
        return dummy.next;
    }
}''','eq(vals(new Solution().removeNthFromEnd(list(1,2,3,4,5),2)),"[1, 2, 3, 5]"); eq(new Solution().removeNthFromEnd(list(1),1)==null,true); eq(vals(new Solution().removeNthFromEnd(list(1,2),2)),"[2]");')
add(24,'把链表每两个相邻节点交换，返回新头。必须交换节点链接，不能仅交换数值；奇数尾节点保留。','1→2→3→4 → 2→1→4→3',
'把所有节点存数组再重连可行，但多用空间。','dummy前驱p指向待处理一对之前。保存a=p.next、b=a.next；先把a接到b后继，再让b指向a，最后p指向b。完成后p移到a，作为下一对的前驱。',
'dummy→1→2→3→4：先让1.next=3，2.next=1，dummy.next=2；p移到1，再交换3、4，得到2→1→4→3。',
'O(n) 时间，每个节点重连常数次；O(1) 空间。','要检查下一对是否有两个节点；不能忘记上一段与新头的连接；p应移到交换后的尾节点a。',r'''
class Solution {
    public ListNode swapPairs(ListNode head) {
        ListNode dummy=new ListNode(0,head),p=dummy;
        while(p.next!=null && p.next.next!=null) {
            ListNode a=p.next,b=a.next;
            a.next=b.next; b.next=a; p.next=b; // 一次重连完整的一对
            p=a; // 原第一个节点现在是本对尾部
        }
        return dummy.next;
    }
}''','eq(vals(new Solution().swapPairs(list(1,2,3,4))),"[2, 1, 4, 3]"); eq(vals(new Solution().swapPairs(list(1,2,3))),"[2, 1, 3]"); eq(new Solution().swapPairs(null)==null,true);')
add(25,'每k个节点一组反转链表，不满k个的最后一组保持原样。只能改变链接，1≤k≤链长。','1→2→3→4→5, k=2 → 2→1→4→3→5',
'每组放入栈再输出可行，但额外空间O(k)。','before是上一组尾。先从before向前找第k个节点kth，找不到就结束。保存after=kth.next，以after为反转初始prev，逐个反转直到cur=after。将before接新头kth，再把before移到原组头（现在的组尾）。',
'第一组[1,2]，after=3，反转后2→1→3；before移到1；第二组[3,4]反转为4→3→5；最后5不足一组，保留。',
'O(n) 时间，每组寻找边界和反转各扫描一次；O(1) 空间。','反转前先确认足够k个；保存after防止丢后段；before须更新到旧组头。',r'''
class Solution {
    public ListNode reverseKGroup(ListNode head,int k) {
        ListNode dummy=new ListNode(0,head),before=dummy;
        while(true) {
            ListNode kth=before;
            for(int i=0;i<k && kth!=null;i++) kth=kth.next;
            if(kth==null) break; // 剩余不足k个，保持原顺序
            ListNode after=kth.next,cur=before.next,prev=after,oldHead=cur;
            while(cur!=after) {
                ListNode next=cur.next; cur.next=prev; prev=cur; cur=next;
            }
            before.next=kth; before=oldHead; // 接回前段，并准备下一组
        }
        return dummy.next;
    }
}''','eq(vals(new Solution().reverseKGroup(list(1,2,3,4,5),2)),"[2, 1, 4, 3, 5]"); eq(vals(new Solution().reverseKGroup(list(1,2,3),3)),"[3, 2, 1]"); eq(vals(new Solution().reverseKGroup(list(1),1)),"[1]");')
add(138,'深拷贝带next与random指针的链表。新链所有节点都必须是新对象，random指向对应的新节点或null。','A(7).next=B(13)，B.random=A → 复制后B′.random=A′，且A′≠A',
'复制next链后，每个random都从头寻找对应位置，可能O(n²)。','用Map<旧节点,新节点>分两遍。第一遍仅创建全部新节点；第二遍根据旧next和random查表连接。Map查null会返回null，因此空指针自然处理。先造全体对象才能正确连接向前和向后的random。',
'先建立A→A′、B→B′映射；再令A′.next=B′，B′.random=A′；返回map.get(head)。旧链不变。',
'O(n) 平均时间，两遍遍历与哈希查找；O(n) 辅助映射，另有O(n)输出节点。','不能让新random指向旧节点；键必须是节点对象，值可重复；空head返回null。',r'''
import java.util.*;
class Solution {
    public Node copyRandomList(Node head) {
        Map<Node,Node> copies=new HashMap<>();
        for(Node p=head;p!=null;p=p.next) copies.put(p,new Node(p.val));
        for(Node p=head;p!=null;p=p.next) {
            Node copy=copies.get(p);
            copy.next=copies.get(p.next);
            copy.random=copies.get(p.random); // 用映射连接到新对象
        }
        return copies.get(head);
    }
}''','Node a=new Node(7),b=new Node(13); a.next=b; b.random=a; Node c=new Solution().copyRandomList(a); eq(c!=a && c.val==7 && c.next!=b && c.next.random==c,true); eq(new Solution().copyRandomList(null)==null,true); Node d=new Node(1); d.random=d; Node e=new Solution().copyRandomList(d); eq(e!=d && e.random==e,true);')
add(148,'把单链表按值升序排列并返回新头。使用归并排序，空链表和单节点直接返回。','4→2→1→3 → 1→2→3→4',
'收集数组排序再重建要额外O(n)；链表插入排序最坏O(n²)。','递归归并：快慢指针找中点，把链切为两段；分别递归得到有序左链和右链；双指针合并。终止条件是空链或单节点，递归返回已排序子链的头。代码选择易懂的自顶向下版本，栈空间O(log n)，并非严格常量空间；若进一步要求O(1)可学习自底向上归并。',
'4,2,1,3拆为[4,2]和[1,3]；再拆到单节点；合并成[2,4]和[1,3]；最后依次选1、2、3、4。',
'O(n log n) 时间，每层合并共O(n)，有log n层；O(log n) 递归栈，合并自身O(1)。','必须切断左链，否则无限递归；fast从head.next开始保证双节点能平分；空间不能误写O(1)。',r'''
class Solution {
    public ListNode sortList(ListNode head) {
        if(head==null || head.next==null) return head; // 最小有序子问题
        ListNode slow=head,fast=head.next;
        while(fast!=null && fast.next!=null) { slow=slow.next; fast=fast.next.next; }
        ListNode right=slow.next; slow.next=null; // 断开，保证子问题严格变小
        return merge(sortList(head),sortList(right));
    }
    private ListNode merge(ListNode a,ListNode b) {
        ListNode dummy=new ListNode(0),tail=dummy;
        while(a!=null && b!=null) {
            if(a.val<=b.val) { tail.next=a; a=a.next; }
            else { tail.next=b; b=b.next; }
            tail=tail.next;
        }
        tail.next=a!=null?a:b;
        return dummy.next;
    }
}''','eq(vals(new Solution().sortList(list(4,2,1,3))),"[1, 2, 3, 4]"); eq(new Solution().sortList(null)==null,true); eq(vals(new Solution().sortList(list(2,2,1))),"[1, 2, 2]");')
add(23,'合并k条升序链表，返回包含全部节点的升序链表。列表可为空，各链也可为空。','[1→4→5, 1→3→4, 2→6] → 1→1→2→3→4→4→5→6',
'反复扫描k个当前链头找最小值，O(Nk)。','最小堆只保存各条链当前未合并的首节点。弹出全局最小节点接到结果，若它有后继就把后继入堆。堆中每条非空链至多一个节点，保证全局顺序。',
'初始堆头值1、1、2；弹1后加入其后继4；再弹另一1加入3；接着2加入6；继续得到3、4、4、5、6。',
'O(N log(k+1)) 时间，N为总节点数，每次堆操作至多log k；O(k) 空间。','堆不能加入null；比较器不要直接相减；输入链应独立，不能共享节点或含环。',r'''
import java.util.*;
class Solution {
    public ListNode mergeKLists(ListNode[] lists) {
        PriorityQueue<ListNode> heap=new PriorityQueue<>((a,b)->Integer.compare(a.val,b.val));
        for(ListNode node:lists) if(node!=null) heap.offer(node);
        ListNode dummy=new ListNode(0),tail=dummy;
        while(!heap.isEmpty()) {
            ListNode node=heap.poll(); // 取所有候选链头中最小者
            if(node.next!=null) heap.offer(node.next);
            tail.next=node; tail=node;
        }
        return dummy.next;
    }
}''','eq(vals(new Solution().mergeKLists(new ListNode[]{list(1,4,5),list(1,3,4),list(2,6)})),"[1, 1, 2, 3, 4, 4, 5, 6]"); eq(new Solution().mergeKLists(new ListNode[]{})==null,true); eq(vals(new Solution().mergeKLists(new ListNode[]{null,list(0)})),"[0]");')
add(146,'实现固定正容量的LRU缓存：get不存在返回-1，存在则提升最近使用；put插入或更新并提升，超容量删除最久未使用键。','容量2；put(1,1),put(2,2),get(1),put(3,3) → get(2)=-1',
'用列表记录顺序，每次查找或移动都可能O(n)。','Map定位双向链表节点，head后为最近使用，tail前为最旧。get命中后摘下节点并插头；put更新也提升，新键插头，超限删除tail.prev并从Map移除。两个哨兵免去空表首尾的特殊判断。设计题类名为LRUCache。',
'put1后顺序[1]；put2后[2,1]；get1后[1,2]；put3后[3,1,2]，淘汰尾2，剩[3,1]。',
'get/put平均O(1) 时间，Map查找平均常数且链表摘插常数；O(capacity) 空间。','更新已有键也算访问；摘链必须双向都修改；淘汰同时删Map，否则出现幽灵键。',r'''
import java.util.*;
class LRUCache {
    private static class Entry {
        int key,value; Entry prev,next;
        Entry(int k,int v) { key=k; value=v; }
    }
    private final int capacity;
    private final Map<Integer,Entry> map=new HashMap<>();
    private final Entry head=new Entry(0,0),tail=new Entry(0,0);
    public LRUCache(int capacity) { this.capacity=capacity; head.next=tail; tail.prev=head; }
    public int get(int key) {
        Entry e=map.get(key);
        if(e==null) return -1;
        remove(e); front(e); // 命中后提升为最近使用
        return e.value;
    }
    public void put(int key,int value) {
        Entry e=map.get(key);
        if(e!=null) { e.value=value; remove(e); front(e); return; }
        e=new Entry(key,value); map.put(key,e); front(e);
        if(map.size()>capacity) {
            Entry oldest=tail.prev;
            remove(oldest); map.remove(oldest.key); // 两种结构同步淘汰
        }
    }
    private void remove(Entry e) { e.prev.next=e.next; e.next.prev=e.prev; }
    private void front(Entry e) {
        e.next=head.next; e.prev=head; head.next.prev=e; head.next=e;
    }
}''','LRUCache c=new LRUCache(2); c.put(1,1); c.put(2,2); eq(c.get(1),1); c.put(3,3); eq(c.get(2),-1); c.put(4,4); eq(c.get(1),-1); eq(c.get(3),3); LRUCache d=new LRUCache(1); d.put(1,1); d.put(1,2); eq(d.get(1),2); d.put(2,3); eq(d.get(1),-1);')
