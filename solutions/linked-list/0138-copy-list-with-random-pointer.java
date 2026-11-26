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
}
