with open('admin.js', 'r', encoding='utf-8') as f:
    js = f.read()

delete_logic = """
window.deleteStat = async function(collectionName, docId) {
    if(confirm('هل أنت متأكد من مسح إحصائيات هذا العنصر بالتحديد؟ لا يمكن التراجع عن هذا الإجراء.')) {
        try {
            await deleteDoc(doc(db, collectionName, docId));
            statsLoaded = false;
            await loadStats();
        } catch (e) {
            console.error("Error deleting stat:", e);
            alert('حدث خطأ أثناء المسح');
        }
    }
}
"""

if 'async function(collectionName' not in js:
    js += '\n' + delete_logic
    with open('admin.js', 'w', encoding='utf-8') as f:
        f.write(js)
    print('Added deleteStat function')
else:
    print('Already added')
