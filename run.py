import json

def generate_section(items, title):
    if not items: return ""
    section_html = f'<div class="mdui-typo-headline mdui-m-t-4 mdui-m-b-2">{title}</div>'
    section_html += '<div class="mdui-row-xs-1 mdui-row-sm-2 mdui-row-md-3">'
    for item in items:
        # 重点：在这里添加了 id 属性
        item_id = item.get('id', '')
        section_html += f"""
        <div class="mdui-col mdui-p-a-2">
            <div class="mdui-card mdui-hoverable item-card" id="{item_id}">
                <div class="mdui-card-primary">
                    <div class="mdui-card-primary-title">{item['name']}</div>
                </div>
                <div class="mdui-card-content mdui-text-color-white-secondary" style="min-height: 50px;">
                    {item['desc']}
                </div>
                <div class="mdui-card-actions">
                    <div class="mdui-chip mdui-m-l-1"><span class="mdui-chip-title">ID: {item_id}</span></div>
                    <a href="{item['download-url']}" class="mdui-btn mdui-ripple mdui-btn-raised mdui-color-theme-accent mdui-float-right">Download</a>
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
                transition: all 0.3s;
            }}
            /* 高亮动画样式 */
            .highlight-active {{
                border: 2px solid #ff4081 !important;
                box-shadow: 0 0 30px rgba(255, 64, 129, 0.5) !important;
                transform: scale(1.05);
            }}
            .mdui-btn {{ border-radius: 12px !important; }}
            footer {{ margin-top: 50px; padding: 30px; background: rgba(0,0,0,0.5); text-align: center; border-radius: 25px 25px 0 0; }}
        </style>
    </head>
    <body class="mdui-theme-layout-dark mdui-theme-primary-blue-grey mdui-theme-accent-pink">
        <div class="mdui-container">
            <div class="mdui-text-center mdui-m-y-5">
                <h1 class="mdui-typo-display-2" style="text-shadow: 0 4px 10px rgba(0,0,0,0.5);">{cfg.get('page_title')}</h1>
                <p class="mdui-typo-subheading">{cfg.get('page_description')}</p>
            </div>

            {generate_section(data.get('client', []), cfg.get('client_title'))}
            {generate_section(data.get('resourcepack', []), cfg.get('resource_title'))}

            <footer>
                <div class="mdui-typo-caption-opacity mdui-m-b-1">Links</div>
                {"".join([f'<a href="{l["url"]}" class="mdui-btn mdui-ripple">{l["name"]}</a>' for l in data.get("links", [])])}
            </footer>
        </div>

        <script>
            // 自动跳转与高亮逻辑
            window.onload = function() {{
                const urlParams = new URLSearchParams(window.location.search);
                const targetId = urlParams.get('id');
                
                if (targetId) {{
                    const element = document.getElementById(targetId);
                    if (element) {{
                        // 1. 滚动到目标位置
                        setTimeout(() => {{
                            element.scrollIntoView({{ behavior: 'smooth', block: 'center' }});
                            // 2. 添加高亮类
                            element.classList.add('highlight-active');
                        }}, 500);
                    }}
                }}
            }};
        </script>
        <script src="https://unpkg.com/mdui@1.0.2/dist/js/mdui.min.js"></script>
    </body>
    </html>
    """

    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html_template)
    print("Generated successfully! Use index.html?id=YOUR_ID to test.")

if __name__ == "__main__":
    generate_html()