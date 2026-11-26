class Solution {
    public ListNode removeNthFromEnd(ListNode head,int n) {
        ListNode dummy=new ListNode(0,head),fast=dummy,slow=dummy;
        for(int i=0;i<n;i++) fast=fast.next; // 保持n个节点的间隔
        while(fast.next!=null) { fast=fast.next; slow=slow.next; }
        slow.next=slow.next.next; // slow指向被删除节点的前驱
        return dummy.next;
    }
}
