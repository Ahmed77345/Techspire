import json
import os

project_path = r"d:\flutter\project\flash\it_graduation_showcase\data\projects.json"
students_path = r"d:\flutter\project\flash\it_graduation_showcase\data\students.json"

new_project = {
    "id": 20,
    "title": "إدارة وكالات الغاز المنزلي",
    "description": "تطبيق إلكتروني لإدارة وكالات الغاز المنزلي، يهدف إلى تنظيم عملية توزيع أسطوانات الغاز.",
    "hero_image": "",
    "meta": {
      "domain": "إدارة خدمية",
      "type": "تطبيق إلكتروني",
      "team_size": "4 طالبات",
      "year": "2026"
    },
    "stats": [
      {
        "icon": "ph-gas-pump",
        "label": "توزيع عادل"
      },
      {
        "icon": "ph-qr-code",
        "label": "تحقق ذكي"
      },
      {
        "icon": "ph-clock",
        "label": "تقليل الازدحام"
      }
    ],
    "about": "مشروعنا هو تطبيق إلكتروني لإدارة وكالات الغاز المنزلي، يهدف إلى تنظيم عملية توزيع أسطوانات الغاز بين الوكلاء والمستهلكين بطريقة رقمية بدلاً من الأساليب التقليدية. يساهم التطبيق في تقليل الازدحام، وتحقيق العدالة في التوزيع، وتسهيل متابعة الطلبات والإبلاغ عن المشكلات، مما يحسن جودة الخدمة ويزيد من كفاءة إدارة الوكالات. يتميز مشروعنا بأنه يقدم حلاً رقميًا متكاملاً يناسب احتياجات المجتمع المحلي، ويجمع بين سهولة الاستخدام، وتنظيم التوزيع، والشفافية.",
    "features": [
      {
        "icon": "ph-map-pin",
        "title": "أقرب وكيل",
        "description": "معرفة أقرب وكيل بالنسبة للمواطن لتسهيل الوصول للخدمة."
      },
      {
        "icon": "ph-bell-ringing",
        "title": "إشعارات فورية",
        "description": "إشعارات للمستهلك قبل التعبئة وبعد تعبئة اسطوانة الغاز."
      },
      {
        "icon": "ph-ticket",
        "title": "حجز إلكتروني",
        "description": "حجز طلب تعبئة غاز إلكترونيًا ومتابعة حالة الطلب من تقديمه حتى الاستلام."
      },
      {
        "icon": "ph-qr-code",
        "title": "رمز QR (باركود)",
        "description": "استخدام رمز QR (باركود) للتحقق من استلام الأسطوانة ومنع التلاعب والتكرار."
      }
    ],
    "interfaces": [],
    "technologies": [
      "Flutter",
      "Firebase"
    ],
    "demo_link": "#",
    "card_icon": "ph-gas-pump"
}

with open(project_path, 'r', encoding='utf-8') as f:
    projects = json.load(f)

projects.append(new_project)

with open(project_path, 'w', encoding='utf-8') as f:
    json.dump(projects, f, ensure_ascii=False, indent=2)


with open(students_path, 'r', encoding='utf-8') as f:
    students = json.load(f)

max_id = max([s['id'] for s in students])

new_students = [
    {
        "id": max_id + 1,
        "name": "م/ رجاء صالح بالطيف",
        "image": "https://firebasestorage.googleapis.com/v0/b/graduates-de1c9.firebasestorage.app/o/projects%2Ffemale_avatar.jpg?alt=media",
        "project_id": 20,
        "bio": "خريجة متميزة تسعى لتطوير مهاراتها التقنية."
    },
    {
        "id": max_id + 2,
        "name": "م/ نفيسة ربيع بيزار",
        "image": "https://firebasestorage.googleapis.com/v0/b/graduates-de1c9.firebasestorage.app/o/projects%2Ffemale_avatar.jpg?alt=media",
        "project_id": 20,
        "bio": "خريجة متميزة تسعى لتطوير مهاراتها التقنية."
    },
    {
        "id": max_id + 3,
        "name": "م/ نسيبة أحمد صرهيد",
        "image": "https://firebasestorage.googleapis.com/v0/b/graduates-de1c9.firebasestorage.app/o/projects%2Ffemale_avatar.jpg?alt=media",
        "project_id": 20,
        "bio": "خريجة متميزة تسعى لتطوير مهاراتها التقنية."
    },
    {
        "id": max_id + 4,
        "name": "م/ اريام عادل العامري",
        "image": "https://firebasestorage.googleapis.com/v0/b/graduates-de1c9.firebasestorage.app/o/projects%2Ffemale_avatar.jpg?alt=media",
        "project_id": 20,
        "bio": "خريجة متميزة تسعى لتطوير مهاراتها التقنية."
    }
]

students.extend(new_students)

with open(students_path, 'w', encoding='utf-8') as f:
    json.dump(students, f, ensure_ascii=False, indent=2)

print("Done")
