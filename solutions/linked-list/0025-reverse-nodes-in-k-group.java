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
}
