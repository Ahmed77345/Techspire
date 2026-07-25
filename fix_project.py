import json
import os

data_dir = r'd:\flutter\project\flash\it_graduation_showcase\data'
projects_path = os.path.join(data_dir, 'projects.json')
students_path = os.path.join(data_dir, 'students.json')

with open(projects_path, 'r', encoding='utf-8') as f:
    projects = json.load(f)

# The new project should be id 19, since 1-18 are taken.
new_project_id = 19

new_project = {
    'id': new_project_id,
    'title': 'منصة إدارة العمل الإغاثي',
    'description': 'منصة رقمية متكاملة لأتمتة وتنظيم سير العمل الإغاثي لضمان كفاءة وشفافية توزيع المساعدات.',
    'hero_image': '',
    'meta': {
      'domain': 'نظم إدارة ومساعدات',
      'type': 'منصة رقمية',
      'team_size': '3 طلاب',
      'year': '2026'
    },
    'stats': [
      {'icon': 'ph-hand-heart', 'label': 'إدارة المساعدات'},
      {'icon': 'ph-qr-code', 'label': 'التحقق الذكي'},
      {'icon': 'ph-shield-check', 'label': 'شفافية وعدالة'}
    ],
    'about': 'منصة رقمية متكاملة لأتمتة وتنظيم سير العمل الإغاثي؛ تهدف إلى إدارة توزيع المساعدات الإنسانية بكفاءة وشفافية، وضمان الاستهداف الدقيق للمستفيدين لمنع تكرار الصرف باستخدام تقنيات التحقق الذكي (QR Code).',
    'features': [
      {'icon': 'ph-qr-code', 'title': 'التحقق الذكي', 'description': 'استخدام تقنية QR Code للتحقق من هوية المستفيدين ومنع تكرار الصرف.'},
      {'icon': 'ph-hand-heart', 'title': 'إدارة التوزيع', 'description': 'تنظيم وأتمتة عملية توزيع المساعدات الإنسانية بكفاءة.'},
      {'icon': 'ph-shield-check', 'title': 'الشفافية والعدالة', 'description': 'ضمان الاستهداف الدقيق للمستفيدين لتحقيق العدالة في التوزيع.'},
      {'icon': 'ph-chart-bar', 'title': 'تقارير وإحصائيات', 'description': 'متابعة وتقييم سير العمل الإغاثي عبر لوحة تحكم إحصائية متكاملة.'}
    ],
    'interfaces': [],
    'technologies': ['Web Technologies', 'QR Code', 'Database'],
    'demo_link': '#',
    'card_icon': 'ph-hand-heart'
}

# Remove any existing project with id 19 just in case
projects = [p for p in projects if p['id'] != new_project_id]
projects.append(new_project)

with open(projects_path, 'w', encoding='utf-8') as f:
    json.dump(projects, f, ensure_ascii=False, indent=2)

with open(students_path, 'r', encoding='utf-8') as f:
    students = json.load(f)

# Update the students
target_ids = [31, 14, 18]

for s in students:
    if s['id'] in target_ids:
        s['project_id'] = new_project_id

with open(students_path, 'w', encoding='utf-8') as f:
    json.dump(students, f, ensure_ascii=False, indent=2)

print('Successfully added project 19 and updated students.')
