"""把原稿中的8张Mermaid图预渲染为SVG；网站运行时不再加载Mermaid。"""
import hashlib,json,pathlib,re,urllib.request
from playwright.sync_api import sync_playwright
from browser_utils import launch_browser

ROOT=pathlib.Path(__file__).resolve().parents[1]
URL='https://cdn.jsdelivr.net/npm/mermaid@10.9.3/dist/mermaid.min.js'
def main():
    vendor=ROOT/'tools/vendor/mermaid.min.js'; vendor.parent.mkdir(exist_ok=True)
    if not vendor.exists():
        with urllib.request.urlopen(URL,timeout=60) as response: vendor.write_bytes(response.read())
    out=ROOT/'web/diagrams'; out.mkdir(parents=True,exist_ok=True)
    diagrams=[]
    for chapter in sorted((ROOT/'chapters').glob('*.md')):
        text=chapter.read_text(encoding='utf-8')
        for qid,body in re.findall(r'<a id="p(\d+)"></a>(.*?)(?=\n---\n)',text,re.S):
            m=re.search(r'```mermaid\n(.*?)\n```',body,re.S)
            if m: diagrams.append((int(qid),m.group(1)))
    with sync_playwright() as p:
        browser=launch_browser(p); page=browser.new_page()
        page.set_content('<html lang="zh-CN"><meta charset="utf-8"><body></body></html>')
        page.add_script_tag(path=str(vendor))
        page.evaluate('mermaid.initialize({startOnLoad:false,securityLevel:"strict",theme:"neutral",fontFamily:"Microsoft YaHei, sans-serif",flowchart:{htmlLabels:false,curve:"linear"}})')
        for qid,source in diagrams:
            svg=page.evaluate('async ({source,id}) => (await mermaid.render("flow"+id,source)).svg',dict(source=source,id=qid))
            (out/f'{qid:04d}.svg').write_text(svg,encoding='utf-8')
        browser.close()
    (out/'provenance.json').write_text(json.dumps(dict(mermaid_version='10.9.3',source=URL,
        bundle_sha256=hashlib.sha256(vendor.read_bytes()).hexdigest(),problem_ids=[i for i,_ in diagrams]),ensure_ascii=False,indent=2),encoding='utf-8')
    print(f'Pre-rendered {len(diagrams)} diagrams, no runtime CDN dependency.')
if __name__=='__main__': main()
