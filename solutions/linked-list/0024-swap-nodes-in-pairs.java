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
}
