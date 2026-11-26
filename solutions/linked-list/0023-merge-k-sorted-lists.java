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
}
