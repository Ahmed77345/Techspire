import glob

html_files = glob.glob('*.html')

for file in html_files:
    with open(file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    old_text = 'تم تقديم هذا الموقع كمبادرة من المطور'
    new_text = 'تم تقديم هذا الموقع كمبادرة من المهندس'
    
    if old_text in content:
        content = content.replace(old_text, new_text)
        with open(file, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f'Changed to Engineer in {file}')
