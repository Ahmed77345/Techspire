with open('admin.js', 'r', encoding='utf-8') as f:
    js = f.read()

modal_logic = """
// ==========================================
// Clear Stats Modal Logic
// ==========================================
const clearStatsModal = document.getElementById('clearStatsModal');
const openClearStatsModalBtn = document.getElementById('openClearStatsModalBtn');
const closeClearStatsModalBtn = document.getElementById('closeClearStatsModalBtn');

function openModal() {
    clearStatsModal.classList.remove('hidden');
    // slight delay for animation
    setTimeout(() => {
        clearStatsModal.classList.remove('opacity-0');
        clearStatsModal.querySelector('div').classList.remove('scale-95');
        clearStatsModal.querySelector('div').classList.add('scale-100');
    }, 10);
}

function closeModal() {
    clearStatsModal.classList.add('opacity-0');
    clearStatsModal.querySelector('div').classList.remove('scale-100');
    clearStatsModal.querySelector('div').classList.add('scale-95');
    setTimeout(() => {
        clearStatsModal.classList.add('hidden');
    }, 300);
}

openClearStatsModalBtn?.addEventListener('click', openModal);
closeClearStatsModalBtn?.addEventListener('click', closeModal);
clearStatsModal?.addEventListener('click', (e) => {
    if(e.target === clearStatsModal) closeModal();
});

// Generic function to clear a collection
async function clearCollection(collectionName, btn) {
    const originalText = btn.innerHTML;
    btn.innerHTML = '<div class="w-full text-center py-1"><i class="ph ph-spinner animate-spin text-xl"></i></div>';
    btn.disabled = true;
    try {
        const querySnapshot = await getDocs(collection(db, collectionName));
        const deletePromises = [];
        querySnapshot.forEach((docSnap) => {
            deletePromises.push(deleteDoc(doc(db, collectionName, docSnap.id)));
        });
        await Promise.all(deletePromises);
        
        // Refresh Stats
        statsLoaded = false;
        await loadStats();
        
        btn.innerHTML = '<div class="w-full text-center text-green-400 py-1"><i class="ph ph-check-circle text-xl"></i> تم المسح</div>';
        setTimeout(() => {
            btn.innerHTML = originalText;
            btn.disabled = false;
        }, 2000);
    } catch (e) {
        console.error("Error clearing " + collectionName, e);
        btn.innerHTML = '<div class="w-full text-center text-red-500 py-1">حدث خطأ</div>';
        setTimeout(() => {
            btn.innerHTML = originalText;
            btn.disabled = false;
        }, 2000);
    }
}

document.getElementById('clearGeneralBtn')?.addEventListener('click', async function() {
    await clearCollection('general_analytics', this);
});
document.getElementById('clearStudentsBtn')?.addEventListener('click', async function() {
    await clearCollection('students_analytics', this);
});
document.getElementById('clearProjectsBtn')?.addEventListener('click', async function() {
    await clearCollection('projects_analytics', this);
});
document.getElementById('clearAllBtn')?.addEventListener('click', async function() {
    const originalText = this.innerHTML;
    this.innerHTML = '<div class="w-full text-center py-1"><i class="ph ph-spinner animate-spin text-xl"></i></div>';
    this.disabled = true;
    try {
        const p1 = clearCollection('general_analytics', document.getElementById('clearGeneralBtn'));
        const p2 = clearCollection('students_analytics', document.getElementById('clearStudentsBtn'));
        const p3 = clearCollection('projects_analytics', document.getElementById('clearProjectsBtn'));
        await Promise.all([p1, p2, p3]);
        
        this.innerHTML = '<div class="w-full text-center text-green-400 py-1"><i class="ph ph-check-circle text-xl"></i> تم مسح كل شيء!</div>';
        setTimeout(() => {
            this.innerHTML = originalText;
            this.disabled = false;
            closeModal();
        }, 2000);
    } catch(e) {
        this.innerHTML = originalText;
        this.disabled = false;
    }
});
"""

js = js + '\n' + modal_logic

with open('admin.js', 'w', encoding='utf-8') as f:
    f.write(js)

print('admin.js updated')
