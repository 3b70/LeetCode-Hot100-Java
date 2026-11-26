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
}
