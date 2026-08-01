with open('admin.js', 'r', encoding='utf-8') as f:
    js = f.read()

# Replace onclick with data attributes
js = js.replace('onclick="window.deleteStat(\'students_analytics\', \'${stat.id}\')" class', 'data-action="delete" data-collection="students_analytics" data-id="${stat.id}" class')
js = js.replace('onclick="window.deleteStat(\'projects_analytics\', \'${stat.id}\')" class', 'data-action="delete" data-collection="projects_analytics" data-id="${stat.id}" class')

delegation_logic = """
// Global event delegation for delete buttons
document.addEventListener('click', async (e) => {
    const btn = e.target.closest('[data-action="delete"]');
    if (btn) {
        const collectionName = btn.getAttribute('data-collection');
        const docId = btn.getAttribute('data-id');
        
        if(confirm('هل أنت متأكد من مسح إحصائيات هذا العنصر بالتحديد؟ لا يمكن التراجع عن هذا الإجراء.')) {
            try {
                // We need to disable the button temporarily
                const originalHtml = btn.innerHTML;
                btn.innerHTML = '<i class="ph ph-spinner animate-spin text-lg"></i>';
                btn.disabled = true;
                
                await deleteDoc(doc(db, collectionName, docId));
                statsLoaded = false;
                await loadStats();
            } catch (err) {
                console.error("Error deleting stat:", err);
                alert('حدث خطأ أثناء المسح');
                btn.innerHTML = originalHtml;
                btn.disabled = false;
            }
        }
    }
});
"""

if 'data-action="delete"' not in js:
    print('Failed to replace onclick. They might not exist or were already replaced.')
else:
    if 'Global event delegation for delete buttons' not in js:
        js += '\n' + delegation_logic
    with open('admin.js', 'w', encoding='utf-8') as f:
        f.write(js)
    print('Event delegation added successfully')
