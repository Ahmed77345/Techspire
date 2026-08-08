import glob

html_files = glob.glob('*.html')

credit_html = """      <!-- Developer Credit -->
      <div class="mb-8 p-4 bg-primaryTeal/10 border border-primaryTeal/20 rounded-2xl inline-flex items-center justify-center gap-3 shadow-lg shadow-primaryTeal/5 hover:scale-105 transition-transform duration-300">
        <i class="ph-fill ph-code text-primaryTeal text-xl"></i>
        <p class="text-white font-medium">تم تقديم هذا الموقع كمبادرة من المطور <a href="#" class="text-primaryTeal font-bold hover:underline">أحمد عمر بن سميط</a></p>
      </div>

"""

for file in html_files:
    with open(file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if 'تم تقديم هذا الموقع كمبادرة' in content:
        continue
        
    if '<!-- Copyright Line -->' in content:
        content = content.replace('<!-- Copyright Line -->', credit_html + '      <!-- Copyright Line -->')
        with open(file, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f'Updated {file}')
