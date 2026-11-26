"""只读检查发布文件与已有内容，输出脱敏结果；不初始化Git、不推送。"""
import hashlib,json,pathlib,re,sys
from datetime import datetime,timezone,timedelta
from public_files import ROOT,public_files

def check():
    files=public_files(); findings=[]
    patterns={
        'GitHub凭据':r'\b(?:gh[pousr]_[A-Za-z0-9]{30,}|github_pat_[A-Za-z0-9_]{30,})\b',
        '云访问密钥':r'\bAKIA[0-9A-Z]{16}\b',
        'API密钥':r'\bsk-(?:proj-)?[A-Za-z0-9_-]{24,}\b',
        '私钥':r'-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----',
        '个人主目录绝对路径':r'(?i)\b[A-Z]:[\\/]Users[\\/][^\s\\/"<>]+',
    }
    manifest=json.loads((ROOT/'sources/manifest.json').read_text(encoding='utf-8'))
    results={r['id']:r for r in json.loads((ROOT/'reports/test-results.json').read_text(encoding='utf-8'))}
    if len(manifest)!=100 or len({q['id'] for q in manifest})!=100: findings.append({'rule':'题目数量/唯一性异常'})
    for q in manifest:
        source=ROOT/q['source']; text=source.read_text(encoding='utf-8')
        # Git在不同系统可能规范换行；只接受原字节或等价CRLF/LF，不接受代码内容变化。
        hashes={hashlib.sha256(b).hexdigest() for b in [source.read_bytes(),text.encode(),text.replace('\n','\r\n').encode()]}
        if q['sha256'] not in hashes or not results.get(q['id'],{}).get('local_pass'):
            findings.append({'rule':'源码内容变化后尚未验证','file':q['source']})
    inventory=[]
    for path in files:
        relative=path.relative_to(ROOT).as_posix()
        data=path.read_bytes()
        inventory.append(dict(path=relative,bytes=len(data),sha256=hashlib.sha256(data).hexdigest()))
        if path.suffix=='.pdf': continue
        text=data.decode('utf-8-sig')
        for name,pattern in patterns.items():
            for m in re.finditer(pattern,text):
                findings.append(dict(rule=name,file=relative,line=text.count('\n',0,m.start())+1))
        if relative=='mkdocs.yml' and re.search(r'(?:file:///|[A-Z]:[\\/])',text):
            findings.append(dict(rule='站点配置包含本机路径',file=relative))
    # 检查PDF可读性、题名可搜索、书签、敏感本机URI；只读取，不重建。
    from pypdf import PdfReader
    pdf=ROOT/'output/pdf/Hot100-Java-完整学习手册.pdf'; reader=PdfReader(pdf)
    pdf_text='\n'.join(p.extract_text() or '' for p in reader.pages)
    missing=[q['id'] for q in manifest if q['name'] not in pdf_text]
    if missing: findings.append(dict(rule='PDF缺少题名',ids=missing))
    for page in reader.pages:
        for annotation in page.get('/Annots',[]):
            action=annotation.get_object().get('/A',{}); uri=str(action.get('/URI',''))
            if uri.startswith('file:'): findings.append(dict(rule='PDF有本机文件链接'))
    if not reader.outline: findings.append(dict(rule='PDF无目录书签'))
    report=dict(date=datetime.now(timezone(timedelta(hours=8))).isoformat(timespec='seconds'),
        account='由gh auth status单独确认，不记录Token',files=len(inventory),
        total_bytes=sum(p['bytes'] for p in inventory),pdf_pages=len(reader.pages),
        problem_count=len(manifest),topics=len({q['category'] for q in manifest}),
        findings=findings,official_snapshots='保留本机，排除公开发布',inventory=inventory)
    work=ROOT/'.tools'; work.mkdir(exist_ok=True)
    (work/'publish-manifest.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    (work/'git-paths.nul').write_bytes(b'\0'.join(p['path'].encode() for p in inventory)+b'\0')
    print(json.dumps({k:v for k,v in report.items() if k!='inventory'},ensure_ascii=False,indent=2))
    if findings: raise SystemExit(1)
    return report
if __name__=='__main__': check()
