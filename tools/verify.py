"""每题独立编译、运行；节点是本地测试桩，不混入提交文件。"""
import concurrent.futures, hashlib, json, pathlib, subprocess, time

ROOT=pathlib.Path(__file__).resolve().parents[1]
FIXTURES=r'''
import java.util.*;
class ListNode {
    int val; ListNode next;
    ListNode(int v) { val=v; }
    ListNode(int v,ListNode n) { val=v; next=n; }
}
class TreeNode {
    int val; TreeNode left,right;
    TreeNode(int v) { val=v; }
}
class Node {
    int val; Node next,random;
    Node(int v) { val=v; }
}
class Test {
    static int assertions;
    static void eq(Object actual,Object expected) {
        assertions++;
        if(!Objects.deepEquals(actual,expected))
            throw new AssertionError("actual="+show(actual)+", expected="+show(expected));
    }
    static String show(Object o) {
        if(o instanceof int[]) return Arrays.toString((int[])o);
        if(o instanceof int[][]) return Arrays.deepToString((int[][])o);
        return String.valueOf(o);
    }
    static ListNode list(int... values) {
        ListNode dummy=new ListNode(0),tail=dummy;
        for(int v:values) { tail.next=new ListNode(v); tail=tail.next; }
        return dummy.next;
    }
    static String vals(ListNode node) {
        List<Integer> a=new ArrayList<>(); Set<ListNode> seen=new HashSet<>();
        while(node!=null) {
            if(!seen.add(node)) throw new AssertionError("unexpected cycle");
            a.add(node.val); node=node.next;
        }
        return a.toString();
    }
    static TreeNode tree(Integer... values) {
        if(values.length==0 || values[0]==null) return null;
        TreeNode root=new TreeNode(values[0]); Queue<TreeNode> q=new ArrayDeque<>(); q.offer(root);
        int i=1;
        while(i<values.length && !q.isEmpty()) {
            TreeNode p=q.poll();
            if(values[i]!=null) { p.left=new TreeNode(values[i]); q.offer(p.left); } i++;
            if(i<values.length) {
                if(values[i]!=null) { p.right=new TreeNode(values[i]); q.offer(p.right); } i++;
            }
        }
        return root;
    }
    static String level(TreeNode root) {
        if(root==null) return "[]";
        List<Integer> a=new ArrayList<>(); Queue<TreeNode> q=new LinkedList<>(); q.offer(root);
        Set<TreeNode> seen=new HashSet<>();
        while(!q.isEmpty()) {
            TreeNode p=q.poll();
            if(p==null) { a.add(null); continue; }
            if(!seen.add(p)) throw new AssertionError("tree cycle/shared node");
            a.add(p.val); q.offer(p.left); q.offer(p.right);
        }
        while(!a.isEmpty() && a.get(a.size()-1)==null) a.remove(a.size()-1);
        return a.toString();
    }
    static void walk(TreeNode n,List<Integer> a) {
        if(n==null) return; walk(n.left,a); a.add(n.val); walk(n.right,a);
    }
    static String inorder(TreeNode n) { List<Integer> a=new ArrayList<>(); walk(n,a); return a.toString(); }
    static int balanced(TreeNode n) {
        if(n==null) return 0;
        int l=balanced(n.left),r=balanced(n.right); eq(Math.abs(l-r)<=1,true); return Math.max(l,r)+1;
    }
    static String chain(TreeNode n) {
        List<Integer> a=new ArrayList<>(); Set<TreeNode> seen=new HashSet<>();
        while(n!=null) { eq(n.left==null,true); eq(seen.add(n),true); a.add(n.val); n=n.right; }
        return a.toString();
    }
    static String norm(List<? extends List<?>> groups) {
        List<String> a=new ArrayList<>(); for(List<?> g:groups) a.add(g.toString());
        Collections.sort(a); return a.toString();
    }
    static String normGroups(List<List<String>> groups) {
        List<List<String>> copy=new ArrayList<>();
        for(List<String> g:groups) { List<String> row=new ArrayList<>(g); Collections.sort(row); copy.add(row); }
        return norm(copy);
    }
    static void queens(List<List<String>> boards,int n) {
        Set<String> distinct=new HashSet<>();
        for(List<String> b:boards) {
            eq(b.size(),n); eq(distinct.add(b.toString()),true);
            Set<Integer> cols=new HashSet<>(),d1=new HashSet<>(),d2=new HashSet<>();
            for(int r=0;r<n;r++) {
                String row=b.get(r); eq(row.length(),n); int c=row.indexOf('Q');
                eq(c>=0 && row.lastIndexOf('Q')==c,true);
                eq(cols.add(c),true); eq(d1.add(r-c),true); eq(d2.add(r+c),true);
            }
        }
    }
    public static void main(String[] args) {
    // TEST_BODY
        System.out.println("PASS assertions="+assertions);
    }
}
'''

def verify_one(q):
    i=q['id']; target=ROOT/q['source']; work=ROOT/'.build'/str(i); work.mkdir(parents=True,exist_ok=True)
    test=ROOT/'tests'/f'{i:04d}-Test.java'
    test.write_text(FIXTURES.replace('// TEST_BODY',q['tests']),encoding='utf-8')
    result=dict(id=i,compiled=False,local_pass=False,official_pass=False,assertions=0,
                source_sha256=hashlib.sha256(target.read_bytes()).hexdigest(),
                test_sha256=hashlib.sha256(test.read_bytes()).hexdigest())
    for name,cmd in [('compile',['javac','-encoding','UTF-8','--release','17','-d',str(work),str(target),str(test)]),
                     ('run',['java','-cp',str(work),'Test'])]:
        if name=='run' and not result['compiled']: break
        try:
            p=subprocess.run(cmd,capture_output=True,text=True,encoding='utf-8',errors='replace',timeout=60)
            result[name+'_log']=(p.stdout+p.stderr).strip()
            if name=='compile': result['compiled']=p.returncode==0
            else:
                result['local_pass']=p.returncode==0
                if result['local_pass']: result['assertions']=int(p.stdout.split('assertions=')[1].strip())
        except (OSError,subprocess.TimeoutExpired) as e: result[name+'_log']=str(e)
    return result

def main():
    manifest=json.loads((ROOT/'sources/manifest.json').read_text(encoding='utf-8'))
    (ROOT/'tests').mkdir(exist_ok=True); (ROOT/'reports').mkdir(exist_ok=True)
    results=[]; start=time.time()
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
        for r in pool.map(verify_one,manifest):
            results.append(r)
            (ROOT/'reports/test-results.json').write_text(json.dumps(results,ensure_ascii=False,indent=2),encoding='utf-8')
            print(f"{r['id']:4}: compiled={r['compiled']} passed={r['local_pass']}",flush=True)
    print(f"Finished {len(results)} in {time.time()-start:.1f}s; passed {sum(r['local_pass'] for r in results)}")
if __name__=='__main__': main()
