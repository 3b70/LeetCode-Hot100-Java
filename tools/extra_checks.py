"""固定种子的穷举/朴素对照，避免仅验证示例。全部Java标准库。"""
EXTRA={
1:r'''
Random rng=new Random(1);
for(int trial=0;trial<150;trial++) {
    int n=2+rng.nextInt(9); int[] input=new int[n];
    for(int j=0;j<n;j++) input[j]=rng.nextInt(21)-10;
    int target=input[0]+input[n-1];
    int[] got=new Solution().twoSum(input,target);
    eq(got.length,2); eq(got[0]!=got[1],true); eq(input[got[0]]+input[got[1]],target);
}
''',
128:r'''
eq(new Solution().longestConsecutive(new int[]{Integer.MIN_VALUE,Integer.MAX_VALUE}),1);
eq(new Solution().longestConsecutive(new int[]{Integer.MIN_VALUE,Integer.MIN_VALUE+1}),2);
Random rng=new Random(128);
for(int t=0;t<150;t++) {
    int[] input=new int[rng.nextInt(15)];
    for(int j=0;j<input.length;j++) input[j]=rng.nextInt(15)-7;
    int[] sorted=input.clone(); Arrays.sort(sorted); int best=0,run=0;
    for(int j=0;j<sorted.length;j++) {
        if(j>0 && sorted[j]==sorted[j-1]) continue;
        run=(j>0 && sorted[j]==sorted[j-1]+1)?run+1:1; best=Math.max(best,run);
    }
    eq(new Solution().longestConsecutive(input),best);
}
''',
11:r'''
Random rng=new Random(11);
for(int t=0;t<150;t++) {
    int[] input=new int[2+rng.nextInt(12)]; for(int j=0;j<input.length;j++) input[j]=rng.nextInt(10);
    int best=0;
    for(int l=0;l<input.length;l++) for(int r=l+1;r<input.length;r++) best=Math.max(best,(r-l)*Math.min(input[l],input[r]));
    eq(new Solution().maxArea(input),best);
}
''',
15:r'''
Random rng=new Random(15);
for(int t=0;t<100;t++) {
    int[] input=new int[1+rng.nextInt(9)]; for(int j=0;j<input.length;j++) input[j]=rng.nextInt(9)-4;
    Set<String> expected=new TreeSet<>();
    for(int x=0;x<input.length;x++) for(int y=x+1;y<input.length;y++) for(int z=y+1;z<input.length;z++) {
        if(input[x]+input[y]+input[z]==0) { int[] row={input[x],input[y],input[z]}; Arrays.sort(row); expected.add(Arrays.toString(row)); }
    }
    List<List<Integer>> got=new Solution().threeSum(input); Set<String> actual=new TreeSet<>();
    for(List<Integer> row:got) actual.add(row.toString());
    eq(actual,expected); eq(got.size(),actual.size());
}
''',
42:r'''
Random rng=new Random(42);
for(int t=0;t<200;t++) {
    int[] a=new int[rng.nextInt(15)]; for(int j=0;j<a.length;j++) a[j]=rng.nextInt(10);
    int expected=0;
    for(int j=0;j<a.length;j++) {
        int lm=0,rm=0; for(int k=0;k<=j;k++) lm=Math.max(lm,a[k]);
        for(int k=j;k<a.length;k++) rm=Math.max(rm,a[k]);
        expected+=Math.min(lm,rm)-a[j];
    }
    eq(new Solution().trap(a),expected);
}
''',
3:r'''
Random rng=new Random(3);
for(int t=0;t<150;t++) {
    StringBuilder text=new StringBuilder(); int n=rng.nextInt(12);
    for(int j=0;j<n;j++) text.append((char)('a'+rng.nextInt(4)));
    String s=text.toString(); int expected=0;
    for(int l=0;l<n;l++) { Set<Character> chars=new HashSet<>(); for(int r=l;r<n;r++) { if(!chars.add(s.charAt(r))) break; expected=Math.max(expected,r-l+1); } }
    eq(new Solution().lengthOfLongestSubstring(s),expected);
}
''',
560:r'''
Random rng=new Random(560);
for(int t=0;t<200;t++) {
    int[] a=new int[rng.nextInt(12)]; for(int j=0;j<a.length;j++) a[j]=rng.nextInt(7)-3;
    int k=rng.nextInt(9)-4,expected=0;
    for(int l=0;l<a.length;l++) { int sum=0; for(int r=l;r<a.length;r++) { sum+=a[r]; if(sum==k) expected++; } }
    eq(new Solution().subarraySum(a,k),expected);
}
''',
239:r'''
Random rng=new Random(239);
for(int t=0;t<150;t++) {
    int[] a=new int[1+rng.nextInt(15)]; for(int j=0;j<a.length;j++) a[j]=rng.nextInt(21)-10;
    int k=1+rng.nextInt(a.length); int[] expected=new int[a.length-k+1];
    for(int l=0;l<expected.length;l++) { int best=Integer.MIN_VALUE; for(int j=l;j<l+k;j++) best=Math.max(best,a[j]); expected[l]=best; }
    eq(new Solution().maxSlidingWindow(a,k),expected);
}
''',
76:r'''
Random rng=new Random(76);
for(int t=0;t<150;t++) {
    StringBuilder sb=new StringBuilder(),tb=new StringBuilder();
    int n=1+rng.nextInt(9),m=1+rng.nextInt(4);
    for(int j=0;j<n;j++) sb.append((char)('A'+rng.nextInt(3)));
    for(int j=0;j<m;j++) tb.append((char)('A'+rng.nextInt(3)));
    String s=sb.toString(),target=tb.toString(); int shortest=Integer.MAX_VALUE;
    for(int l=0;l<n;l++) for(int r=l;r<n;r++) {
        int[] have=new int[3],need=new int[3];
        for(int j=l;j<=r;j++) have[s.charAt(j)-'A']++;
        for(char ch:target.toCharArray()) need[ch-'A']++;
        boolean ok=true; for(int j=0;j<3;j++) if(have[j]<need[j]) ok=false;
        if(ok) shortest=Math.min(shortest,r-l+1);
    }
    String got=new Solution().minWindow(s,target);
    eq(got.length(),shortest==Integer.MAX_VALUE?0:shortest);
    if(!got.isEmpty()) {
        eq(s.contains(got),true); int[] balance=new int[3];
        for(char ch:got.toCharArray()) balance[ch-'A']++;
        for(char ch:target.toCharArray()) balance[ch-'A']--;
        for(int x:balance) eq(x>=0,true);
    }
}
''',
41:r'''
Random rng=new Random(41);
for(int t=0;t<150;t++) {
    int[] a=new int[1+rng.nextInt(12)]; Set<Integer> seen=new HashSet<>();
    for(int j=0;j<a.length;j++) { a[j]=rng.nextInt(20)-5; seen.add(a[j]); }
    int expected=1; while(seen.contains(expected)) expected++;
    eq(new Solution().firstMissingPositive(a),expected);
}
''',
25:r'''
for(int n=1;n<=12;n++) for(int k=1;k<=n;k++) {
    int[] input=new int[n]; for(int j=0;j<n;j++) input[j]=j+1;
    int[] expected=input.clone();
    for(int start=0;start+k<=n;start+=k) for(int l=start,r=start+k-1;l<r;l++,r--) { int tmp=expected[l]; expected[l]=expected[r]; expected[r]=tmp; }
    eq(vals(new Solution().reverseKGroup(list(input),k)),Arrays.toString(expected));
}
''',
146:r'''
Random rng=new Random(146);
for(int capacity=1;capacity<=5;capacity++) {
    LRUCache actual=new LRUCache(capacity);
    LinkedHashMap<Integer,Integer> expected=new LinkedHashMap<>(16,0.75f,true);
    for(int t=0;t<300;t++) {
        int key=rng.nextInt(10);
        if(rng.nextBoolean()) {
            int value=rng.nextInt(100); actual.put(key,value); expected.put(key,value);
            if(expected.size()>capacity) expected.remove(expected.keySet().iterator().next());
        } else eq(actual.get(key),expected.getOrDefault(key,-1));
    }
}
''',
437:r'''
class Reference {
    int from(TreeNode node,long remaining) {
        if(node==null) return 0;
        return (remaining==node.val?1:0)+from(node.left,remaining-node.val)+from(node.right,remaining-node.val);
    }
    int all(TreeNode node,int target) {
        if(node==null) return 0;
        return from(node,target)+all(node.left,target)+all(node.right,target);
    }
}
Random rng=new Random(437); Reference ref=new Reference();
for(int t=0;t<120;t++) {
    Integer[] values=new Integer[1+rng.nextInt(15)]; for(int j=0;j<values.length;j++) values[j]=rng.nextInt(7)-3;
    TreeNode node=tree(values); int target=rng.nextInt(9)-4;
    eq(new Solution().pathSum(node,target),ref.all(node,target));
}
''',
4:r'''
Random rng=new Random(4);
for(int t=0;t<200;t++) {
    int m=rng.nextInt(8),n=1+rng.nextInt(8); int[] a=new int[m],b=new int[n],both=new int[m+n];
    for(int j=0;j<m;j++) a[j]=rng.nextInt(21)-10;
    for(int j=0;j<n;j++) b[j]=rng.nextInt(21)-10;
    Arrays.sort(a); Arrays.sort(b); System.arraycopy(a,0,both,0,m); System.arraycopy(b,0,both,m,n); Arrays.sort(both);
    double expected=(m+n)%2==1?both[(m+n)/2]:((double)both[(m+n)/2-1]+both[(m+n)/2])/2;
    eq(new Solution().findMedianSortedArrays(a,b),expected);
}
''',
84:r'''
Random rng=new Random(84);
for(int t=0;t<200;t++) {
    int[] a=new int[1+rng.nextInt(15)]; for(int j=0;j<a.length;j++) a[j]=rng.nextInt(10);
    int expected=0;
    for(int l=0;l<a.length;l++) { int low=Integer.MAX_VALUE; for(int r=l;r<a.length;r++) { low=Math.min(low,a[r]); expected=Math.max(expected,low*(r-l+1)); } }
    eq(new Solution().largestRectangleArea(a),expected);
}
''',
295:r'''
MedianFinder stream=new MedianFinder(); List<Integer> sorted=new ArrayList<>(); Random rng=new Random(295);
for(int t=0;t<250;t++) {
    int x=rng.nextInt(201)-100; stream.addNum(x); sorted.add(x); Collections.sort(sorted);
    int n=sorted.size(); double expected=n%2==1?sorted.get(n/2):((double)sorted.get(n/2-1)+sorted.get(n/2))/2;
    eq(stream.findMedian(),expected);
}
''',
300:r'''
Random rng=new Random(300);
for(int t=0;t<100;t++) {
    int[] a=new int[1+rng.nextInt(10)]; for(int j=0;j<a.length;j++) a[j]=rng.nextInt(11)-5;
    int expected=0;
    for(int mask=0;mask<(1<<a.length);mask++) {
        boolean ok=true,first=true; int last=0,size=0;
        for(int j=0;j<a.length;j++) if((mask&(1<<j))!=0) { if(!first && a[j]<=last) ok=false; first=false; last=a[j]; size++; }
        if(ok) expected=Math.max(expected,size);
    }
    eq(new Solution().lengthOfLIS(a),expected);
}
''',
152:r'''
Random rng=new Random(152);
for(int t=0;t<150;t++) {
    int[] a=new int[1+rng.nextInt(9)]; for(int j=0;j<a.length;j++) a[j]=rng.nextInt(7)-3;
    int expected=Integer.MIN_VALUE;
    for(int l=0;l<a.length;l++) { int product=1; for(int r=l;r<a.length;r++) { product*=a[r]; expected=Math.max(expected,product); } }
    eq(new Solution().maxProduct(a),expected);
}
''',
416:r'''
Random rng=new Random(416);
for(int t=0;t<120;t++) {
    int[] a=new int[1+rng.nextInt(10)]; int sum=0; for(int j=0;j<a.length;j++) { a[j]=1+rng.nextInt(8); sum+=a[j]; }
    boolean expected=false;
    for(int mask=0;mask<(1<<a.length);mask++) { int part=0; for(int j=0;j<a.length;j++) if((mask&(1<<j))!=0) part+=a[j]; if(part*2==sum) expected=true; }
    eq(new Solution().canPartition(a),expected);
}
''',
32:r'''
for(int n=0;n<=9;n++) for(int mask=0;mask<(1<<n);mask++) {
    StringBuilder sb=new StringBuilder(); for(int j=0;j<n;j++) sb.append((mask&(1<<j))==0?'(':')');
    String s=sb.toString(); int expected=0;
    for(int l=0;l<n;l++) { int balance=0; for(int r=l;r<n;r++) { balance+=s.charAt(r)=='('?1:-1; if(balance<0) break; if(balance==0) expected=Math.max(expected,r-l+1); } }
    eq(new Solution().longestValidParentheses(s),expected);
}
''',
31:r'''
class Permutations {
    Set<String> seen=new TreeSet<>(); List<int[]> all=new ArrayList<>();
    void generate(int[] a,int start) {
        if(start==a.length) { if(seen.add(Arrays.toString(a))) all.add(a.clone()); return; }
        for(int j=start;j<a.length;j++) {
            int tmp=a[start]; a[start]=a[j]; a[j]=tmp;
            generate(a,start+1);
            tmp=a[start]; a[start]=a[j]; a[j]=tmp;
        }
    }
}
for(int[] base:new int[][]{{1},{1,2,3},{1,1,2},{1,2,2,3}}) {
    Permutations p=new Permutations(); p.generate(base,0);
    p.all.sort((x,y)->{ for(int j=0;j<x.length;j++) if(x[j]!=y[j]) return Integer.compare(x[j],y[j]); return 0; });
    for(int j=0;j<p.all.size();j++) { int[] got=p.all.get(j).clone(); new Solution().nextPermutation(got); eq(got,p.all.get((j+1)%p.all.size())); }
}
'''
}
