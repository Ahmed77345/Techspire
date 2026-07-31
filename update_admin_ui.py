import json

admin_html_path = r'd:\flutter\project\flash\it_graduation_showcase\admin.html'
with open(admin_html_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Only modify if not already modified
if 'tabs-container' not in content:
    tabs_html = """
      <!-- Tabs -->
      <div class="tabs-container flex gap-4 mb-6 border-b border-white/10 pb-2">
        <button id="tabMessages" class="tab-btn active-tab text-primaryTeal font-bold px-4 py-2 border-b-2 border-primaryTeal transition">الرسائل الواردة</button>
        <button id="tabStats" class="tab-btn text-textMuted hover:text-white px-4 py-2 transition border-b-2 border-transparent">الإحصائيات</button>
      </div>
      
      <!-- Messages Tab -->
      <div id="messagesContent" class="tab-content flex-col gap-6 flex">
"""

    stats_html = """
      </div> <!-- End Messages Tab -->

      <!-- Stats Tab -->
      <div id="statsContent" class="tab-content hidden flex-col gap-8">
        
        <!-- General Stats -->
        <div class="bg-cardDark p-6 rounded-2xl border border-white/10 flex justify-between items-center shadow-lg">
          <div>
            <h2 class="text-xl font-bold text-white mb-1">النقرات على زر "رؤية الخريجين"</h2>
            <p class="text-sm text-textMuted">كم مرة تم الضغط على الزر في الصفحة الرئيسية</p>
          </div>
          <div class="text-2xl px-6 py-3 rounded-xl bg-primaryTeal/20 text-primaryTeal font-extrabold border border-primaryTeal/30">
            <span id="generalViewsCount">0</span>
          </div>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
          <!-- Students Stats -->
          <div class="bg-cardDark p-6 rounded-2xl border border-white/10 shadow-lg flex flex-col max-h-[500px]">
            <h2 class="text-xl font-bold text-white mb-4">زيارات ملفات الخريجين</h2>
            <div class="overflow-y-auto pr-2 custom-scrollbar flex-1 flex flex-col gap-3" id="studentsStatsList">
              <div class="text-center py-10"><i class="ph ph-spinner animate-spin text-3xl text-primaryTeal"></i></div>
            </div>
          </div>

          <!-- Projects Stats -->
          <div class="bg-cardDark p-6 rounded-2xl border border-white/10 shadow-lg flex flex-col max-h-[500px]">
            <h2 class="text-xl font-bold text-white mb-4">زيارات المشاريع</h2>
            <div class="overflow-y-auto pr-2 custom-scrollbar flex-1 flex flex-col gap-3" id="projectsStatsList">
              <div class="text-center py-10"><i class="ph ph-spinner animate-spin text-3xl text-primaryTeal"></i></div>
            </div>
          </div>
        </div>
      </div> <!-- End Stats Tab -->
"""

    content = content.replace('<div class="bg-cardDark p-6 rounded-2xl border border-white/10 flex justify-between items-center">', tabs_html + '<div class="bg-cardDark p-6 rounded-2xl border border-white/10 flex justify-between items-center">')
    
    content = content.replace('      <div id="adminCommentsList" class="flex flex-col gap-4">\n        <!-- Loading -->\n        <div class="text-center py-10">\n          <i class="ph ph-spinner animate-spin text-4xl text-primaryTeal"></i>\n        </div>\n      </div>', '      <div id="adminCommentsList" class="flex flex-col gap-4">\n        <!-- Loading -->\n        <div class="text-center py-10">\n          <i class="ph ph-spinner animate-spin text-4xl text-primaryTeal"></i>\n        </div>\n      </div>' + stats_html)

    with open(admin_html_path, 'w', encoding='utf-8') as f:
        f.write(content)


admin_js_path = r'd:\flutter\project\flash\it_graduation_showcase\admin.js'
with open(admin_js_path, 'r', encoding='utf-8') as f:
    js_content = f.read()

if 'loadStats' not in js_content:
    # Add imports for getDocs, collection
    if 'getDocs' not in js_content:
        js_content = js_content.replace('getFirestore, collection, onSnapshot, query, orderBy, doc, updateDoc, deleteDoc', 'getFirestore, collection, onSnapshot, query, orderBy, doc, updateDoc, deleteDoc, getDocs')

    stats_logic = """

// Tabs Logic
const tabMessages = document.getElementById('tabMessages');
const tabStats = document.getElementById('tabStats');
const messagesContent = document.getElementById('messagesContent');
const statsContent = document.getElementById('statsContent');

if(tabMessages && tabStats) {
  tabMessages.addEventListener('click', () => {
    tabMessages.classList.add('active-tab', 'text-primaryTeal', 'border-primaryTeal');
    tabMessages.classList.remove('text-textMuted', 'border-transparent');
    tabStats.classList.remove('active-tab', 'text-primaryTeal', 'border-primaryTeal');
    tabStats.classList.add('text-textMuted', 'border-transparent');
    
    messagesContent.classList.remove('hidden');
    messagesContent.classList.add('flex');
    statsContent.classList.add('hidden');
    statsContent.classList.remove('flex');
  });

  tabStats.addEventListener('click', () => {
    tabStats.classList.add('active-tab', 'text-primaryTeal', 'border-primaryTeal');
    tabStats.classList.remove('text-textMuted', 'border-transparent');
    tabMessages.classList.remove('active-tab', 'text-primaryTeal', 'border-primaryTeal');
    tabMessages.classList.add('text-textMuted', 'border-transparent');
    
    statsContent.classList.remove('hidden');
    statsContent.classList.add('flex');
    messagesContent.classList.add('hidden');
    messagesContent.classList.remove('flex');
    
    loadStats();
  });
}

// Stats Logic
let statsLoaded = false;
async function loadStats() {
  if (statsLoaded) return;
  
  try {
    // 1. Fetch metadata (Students & Projects) to map IDs to Names
    const [studentsRes, projectsRes] = await Promise.all([
      fetch('data/students.json'),
      fetch('data/projects.json')
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
    generalSnap.forEach(doc => {
      if(doc.id === 'view_graduates_btn') {
        totalBtnClicks = doc.data().views || 0;
      }
    });
    document.getElementById('generalViewsCount').innerText = totalBtnClicks;
    
    // 3. Fetch Students Stats
    const studentsSnap = await getDocs(collection(db, 'students_analytics'));
    let studentsStats = [];
    studentsSnap.forEach(doc => {
      studentsStats.push({ id: doc.id, views: doc.data().views || 0 });
    });
    studentsStats.sort((a, b) => b.views - a.views);
    
    const studentsListEl = document.getElementById('studentsStatsList');
    studentsListEl.innerHTML = '';
    if(studentsStats.length === 0) {
      studentsListEl.innerHTML = '<p class="text-textMuted text-center text-sm">لا توجد بيانات بعد.</p>';
    } else {
      studentsStats.forEach(stat => {
        const name = studentsMap[stat.id] || `خريج #${stat.id}`;
        studentsListEl.innerHTML += `
          <div class="flex justify-between items-center bg-bgDark p-3 rounded-lg border border-white/5">
            <span class="text-sm font-semibold">${name}</span>
            <span class="bg-primaryTeal/20 text-primaryTeal px-2 py-1 rounded text-xs font-bold">${stat.views} زيارة</span>
          </div>
        `;
      });
    }
    
    // 4. Fetch Projects Stats
    const projectsSnap = await getDocs(collection(db, 'projects_analytics'));
    let projectsStats = [];
    projectsSnap.forEach(doc => {
      projectsStats.push({ id: doc.id, views: doc.data().views || 0 });
    });
    projectsStats.sort((a, b) => b.views - a.views);
    
    const projectsListEl = document.getElementById('projectsStatsList');
    projectsListEl.innerHTML = '';
    if(projectsStats.length === 0) {
      projectsListEl.innerHTML = '<p class="text-textMuted text-center text-sm">لا توجد بيانات بعد.</p>';
    } else {
      projectsStats.forEach(stat => {
        const name = projectsMap[stat.id] || `مشروع #${stat.id}`;
        projectsListEl.innerHTML += `
          <div class="flex justify-between items-center bg-bgDark p-3 rounded-lg border border-white/5">
            <span class="text-sm font-semibold truncate max-w-[70%]">${name}</span>
            <span class="bg-primaryTeal/20 text-primaryTeal px-2 py-1 rounded text-xs font-bold whitespace-nowrap">${stat.views} زيارة</span>
          </div>
        `;
      });
    }
    
    statsLoaded = true;
  } catch (error) {
    console.error("Error loading stats:", error);
  }
}
"""
    
    js_content += stats_logic
    with open(admin_js_path, 'w', encoding='utf-8') as f:
        f.write(js_content)

print("UI updated")
