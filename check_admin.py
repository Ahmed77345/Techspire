with open('admin.js', 'r', encoding='utf-8') as f:
    js = f.read()

if 'data-action="delete"' in js:
    print('Found data-action=delete')
else:
    print('NOT FOUND data-action=delete')

if 'ph-trash' in js:
    print('Found ph-trash')
else:
    print('NOT FOUND ph-trash')
