"""导航由官方清单生成，主题设置留在mkdocs.yml独立维护。"""
import json,os
from pathlib import Path

def on_config(config):
    root=Path(__file__).resolve().parents[1]
    path=root/'site-nav.json'
    if not path.exists():
        raise RuntimeError('请先运行 python tools/site_build.py 生成100题独立页面。')
    config['nav']=json.loads(path.read_text(encoding='utf-8'))
    url=os.environ.get('HOT100_SITE_URL','').strip()
    if url:
        if not url.startswith('https://'):
            raise RuntimeError('HOT100_SITE_URL必须为实际HTTPS网址。')
        config['site_url']=url.rstrip('/')+'/'
    return config
