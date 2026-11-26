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
}
