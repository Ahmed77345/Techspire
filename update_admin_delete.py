with open('admin.js', 'r', encoding='utf-8') as f:
    js = f.read()

import re

# Update students render
old_students_render = """
      studentsListEl.innerHTML += `
        <div class="flex justify-between items-center bg-bgDark p-3 rounded-lg border border-white/5">
          <span class="text-sm font-semibold">${stat.name}</span>
          <span class="bg-primaryTeal/20 text-primaryTeal px-2 py-1 rounded text-xs font-bold">${stat.views} زيارة</span>
        </div>
      `;
"""

new_students_render = """
      studentsListEl.innerHTML += `
        <div class="flex justify-between items-center bg-bgDark p-3 rounded-lg border border-white/5 group">
          <span class="text-sm font-semibold">${stat.name}</span>
          <div class="flex items-center gap-2">
            <span class="bg-primaryTeal/20 text-primaryTeal px-2 py-1 rounded text-xs font-bold">${stat.views} زيارة</span>
            <button onclick="window.deleteStat('students_analytics', '${stat.id}')" class="text-red-500/50 hover:text-red-500 hover:bg-red-500/10 p-1.5 rounded-lg transition-all opacity-0 group-hover:opacity-100" title="مسح الإحصائية">
              <i class="ph ph-trash text-lg"></i>
            </button>
          </div>
        </div>
      `;
"""

# Update projects render
old_projects_render = """
      projectsListEl.innerHTML += `
        <div class="flex justify-between items-center bg-bgDark p-3 rounded-lg border border-white/5">
          <span class="text-sm font-semibold truncate max-w-[70%]">${stat.name}</span>
          <span class="bg-primaryTeal/20 text-primaryTeal px-2 py-1 rounded text-xs font-bold whitespace-nowrap">${stat.views} زيارة</span>
        </div>
      `;
"""

new_projects_render = """
      projectsListEl.innerHTML += `
        <div class="flex justify-between items-center bg-bgDark p-3 rounded-lg border border-white/5 group">
          <span class="text-sm font-semibold truncate max-w-[60%]">${stat.name}</span>
          <div class="flex items-center gap-2">
            <span class="bg-primaryTeal/20 text-primaryTeal px-2 py-1 rounded text-xs font-bold whitespace-nowrap">${stat.views} زيارة</span>
            <button onclick="window.deleteStat('projects_analytics', '${stat.id}')" class="text-red-500/50 hover:text-red-500 hover:bg-red-500/10 p-1.5 rounded-lg transition-all opacity-0 group-hover:opacity-100" title="مسح الإحصائية">
              <i class="ph ph-trash text-lg"></i>
            </button>
          </div>
        </div>
      `;
"""

delete_logic = """
window.deleteStat = async function(collectionName, docId) {
    if(confirm('هل أنت متأكد من تصفير إحصائيات هذا العنصر؟')) {
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

js = js.replace(old_students_render.strip(), new_students_render.strip())
js = js.replace(old_projects_render.strip(), new_projects_render.strip())

if 'window.deleteStat' not in js:
    js += '\n' + delete_logic

with open('admin.js', 'w', encoding='utf-8') as f:
    f.write(js)

print('admin.js updated for individual deletion')
