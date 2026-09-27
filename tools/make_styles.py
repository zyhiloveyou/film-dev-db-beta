#!/usr/bin/env python3
"""生成两个候选样式的页面（功能/数据与 index.html 完全一致，仅替换 CSS）。
用法: python3 tools/make_styles.py  （在 film-dev-db-beta 目录运行）
输出: web/style-darkroom.html, web/style-editorial.html
"""
import os, re

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(BASE, 'web', 'index.html')
FOOTER_OLD = '<footer>数据仅供个人参考 · 时间为起点值，请按自己的设备微调</footer>'

# ============================================================
# 样式 A：暗房胶片风 —— 安全灯琥珀色 + 胶片齿孔 + 等宽数字 + 底部导航
# ============================================================
CSS_DARK = r"""
:root{
  --bg:#0c0c0e; --card:#16161a; --ink:#f2ede3; --sub:#8b8577; --line:#282830;
  --acc:#ff9d3c; --acc-soft:#3a2410; --ok:#3fb950; --warn:#ff9d3c;
  --chip:#1d1d23; --chip-ink:#c9c3b6; --radius:8px; --shadow:none;
  --mono:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;
}
*{box-sizing:border-box;-webkit-tap-highlight-color:transparent}
html,body{margin:0;padding:0}
body{
  background:var(--bg); color:var(--ink);
  font:15px/1.55 -apple-system,BlinkMacSystemFont,"PingFang SC","Microsoft YaHei",Segoe UI,sans-serif;
  background-image:radial-gradient(circle at 50% -10%, #1a1408 0%, transparent 55%);
}
/* 顶部安全灯条 */
body::before{
  content:''; position:fixed; top:0; left:0; right:0; height:3px; z-index:120;
  background:linear-gradient(90deg,#ff7a18,#ffb347 50%,#ff7a18);
  box-shadow:0 0 14px rgba(255,157,60,.55);
}
button{font:inherit;cursor:pointer;border:none;background:none;color:inherit}
input,select{font:inherit;color:inherit}

/* header */
header{
  position:sticky;top:0;z-index:50;background:rgba(12,12,14,.96);backdrop-filter:blur(8px);
  padding:16px 16px 12px;display:flex;align-items:center;gap:10px;border-bottom:1px solid var(--line);
}
header::after{ /* 胶片齿孔带 */
  content:'';position:absolute;left:0;right:0;bottom:-9px;height:9px;
  background-image:radial-gradient(circle at 6px 50%, #2c2c34 2.6px, transparent 3px);
  background-size:18px 100%; opacity:.9;
}
header h1{font-size:15px;font-weight:600;letter-spacing:2.5px;text-transform:uppercase;flex:1;
  white-space:nowrap;overflow:hidden;text-overflow:ellipsis;font-family:var(--mono);color:var(--acc)}
header h1 small{display:block;font-weight:400;color:var(--sub);font-size:10.5px;letter-spacing:1px;margin:2px 0 0;text-transform:none}
.icon-btn{width:36px;height:36px;border-radius:6px;display:flex;align-items:center;justify-content:center;
  font-size:16px;background:var(--chip);border:1px solid var(--line);flex:none}
#btn-dark{display:none}  /* 暗房模式本身就是深色 */

/* 底部导航（App 感） */
nav.tabs{
  position:fixed;bottom:0;left:0;right:0;top:auto;z-index:60;display:flex;
  background:rgba(17,17,20,.98);backdrop-filter:blur(10px);
  border-top:1px solid var(--line);padding:6px 4px calc(6px + env(safe-area-inset-bottom));
}
nav.tabs button{flex:1;padding:8px 4px;font-size:11px;color:var(--sub);border-radius:6px;line-height:1.4}
nav.tabs button.on{color:#0c0c0e;background:var(--acc);font-weight:700;box-shadow:0 0 12px rgba(255,157,60,.35)}

main{max-width:820px;margin:0 auto;padding:18px 12px 110px}
section.page{display:none}
section.page.on{display:block}

/* 搜索 */
.searchbar{position:sticky;top:74px;z-index:48;background:var(--bg);padding:6px 0 10px;margin:0 0 6px}
.searchbar input{width:100%;padding:12px 38px 12px 14px;border:1px solid var(--line);border-radius:var(--radius);
  background:#101014;outline:none;font-size:15px}
.searchbar input:focus{border-color:var(--acc);box-shadow:0 0 0 3px rgba(255,157,60,.12)}
.searchbar .mag{position:absolute;right:12px;top:50%;transform:translateY(-50%);color:var(--acc);opacity:.8}
.hot{display:flex;gap:8px;flex-wrap:wrap;margin:2px 0 14px}
.hot button{background:var(--chip);color:var(--chip-ink);padding:8px 13px;border-radius:6px;font-size:12.5px;
  border:1px solid var(--line);font-family:var(--mono)}
.hint{color:var(--sub);font-size:13px;text-align:center;padding:30px 10px}

/* 胶片列表 */
.film-list{display:flex;flex-direction:column;gap:0;padding-bottom:6px}
.film-letter{font-size:10.5px;color:var(--acc);padding:14px 4px 6px;font-weight:700;letter-spacing:2px;
  font-family:var(--mono);border-bottom:1px solid var(--line)}
.film-item{display:flex;align-items:center;gap:10px;padding:12px 6px;background:transparent;
  border-bottom:1px solid var(--line)}
.film-item .nm{flex:1;font-weight:500;font-size:14.5px}
.film-item .cnt{color:var(--sub);font-size:11px;font-family:var(--mono)}
.film-item .fav{font-size:16px;color:#4a4a52;width:32px;height:32px}
.film-item .fav.on{color:var(--acc);text-shadow:0 0 10px rgba(255,157,60,.6)}

/* 配方视图 */
.view-head{display:flex;align-items:center;gap:10px;margin:4px 0 12px}
.view-head .back{width:36px;height:36px;border-radius:6px;background:var(--chip);border:1px solid var(--line);font-size:15px;flex:none}
.view-head h2{font-size:16px;flex:1;font-family:var(--mono);letter-spacing:.5px;color:var(--acc)}
.ctl{position:sticky;top:130px;z-index:40;background:var(--bg);padding:8px 0 10px}
.ctl-row{display:flex;gap:8px;align-items:center;flex-wrap:wrap;margin-bottom:8px}
.seg{display:flex;background:#101014;border:1px solid var(--line);border-radius:var(--radius);overflow:hidden;flex:1;min-width:230px}
.seg button{flex:1;padding:9px 4px;font-size:12.5px;color:var(--sub);font-weight:600;font-family:var(--mono)}
.seg button.on{background:var(--acc);color:#0c0c0e;box-shadow:0 0 12px rgba(255,157,60,.3)}
.chips{display:flex;gap:6px;overflow-x:auto;padding-bottom:4px;scrollbar-width:none}
.chips::-webkit-scrollbar{display:none}
.chips button{flex:none;background:var(--chip);color:var(--chip-ink);border:1px solid var(--line);
  padding:7px 12px;border-radius:6px;font-size:12.5px;font-family:var(--mono)}
.chips button.on{background:var(--acc);color:#0c0c0e;border-color:var(--acc);font-weight:700}
.chips .dev-select{width:100%;padding:11px 12px;border:1px solid var(--line);border-radius:var(--radius);
  background:#101014;color:var(--ink);font-size:14px;outline:none;flex:none}
.tempwrap{display:flex;align-items:center;gap:10px;flex:1;min-width:200px}
.tempwrap input[type=range]{flex:1;accent-color:var(--acc)}
.tempwrap .tv{font-weight:700;min-width:56px;text-align:center;font-size:13px;font-family:var(--mono);color:var(--acc)}
.note-line{color:var(--sub);font-size:11.5px;padding:2px 2px 10px;font-family:var(--mono)}

/* 配方卡 = 胶片格 */
.rcard{background:var(--card);border:1px solid var(--line);border-left:3px solid var(--acc);
  border-radius:var(--radius);margin-bottom:12px;overflow:hidden}
.rcard .rhead{display:flex;align-items:center;gap:8px;padding:12px 12px 8px}
.rcard .rhead .dn{font-weight:600;font-size:14.5px;flex:1}
.rcard .rhead .dil{background:var(--acc-soft);color:var(--acc);font-size:11.5px;padding:2px 9px;
  border-radius:4px;font-family:var(--mono);border:1px solid rgba(255,157,60,.25)}
.rtable{width:100%;border-collapse:collapse;font-size:13px}
.rtable th{color:var(--sub);font-weight:600;font-size:10.5px;text-align:right;padding:6px 9px;
  border-top:1px solid var(--line);text-transform:uppercase;letter-spacing:1px;font-family:var(--mono)}
.rtable td{padding:7px 9px;text-align:right;border-top:1px solid var(--line);white-space:nowrap;
  font-family:var(--mono);font-size:12.5px}
.rtable td:first-child,.rtable th:first-child{text-align:left}
.rtable .iso{font-weight:700;color:var(--ink)}
.rtable .t35{font-weight:700;font-size:14px;color:var(--ink)}
.rtable .t35.conv{color:var(--acc)}
.rtable .sub{color:var(--sub);font-size:11px}
.rtable a{color:var(--acc);text-decoration:none;border-bottom:1px dotted var(--acc)}
.rtable .na{color:#3a3a42}
.tnote{font-size:11px;color:var(--sub);padding:4px 12px 10px;font-family:var(--mono)}
.empty{padding:30px 10px;text-align:center;color:var(--sub)}

/* 官方数据 */
.of-head{display:flex;gap:6px;margin:4px 0 12px;overflow-x:auto;scrollbar-width:none}
.of-head::-webkit-scrollbar{display:none}
.of-head button{flex:none;background:var(--chip);color:var(--chip-ink);border:1px solid var(--line);
  padding:8px 13px;border-radius:6px;font-size:12.5px;font-family:var(--mono)}
.of-head button.on{background:var(--acc);color:#0c0c0e;border-color:var(--acc);font-weight:700}
.otable{width:100%;border-collapse:collapse;font-size:12.5px;background:var(--card);border:1px solid var(--line)}
.otable th{background:#101014;text-align:left;padding:9px 10px;font-size:11px;color:var(--acc);
  font-family:var(--mono);text-transform:uppercase;letter-spacing:.5px}
.otable td{padding:8px 10px;border-top:1px solid var(--line);font-family:var(--mono);font-size:12px}
.otable .r{text-align:right}
.otable tr:nth-child(even) td{background:rgba(255,255,255,.02)}

/* 说明页 */
.about{background:var(--card);border:1px solid var(--line);border-radius:var(--radius);padding:16px;font-size:13.5px}
.about h3{font-size:12px;margin:18px 0 8px;color:var(--acc);font-family:var(--mono);letter-spacing:1.5px;text-transform:uppercase}
.about p{margin:6px 0}
.about .muted{color:var(--sub);font-size:12.5px}
.about table{border-collapse:collapse;width:100%;font-size:12.5px;margin:8px 0}
.about td,.about th{border:1px solid var(--line);padding:6px 8px;text-align:left}
.about a{color:var(--acc)}
.badge{display:inline-block;background:var(--acc-soft);color:var(--acc);padding:1px 8px;border-radius:4px;
  font-size:11.5px;margin:1px 2px;font-family:var(--mono);border:1px solid rgba(255,157,60,.25)}

footer{text-align:center;color:var(--sub);font-size:11px;padding:24px 12px 40px;font-family:var(--mono)}
.style-switch{margin-bottom:10px;font-size:12px}
.style-switch a{color:var(--acc);text-decoration:none;margin:0 4px;border-bottom:1px dotted var(--acc)}
.style-switch b{color:var(--ink)}
"""

