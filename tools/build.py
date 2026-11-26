"""从官方清单、题解数据、附录和测试记录生成文件，禁止手改生成章节。"""
import json,pathlib,re,hashlib
from content import P
import arrays_content,lists_content,trees_content,search_content,binary_content,stack_heap_content,dp_content,final_content
from extra_checks import EXTRA

ROOT=pathlib.Path(__file__).resolve().parents[1]
FOLDERS=['hash','two-pointers','sliding-window','substring','array','matrix','linked-list','binary-tree','graph','backtracking','binary-search','stack','heap','greedy','dp','multidimensional-dp','tricks']
def write(name,text):
    p=ROOT/name; p.parent.mkdir(parents=True,exist_ok=True); p.write_text(text,encoding='utf-8')

def emit_sources():
    official=json.loads((ROOT/'sources/problems.json').read_text(encoding='utf-8'))
    assert len(official)==len(P)==100 and {q['id'] for q in official}==set(P)
    manifest=[]
    for q in official:
        p=P[q['id']]; path=f"solutions/{FOLDERS[q['chapter']-1]}/{q['id']:04d}-{q['slug']}.java"
        assert '//' in p['code'] and p['tests'] and all(p.values())
        write(path,p['code']+'\n')
        tests=p['tests'].replace('norm(new Solution().groupAnagrams','normGroups(new Solution().groupAnagrams')+'\n'+EXTRA.get(q['id'],'')
        manifest.append(dict(**q,source=path,tests=tests,sha256=hashlib.sha256((ROOT/path).read_bytes()).hexdigest()))
    write('sources/manifest.json',json.dumps(manifest,ensure_ascii=False,indent=2)); return manifest

if __name__=='__main__':
    manifest=emit_sources()
    # 后面的文档生成函数由本文件定义后再调用；--sources仅生成代码以便并行验证。
    import sys
    if '--sources' not in sys.argv:
        from render import render
        render(ROOT,manifest,P)
