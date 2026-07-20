// Global State
let studentsData = [];
let projectsData = [];

// Firebase Storage Helper
function getFirebaseImageUrl(localPath) {
  if (!localPath || typeof localPath !== 'string') return localPath;
  if (localPath.startsWith('http') || localPath.startsWith('data:')) return localPath;
  
  const cleanPath = localPath.replace('./images/', '').replace('../images/', '').replace(/^images\//, '');
  const encodedPath = encodeURIComponent(cleanPath);
  return `https://firebasestorage.googleapis.com/v0/b/graduates-de1c9.firebasestorage.app/o/${encodedPath}?alt=media`;
}

// DOM Elements
const studentsGrid = document.getElementById('studentsGrid');
const projectsGrid = document.getElementById('projectsGrid');
const searchInput = document.getElementById('searchInput');

// Initialize Application
async function init() {
  try {
    // Fetch data concurrently with cache buster
    const [studentsRes, projectsRes] = await Promise.all([
      fetch(`./data/students.json?t=${new Date().getTime()}`),
      fetch(`./data/projects.json?t=${new Date().getTime()}`)
    ]);

    studentsData = await studentsRes.json();
    projectsData = await projectsRes.json();

    // Sort students by name and projects by title
    studentsData.sort((a, b) => a.name.localeCompare(b.name, 'ar'));
    projectsData.sort((a, b) => a.title.localeCompare(b.title, 'ar'));

    // Map projects to students for easier access
    studentsData = studentsData.map(student => {
      const project = projectsData.find(p => p.id === student.project_id);
      return { ...student, project };
    });

    // Render initial data
    renderStudents(studentsData);
    renderProjects(projectsData);

    // Setup event listeners
    if(searchInput) {
      searchInput.addEventListener('input', handleSearch);
    }

    // Setup Mobile Menu Toggle
    const mobileMenuBtn = document.getElementById('mobileMenuBtn');
    const mobileMenu = document.getElementById('mobileMenu');
    const mobileMenuIcon = document.getElementById('mobileMenuIcon');
    
    if (mobileMenuBtn && mobileMenu && mobileMenuIcon) {
      mobileMenuBtn.addEventListener('click', () => {
        mobileMenu.classList.toggle('hidden');
        if (mobileMenu.classList.contains('hidden')) {
          mobileMenuIcon.classList.remove('ph-x');
          mobileMenuIcon.classList.add('ph-list');
        } else {
          mobileMenuIcon.classList.remove('ph-list');
          mobileMenuIcon.classList.add('ph-x');
        }
      });
    }

    // Setup Navbar scroll effect
    window.addEventListener('scroll', () => {
      const nav = document.getElementById('navbar');
      if (window.scrollY > 50) {
        nav.classList.add('shadow-lg', 'bg-bgDark/95');
        nav.classList.remove('bg-bgDark/80');
      } else {
        nav.classList.remove('shadow-lg', 'bg-bgDark/95');
        nav.classList.add('bg-bgDark/80');
      }
    });

  } catch (error) {
    console.error("Error loading data:", error);
    const errorMsg = '<div class="col-span-full text-center py-10 text-red-500">حدث خطأ أثناء تحميل البيانات. يرجى التأكد من رفع مجلد data بشكل صحيح.</div>';
    if(studentsGrid) studentsGrid.innerHTML = errorMsg;
    if(projectsGrid) projectsGrid.innerHTML = errorMsg;
  }
}

// Render Students Cards
function renderStudents(students) {
  if (!studentsGrid) return;

  if (students.length === 0) {
    studentsGrid.innerHTML = '<div class="col-span-full text-center py-10 text-textMuted">لا يوجد نتائج للبحث...</div>';
    return;
  }

  const html = students.map(student => {
    return `
      <div class="bg-cardDark rounded-2xl border border-white/5 hover:border-primaryTeal/50 transition-all group overflow-hidden flex flex-col shadow-lg h-full">
        <div class="relative aspect-[3/4] overflow-hidden bg-gradient-to-b from-cardDark to-bgDark">
          <!-- Graduate Image -->
          <img src="${getFirebaseImageUrl(student.image)}" alt="${student.name}" class="w-full h-full object-cover object-top opacity-90 group-hover:opacity-100 group-hover:scale-105 transition-all duration-500">
          <!-- Gradient Overlay -->
          <div class="absolute inset-0 bg-gradient-to-t from-bgDark via-bgDark/20 to-transparent"></div>
        </div>
        
        <div class="p-5 flex flex-col items-center text-center -mt-6 relative z-10 flex-1">
          <h3 class="text-[15px] sm:text-base font-bold text-white mb-1 drop-shadow-md px-4 w-full break-words leading-normal">${student.name}</h3>
          <span class="text-[11px] sm:text-xs text-primaryTeal mb-5 font-semibold px-4 break-words text-center">خريج تقنية المعلومات</span>
          
          <a href="student.html?id=${student.id}" class="mt-auto w-full border border-white/10 rounded-xl py-2.5 flex items-center justify-center gap-2 text-sm text-textMuted group-hover:bg-primaryTeal group-hover:text-white group-hover:border-primaryTeal transition-all shadow-sm">
            <span>عرض الملف الشخصي</span>
            <i class="ph ph-arrow-left"></i>
          </a>
        </div>
      </div>
    `;
  }).join('');

  studentsGrid.innerHTML = html;
}

// Render Projects Cards
function renderProjects(projects) {
  if (!projectsGrid) return;

  if (projects.length === 0) {
    projectsGrid.innerHTML = '<div class="col-span-full text-center py-10 text-textMuted">لا يوجد نتائج للبحث...</div>';
    return;
  }

  const html = projects.map((project, index) => {
    const gradients = [
      "from-teal-900 to-bgDark",
      "from-blue-900 to-bgDark",
      "from-indigo-900 to-bgDark",
      "from-emerald-900 to-bgDark",
      "from-cyan-900 to-bgDark"
    ];
    const icons = ["ph-rocket", "ph-code", "ph-cpu", "ph-globe-hemisphere-west", "ph-database"];
    const gradient = gradients[index % gradients.length];
    const icon = project.card_icon || icons[index % icons.length];

    return `
      <div class="bg-cardDark rounded-2xl border border-white/5 hover:border-primaryTeal/50 transition-all group overflow-hidden flex flex-col shadow-lg">
        <div class="h-48 flex items-center justify-center relative bg-gradient-to-b ${gradient}">
          <!-- Abstract Grid Pattern -->
          <div class="absolute inset-0 opacity-20 group-hover:opacity-40 transition-opacity duration-500" style="background-image: linear-gradient(rgba(255,255,255,0.1) 1px, transparent 1px), linear-gradient(90deg, rgba(255,255,255,0.1) 1px, transparent 1px); background-size: 20px 20px;"></div>
          
          <i class="ph ${icon} text-7xl text-white/20 group-hover:text-white/50 group-hover:scale-110 transition-all duration-700 relative z-10 drop-shadow-[0_0_15px_rgba(255,255,255,0.1)]"></i>
          <div class="absolute inset-0 bg-gradient-to-t from-cardDark via-transparent to-transparent z-10"></div>
          
          <div class="absolute top-4 right-4 bg-bgDark/80 backdrop-blur-md border border-white/10 px-3 py-1.5 rounded-full text-xs font-bold text-primaryTeal shadow-lg z-20">
            مشروع تخرج
          </div>
        </div>
        
        <div class="p-6 flex-1 flex flex-col relative z-10 -mt-2">
          <h3 class="text-xl font-bold text-white mb-3 drop-shadow-sm">${project.title}</h3>
          <p class="text-sm text-textMuted mb-6 flex-1 line-clamp-3 leading-relaxed">${project.description}</p>
          
          <a href="project.html?id=${project.id}" class="w-full border border-white/10 rounded-xl py-2.5 flex items-center justify-center gap-2 text-sm font-semibold text-textMuted group-hover:bg-primaryTeal group-hover:text-white group-hover:border-primaryTeal transition-all shadow-sm">
            <span>عرض التفاصيل</span>
            <i class="ph ph-arrow-left"></i>
          </a>
        </div>
      </div>
    `;
  }).join('');

  projectsGrid.innerHTML = html;
}

// Handle Search Input
function handleSearch(e) {
  const query = e.target.value.toLowerCase().trim();
  
  if (studentsGrid) {
    const filteredStudents = studentsData.filter(student => 
      student.name.toLowerCase().includes(query)
    );
    renderStudents(filteredStudents);
  }
  
  if (projectsGrid) {
    const filteredProjects = projectsData.filter(project => 
      project.title.toLowerCase().includes(query) || 
      project.description.toLowerCase().includes(query)
    );
    renderProjects(filteredProjects);
  }
}

// Check which page we are on and act accordingly
document.addEventListener('DOMContentLoaded', () => {
  const path = window.location.pathname;
  
  if (path.includes('student.html') || path.endsWith('/student')) {
    initStudentPage();
  } else if (path.includes('project.html') || path.endsWith('/project')) {
    initProjectPage();
  } else {
    // Assume index
    init();
  }
});

// Student Details Page Logic
async function initStudentPage() {
  const urlParams = new URLSearchParams(window.location.search);
  const studentId = parseInt(urlParams.get('id'));

  if (!studentId) {
    document.body.innerHTML = '<div class="text-center mt-20 text-2xl text-white">طالب غير موجود</div>';
    return;
  }

  try {
    const [studentsRes, projectsRes] = await Promise.all([
      fetch(`./data/students.json?t=${new Date().getTime()}`),
      fetch(`./data/projects.json?t=${new Date().getTime()}`)
    ]);
    const students = await studentsRes.json();
    const projects = await projectsRes.json();

    const student = students.find(s => s.id === studentId);
    if (!student) {
      document.getElementById('studentDetails').innerHTML = '<div class="text-center py-20 text-xl text-white">لم يتم العثور على الطالب.</div>';
      return;
    }

    const project = projects.find(p => p.id === student.project_id);

    // Populate DOM
    document.getElementById('sName').textContent = student.name;
    const sImageUrl = getFirebaseImageUrl(student.image);
    document.getElementById('sImage').src = sImageUrl;
    
    const bgImage = document.getElementById('sBgImage');
    if(bgImage) bgImage.src = sImageUrl;
    
    if (project) {
      document.getElementById('sProject').textContent = project.title;
      document.getElementById('sProjectLink').href = `project.html?id=${project.id}`;
      document.getElementById('sProjectLink').style.display = 'inline-flex';
    } else {
      document.getElementById('sProjectLink').style.display = 'none';
    }

  } catch (error) {
    console.error(error);
  }
}

// Project Details Page Logic
async function initProjectPage() {
  const urlParams = new URLSearchParams(window.location.search);
  let projectId = parseInt(urlParams.get('id'));

  // If no ID is provided, default to ID 4 (the detailed one) for demonstration
  if (!projectId) {
    projectId = 4; 
  }

  try {
    const [studentsRes, projectsRes] = await Promise.all([
      fetch(`./data/students.json?t=${new Date().getTime()}`),
      fetch(`./data/projects.json?t=${new Date().getTime()}`)
    ]);
    const students = await studentsRes.json();
    const projects = await projectsRes.json();

    const project = projects.find(p => p.id === projectId);
    if (!project) {
      document.getElementById('projectContainer').innerHTML = '<div class="text-center py-20 text-xl text-white">لم يتم العثور على المشروع.</div>';
      return;
    }

    const projectStudents = students.filter(s => s.project_id === projectId).sort((a, b) => a.name.localeCompare(b.name, 'ar'));

    // No hero image needed anymore
    const bgImage = document.getElementById('pBgImage');
    if(bgImage) bgImage.style.display = 'none';

    const meta = project.meta || { domain: "عام", type: "نظام", team_size: projectStudents.length + " أعضاء", year: "2026" };
    const stats = project.stats || [
      {icon: "ph-star", label: "مميز"}, {icon: "ph-code", label: "برمجة"}, {icon: "ph-desktop", label: "واجهات"}, {icon: "ph-check-circle", label: "مكتمل"}
    ];
    const about = project.about || project.description;
    const features = project.features || [
      {icon: "ph-check", title: "ميزة ١", description: "وصف الميزة الأولى هنا"},
      {icon: "ph-check", title: "ميزة ٢", description: "وصف الميزة الثانية هنا"},
      {icon: "ph-check", title: "ميزة ٣", description: "وصف الميزة الثالثة هنا"},
      {icon: "ph-check", title: "ميزة ٤", description: "وصف الميزة الرابعة هنا"}
    ];
    const technologies = project.technologies || [];

    let techHTML = '';
    if(technologies.length > 0 && typeof technologies[0] === 'object') {
      techHTML = technologies.map(t => `
        <div class="flex flex-col items-center justify-center gap-2">
          <div class="w-16 h-16 bg-cardDark border border-white/5 rounded-2xl flex items-center justify-center shadow-inner p-3">
            <img src="${t.icon}" alt="${t.name}" class="w-full h-full object-contain filter drop-shadow-md">
          </div>
          <span class="text-xs text-textMuted font-semibold text-center">${t.name}</span>
        </div>
      `).join('');
    } else {
      techHTML = technologies.map(t => `<span class="bg-primaryTeal/20 text-primaryTeal border border-primaryTeal/30 px-4 py-1.5 rounded-full text-sm font-semibold m-1">${t}</span>`).join('');
    }

    const teamHTML = projectStudents.map(s => `
      <a href="student.html?id=${s.id}" class="flex flex-col items-center gap-3 group">
        <div class="w-24 h-32 sm:w-28 sm:h-36 rounded-2xl border-4 border-cardDark bg-bgDark overflow-hidden relative shadow-lg group-hover:border-primaryTeal/50 transition-colors">
          <img src="${getFirebaseImageUrl(s.image)}" class="w-full h-full object-cover object-top">
          <div class="absolute inset-0 bg-primaryTeal/20 opacity-0 group-hover:opacity-100 transition-opacity"></div>
        </div>
        <span class="font-bold text-white text-sm sm:text-base text-center">${s.name}</span>
      </a>
    `).join('');

    const html = `
      <!-- Hero Card -->
      <div class="bg-cardDark rounded-[32px] border border-white/5 shadow-2xl overflow-hidden relative">
        <div class="absolute top-0 right-0 w-96 h-96 bg-primaryTeal/5 rounded-full blur-3xl -mr-20 -mt-20 pointer-events-none"></div>
        <div class="absolute bottom-0 left-0 w-96 h-96 bg-primaryTeal/5 rounded-full blur-3xl -ml-20 -mb-20 pointer-events-none"></div>
        
        <div class="flex flex-col items-center text-center">
          <div class="w-full p-8 sm:p-16 flex flex-col justify-center items-center relative z-10">
            <div class="inline-flex items-center gap-2 text-primaryTeal bg-primaryTeal/10 border border-primaryTeal/20 px-4 py-1.5 rounded-full text-sm font-bold w-max mb-6">
              <i class="ph ph-graduation-cap text-lg"></i>
              مشروع تخرج
            </div>
            
            <h1 class="text-4xl sm:text-5xl md:text-6xl font-extrabold text-white mb-6 font-readex leading-tight">${project.title}</h1>
            <p class="text-lg md:text-xl text-textMuted leading-relaxed mb-10 max-w-4xl">${about}</p>
            
            <div class="flex flex-wrap justify-center gap-3 mb-4">
              ${techHTML}
            </div>
          </div>
        </div>
      </div>

      <!-- Complex Grid Layout -->
      <div class="grid grid-cols-1 xl:grid-cols-12 gap-6 mt-2">
        
        <!-- Row 1: Features (12 cols) -->
        <div class="xl:col-span-12 bg-cardDark rounded-[32px] border border-white/5 p-8 flex flex-col">
          <h3 class="text-2xl font-bold text-white mb-8 text-center">أهم المميزات</h3>
          <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-4 gap-4 flex-1">
            ${features.map(f => `
              <div class="bg-cardLight border border-white/5 rounded-2xl p-5 flex flex-col items-center text-center gap-3 hover:bg-cardLight/80 transition-colors">
                <div class="w-14 h-14 shrink-0 rounded-full bg-bgDark border border-white/5 flex items-center justify-center text-primaryTeal text-3xl mb-2 shadow-inner">
                  <i class="ph ${f.icon}"></i>
                </div>
                <div>
                  <h4 class="font-bold text-white text-base mb-2">${f.title}</h4>
                  <p class="text-sm text-textMuted leading-relaxed">${f.description}</p>
                </div>
              </div>
            `).join('')}
          </div>
        </div>

        <!-- Row 2: Team (12 cols) -->
        <div class="xl:col-span-12 bg-cardDark rounded-[32px] border border-white/5 p-10 flex flex-col relative overflow-hidden">
          <div class="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-full h-full bg-primaryTeal/5 blur-[100px] pointer-events-none rounded-full"></div>
          <h3 class="text-3xl font-extrabold text-white mb-10 text-center font-readex z-10 relative">فريق العمل</h3>
          <div class="flex justify-center flex-wrap gap-8 sm:gap-12 mb-4 z-10 relative">
            ${teamHTML}
          </div>
        </div>

      </div>
    `;

    document.getElementById('projectContainer').innerHTML = html;

  } catch (error) {
    console.error(error);
  }
}
