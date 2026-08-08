import glob

html_files = glob.glob('*.html')

for file in html_files:
    with open(file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    old_text = 'المطور <a href="#" class="text-primaryTeal font-bold hover:underline">أحمد عمر بن سميط</a>'
    new_text = 'المطور <a href="student.html?id=25" class="text-primaryTeal font-bold hover:underline">أحمد عمر بن سميط</a>'
    
    if old_text in content:
        content = content.replace(old_text, new_text)
        with open(file, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f'Linked ID 25 in {file}')
