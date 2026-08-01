import re

# Update admin.html
with open('admin.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Replace general stats card with a grid of 3 cards
general_stats_html = """
        <!-- General Stats -->
        <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div class="bg-cardDark p-6 rounded-2xl border border-white/10 flex flex-col justify-between items-center shadow-lg gap-4 text-center">
            <h2 class="text-lg font-bold text-white">زر "رؤية الخريجين"</h2>
            <div class="text-2xl px-6 py-2 rounded-xl bg-primaryTeal/20 text-primaryTeal font-extrabold border border-primaryTeal/30">
              <span id="generalViewsCount">0</span>
            </div>
          </div>
          <div class="bg-cardDark p-6 rounded-2xl border border-white/10 flex flex-col justify-between items-center shadow-lg gap-4 text-center">
            <h2 class="text-lg font-bold text-white">زر القائمة: "الخريجون"</h2>
            <div class="text-2xl px-6 py-2 rounded-xl bg-primaryTeal/20 text-primaryTeal font-extrabold border border-primaryTeal/30">
              <span id="navGraduatesViewsCount">0</span>
            </div>
          </div>
          <div class="bg-cardDark p-6 rounded-2xl border border-white/10 flex flex-col justify-between items-center shadow-lg gap-4 text-center">
            <h2 class="text-lg font-bold text-white">زر القائمة: "المشاريع"</h2>
            <div class="text-2xl px-6 py-2 rounded-xl bg-primaryTeal/20 text-primaryTeal font-extrabold border border-primaryTeal/30">
              <span id="navProjectsViewsCount">0</span>
            </div>
          </div>
        </div>
"""

# Find the general stats div and replace it
html = re.sub(
    r'<!-- General Stats -->.*?<div class="grid grid-cols-1 md:grid-cols-2 gap-6">',
    general_stats_html + '\n        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">',
    html,
    flags=re.DOTALL
)

# Add search inputs above the lists
html = html.replace(
    '<h2 class="text-xl font-bold text-white mb-4">زيارات ملفات الخريجين</h2>',
    '<h2 class="text-xl font-bold text-white mb-2">زيارات ملفات الخريجين</h2>\n            <input type="text" id="searchStudents" placeholder="ابحث باسم الخريج..." class="w-full bg-bgDark border border-white/10 rounded-lg px-4 py-2 text-sm text-white focus:outline-none focus:border-primaryTeal transition mb-4">'
)

html = html.replace(
    '<h2 class="text-xl font-bold text-white mb-4">زيارات المشاريع</h2>',
    '<h2 class="text-xl font-bold text-white mb-2">زيارات المشاريع</h2>\n            <input type="text" id="searchProjects" placeholder="ابحث باسم المشروع..." class="w-full bg-bgDark border border-white/10 rounded-lg px-4 py-2 text-sm text-white focus:outline-none focus:border-primaryTeal transition mb-4">'
)

with open('admin.html', 'w', encoding='utf-8') as f:
    f.write(html)

# Update admin.js
with open('admin.js', 'r', encoding='utf-8') as f:
    js = f.read()

# Replace the data fetching and rendering logic
new_js_logic = """
// Stats Logic
let statsLoaded = false;
let globalStudentsStats = [];
let globalProjectsStats = [];

async function loadStats() {
  if (statsLoaded) return;
  
  try {
    // 1. Fetch metadata (Students & Projects) to map IDs to Names
    const [studentsRes, projectsRes] = await Promise.all([
      fetch('/data/students.json'),
      fetch('/data/projects.json')
    ]);
    const students = await studentsRes.json();
    const projects = await projectsRes.json();
    
    const studentsMap = {};
    students.forEach(s => studentsMap[s.id] = s.name);
    
    const projectsMap = {};
    projects.forEach(p => projectsMap[p.id] = p.title);
    
    // 2. Fetch General Stats
    const generalSnap = await getDocs(collection(db, 'general_analytics'));
    let totalBtnClicks = 0;
    let navGraduatesClicks = 0;
    let navProjectsClicks = 0;
    
    generalSnap.forEach(doc => {
      if(doc.id === 'view_graduates_btn') {
        totalBtnClicks = doc.data().views || 0;
      }
      if(doc.id === 'nav_graduates_btn') {
        navGraduatesClicks = doc.data().views || 0;
      }
      if(doc.id === 'nav_projects_btn') {
        navProjectsClicks = doc.data().views || 0;
      }
    });
    document.getElementById('generalViewsCount').innerText = totalBtnClicks;
    document.getElementById('navGraduatesViewsCount').innerText = navGraduatesClicks;
    document.getElementById('navProjectsViewsCount').innerText = navProjectsClicks;
    
    // 3. Fetch Students Stats
    const studentsSnap = await getDocs(collection(db, 'students_analytics'));
    globalStudentsStats = [];
    studentsSnap.forEach(doc => {
      globalStudentsStats.push({ id: doc.id, views: doc.data().views || 0, name: studentsMap[doc.id] || `خريج #${doc.id}` });
    });
    globalStudentsStats.sort((a, b) => b.views - a.views);
    renderStudentsStats(globalStudentsStats);
    
    // 4. Fetch Projects Stats
    const projectsSnap = await getDocs(collection(db, 'projects_analytics'));
    globalProjectsStats = [];
    projectsSnap.forEach(doc => {
      globalProjectsStats.push({ id: doc.id, views: doc.data().views || 0, name: projectsMap[doc.id] || `مشروع #${doc.id}` });
    });
    globalProjectsStats.sort((a, b) => b.views - a.views);
    renderProjectsStats(globalProjectsStats);
    
    statsLoaded = true;
  } catch (error) {
    console.error("Error loading stats:", error);
    document.getElementById('studentsStatsList').innerHTML = `<p class="text-red-400 text-center text-sm p-4 bg-red-900/20 rounded">خطأ: ${error.message}</p>`;
    document.getElementById('projectsStatsList').innerHTML = `<p class="text-red-400 text-center text-sm p-4 bg-red-900/20 rounded">خطأ: ${error.message}</p>`;
  }
}

function renderStudentsStats(data) {
  const studentsListEl = document.getElementById('studentsStatsList');
  studentsListEl.innerHTML = '';
  if(data.length === 0) {
    studentsListEl.innerHTML = '<p class="text-textMuted text-center text-sm p-4">لا توجد بيانات مطابقة.</p>';
  } else {
    data.forEach(stat => {
      studentsListEl.innerHTML += `
        <div class="flex justify-between items-center bg-bgDark p-3 rounded-lg border border-white/5">
          <span class="text-sm font-semibold">${stat.name}</span>
          <span class="bg-primaryTeal/20 text-primaryTeal px-2 py-1 rounded text-xs font-bold">${stat.views} زيارة</span>
        </div>
      `;
    });
  }
}

function renderProjectsStats(data) {
  const projectsListEl = document.getElementById('projectsStatsList');
  projectsListEl.innerHTML = '';
  if(data.length === 0) {
    projectsListEl.innerHTML = '<p class="text-textMuted text-center text-sm p-4">لا توجد بيانات مطابقة.</p>';
  } else {
    data.forEach(stat => {
      projectsListEl.innerHTML += `
        <div class="flex justify-between items-center bg-bgDark p-3 rounded-lg border border-white/5">
          <span class="text-sm font-semibold truncate max-w-[70%]">${stat.name}</span>
          <span class="bg-primaryTeal/20 text-primaryTeal px-2 py-1 rounded text-xs font-bold whitespace-nowrap">${stat.views} زيارة</span>
        </div>
      `;
    });
  }
}

// Attach Search Listeners
document.getElementById('searchStudents')?.addEventListener('input', (e) => {
  const query = e.target.value.toLowerCase().trim();
  const filtered = globalStudentsStats.filter(s => s.name.toLowerCase().includes(query));
  renderStudentsStats(filtered);
});

document.getElementById('searchProjects')?.addEventListener('input', (e) => {
  const query = e.target.value.toLowerCase().trim();
  const filtered = globalProjectsStats.filter(p => p.name.toLowerCase().includes(query));
  renderProjectsStats(filtered);
});
"""

js = re.sub(
    r'// Stats Logic.*',
    new_js_logic.strip(),
    js,
    flags=re.DOTALL
)

with open('admin.js', 'w', encoding='utf-8') as f:
    f.write(js)

print('admin.html and admin.js updated')
