with open('admin.js', 'r', encoding='utf-8') as f:
    js = f.read()

import re

# Remove the old delegation block
old_delegation_match = re.search(r'// Global event delegation for delete buttons.*?\}\);\s*', js, re.DOTALL)
if old_delegation_match:
    js = js.replace(old_delegation_match.group(0), '')

new_delegation_logic = """
// Global event delegation for delete buttons
document.addEventListener('click', async (e) => {
    const btn = e.target.closest('[data-action="delete"]');
    if (btn) {
        if (btn.getAttribute('data-confirming') !== 'true') {
            btn.setAttribute('data-confirming', 'true');
            btn.innerHTML = '<span class="text-xs font-bold px-1 text-red-500">تأكيد؟</span>';
            btn.classList.add('bg-red-500/20');
            
            setTimeout(() => {
                if (btn && btn.getAttribute('data-confirming') === 'true') {
                    btn.removeAttribute('data-confirming');
                    btn.innerHTML = '<i class="ph ph-trash text-lg"></i>';
                    btn.classList.remove('bg-red-500/20');
                }
            }, 3000);
            return;
        }

        const collectionName = btn.getAttribute('data-collection');
        const docId = btn.getAttribute('data-id');
        
        try {
            btn.innerHTML = '<i class="ph ph-spinner animate-spin text-lg"></i>';
            btn.disabled = true;
            
            await deleteDoc(doc(db, collectionName, docId));
            statsLoaded = false;
            await loadStats();
        } catch (err) {
            console.error("Error deleting stat:", err);
            alert('حدث خطأ أثناء المسح: ' + err.message);
            btn.removeAttribute('data-confirming');
            btn.innerHTML = '<i class="ph ph-trash text-lg"></i>';
            btn.classList.remove('bg-red-500/20');
            btn.disabled = false;
        }
    }
});
"""

js += '\n' + new_delegation_logic

with open('admin.js', 'w', encoding='utf-8') as f:
    f.write(js)

print('Updated event delegation to bypass native confirm dialog.')
