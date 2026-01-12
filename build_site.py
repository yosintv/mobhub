import json
import os
import glob

def generate_site():
    phones = []
    # 1. Locate all JSON files in the data directory
    # Using recursive=True to find files even in subfolders
    json_files = glob.glob('data/**/*.json', recursive=True)
    
    print(f"--- Debugging ---")
    print(f"Checking directory: {os.getcwd()}")
    print(f"Files found: {json_files}")

    if not json_files:
        print("CRITICAL ERROR: No JSON files found in 'data/' folder.")
        return

    for file_path in json_files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = json.load(f)
                # Handle both [ {data} ] and {data} formats
                if isinstance(content, list):
                    phones.extend(content)
                else:
                    phones.append(content)
        except Exception as e:
            print(f"Error reading {file_path}: {e}")

    print(f"Successfully loaded {len(phones)} phones.")
    
    # 2. Start building HTML with SEO Meta Tags
    html_content = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Mobile Specs Pro | Latest Smartphone Specifications 2026</title>
    <meta name="description" content="Ultimate directory for smartphone specs. Get detailed data on Samsung Galaxy A56 and more.">
    <meta name="robots" content="index, follow">
    <style>
        :root { --blue: #2563eb; --text: #1e293b; --bg: #f8fafc; }
        body { font-family: 'Segoe UI', sans-serif; background: var(--bg); color: var(--text); margin: 0; padding: 20px; }
        .container { max-width: 900px; margin: 0 auto; }
        .card { background: white; border-radius: 12px; padding: 20px; margin-bottom: 25px; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1); display: flex; gap: 20px; border: 1px solid #e2e8f0; }
        .card img { width: 140px; height: auto; object-fit: contain; }
        .info { flex: 1; }
        h2 { margin-top: 0; color: var(--blue); border-bottom: 2px solid #eff6ff; padding-bottom: 5px; }
        .spec-list { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; font-size: 0.9rem; }
        .label { font-weight: bold; color: #64748b; }
    </style>
</head>
<body>
    <div class="container">
        <header style="text-align:center; padding: 20px 0;">
            <h1>Mobile Specification Directory</h1>
        </header>"""

    for phone in phones:
        # Generate JSON-LD Schema for SEO Rich Snippets
        schema = {
            "@context": "https://schema.org/",
            "@type": "Product",
            "name": f"Samsung Galaxy A56",
            "image": phone.get("image_url"),
            "description": f"Specs: {phone.get('display', {}).get('size')} display, {phone.get('battery', {}).get('type')} battery.",
            "offers": {"@type": "Offer", "price": phone.get("misc", {}).get("price", {}).get("usd", "399.99").replace('$', '')}
        }
        
        html_content += f"""
        <script type="application/ld+json">{json.dumps(schema)}</script>
        <article class="card">
            <img src="{phone.get('image_url')}" alt="Smartphone Image" loading="lazy">
            <div class="info">
                <h2>Samsung Galaxy A56</h2>
                <div class="spec-list">
                    <div><span class="label">Display:</span> {phone.get('display', {}).get('size', 'N/A')}</div>
                    <div><span class="label">Chipset:</span> {phone.get('platform', {}).get('chipset', 'N/A')}</div>
                    <div><span class="label">Battery:</span> {phone.get('battery', {}).get('type', 'N/A')}</div>
                    <div><span class="label">Camera:</span> {phone.get('main_camera', {}).get('setup', 'N/A')}</div>
                </div>
                <p style="margin-top:15px; font-weight:bold; color:var(--blue);">Price: {phone.get('misc',{}).get('price',{}).get('usd', 'N/A')}</p>
            </div>
        </article>"""

    html_content += "</div></body></html>"

    # 3. Save output
    os.makedirs('docs', exist_ok=True)
    with open('docs/index.html', 'w', encoding='utf-8') as f:
        f.write(html_content)
    print("\nSUCCESS: Website generated in docs/index.html")

if __name__ == "__main__":
    generate_site()
