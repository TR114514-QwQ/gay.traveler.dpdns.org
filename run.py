import json

def generate_section(items, title):
    if not items: return ""
    section_html = f'<div class="mdui-typo-headline mdui-m-t-4 mdui-m-b-2">{title}</div>'
    section_html += '<div class="mdui-row-xs-1 mdui-row-sm-2 mdui-row-md-3">'
    for item in items:
        item_id = item.get('id', '0')
        section_html += f"""
        <div class="mdui-col mdui-p-a-2">
            <div class="mdui-card mdui-hoverable item-card" id="{item_id}">
                <div class="mdui-card-primary">
                    <div class="mdui-card-primary-title">{item['name']}</div>
                </div>
                <div class="mdui-card-content mdui-text-color-white-secondary" style="min-height: 50px;">
                    {item['desc']}
                </div>
                
                <div class="mdui-card-actions" style="display: flex; flex-direction: column; align-items: flex-start; padding: 16px;">
                    <!-- 第一行：ID和复制按钮 -->
                    <div style="display: flex; align-items: center; width: 100%; margin-bottom: 12px;">
                        <button class="mdui-btn mdui-btn-icon mdui-ripple mdui-text-color-theme-accent" 
                                onclick="copyLink('{item_id}')" mdui-tooltip="{{content: '复制此项链接'}}">
                            <i class="mdui-icon material-icons">link</i>
                        </button>
                        <span class="mdui-typo-caption-opacity" style="word-break: break-all; margin-left: 4px;">ID: {item_id}</span>
                    </div>
                    
                    <!-- 第二行：下载按钮（全宽） -->
                    <a href="{item['download-url']}" 
                       class="mdui-btn mdui-btn-raised mdui-ripple mdui-color-theme-accent" 
                       style="width: 100%; border-radius: 12px !important;">
                       <i class="mdui-icon material-icons mdui-icon-left">file_download</i>Download
                    </a>
                </div>
            </div>
        </div>"""
    section_html += '</div>'
    return section_html

def generate_html():
    try:
        with open('data.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        print(f"Error: {e}")
        return

    cfg = data.get("config", {})
    
    html_template = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{cfg.get('page_title')}</title>
        <link rel="stylesheet" href="https://unpkg.com/mdui@1.0.2/dist/css/mdui.min.css"/>
        <style>
            body {{
                background: url('{cfg.get('background_api')}') no-repeat center center fixed;
                background-size: cover;
                min-height: 100vh;
                scroll-behavior: smooth;
            }}
            .item-card {{
                border-radius: 25px !important;
                background: rgba(30, 30, 30, 0.75) !important;
                backdrop-filter: blur(15px);
                border: 1px solid rgba(255,255,255,0.1);
                transition: all 0.3s cubic-bezier(.25,.8,.25,1);
            }}
            .highlight-active {{
                border: 2px solid #ff4081 !important;
                box-shadow: 0 0 30px rgba(255, 64, 129, 0.5) !important;
                transform: scale(1.03);
            }}
            footer {{ margin-top: 50px; padding: 30px; background: rgba(0,0,0,0.6); text-align: center; border-radius: 25px 25px 0 0; }}
            .mdui-typo-display-2 {{ font-weight: bold; text-shadow: 0 4px 15px rgba(0,0,0,0.8); }}
        </style>
    </head>
    <body class="mdui-theme-layout-dark mdui-theme-primary-blue-grey mdui-theme-accent-pink">
        <div class="mdui-container">
            <div class="mdui-text-center mdui-m-y-5">
                <h1 class="mdui-typo-display-2">{cfg.get('page_title')}</h1>
                <p class="mdui-typo-subheading mdui-m-t-2">{cfg.get('page_description')}</p>
            </div>

            {generate_section(data.get('client', []), cfg.get('client_title'))}
            {generate_section(data.get('resourcepack', []), cfg.get('resource_title'))}

            <footer>
                <div class="mdui-typo-caption-opacity mdui-m-b-1">Links</div>
                {"".join([f'<a href="{l["url"]}" target="_blank" class="mdui-btn mdui-ripple">{l["name"]}</a>' for l in data.get("links", [])])}
            </footer>
        </div>

        <script src="https://unpkg.com/mdui@1.0.2/dist/js/mdui.min.js"></script>
        <script>
            function copyLink(id) {{
                const baseUrl = window.location.href.split('?')[0];
                const shareUrl = baseUrl + '?id=' + id;
                navigator.clipboard.writeText(shareUrl).then(() => {{
                    mdui.snackbar({{
                        message: '链接已复制: ' + id,
                        position: 'bottom'
                    }});
                }}).catch(err => {{
                    console.error('复制失败', err);
                }});
            }}

            window.onload = function() {{
                const urlParams = new URLSearchParams(window.location.search);
                const targetId = urlParams.get('id');
                if (targetId) {{
                    const element = document.getElementById(targetId);
                    if (element) {{
                        setTimeout(() => {{
                            element.scrollIntoView({{ behavior: 'smooth', block: 'center' }});
                            element.classList.add('highlight-active');
                        }}, 500);
                    }}
                }}
            }};
        </script>
    </body>
    </html>
    """

    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html_template)
    print("生成完成！布局已优化，不再错位。")

if __name__ == "__main__":
    generate_html()