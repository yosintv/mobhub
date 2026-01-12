import json
import os
import glob 

def generate_site():
    phones = []
    # 1. Find all JSON files in the data folder
    json_files = glob.glob('data/*.json')
    
    if not json_files:
        print("Error: No JSON files found in 'data/'. Check your folder name!")
        return

    for file_path in json_files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                if isinstance(data, list):
                    phones.extend(data)
                else:
                    phones.append(data)
        except Exception as e:
            print(f"Failed to read {file_path}: {e}")

    # 2. Build the HTML
    html_content = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Mobile Specs Directory | Latest Smartphones</title>
    <meta name="description" content="Technical specs and pricing for the latest mobile devices.">
    <style>
        body { font-family: system-ui, sans-serif; background: #f4f4f9; padding: 20px; color: #333; }
        .container { max-width: 800px; margin: 0 auto; }
        .card { background: white; border-radius: 10px; padding: 20px; margin-bottom: 20px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); display: flex; align-items: center; }
        .card img { width: 120px; margin-right: 20px; }
        h2 { margin-top: 0; color: #007bff; }
        .specs { font-size: 0.9rem; color: #666; }
    </style>
</head>
<body>
    <div class="container">
        <h1>Mobile Specs Directory</h1>"""

    for phone in phones:
        html_content += f"""
        <div class="card">
            <img src="{phone.get('image_url')}" alt="Phone Image">
            <div class="info">
                <h2>Samsung Galaxy A56</h2>
                <div class="specs">
                    <p><b>Display:</b> {phone.get('display', {}).get('size')}</p>
                    <p><b>Processor:</b> {phone.get('platform', {}).get('chipset')}</p>
                    <p><b>Battery:</b> {phone.get('battery', {}).get('type')}</p>
                </div>
            </div>
        </div>"""

    html_content += "</div></body></html>"

    # 3. Save to ROOT instead of docs/
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    # 4. Create .nojekyll to fix GitHub Pages build errors
    with open('.nojekyll', 'w') as f:
        pass 

    print("SUCCESS: index.html and .nojekyll created in the root folder.")

if __name__ == "__main__":
    generate_site()
