"""离线、独立审计：官方快照→清单→源码→测试记录→章节→主手册。"""
import hashlib,json,pathlib,re
from urllib.parse import unquote
from verify import FIXTURES

ROOT=pathlib.Path(__file__).resolve().parents[1]
def main():
    errors=[]; optional_missing=[]
    def check(condition,message):
        if not condition: errors.append(message)
    official=json.loads((ROOT/'sources/official-data.json').read_text(encoding='utf-8'))
    html=(ROOT/'sources/official-page.html').read_text(encoding='utf-8')
    embedded=json.loads(re.search(r'<script id="__NEXT_DATA__" type="application/json">(.*?)</script>',html).group(1))
    check(embedded==official,'HTML与已保存嵌入数据不同')
    groups=official['props']['pageProps']['dehydratedState']['queries'][0]['state']['data']['studyPlanV2Detail']['planSubGroups']
    check(len(groups)==17,'官方分类数量不是17')
    reference={int(q['questionFrontendId']):(q,g['name'],i) for i,g in enumerate(groups,1) for q in g['questions']}
    check(sum(len(g['questions']) for g in groups)==len(reference)==100,'官方数量/唯一性异常')
    manifest=json.loads((ROOT/'sources/manifest.json').read_text(encoding='utf-8'))
    extracted=json.loads((ROOT/'sources/problems.json').read_text(encoding='utf-8'))
    check(len(manifest)==100 and len({q['id'] for q in manifest})==100,'manifest数量或唯一性异常')
    for key in extracted[0]:
        check([q[key] for q in manifest]==[q[key] for q in extracted],f'清单字段{key}不一致')
    results=json.loads((ROOT/'reports/test-results.json').read_text(encoding='utf-8'))
    check(len(results)==len({r['id'] for r in results})==100,'测试记录数量或唯一性异常')
    by_id={r['id']:r for r in results}
    full=(ROOT/'Hot100-Java-完整学习手册.md').read_text(encoding='utf-8')
    check(len(re.findall(r'<a id="p\d+"></a>',full))==100,'主手册题解不是100')
    code_blocks=re.findall(r'```java\n(.*?)\n```',full,re.S)
    chapters=list((ROOT/'chapters').glob('*.md'))
    check(len(chapters)==17,'章节不是17个')
    check(len(list((ROOT/'solutions').rglob('*.java')))==100,'源码不是100个')
    check(len(list((ROOT/'tests').glob('*.java')))==100,'独立测试不是100个')
    for q in manifest:
        i=q['id']; oq,category,chapter=reference[i]
        check(q['name']==oq['translatedTitle'] and q['category']==category and q['chapter']==chapter,f'{i}官方名称/分类不符')
        check(q['slug']==oq['titleSlug'] and q['difficulty']=={'EASY':'简单','MEDIUM':'中等','HARD':'困难'}[oq['difficulty']],f'{i}官方链接/难度不符')
        source=(ROOT/q['source']).read_text(encoding='utf-8'); test=ROOT/'tests'/f'{i:04d}-Test.java'
        r=by_id.get(i,{})
        check(hashlib.sha256((ROOT/q['source']).read_bytes()).hexdigest()==q['sha256']==r.get('source_sha256'),f'{i}源码哈希/验证版本不一致')
        check(source.strip() in code_blocks,f'{i}主手册缺对应完整源码')
        check(test.read_text(encoding='utf-8')==FIXTURES.replace('// TEST_BODY',q['tests']),f'{i}测试源与清单不一致')
        check(hashlib.sha256(test.read_bytes()).hexdigest()==r.get('test_sha256'),f'{i}测试记录对应的用例已变化')
        check(r.get('compiled') and r.get('local_pass') and not r.get('official_pass'),f'{i}验证状态异常')
        check(bool(re.search(r'//[^\n]*[\u4e00-\u9fff]',source)),f'{i}没有中文行注释')
        chapter_text=(ROOT/f'chapters/{chapter:02d}-{category}.md').read_text(encoding='utf-8')
        check(source.strip() in re.findall(r'```java\n(.*?)\n```',chapter_text,re.S),f'{i}章节源码不匹配')
        match=re.search(fr'<a id="p{i}"></a>(.*?)(?=\n---\n)',chapter_text,re.S)
        check(match is not None,f'{i}章节缺题解')
        if match:
            for n in range(1,10): check(len(re.findall(fr'^### {n}\.',match[1],re.M))==1,f'{i}第{n}部分缺失/重复')
    # 链接只验证本地目标存在及显式锚点，不发起不必要的100次网络请求。
    for md in list(ROOT.glob('*.md'))+list((ROOT/'chapters').glob('*.md')):
        text=md.read_text(encoding='utf-8')
        check(text.count('```')%2==0,f'{md.name}代码围栏不成对')
        for url in re.findall(r'\]\(([^)]+)\)',text):
            if re.match(r'^[a-z]+:',url): continue
            target,_,anchor=url.partition('#')
            dest=(md.parent/unquote(target)) if target else md
            if not dest.exists() and target.split('/')[0] in ['site','output']:
                optional_missing.append(target); continue # Java源稿审计与可选网站/PDF产物审计分开
            check(dest.exists(),f'{md.name}死链接：{url}')
            if dest.exists() and anchor and re.match(r'(p\d+|java-\d+)$',anchor):
                check(f'id="{anchor}"' in dest.read_text(encoding='utf-8'),f'{md.name}锚点不存在：{url}')
    report=dict(date='2026-11-25',official_snapshot_sha256=hashlib.sha256((ROOT/'sources/official-page.html').read_bytes()).hexdigest(),
                unique_problems=len(reference),chapter_files=len(chapters),source_files=100,
                compiled=sum(r['compiled'] for r in results),local_pass=sum(r['local_pass'] for r in results),
                assertions=sum(r['assertions'] for r in results),official_submissions=0,
                optional_generated_assets_missing=sorted(set(optional_missing)),errors=errors)
    (ROOT/'reports/audit.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps(report,ensure_ascii=False,indent=2))
    if errors: raise SystemExit(1)
if __name__=='__main__': main()
