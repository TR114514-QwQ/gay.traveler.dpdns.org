import json

def generate_section(items, title):
    if not items: return ""
    # 这里直接使用传入的 title 变量
    section_html = f'<div class="mdui-typo-headline mdui-m-t-4 mdui-m-b-2">{title}</div>'
    section_html += '<div class="mdui-row-xs-1 mdui-row-sm-2 mdui-row-md-3">'
    for item in items:
        section_html += f"""
        <div class="mdui-col mdui-p-a-2">
            <div class="mdui-card mdui-hoverable" style="border-radius: 25px !important; background: rgba(30, 30, 30, 0.75) !important; backdrop-filter: blur(15px); border: 1px solid rgba(255,255,255,0.1);">
                <div class="mdui-card-primary">
                    <div class="mdui-card-primary-title">{item['name']}</div>
                </div>
                <div class="mdui-card-content mdui-text-color-white-secondary" style="min-height: 50px;">
                    {item['desc']}
                </div>
                <div class="mdui-card-actions">
                    <a href="{item['download-url']}" class="mdui-btn mdui-ripple mdui-btn-raised mdui-color-theme-accent mdui-float-right" style="border-radius: 12px !important;">Download</a>
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
    
    # 核心修正：从 config 中获取自定义标题
    c_title = cfg.get('client_title', 'Clients') 
    r_title = cfg.get('resource_title', 'Resource Packs')

    links_html = "".join([f'<a href="{l["url"]}" target="_blank" class="mdui-btn mdui-ripple">{l["name"]}</a>' for l in data.get("links", [])])

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
            }}
            footer {{
                margin-top: 50px;
                padding: 30px;
                background: rgba(0,0,0,0.5);
                text-align: center;
                border-radius: 25px 25px 0 0;
            }}
        </style>
    </head>
    <body class="mdui-theme-layout-dark mdui-theme-primary-blue-grey mdui-theme-accent-pink">
        <div class="mdui-container">
            <div class="mdui-text-center mdui-m-y-5">
                <h1 class="mdui-typo-display-2" style="text-shadow: 0 4px 10px rgba(0,0,0,0.5);">{cfg.get('page_title')}</h1>
                <p class="mdui-typo-subheading">{cfg.get('page_description')}</p>
            </div>

            {generate_section(data.get('client', []), c_title)}
            {generate_section(data.get('resourcepack', []), r_title)}

            <footer>
                <div class="mdui-typo-caption-opacity mdui-m-b-1">Links</div>
                {links_html}
            </footer>
        </div>
        <script src="https://unpkg.com/mdui@1.0.2/dist/js/mdui.min.js"></script>
    </body>
    </html>
    """

    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html_template)
    print("Generated successfully!")

if __name__ == "__main__":
    generate_html()