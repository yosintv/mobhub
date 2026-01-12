import json
import os
import glob

# 1. Load data from all JSON files
phones = []
json_files = glob.glob('data/*.json')

for file_path in json_files:
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            if isinstance(data, list):
                phones.extend(data)
            else:
                phones.append(data)
    except Exception as e:
        print(f"Error loading {file_path}: {e}")

# 2. SEO Helper: Generate JSON-LD Schema for a specific phone
def generate_schema(phone):
    schema = {
        "@context": "https://schema.org/",
        "@type": "Product",
        "name": f"Samsung Galaxy A56", # In a real app, extract this from a 'name' key
        "image": phone.get("image_url"),
        "description": f"Detailed specifications for Samsung Galaxy A56 featuring {phone.get('display', {}).get('type')} and {phone.get('platform', {}).get('chipset')}.",
        "brand": {
            "@type": "Brand",
            "name": "Samsung"
        },
        "offers": {
            "@type": "Offer",
            "priceCurrency": "USD",
            "price": phone.get("misc", {}).get("price", {}).get("usd", "").replace('$', '').replace(',', ''),
            "availability": "https://schema.org/InStock"
        }
    }
    return json.dumps(schema)

# 3. Build the HTML with SEO Meta Tags
html_start = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    
    <title>Mobile Specs Pro - Latest Smartphone Specifications 2026</title>
    <meta name="description" content="Compare the latest mobile phone specifications, prices, and features. Detailed technical data for Samsung Galaxy A56 and more.">
    <meta name="keywords" content="Mobile Specs, Smartphone Comparison, Samsung Galaxy A56 Specs, Android 15 Phones">
    <meta name="robots" content="index, follow">
    
    <meta property="og:title" content="Mobile Specs Pro - Smartphone Directory">
    <meta property="og:description" content="Expert technical specifications for the newest mobile devices.">
    <meta property="og:type" content="website">
    <meta property="og:url" content="https://yourdomain.com">
    
    <style>
        :root {{ --primary: #2563eb; --dark: #1e293b; --light: #f8fafc; }}
        body {{ font-family: 'Inter', system-ui, sans-serif; background: var(--light); color: var(--dark); margin: 0; padding: 20px; }}
        .container {{ max-width: 1000px; margin: 0 auto; }}
        header {{ text-align: center; padding: 40px 0; }}
        .phone-card {{ background: white; border-radius: 16px; overflow: hidden; display: flex; box-shadow: 0 10px 15px -3px rgba(0,0,0,0.1); margin-bottom: 30px; border: 1px solid #e2e8f0; }}
        .image-box {{ background: #fff; padding: 20px; display: flex; align-items: center; justify-content: center; width: 300px; }}
        .image-box img {{ max-width: 100%; height: auto; }}
        .details {{ padding: 30px; flex: 1; }}
        .price-tag {{ font-size: 1.5rem; font-weight: bold; color: var(--primary); }}
        .spec-table {{ width: 100%; border-collapse: collapse; margin-top: 15px; }}
        .spec-table td {{ padding: 8px 0; border-bottom: 1px solid #f1f5f9; font-size: 0.9rem; }}
        .label {{ color: #64748b; font-weight: 600; width: 120px; }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>Mobile Specification Directory</h1>
            <p>Accurate, up-to-date technical data for modern smartphones.</p>
        </header>
"""

html_cards = ""
for phone in phones:
    # Generate the Schema script tag for this specific phone
    schema_script = f'<script type="application/ld+json">{generate_schema(phone)}</script>'
    
    html_cards += f"""
    {schema_script}
    <article class="phone-card">
        <div class="image-box">
            <img src="{phone.get('image_url')}" alt="Samsung Galaxy A56" loading="lazy">
        </div>
        <div class="details">
            <h2>Samsung Galaxy A56</h2>
            <p class="price-tag">{phone.get('misc', {}).get('price', {}).get('usd', 'N/A')}</p>
            <table class="spec-table">
                <tr><td class="label">Display</td><td>{phone.get('display', {}).get('size')} {phone.get('display', {}).get('type')}</td></tr>
                <tr><td class="label">Processor</td><td>{phone.get('platform', {}).get('chipset')}</td></tr>
                <tr><td class="label">Battery</td><td>{phone.get('battery', {}).get('type')}</td></tr>
                <tr><td class="label">Camera</td><td>{phone.get('main_camera', {}).get('sensors')[0]}</td></tr>
                <tr><td class="label">OS</td><td>{phone.get('platform', {}).get('os')}</td></tr>
            </table>
        </div>
    </article>
    """

html_end = """
    </div>
</body>
</html>"""

# Write the final file
os.makedirs('docs', exist_ok=True)
with open('docs/index.html', 'w', encoding='utf-8') as f:
    f.write(html_start + html_cards + html_end)

print("SEO Website Generated Successfully in /docs/index.html")
