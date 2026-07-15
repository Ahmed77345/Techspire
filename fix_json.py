import json
import os

base_dir = r'd:\flutter\project\flash\it_graduation_showcase\data'
stud_file = os.path.join(base_dir, 'students.json')

with open(stud_file, 'r', encoding='utf-8') as f:
    text = f.read()

text = text.replace('    \"project_id\": 0,\n  },\n  {\n    \"id\": 41,', '    \"project_id\": 0,\n    \"bio\": \"خريج متميز يسعى لتطوير مهاراته التقنية.\"\n  },\n  {\n    \"id\": 41,')

try:
    data = json.loads(text)
    with open(stud_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print('Fixed JSON syntax successfully')
except Exception as e:
    print('Error parsing JSON:', str(e))
