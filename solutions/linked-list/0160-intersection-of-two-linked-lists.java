class Solution {
    public ListNode getIntersectionNode(ListNode headA,ListNode headB) {
        ListNode p=headA,q=headB;
        while(p!=q) {
            p=(p==null)?headB:p.next; // 走完自己的链后换另一条链
            q=(q==null)?headA:q.next;
        }
        return p; // 无交点时两者都为null
    }
}
