"""只读验证已发布网站，不能用于创建仓库、登录或部署。"""
import argparse,concurrent.futures,html,json,re,time,urllib.request
from urllib.parse import urljoin,urlsplit
from public_files import ROOT
from site_audit import Page

def fetch(url):
    request=urllib.request.Request(url,headers={'User-Agent':'Hot100-Pages-Verification','Cache-Control':'no-cache'})
    with urllib.request.urlopen(request,timeout=25) as response:
        if response.status!=200 or not response.url.startswith('https://'):
            raise RuntimeError('公网访问未返回HTTPS 200')
        return response.read()

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--url',required=True); ap.add_argument('--commit',required=True)
    args=ap.parse_args(); base=args.url.rstrip('/')+'/'
    if not base.startswith('https://') or not re.fullmatch('[0-9a-f]{40}',args.commit): raise ValueError('需要实际HTTPS网址与40位提交SHA')
    # 等待CDN看到本次提交，避免访问到旧网站时误报更新成功。
    for attempt in range(15):
        try:
            info=json.loads(fetch(urljoin(base,'build-info.json')+'?commit='+args.commit))
            if info.get('git_sha')==args.commit: break
        except Exception: pass
        if attempt==14: raise RuntimeError('在等待期内未看到本次提交的网站版本')
        time.sleep(6)
    manifest=json.loads((ROOT/'sources/manifest.json').read_text(encoding='utf-8'))
    selected=[q for q in manifest if q['id'] in {1,49,128,206,146,94,200,46,322,72}]
    targets=[('首页','index.html',None)]+[(f'专题{i:02d}',f'topics/{i:02d}.html',None) for i in [1,7,15]]
    targets += [(str(q['id']),f'problems/{q["id"]:04d}-{q["slug"]}.html',q) for q in selected]
    def check(item):
        label,path,q=item; data=fetch(urljoin(base,path)); text=data.decode('utf-8'); page=Page(text)
        if q:
            if q['name'] not in html.unescape(re.search(r'<title>(.*?)</title>',text,re.S)[1]): raise RuntimeError(f'{label}页面标题不符')
            source=(ROOT/q['source']).read_text(encoding='utf-8').strip()
            if source not in [s.strip() for s in page.codes]: raise RuntimeError(f'{label}公网代码与原稿不同')
        return dict(label=label,path=path,https_status=200,bytes=len(data))
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as pool: results=list(pool.map(check,targets))
    home=Page(fetch(urljoin(base,'index.html')).decode('utf-8'))
    resources=[]
    for tag,url,a in home.links:
        if tag=='script' or (tag=='link' and a.get('rel')=='stylesheet'):
            resource=urljoin(base,url); fetch(resource); resources.append(resource)
    report=dict(url=base,git_sha=args.commit,passed=True,pages=results,resources=resources,
                physical_iphone_tested=False,note='HTTP与源码检查不替代浏览器搜索/复制测试，另运行site_browser_check.py --base-url。')
    work=ROOT/'.tools'; work.mkdir(exist_ok=True)
    (work/'public-verification.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps(report,ensure_ascii=False,indent=2))
if __name__=='__main__': main()
