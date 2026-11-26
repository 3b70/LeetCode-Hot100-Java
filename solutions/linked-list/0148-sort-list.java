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
}