# ============================================================
# 样式 B：极简杂志/手册风 —— 纸感米白 + 衬线标题 + 细线 + 印刷红
# ============================================================
CSS_EDIT = r"""
:root{
  --bg:#faf8f3; --card:#fffefb; --ink:#1a1a16; --sub:#6f6c62; --line:#e3ded1;
  --acc:#a8342a; --acc-soft:#f5e8e5; --ok:#2f6b45; --warn:#a8342a;
  --chip:#f1ece0; --chip-ink:#3b382f; --radius:0px; --shadow:none;
  --serif:Georgia,"Times New Roman","Songti SC","Noto Serif SC",serif;
  --sans:"Helvetica Neue",Helvetica,Arial,"PingFang SC","Microsoft YaHei",sans-serif;
}
*{box-sizing:border-box;-webkit-tap-highlight-color:transparent}
html,body{margin:0;padding:0}
body{background:var(--bg);color:var(--ink);font:14.5px/1.6 var(--sans);
  background-image:linear-gradient(rgba(0,0,0,.012) 1px,transparent 1px);background-size:100% 28px}
button{font:inherit;cursor:pointer;border:none;background:none;color:inherit}
input,select{font:inherit;color:inherit}

header{position:sticky;top:0;z-index:50;background:rgba(250,248,243,.97);backdrop-filter:blur(6px);
  padding:18px 18px 12px;display:flex;align-items:flex-end;gap:12px;border-bottom:3px double var(--ink)}
header h1{font-family:var(--serif);font-size:25px;font-weight:400;letter-spacing:-.3px;flex:1;line-height:1.15}
header h1 small{display:block;font-family:var(--sans);font-size:10.5px;color:var(--sub);
  letter-spacing:2.5px;text-transform:uppercase;margin-top:6px;font-weight:600}
.icon-btn{width:34px;height:34px;border:1px solid var(--line);border-radius:0;display:flex;
  align-items:center;justify-content:center;font-size:15px;background:transparent;flex:none;color:var(--sub)}
#btn-dark{display:none}

nav.tabs{position:sticky;top:0;z-index:49;display:flex;background:var(--bg);
  border-bottom:1px solid var(--line);padding:0 12px;overflow-x:auto;scrollbar-width:none}
nav.tabs::-webkit-scrollbar{display:none}
nav.tabs button{flex:1;min-width:92px;padding:13px 6px;font-size:10.5px;letter-spacing:1.8px;
  text-transform:uppercase;color:var(--sub);border-bottom:2px solid transparent;white-space:nowrap;font-weight:600}
nav.tabs button.on{color:var(--acc);border-bottom-color:var(--acc)}

main{max-width:760px;margin:0 auto;padding:16px 16px 80px}
section.page{display:none}
section.page.on{display:block}

.searchbar{position:relative;margin:8px 0 14px}
.searchbar input{width:100%;padding:11px 36px 11px 0;border:none;border-bottom:1px solid var(--ink);
  border-radius:0;background:transparent;outline:none;font-size:16px;font-family:var(--serif)}
.searchbar input:focus{border-bottom:2px solid var(--acc)}
.searchbar .mag{position:absolute;right:4px;top:50%;transform:translateY(-50%);color:var(--sub);font-size:14px}
.hot{display:flex;gap:0;flex-wrap:wrap;margin:0 0 18px;border-top:1px solid var(--line)}
.hot button{background:transparent;color:var(--ink);padding:10px 14px 10px 0;font-size:12.5px;
  border-bottom:1px solid var(--line);margin-right:14px}
.hint{color:var(--sub);font-size:13px;text-align:center;padding:34px 10px;font-family:var(--serif);font-style:italic}

.film-list{display:flex;flex-direction:column;gap:0;padding-bottom:6px}
.film-letter{font-family:var(--serif);font-size:13px;color:var(--acc);padding:18px 0 6px;font-weight:700;
  border-bottom:1px solid var(--ink);letter-spacing:3px}
.film-item{display:flex;align-items:baseline;gap:10px;padding:11px 2px;border-bottom:1px solid var(--line);background:transparent}
.film-item .nm{flex:1;font-size:15px;font-family:var(--serif)}
.film-item .cnt{color:var(--sub);font-size:10.5px;letter-spacing:.5px}
.film-item .fav{font-size:14px;color:#c3bcac;width:30px;height:30px}
.film-item .fav.on{color:var(--acc)}

.view-head{display:flex;align-items:baseline;gap:10px;margin:6px 0 14px;border-bottom:1px solid var(--ink);padding-bottom:10px}
.view-head .back{width:30px;height:30px;border:1px solid var(--line);background:transparent;font-size:14px;flex:none;color:var(--sub)}
.view-head h2{font-size:21px;flex:1;font-family:var(--serif);font-weight:400}
.ctl{position:sticky;top:104px;z-index:40;background:var(--bg);padding:10px 0}
.ctl-row{display:flex;gap:8px;align-items:center;flex-wrap:wrap;margin-bottom:10px}
.seg{display:flex;border:1px solid var(--ink);flex:1;min-width:230px;overflow:hidden}
.seg button{flex:1;padding:9px 4px;font-size:11px;color:var(--sub);letter-spacing:1.2px;text-transform:uppercase;font-weight:600}
.seg button.on{background:var(--ink);color:var(--bg)}
.chips{display:flex;gap:0;overflow-x:auto;padding-bottom:4px;scrollbar-width:none;border-bottom:1px solid var(--line)}
.chips::-webkit-scrollbar{display:none}
.chips button{flex:none;background:transparent;color:var(--sub);padding:8px 13px;font-size:12px;border-bottom:2px solid transparent}
.chips button.on{color:var(--acc);border-bottom-color:var(--acc);font-weight:700}
.chips .dev-select{width:100%;padding:10px 4px;border:none;border-bottom:1px solid var(--ink);background:transparent;
  font-size:14px;outline:none;font-family:var(--serif);flex:none}
.tempwrap{display:flex;align-items:center;gap:10px;flex:1;min-width:200px}
.tempwrap input[type=range]{flex:1;accent-color:var(--acc)}
.tempwrap .tv{font-family:var(--serif);font-weight:700;min-width:54px;text-align:center;font-size:15px;color:var(--acc)}
.note-line{color:var(--sub);font-size:11.5px;padding:2px 0 12px;font-style:italic;font-family:var(--serif)}

.rcard{background:transparent;border:none;border-top:1px solid var(--ink);padding:0 0 6px;margin-bottom:18px}
.rcard .rhead{display:flex;align-items:baseline;gap:10px;padding:12px 0 6px}
.rcard .rhead .dn{font-family:var(--serif);font-size:17px;flex:1}
.rcard .rhead .dil{font-size:12px;color:var(--acc);border-bottom:1px solid var(--acc);padding-bottom:1px}
.rtable{width:100%;border-collapse:collapse;font-size:13px}
.rtable th{color:var(--sub);font-weight:600;font-size:10px;text-align:right;padding:8px 6px;
  border-bottom:1px solid var(--line);text-transform:uppercase;letter-spacing:1.4px}
.rtable td{padding:9px 6px;text-align:right;border-bottom:1px solid var(--line);white-space:nowrap;font-size:13px}
.rtable td:first-child,.rtable th:first-child{text-align:left}
.rtable .iso{font-weight:700}
.rtable .t35{font-family:var(--serif);font-size:16px;font-weight:400}
.rtable .t35.conv{color:var(--acc)}
.rtable .sub{color:var(--sub);font-size:11px}
.rtable a{color:var(--acc);text-decoration:none;border-bottom:1px solid var(--acc)}
.rtable .na{color:#c9c2b2}
.tnote{font-size:11px;color:var(--sub);padding:6px 0 4px;font-style:italic}
.empty{padding:34px 10px;text-align:center;color:var(--sub);font-family:var(--serif);font-style:italic}

.of-head{display:flex;gap:0;margin:6px 0 16px;overflow-x:auto;scrollbar-width:none;border-bottom:1px solid var(--line)}
.of-head::-webkit-scrollbar{display:none}
.of-head button{flex:none;background:transparent;color:var(--sub);padding:9px 15px;font-size:12px;
  border-bottom:2px solid transparent}
.of-head button.on{color:var(--ink);border-bottom-color:var(--acc);font-weight:700}
.otable{width:100%;border-collapse:collapse;font-size:12.5px}
.otable th{background:transparent;text-align:left;padding:9px 8px;font-size:10px;letter-spacing:1.2px;
  text-transform:uppercase;color:var(--sub);border-bottom:1px solid var(--ink)}
.otable td{padding:8px;border-bottom:1px solid var(--line)}
.otable .r{text-align:right;font-family:var(--serif);font-size:14px}
.otable tr:nth-child(even) td{background:rgba(0,0,0,.015)}

.about{background:transparent;border-top:1px solid var(--ink);padding:14px 0;font-size:14px}
.about h3{font-size:11px;margin:18px 0 8px;letter-spacing:2px;text-transform:uppercase;color:var(--acc);font-weight:700}
.about p{margin:6px 0}
.about .muted{color:var(--sub);font-size:13px}
.about table{border-collapse:collapse;width:100%;font-size:13px;margin:10px 0}
.about td,.about th{border-bottom:1px solid var(--line);padding:7px 8px;text-align:left}
.about a{color:var(--acc)}
.badge{display:inline-block;border:1px solid var(--line);padding:0 7px;font-size:11px;margin:1px 2px;color:var(--sub)}

footer{text-align:center;color:var(--sub);font-size:11px;padding:26px 16px 44px;font-family:var(--serif);font-style:italic}
.style-switch{margin-bottom:10px;font-style:normal;font-family:var(--sans);font-size:12px}
.style-switch a{color:var(--acc);text-decoration:none;margin:0 4px;border-bottom:1px solid var(--acc)}
.style-switch b{color:var(--ink)}
"""

def make(css, active):
    src = open(SRC, encoding='utf-8').read()
    head, rest = src.split('<style>', 1)
    old_css, tail = rest.split('</style>', 1)
    if active == 'dark':
        foot = ('<footer><div class="style-switch">样式：<a href="./">经典</a> · '
                '<b>暗房胶片</b> · <a href="style-editorial.html">杂志手册</a></div>'
                '数据仅供个人参考 · 时间为起点值，请按自己的设备微调</footer>')
    else:
        foot = ('<footer><div class="style-switch">样式：<a href="./">经典</a> · '
                '<a href="style-darkroom.html">暗房胶片</a> · <b>杂志手册</b></div>'
                '数据仅供个人参考 · 时间为起点值，请按自己的设备微调</footer>')
    return head + '<style>\n' + css + '\n</style>' + tail.replace(FOOTER_OLD, foot)

def main():
    out = {
        'web/style-darkroom.html': make(CSS_DARK, 'dark'),
        'web/style-editorial.html': make(CSS_EDIT, 'edit'),
    }
    for path, content in out.items():
        full = os.path.join(BASE, path)
        open(full, 'w', encoding='utf-8').write(content)
        print(f'{path}: {len(content)/1024:.0f} KB')

if __name__ == '__main__':
    main()
