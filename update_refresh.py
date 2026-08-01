import re

with open('admin.html', 'r', encoding='utf-8') as f:
    html = f.read()

refresh_btn = """
        <div class="flex justify-end mb-6">
          <button id="refreshStatsBtn" class="inline-flex items-center gap-2 bg-primaryTeal hover:bg-primaryHover text-white px-4 py-2 rounded-lg font-bold transition-all shadow-[0_0_15px_rgba(53,127,116,0.3)]">
            <i class="ph ph-arrows-clockwise"></i>
            تحديث الإحصائيات
          </button>
        </div>
"""

# Increase cache buster
html = html.replace('admin.js?v=3', 'admin.js?v=4')
html = html.replace('<!-- General Stats -->', refresh_btn + '        <!-- General Stats -->')

with open('admin.html', 'w', encoding='utf-8') as f:
    f.write(html)

with open('admin.js', 'r', encoding='utf-8') as f:
    js = f.read()

refresh_logic = """
// Refresh Button Logic
document.getElementById('refreshStatsBtn')?.addEventListener('click', () => {
  const btn = document.getElementById('refreshStatsBtn');
  const icon = btn.querySelector('i');
  icon.classList.add('animate-spin');
  statsLoaded = false;
  
  // Show loading spinners in lists
  document.getElementById('studentsStatsList').innerHTML = '<div class="text-center py-10"><i class="ph ph-spinner animate-spin text-3xl text-primaryTeal"></i></div>';
  document.getElementById('projectsStatsList').innerHTML = '<div class="text-center py-10"><i class="ph ph-spinner animate-spin text-3xl text-primaryTeal"></i></div>';
  document.getElementById('generalViewsCount').innerText = '...';
  document.getElementById('navGraduatesViewsCount').innerText = '...';
  document.getElementById('navProjectsViewsCount').innerText = '...';
  
  loadStats().then(() => {
    setTimeout(() => icon.classList.remove('animate-spin'), 500);
  });
});
"""

js = js + "\n" + refresh_logic

with open('admin.js', 'w', encoding='utf-8') as f:
    f.write(js)

print('Refresh button added')
