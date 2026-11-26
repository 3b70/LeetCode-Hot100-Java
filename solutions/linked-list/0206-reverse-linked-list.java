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
}
