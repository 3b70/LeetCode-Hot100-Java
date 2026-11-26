"""从已验证的Markdown章节生成网站页；不修改Java源码、不联网、不发布。"""
import html,json,pathlib,re,shutil,zipfile,os,hashlib
from public_files import markdown_files

ROOT=pathlib.Path(__file__).resolve().parents[1]
DOCS=ROOT/'docs'
PDF_NAME='Hot100-Java-完整学习手册.pdf'
DIFFICULTY={'简单':0,'中等':1,'困难':2}

def write(path,text):
    p=DOCS/path; p.parent.mkdir(parents=True,exist_ok=True); p.write_text(text,encoding='utf-8')

def protect_generics(text):
    # Markdown把Map<K,V>中的类型参数误识别为HTML时会吞字；仅转义正文，保留源码原样。
    parts=re.split(r'(```.*?```|`[^`\n]*`)',text,flags=re.S)
    for i in range(0,len(parts),2):
        parts[i]=re.sub(r'<[A-Z][A-Za-z0-9_, ?\[\]<>]*>',lambda m:html.escape(m.group(0)),parts[i])
    return ''.join(parts)

def groups(manifest):
    return [sorted([q for q in manifest if q['chapter']==i],key=lambda q:DIFFICULTY[q['difficulty']]) for i in range(1,18)]

def diagram_replace(text,relative):
    # 若未预渲染，显式保留原图源码，避免悄悄遗漏讲解。
    def replace(m):
        qid=m.group(1); body=m.group(2)
        svg=ROOT/'web/diagrams'/f'{int(qid):04d}.svg'
        if '```mermaid' in body:
            if not svg.exists(): raise RuntimeError(f'缺少{svg}，先运行tools/render_diagrams.py')
            body=re.sub(r'```mermaid\n.*?\n```',f'![算法执行流程]({relative}{svg.name})',body,flags=re.S)
        return f'<a id="p{qid}"></a>'+body
    # 文档中每题的显式锚点作为图对应关系；尾部由下一题或文本末尾界定。
    return re.sub(r'<a id="p(\d+)"></a>(.*?)(?=<a id="p\d+"></a>|\Z)',replace,text,flags=re.S)

def problem_body(chapter,q):
    m=re.search(fr'<a id="p{q["id"]}"></a>\s*(.*?)(?=\n---\n)',chapter,re.S)
    if not m: raise ValueError(f'章节缺少题目 {q["id"]}')
    body=m.group(1).strip()
    body=re.sub(r'^## ', '# ',body,count=1,flags=re.M)
    body=re.sub(r'^### ', '## ',body,flags=re.M)
    body=body.replace('../Java基础知识附录.md#java-','../appendices/java-basics.md#java-')
    body=re.sub(r'基础章节。','基础章节。',body)
    svg=ROOT/'web/diagrams'/f'{q["id"]:04d}.svg'
    if '```mermaid' in body:
        if not svg.exists(): raise ValueError(f'先渲染流程图：{q["id"]}')
        body=re.sub(r'```mermaid\n.*?\n```',f'![算法执行流程](../assets/diagrams/{svg.name})',body,flags=re.S)
    # 在不改变题解正文的前提下，独立命名网站标题，便于目录与搜索。
    return protect_generics(body)

def pager(ordered,index):
    q=ordered[index]
    def link(item,label):
        return f'<a href="{item["id"]:04d}-{item["slug"]}.html" rel="{"prev" if label=="上一题" else "next"}">{label}：{item["id"]} {html.escape(item["name"])}</a>'
    prev=link(ordered[index-1],'上一题') if index else '<span>这是第一题</span>'
    nxt=link(ordered[index+1],'下一题') if index+1<len(ordered) else '<span>已到最后一题</span>'
    return f'<nav class="problem-pager" aria-label="题目翻页">{prev}{nxt}</nav>'

def table(items,prefix=''):
    out=['|题号|题目|难度|','|---|---|---|']
    out.extend(f'|{q["id"]}|[{q["name"]}]({prefix}{q["id"]:04d}-{q["slug"]}.md)|{q["difficulty"]}|' for q in items)
    return '\n'.join(out)

