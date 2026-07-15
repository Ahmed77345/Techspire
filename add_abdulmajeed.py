import json
import os

base_dir = r'd:\flutter\project\flash\it_graduation_showcase\data'
stud_file = os.path.join(base_dir, 'students.json')

with open(stud_file, 'r', encoding='utf-8') as f:
    students = json.load(f)

# Check if he already exists
found = False
for s in students:
    if 'عبدالمجيد' in s['name'] and 'الانسي' in s['name']:
        s['image'] = './images/students/abdulmajeed_alansi.jpg'
        found = True
        print(f"UPDATED: ID: {s['id']}")

if not found:
    new_student = {
        'id': 43,
        'name': 'م/ عبدالمجيد عبدالله الانسي',
        'image': './images/students/abdulmajeed_alansi.jpg',
        'project_id': 0,
        'bio': 'خريج متميز يسعى لتطوير مهاراته التقنية.'
    }
    students.append(new_student)
    print('ADDED ABDULMAJEED AS ID 43')

with open(stud_file, 'w', encoding='utf-8') as f:
    json.dump(students, f, ensure_ascii=False, indent=2)

