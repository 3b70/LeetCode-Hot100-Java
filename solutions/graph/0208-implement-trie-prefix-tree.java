class Trie {
    private final Trie[] children=new Trie[26];
    private boolean end;
    public Trie() {}
    public void insert(String word) {
        Trie node=this;
        for(char c:word.toCharArray()) {
            int i=c-'a';
            if(node.children[i]==null) node.children[i]=new Trie();
            node=node.children[i];
        }
        node.end=true; // 单独标记完整单词的终点
    }
    public boolean search(String word) { Trie node=walk(word); return node!=null && node.end; }
    public boolean startsWith(String prefix) { return walk(prefix)!=null; }
    private Trie walk(String s) {
        Trie node=this;
        for(char c:s.toCharArray()) {
            node=node.children[c-'a'];
            if(node==null) return null; // 某条边不存在就无法匹配
        }
        return node;
    }
}
