with open('project.html', 'r', encoding='utf-8') as f:
    html = f.read()
import re
match = re.search(r'<img.*?id=".*?Image.*?".*?>', html)
if match:
    print('Found in project.html:', match.group(0))

with open('app_v5.js', 'r', encoding='utf-8') as f:
    js = f.read()
for i, line in enumerate(js.splitlines()):
    if 'Image' in line and 'ElementById' in line:
        print('Found in app_v5.js:', line.strip())
