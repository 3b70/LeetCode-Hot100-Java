"""用本机Edge/Chrome做真实渲染、搜索、复制、主题和窄屏检查，不上传。"""
import argparse,functools,http.server,json,pathlib,threading
from urllib.parse import urlsplit
from playwright.sync_api import sync_playwright
from browser_utils import launch_browser

ROOT=pathlib.Path(__file__).resolve().parents[1]
class QuietHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self,*args): pass

def main():
    parser=argparse.ArgumentParser(); parser.add_argument('--base-url'); args=parser.parse_args()
    shots=ROOT/('reports/screenshots/public' if args.base_url else 'reports/screenshots'); shots.mkdir(parents=True,exist_ok=True)
    server=None
    if args.base_url:
        base=args.base_url.rstrip('/')+'/'
        if not base.startswith('https://'): raise ValueError('公网验证必须使用HTTPS')
        u=urlsplit(base); origin=u.scheme+'://'+u.netloc
    else:
        handler=functools.partial(QuietHandler,directory=str(ROOT))
        server=http.server.ThreadingHTTPServer(('127.0.0.1',0),handler)
        thread=threading.Thread(target=server.serve_forever,daemon=True); thread.start()
        origin=f'http://127.0.0.1:{server.server_address[1]}'; base=origin+'/site/'
    report=dict(engine='Windows本机Chromium（Edge/Chrome）',physical_iphone_tested=False,
                served_under_subpath=urlsplit(base).path,completed=False,checks=[],screenshots=[],external_requests=[],console_errors=[])
    manifest=json.loads((ROOT/'sources/site-manifest.json').read_text(encoding='utf-8'))
    by_id={q['id']:q for q in manifest}
    def url(i): return base+by_id[i]['page'].replace('.md','.html')
    def record(name,condition,details=None):
        report['checks'].append(dict(name=name,passed=bool(condition),details=details))
        if not condition: raise AssertionError(f'{name}: {details}')
    try:
        with sync_playwright() as p:
            browser=launch_browser(p)
            desktop=browser.new_context(viewport={'width':1440,'height':1000},color_scheme='light')
            desktop.grant_permissions(['clipboard-read','clipboard-write'],origin=origin)
            page=desktop.new_page()
            page.on('pageerror',lambda e:report['console_errors'].append(str(e)))
            def watch(request):
                if request.url.startswith('http') and not request.url.startswith(origin): report['external_requests'].append(request.url)
            page.on('request',watch)
            page.goto(base,wait_until='networkidle')
            if args.base_url: record('公网HTTPS首页',page.url.startswith(base))
            record('首页含100题目录',page.locator('.md-content a[href^="problems/"]').count()==100)
            record('首页17专题导航',page.locator('.md-content a[href^="topics/"]').count()==17)
            record('中文界面',page.locator('html').get_attribute('lang')=='zh')
            page.screenshot(path=str(shots/'desktop-home.png')); report['screenshots'].append('reports/screenshots/desktop-home.png')
            for term,expected in [('206','反转链表'),('两数之和','两数之和'),('HashMap','HashMap'),('递归','递归')]:
                page.locator('input[data-md-component="search-query"]').click()
                search=page.locator('input[data-md-component="search-query"]'); search.fill(term)
                page.wait_for_function('(s)=>document.querySelector(".md-search-result__list")?.textContent.replace(/\u200b/g, "").includes(s)',arg=expected)
                record('搜索：'+term,expected in page.locator('.md-search-result__list').inner_text().replace('\u200b',''))
                search.fill(''); page.keyboard.press('Escape')
            page.goto(url(1),wait_until='networkidle')
            record('Java代码高亮',page.locator('.highlight .k, .highlight .kd').count()>0)
            record('中文注释独立配色',page.locator('.highlight .c1').count()>=2)
            expected_code=(ROOT/by_id[1]['source']).read_text(encoding='utf-8').strip()
            page.evaluate('navigator.clipboard.writeText("__hot100_copy_test__")')
            page.locator('button[data-md-type="copy"]').first.click()
            page.wait_for_function(r'(expected)=>navigator.clipboard.readText().then(t=>t.replace(/\r\n/g,"\n").trim()===expected)',arg=expected_code)
            copied=page.evaluate('navigator.clipboard.readText()').replace('\r\n','\n')
            record('一键复制原始Java代码',copied.strip()==expected_code)
            before=page.locator('body').get_attribute('data-md-color-scheme')
            page.locator('form[data-md-component="palette"] label:visible').first.click()
            after=page.locator('body').get_attribute('data-md-color-scheme')
            record('浅色深色切换',before!=after,dict(before=before,after=after))
            page.screenshot(path=str(shots/'desktop-dark-problem.png')); report['screenshots'].append('reports/screenshots/desktop-dark-problem.png')
            following=page.locator('.problem-pager a[rel="next"]').first
            target=following.get_attribute('href'); following.click(); page.wait_for_load_state('networkidle')
            record('下一题导航',page.url.endswith(target))
            for width in [320,390,430]:
                mobile=browser.new_context(viewport={'width':width,'height':844},is_mobile=True,has_touch=True,device_scale_factor=1,color_scheme='light')
                mobile.grant_permissions(['clipboard-read','clipboard-write'],origin=origin)
                mp=mobile.new_page(); mp.on('pageerror',lambda e:report['console_errors'].append(str(e))); mp.on('request',watch)
                for i in [None,1,51,72,295]:
                    mp.goto(base if i is None else url(i),wait_until='networkidle')
                    metrics=mp.evaluate('''() => ({width:innerWidth,body:document.documentElement.scrollWidth,
                         codeScroll:[...document.querySelectorAll('pre code')].every(e=>getComputedStyle(e).whiteSpace==='pre' && getComputedStyle(e).overflowX==='auto'),
                         missingImages:[...document.images].filter(i=>!i.complete || i.naturalWidth===0).length})''')
                    record(f'窄屏{width}px：'+('首页' if i is None else str(i)),metrics['body']<=width+1 and metrics['codeScroll'] and not metrics['missingImages'],metrics)
                mp.goto(url(1),wait_until='networkidle')
                mp.locator('label[for="__drawer"]:visible').first.click()
                record(f'{width}px手机菜单',mp.locator('#__drawer').is_checked())
                mp.locator('label.md-overlay[for="__drawer"]').click(position={'x':width-4,'y':80})
                record(f'{width}px关闭手机菜单',not mp.locator('#__drawer').is_checked())
                if width==390:
                    mp.goto(url(1),wait_until='networkidle')
                    mp.locator('.highlight').first.scroll_into_view_if_needed()
                    mp.evaluate('navigator.clipboard.writeText("__hot100_mobile_copy__")')
                    mp.locator('button[data-md-type="copy"]').first.click()
                    mp.wait_for_function(r'(expected)=>navigator.clipboard.readText().then(t=>t.replace(/\r\n/g,"\n").trim()===expected)',arg=expected_code)
                    record('手机触摸复制Java源码',True)
                    scroll=mp.locator('pre code').first.evaluate('(e)=>{e.scrollLeft=70;const moved=e.scrollLeft;e.scrollLeft=0;return {moved,width:e.clientWidth,scroll:e.scrollWidth}}')
                    record('手机长代码可横向滚动',scroll['moved']>0,scroll)
                    mp.screenshot(path=str(shots/'mobile-code-390.png')); report['screenshots'].append('reports/screenshots/mobile-code-390.png')
                    mp.goto(base,wait_until='networkidle')
                    mp.screenshot(path=str(shots/'mobile-home-390.png')); report['screenshots'].append('reports/screenshots/mobile-home-390.png')
                    mp.locator('label[for="__search"]:visible').first.click()
                    mp.locator('input[data-md-component="search-query"]').fill('两数之和')
                    mp.wait_for_function('document.querySelector(".md-search-result__list")?.textContent.replace(/\u200b/g, "").includes("两数之和")')
                    record('手机中文搜索',True)
                    mp.screenshot(path=str(shots/'mobile-search-390.png')); report['screenshots'].append('reports/screenshots/mobile-search-390.png')
                mobile.close()
            if not args.base_url:
                # file://双击场景也要真实验证，不只检查HTTP。
                local=browser.new_context(viewport={'width':1280,'height':900}); lp=local.new_page()
                lp.goto((ROOT/'site/index.html').as_uri(),wait_until='networkidle')
                lp.locator('input[data-md-component="search-query"]').click()
                lp.locator('input[data-md-component="search-query"]').fill('206')
                lp.wait_for_function('document.querySelector(".md-search-result__list")?.textContent.replace(/\u200b/g, "").includes("反转链表")')
                record('Windows双击HTML离线搜索',True)
            record('无外部运行网络请求',not report['external_requests'],report['external_requests'])
            record('无页面JavaScript异常',not report['console_errors'],report['console_errors'])
            report['completed']=True
            browser.close()
    finally:
        if server: server.shutdown(); server.server_close()
        report['passed']=report['completed'] and all(c['passed'] for c in report['checks']) and len(report['checks'])>=30
        (ROOT/('reports/browser-check-public.json' if args.base_url else 'reports/browser-check.json')).write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps(report,ensure_ascii=False,indent=2))
if __name__=='__main__': main()
