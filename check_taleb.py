import json
import os

base_dir = r'd:\flutter\project\flash\it_graduation_showcase\data'
stud_file = os.path.join(base_dir, 'students.json')

with open(stud_file, 'r', encoding='utf-8') as f:
    students = json.load(f)

found = False
for s in students:
    if 'طالب' in s['name'] or 'محيفوظ' in s['name']:
        print(f"FOUND: ID: {s['id']}, Name: {s['name']}")
        found = True

if not found:
    new_student = {
        'id': 42,
        'name': 'م/ طالب حامد محيفوظ',
        'image': './images/students/taleb.jpg',
        'project_id': 0,
        'bio': 'خريج متميز يسعى لتطوير مهاراته التقنية.'
    }
    students.append(new_student)
    with open(stud_file, 'w', encoding='utf-8') as f:
        json.dump(students, f, ensure_ascii=False, indent=2)
    print('ADDED TALEB AS ID 42')

