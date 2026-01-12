import json
import os

# Load the data
with open('data/phones.json', 'r') as f:
    phones = json.load(f)

# Create the HTML content
html_cards = ""
for phone in phones:
    html_cards += f"""
    <div class="card">
        <h2>{phone['brand']} {phone['model']}</h2>
        <ul>
            <li><strong>Display:</strong> {phone['specs']['display']}</li>
            <li><strong>Processor:</strong> {phone['specs']['processor']}</li>
            <li><strong>Battery:</strong> {phone['specs']['battery']}</li>
        </ul>
    </div>
    """

full_html = f"""
<!DOCTYPE html>
<html>
<head>
    <title>Mobile Specs</title>
    <style>
        body {{ font-family: sans-serif; background: #f4f4f4; padding: 20px; }}
        .card {{ background: white; padding: 15px; margin: 10px; border-radius: 8px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); }}
    </style>
</head>
<body>
    <h1>Mobile Specifications</h1>
    <div class="container">{html_cards}</div>
</body>
</html>
"""

# Ensure the docs folder exists and write the file
if not os.path.exists('docs'):
    os.makedirs('docs')

with open('docs/index.html', 'w') as f:
    f.write(full_html)

print("Website generated successfully in /docs!")
