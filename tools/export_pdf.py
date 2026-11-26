"""打印同一Markdown内容为全文PDF，嵌入中文字体并验证题目覆盖。"""
import html,json,pathlib,re,shutil,subprocess
import markdown
from pygments.formatters import HtmlFormatter
from pypdf import PdfReader
from playwright.sync_api import sync_playwright
from browser_utils import launch_browser
from site_build import diagram_replace,protect_generics,PDF_NAME

ROOT=pathlib.Path(__file__).resolve().parents[1]
PRINT_CSS='''
@page { size: A4; margin: 17mm 15mm 18mm; }
* { box-sizing: border-box; }
html { font-size: 10pt; }
body { margin: 0; color: #172033; font-family: "Microsoft YaHei", "PingFang SC", sans-serif; line-height: 1.72; }
h1 { font-size: 21pt; line-height: 1.4; color: #283c78; break-after: avoid; margin: 0 0 7mm; }
h1:not(:first-child) { break-before: page; }
h2 { font-size: 15pt; line-height: 1.5; margin: 6mm 0 3mm; break-after: avoid; }
h3 { font-size: 11.5pt; margin: 5mm 0 2mm; break-after: avoid; }
p, li { orphans: 3; widows: 3; overflow-wrap: anywhere; }
a { color: #214f91; text-decoration: none; }
code { font-family: Consolas, "Microsoft YaHei", monospace; font-size: 8.7pt; }
pre { white-space: pre-wrap; overflow-wrap: anywhere; word-break: normal; line-height: 1.55; margin: 3mm 0; padding: 3.5mm; border: .3mm solid #d8deea; border-radius: 1.5mm; background: #f5f7fb; }
pre code { white-space: pre-wrap; overflow-wrap: anywhere; }
.highlight { background: transparent; break-inside: avoid; }
.code-section { break-inside: avoid; }
.highlight .c, .highlight .c1, .highlight .cm { color: #426339; }
table { width: 100%; table-layout: fixed; border-collapse: collapse; margin: 3mm 0; font-size: 8.2pt; }
th { background: #edf1f8; text-align: left; }
td,th { border: .2mm solid #ccd5e3; padding: 1.6mm 2mm; overflow-wrap: anywhere; word-break: break-word; vertical-align: top; }
thead { display: table-header-group; }
tr { break-inside: avoid; }
img { display: block; max-width: 100%; max-height: 115mm; margin: 4mm auto; }
p:has(+ p > img) { break-after: avoid; }
hr { margin-block: 6mm; border: 0; border-top: .2mm solid #cdd6e6; }
'''

def main():
    raw=(ROOT/'Hot100-Java-完整学习手册.md').read_text(encoding='utf-8')
    raw=re.sub(r'\n---\s*\Z','\n',raw) # 避免末尾分隔线单独挤出一张空白页
    # 图片使用本地绝对URI，PDF与网站来自同一份题解和SVG。
    raw=diagram_replace(raw,(ROOT/'web/diagrams').as_uri()+'/')
    body=markdown.markdown(protect_generics(raw),extensions=['tables','fenced_code','codehilite','toc'],
        extension_configs={'codehilite':{'guess_lang':False,'css_class':'highlight'}})
    body=re.sub(r'(<h3\b[^>]*>4\..*?)(?=<h3\b[^>]*>5\.)',r'<section class="code-section">\1</section>',body,flags=re.S)
    css=HtmlFormatter(style='friendly').get_style_defs('.highlight')+'\n'+PRINT_CSS
    document='<!doctype html><html lang="zh-CN"><meta charset="utf-8"><title>LeetCode Hot 100 Java 完整学习手册</title><style>'+css+'</style><body>'+body+'</body></html>'
    work=ROOT/'tmp/pdfs'; work.mkdir(parents=True,exist_ok=True)
    path=work/'print.html'; path.write_text(document,encoding='utf-8')
    output=ROOT/'output/pdf'/PDF_NAME; output.parent.mkdir(parents=True,exist_ok=True)
    with sync_playwright() as p:
        browser=launch_browser(p); page=browser.new_page()
        page.goto(path.as_uri(),wait_until='networkidle')
        page.evaluate('document.fonts.ready')
        page.emulate_media(media='print')
        metrics=page.evaluate('''() => ({missingImages:[...document.images].filter(i=>!i.complete || i.naturalWidth===0).length,
           overflowBlocks:[...document.querySelectorAll('pre')].filter(e=>e.scrollWidth>e.clientWidth+1).length})''')
        if metrics['missingImages'] or metrics['overflowBlocks']: raise RuntimeError(f'打印布局异常：{metrics}')
        page.pdf(path=str(output),format='A4',print_background=True,prefer_css_page_size=True,
                 display_header_footer=True,header_template='<span></span>',
                 footer_template='<div style="width:100%;font-size:8px;text-align:center;color:#667085">Java Hot 100 · <span class="pageNumber"></span> / <span class="totalPages"></span></div>',
                 outline=True,tagged=True)
        browser.close()
    reader=PdfReader(output); pages=[p.extract_text() or '' for p in reader.pages]; text='\n'.join(pages)
    manifest=json.loads((ROOT/'sources/manifest.json').read_text(encoding='utf-8'))
    coverage={q['id']: next((i+1 for i,t in enumerate(pages) if re.search(fr'{q["id"]}\s*\.\s*{re.escape(q["name"])}',t)),None) for q in manifest}
    absent=[i for i,n in coverage.items() if n is None]
    if absent: raise RuntimeError(f'PDF缺少题目标题：{absent}')
    if '\ufffd' in text: raise RuntimeError('PDF出现替代字符，需检查中文字体')
    # 优先按环境可用的Poppler或PyMuPDF渲染，抽查封面、代码、图、末题。
    sample=sorted(set([1,coverage[1],coverage[1]+1,coverage[76],coverage[76]+1,coverage[51],coverage[51]+1,coverage[72],coverage[72]+1,coverage[287],len(pages)]))
    rendered=[]
    try:
        import pymupdf
        doc=pymupdf.open(output)
        for number in sample:
            png=work/f'page-{number:03d}.png'
            doc[number-1].get_pixmap(matrix=pymupdf.Matrix(1.25,1.25)).save(png)
            rendered.append(str(png.relative_to(ROOT)))
        doc.close()
    except ImportError:
        renderer=shutil.which('pdftoppm')
        if not renderer: raise RuntimeError('缺少PDF渲染工具：需要PyMuPDF或Poppler以完成视觉检查。')
        for number in sample:
            prefix=work/f'page-{number:03d}'
            subprocess.run([renderer,'-f',str(number),'-l',str(number),'-scale-to','1400','-singlefile','-png',str(output),str(prefix)],check=True,capture_output=True)
            rendered.append(str(prefix.with_suffix('.png').relative_to(ROOT)))
    def count_outline(items): return sum(count_outline(x) if isinstance(x,list) else 1 for x in items)
    report=dict(file=str(output.relative_to(ROOT)),pages=len(pages),bytes=output.stat().st_size,
        covered_problem_titles=len(coverage),missing_titles=absent,text_selectable=True,
        replacement_characters=text.count('\ufffd'),bookmarks=count_outline(reader.outline),print_metrics=metrics,
        sample_renders=rendered,visual_review='待人工查看抽样PNG',limitations='未逐页人工审阅；手机建议使用可缩放的PDF阅读器。')
    (ROOT/'reports/pdf-check.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps(report,ensure_ascii=False,indent=2))
if __name__=='__main__': main()
