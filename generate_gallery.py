#!/usr/bin/env python3
"""
生成食材图片画廊的静态 HTML 页面
从 JSON 文件中提取前 100 个食材，使用云端存储 URL 显示图片
"""

import json
import os

def extract_first_100_items(json_file):
    """
    从 JSON 文件中提取前 100 个食材项目
    
    Args:
        json_file (str): JSON 文件路径
        
    Returns:
        list: 包含前 100 个食材的列表
    """
    try:
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        all_items = []
        
        # 遍历所有类别，收集所有食材
        for category, items in data.items():
            if isinstance(items, list):
                for item in items:
                    all_items.append({
                        'name': item['name'],
                        'filename': item['filename'],
                        'category': category
                    })
        
        # 返回所有 item
        return all_items
        
    except Exception as e:
        print(f"错误: {e}")
        return []

def generate_image_url(filename):
    """
    生成云端存储的图片 URL
    
    Args:
        filename (str): 图片文件名
        
    Returns:
        str: 完整的图片 URL
    """
    return f"https://rtaicookbook.oss-cn-hongkong.aliyuncs.com/generated_images/{filename}?x-oss-process=image/resize,w_240"

def generate_html(items, output_file):
    """
    生成静态 HTML 页面
    
    Args:
        items (list): 食材列表
        output_file (str): 输出 HTML 文件路径
    """
    total_count = len(items)
    
    html_content = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>食材图片画廊 - 完整收录</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background-color: #f8f9fa;
            padding: 20px;
            line-height: 1.6;
        }}
        
        .header {{
            text-align: center;
            margin-bottom: 40px;
        }}
        
        .header h1 {{
            color: #2c3e50;
            font-size: 2.5rem;
            margin-bottom: 10px;
        }}
        
        .header p {{
            color: #7f8c8d;
            font-size: 1.1rem;
        }}
        
        .gallery {{
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 20px;
            max-width: 1200px;
            margin: 0 auto;
        }}
        
        .item {{
            background: white;
            border-radius: 12px;
            padding: 15px;
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
            transition: transform 0.3s ease, box-shadow 0.3s ease;
            text-align: center;
        }}
        
        .item:hover {{
            transform: translateY(-5px);
            box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);
        }}
        
        .item img {{
            width: 100%;
            height: 200px;
            object-fit: cover;
            border-radius: 8px;
            margin-bottom: 10px;
            background-color: #f1f2f6;
        }}
        
        .item-name {{
            font-weight: 600;
            color: #2c3e50;
            font-size: 0.9rem;
            margin-bottom: 5px;
            text-transform: capitalize;
        }}
        
        .item-category {{
            color: #7f8c8d;
            font-size: 0.8rem;
            background-color: #ecf0f1;
            padding: 3px 8px;
            border-radius: 12px;
            display: inline-block;
        }}
        
        .stats {{
            text-align: center;
            margin-bottom: 30px;
            color: #7f8c8d;
        }}
        
        /* 响应式设计 */
        @media (max-width: 1024px) {{
            .gallery {{
                grid-template-columns: repeat(3, 1fr);
            }}
        }}
        
        @media (max-width: 768px) {{
            .gallery {{
                grid-template-columns: repeat(2, 1fr);
                gap: 15px;
            }}
            
            .header h1 {{
                font-size: 2rem;
            }}
        }}
        
        @media (max-width: 480px) {{
            .gallery {{
                grid-template-columns: 1fr;
            }}
            
            body {{
                padding: 15px;
            }}
        }}
        
        /* 加载动画 */
        .item img {{
            opacity: 0;
            animation: fadeIn 0.5s ease forwards;
        }}
        
        @keyframes fadeIn {{
            to {{
                opacity: 1;
            }}
        }}
        
        /* 错误处理 */
        .item img[src=""], .item img:not([src]) {{
            background-color: #ecf0f1;
            background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='100' height='100' viewBox='0 0 100 100'%3E%3Ctext x='50' y='50' font-family='Arial' font-size='12' fill='%23bdc3c7' text-anchor='middle' dy='.3em'%3E图片加载中...%3C/text%3E%3C/svg%3E");
            background-repeat: no-repeat;
            background-position: center;
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>🍽️ 食材图片画廊</h1>
        <p>完整收录所有高质量食材图片</p>
    </div>
    
    <div class="stats">
        <p>共展示 <strong>{total_count}</strong> 个食材</p>
    </div>
    
    <div class="gallery">
"""

    # 添加每个食材项目
    for i, item in enumerate(items):
        image_url = generate_image_url(item['filename'])
        html_content += f"""        <div class="item" style="animation-delay: {i * 0.05}s;">
            <img src="{image_url}" alt="{item['name']}" loading="lazy" 
                 onerror="this.style.backgroundImage='url(data:image/svg+xml,%3Csvg xmlns=\\'http://www.w3.org/2000/svg\\' width=\\'100\\' height=\\'100\\' viewBox=\\'0 0 100 100\\'%3E%3Ctext x=\\'50\\' y=\\'50\\' font-family=\\'Arial\\' font-size=\\'12\\' fill=\\'%23e74c3c\\' text-anchor=\\'middle\\' dy=\\'.3em\\'%3E加载失败%3C/text%3E%3C/svg%3E)'; this.style.backgroundColor='#fadbd8';">
            <div class="item-name">{item['name']}</div>
            <div class="item-category">{item['category']}</div>
        </div>
"""

    html_content += """    </div>
    
    <script>
        // 图片懒加载优化
        if ('IntersectionObserver' in window) {
            const imageObserver = new IntersectionObserver((entries, observer) => {
                entries.forEach(entry => {
                    if (entry.isIntersecting) {
                        const img = entry.target;
                        img.src = img.dataset.src || img.src;
                        img.classList.remove('lazy');
                        imageObserver.unobserve(img);
                    }
                });
            });
            
            document.querySelectorAll('img[loading="lazy"]').forEach(img => {
                imageObserver.observe(img);
            });
        }
        
        // 添加点击放大功能
        document.querySelectorAll('.item img').forEach(img => {
            img.addEventListener('click', function() {
                const modal = document.createElement('div');
                modal.style.cssText = `
                    position: fixed;
                    top: 0;
                    left: 0;
                    width: 100%;
                    height: 100%;
                    background: rgba(0,0,0,0.8);
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    z-index: 1000;
                    cursor: pointer;
                `;
                
                const modalImg = document.createElement('img');
                modalImg.src = this.src.replace('w_240', 'w_800');
                modalImg.style.cssText = `
                    max-width: 90%;
                    max-height: 90%;
                    border-radius: 8px;
                    box-shadow: 0 4px 20px rgba(0,0,0,0.3);
                `;
                
                modal.appendChild(modalImg);
                document.body.appendChild(modal);
                
                modal.addEventListener('click', () => {
                    document.body.removeChild(modal);
                });
            });
        });
        
        console.log('食材图片画廊加载完成！共展示 {len(items)} 个食材');
    </script>
</body>
</html>"""

    # 写入文件
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"HTML 文件已生成: {output_file}")
    print(f"共包含 {len(items)} 个食材")

def main():
    """
    主函数
    """
    # 使用更大的 JSON 文件
    json_file = "ingredients_global_650_final_fixed.json"
    output_file = "ingredients_gallery.html"
    
    print("正在提取所有食材...")
    items = extract_first_100_items(json_file)  # 函数名保持不变，但现在返回所有item
    
    if items:
        print(f"成功提取 {len(items)} 个食材")
        print("正在生成 HTML 文件...")
        generate_html(items, output_file)
        print(f"✅ 完成！请打开 {output_file} 查看结果")
    else:
        print("❌ 提取食材失败")

if __name__ == "__main__":
    main()