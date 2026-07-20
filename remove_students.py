import json

with open('data/students.json', 'r', encoding='utf-8') as f1:
    students = json.load(f1)

active = []
to_remove = []

for s in students:
    if 'بن حيدرة' in s['name'] or 'الحريري' in s['name']:
        to_remove.append(s)
    else:
        active.append(s)

with open('data/students.json', 'w', encoding='utf-8') as f1_out:
    json.dump(active, f1_out, ensure_ascii=False, indent=2)

with open('data/students_commented.json', 'r', encoding='utf-8') as f2:
    commented = json.load(f2)

commented.extend(to_remove)

with open('data/students_commented.json', 'w', encoding='utf-8') as f2_out:
    json.dump(commented, f2_out, ensure_ascii=False, indent=2)

print("Removed:", [s['name'] for s in to_remove])
