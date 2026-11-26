"""仅使用本机已安装浏览器，不自动下载整套浏览器。"""
def launch_browser(playwright):
    failures=[]
    for channel in ['msedge','chrome']:
        try:
            return playwright.chromium.launch(channel=channel,headless=True,args=['--allow-file-access-from-files'])
        except Exception as exc:
            failures.append(f'{channel}: {exc}')
    raise RuntimeError('需要已安装的Edge或Chrome。\n'+'\n'.join(failures))
