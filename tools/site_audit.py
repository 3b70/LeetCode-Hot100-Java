"""验证整个HTML站点：链接、题目覆盖、原样源码、翻页和离线资源。"""
import hashlib,json,pathlib,re
from html.parser import HTMLParser
from urllib.parse import unquote,urlsplit

ROOT=pathlib.Path(__file__).resolve().parents[1]
SITE=ROOT/'site'
class Page(HTMLParser):
    def __init__(self,text):
        super().__init__(convert_charrefs=True)
        self.links=[]; self.ids=set(); self.codes=[]; self.pre=0; self.code=0; self.buf=[]; self.text=[]
        self.feed(text)
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if a.get('id'): self.ids.add(a['id'])
        for key in ['href','src']:
            if key in a: self.links.append((tag,a[key],a))
        if tag=='pre': self.pre+=1
        if tag=='code' and self.pre: self.code+=1; self.buf=[]
    def handle_endtag(self,tag):
        if tag=='code' and self.code:
            self.codes.append(''.join(self.buf)); self.code-=1
        if tag=='pre': self.pre-=1
    def handle_data(self,data):
        self.text.append(data)
        if self.code: self.buf.append(data)

def main():
    errors=[]; checked=0; external_assets=[]
    pages={path.resolve():Page(path.read_text(encoding='utf-8')) for path in SITE.rglob('*.html')}
    for path,page in pages.items():
        for tag,url,attrs in page.links:
            u=urlsplit(url)
            if u.scheme or u.netloc:
                if tag in ['script','img','link'] and attrs.get('rel')!='canonical': external_assets.append(url)
                continue
            if not u.path and not u.fragment: continue
            dest=(path.parent/unquote(u.path)).resolve() if u.path else path
            if dest.is_dir(): dest=dest/'index.html'
            checked+=1
            if not dest.exists(): errors.append(f'{path.relative_to(SITE)} → {url}不存在'); continue
            if u.fragment and dest in pages and unquote(u.fragment) not in pages[dest].ids:
                errors.append(f'{path.relative_to(SITE)} → {url}锚点不存在')
    manifest=json.loads((ROOT/'sources/site-manifest.json').read_text(encoding='utf-8'))
    assert len(manifest)==100
    for index,q in enumerate(manifest):
        path=SITE/pathlib.Path(q['page']).with_suffix('.html'); page=pages.get(path.resolve())
        if page is None: errors.append(f'{q["id"]}缺独立HTML'); continue
        source=(ROOT/q['source']).read_text(encoding='utf-8').strip()
        if source not in [x.strip() for x in page.codes]: errors.append(f'{q["id"]}网页源码与.java不一致')
        download=SITE/'downloads'/q['source']
        if not download.exists() or download.read_bytes()!=(ROOT/q['source']).read_bytes(): errors.append(f'{q["id"]}下载源码不一致')
        if q['url'] not in [url for _,url,_ in page.links]: errors.append(f'{q["id"]}缺官方链接')
        adjacent={a['rel']:url for tag,url,a in page.links if tag=='a' and a.get('rel') in ['prev','next']}
        for direction,neighbor in [('prev',index-1),('next',index+1)]:
            expected=pathlib.Path(manifest[neighbor]['page']).with_suffix('.html').name if 0<=neighbor<100 else None
            if adjacent.get(direction)!=expected: errors.append(f'{q["id"]} {direction}导航异常')
    search=json.loads((SITE/'search/search_index.json').read_text(encoding='utf-8'))
    indexed={d['location'].split('#')[0] for d in search['docs']}
    for q in manifest:
        if str(pathlib.Path(q['page']).with_suffix('.html')).replace('\\','/') not in indexed: errors.append(f'{q["id"]}未入搜索索引')
    if external_assets: errors.append(f'存在外部运行资源：{sorted(set(external_assets))}')
    pdf=ROOT/'output/pdf/Hot100-Java-完整学习手册.pdf'
    if pdf.exists():
        built_pdf=SITE/'downloads'/pdf.name
        if not built_pdf.exists() or built_pdf.read_bytes()!=pdf.read_bytes(): errors.append('网站下载的PDF不是最新导出版')
    report=dict(problem_pages=len(manifest),html_pages=len(pages),checked_local_links=checked,
        search_documents=len(search['docs']),all_problem_pages_searchable=not any('未入搜索' in s for s in errors),
        independent_java_files=len(list((SITE/'downloads/solutions').rglob('*.java'))),external_runtime_assets=sorted(set(external_assets)),
        pdf_download=(SITE/'downloads/Hot100-Java-完整学习手册.pdf').exists(),errors=errors)
    (ROOT/'reports/site-audit.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps(report,ensure_ascii=False,indent=2))
    if errors: raise SystemExit(1)
if __name__=='__main__': main()
