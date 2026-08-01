with open('app_v5.js', 'r', encoding='utf-8') as f:
    js = f.read()

fallback_logic = """
document.getElementById('sImage').src = sImageUrl;
document.getElementById('sImage').onerror = function() {
    this.onerror = null;
    this.src = 'https://ui-avatars.com/api/?name=' + encodeURIComponent(student.name || 'خريج') + '&background=357F74&color=fff&size=512&font-size=0.33';
};
"""

js = js.replace("document.getElementById('sImage').src = sImageUrl;", fallback_logic.strip())

with open('app_v5.js', 'w', encoding='utf-8') as f:
    f.write(js)

print('Added image fallback for students')
