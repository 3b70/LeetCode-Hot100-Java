import java.util.*;
class MinStack {
    private final Deque<Integer> data=new ArrayDeque<>(),mins=new ArrayDeque<>();
    public MinStack() {}
    public void push(int val) {
        data.push(val);
        mins.push(mins.isEmpty()?val:Math.min(val,mins.peek())); // 为本层保存最小值
    }
    public void pop() { data.pop(); mins.pop(); }
    public int top() { return data.peek(); }
    public int getMin() { return mins.peek(); }
}