def main():
    manifest=json.loads((ROOT/'sources/manifest.json').read_text(encoding='utf-8'))
    assert len(manifest)==len({q['id'] for q in manifest})==100
    tests={q['id']:q for q in json.loads((ROOT/'reports/test-results.json').read_text(encoding='utf-8'))}
    if not all(tests.get(q['id'],{}).get('local_pass') for q in manifest):
        raise RuntimeError('有题目尚未通过本地测试，请先处理。')
    DOCS.mkdir(exist_ok=True)
    grouped=groups(manifest); ordered=[q for g in grouped for q in g]
    nav=[{'首页与全部题目':'index.md'},{'初学者学习顺序':'learning-order.md'},
         {'Java基础知识':'appendices/java-basics.md'},{'Java API速查':'appendices/java-api.md'},
         {'算法与数据结构':'appendices/algorithms.md'},{'手机与电脑阅读':'reading.md'},{'本地验证记录':'validation.md'}]
    page_paths={q['id']:f'problems/{q["id"]:04d}-{q["slug"]}.md' for q in manifest}
    for index,q in enumerate(ordered):
        chapter=(ROOT/f'chapters/{q["chapter"]:02d}-{q["category"]}.md').read_text(encoding='utf-8')
        body=problem_body(chapter,q)
        title=f'{q["id"]} {q["name"]}'
        desc=f'{q["category"]} · {q["difficulty"]} · Java 17 · 中文注释与示例执行'
        header=f'---\ntitle: {title}\ndescription: {desc}\n---\n\n'
        first,rest=body.split('\n',1)
        links=f'[官方力扣题目]({q["url"]}) · [下载本题Java源码](../downloads/{q["source"]})\n'
        write(page_paths[q['id']],header+first+'\n\n'+links+'\n'+pager(ordered,index)+'\n\n'+rest+'\n\n'+pager(ordered,index)+'\n')
        target=DOCS/'downloads'/q['source']; target.parent.mkdir(parents=True,exist_ok=True)
        shutil.copyfile(ROOT/q['source'],target)
    for c,g in enumerate(grouped,1):
        name=g[0]['category']; folder=f'topics/{c:02d}'
        overview=f'{folder}.md'
        write(overview,f'# {c:02d} {name}\n\n共 {len(g)} 题。简单、中等、困难依次排列，同难度保留官方顺序。\n\n'+table(g,'../problems/')+'\n')
        nav.append({f'{c:02d} {name}':[{'专题概览':overview}]+[{f'{q["id"]} {q["name"]}':page_paths[q['id']]} for q in g]})
    java=(ROOT/'Java基础知识附录.md').read_text(encoding='utf-8')
    write('appendices/java-basics.md',protect_generics(java))
    api=java.split('## Java 常用 API 速查表',1)[1].split('## 力扣提交与本地运行',1)[0]
    write('appendices/java-api.md',protect_generics('# Java 常用 API 速查表\n\n[返回Java基础知识](java-basics.md)\n\n'+api))
    write('appendices/algorithms.md',protect_generics((ROOT/'算法知识附录.md').read_text(encoding='utf-8')))
    plan=(ROOT/'初学者推荐刷题顺序.md').read_text(encoding='utf-8')
    for q in manifest: plan=plan.replace(f']({q["url"]})',f']({page_paths[q["id"]]})')
    write('learning-order.md',plan)
    reading=(ROOT/'手机与电脑阅读说明.md').read_text(encoding='utf-8')
    reading=reading.replace('(output/pdf/'+PDF_NAME+')','(downloads/'+PDF_NAME+')').replace('(完整性检查报告.md)','(validation.md)')
    write('reading.md',reading)
    report=(ROOT/'完整性检查报告.md').read_text(encoding='utf-8')
    write('validation.md',report)
    write('assets/favicon.svg','<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><rect width="64" height="64" rx="12" fill="#3f51b5"/><text x="32" y="41" text-anchor="middle" fill="white" font-size="26" font-family="sans-serif">100</text></svg>')
    shutil.copytree(ROOT/'web/stylesheets',DOCS/'stylesheets',dirs_exist_ok=True)
    shutil.copytree(ROOT/'web/javascripts',DOCS/'javascripts',dirs_exist_ok=True)
    shutil.copytree(ROOT/'web/diagrams',DOCS/'assets/diagrams',dirs_exist_ok=True)
    shutil.copytree(ROOT/'web/assets',DOCS/'assets',dirs_exist_ok=True)
    download=DOCS/'downloads'; download.mkdir(exist_ok=True)
    with zipfile.ZipFile(download/'hot100-java-sources.zip','w',zipfile.ZIP_DEFLATED) as z:
        for q in manifest: z.write(ROOT/q['source'],q['source'])
    with zipfile.ZipFile(download/'hot100-markdown.zip','w',zipfile.ZIP_DEFLATED) as z:
        for path in markdown_files():
            z.write(path,path.relative_to(ROOT).as_posix())
    pdf=ROOT/'output/pdf'/PDF_NAME
    downloads='[下载100份Java源码](downloads/hot100-java-sources.zip) · [下载Markdown原稿](downloads/hot100-markdown.zip)'
    if pdf.exists():
        shutil.copyfile(pdf,download/PDF_NAME)
        downloads=f'[下载完整PDF](downloads/{PDF_NAME}) · '+downloads
    else:
        reading=reading.replace(f'[PDF 文件](downloads/{PDF_NAME})','PDF 文件（此构建尚未导出，请先运行 tools/export_pdf.py）')
        write('reading.md',reading)
    home='# LeetCode Hot 100 Java 学习手册\n\n100 道题，从 Java 语法、集合到数据结构与算法。每题含完整中文注释代码、API解释、手动执行和易错点。\n\n'
    home+='<div class="learning-entry" markdown="1">\n\n**第一次学习，从这里开始**\n\n[Java基础知识](appendices/java-basics.md) · [七阶段推荐顺序与30/60天计划](learning-order.md) · [算法知识附录](appendices/algorithms.md) · [Java常用API速查](appendices/java-api.md)\n\n</div>\n\n'
    home+='搜索框可输入题号（如 `206`）、中文题名（如 `两数之和`）、Java知识点（如 `HashMap`、`递归`）。手机打开左上角菜单选择专题。右上角切换浅色/深色。\n\n'
    home+='## 离线资料\n\n'+downloads+'\n\n[手机与电脑阅读说明](reading.md) · [本地验证记录](validation.md)\n\n'
    home+='核对官方题单日期：2026-11-25。17个专题、100个不同题号；100题已通过Java17目标编译和本地测试，未进行力扣官方提交。\n\n## 17个算法专题\n\n'
    home+=' · '.join(f'[{c:02d} {g[0]["category"]}](topics/{c:02d}.md)' for c,g in enumerate(grouped,1))+'\n\n## Hot 100 全部题目目录\n\n'
    for c,g in enumerate(grouped,1): home+=f'### {c:02d} {g[0]["category"]}\n\n'+table(g,'problems/')+'\n\n'
    write('index.md',home)
    write('build-info.json',json.dumps(dict(git_sha=os.environ.get('GITHUB_SHA'),
        problems=100,topics=17,manifest_sha256=hashlib.sha256((ROOT/'sources/manifest.json').read_bytes()).hexdigest()),indent=2))
    (ROOT/'site-nav.json').write_text(json.dumps(nav,ensure_ascii=False,indent=2),encoding='utf-8')
    (ROOT/'sources/site-manifest.json').write_text(json.dumps([dict(id=q['id'],page=page_paths[q['id']],source=q['source'],url=q['url']) for q in ordered],ensure_ascii=False,indent=2),encoding='utf-8')
    print('Generated 100 problem pages, 17 topic pages, appendices, navigation and downloads.')
if __name__=='__main__': main()
