import { initializeApp } from "https://www.gstatic.com/firebasejs/10.8.1/firebase-app.js";
import { getAuth, signInWithEmailAndPassword, signOut, onAuthStateChanged } from "https://www.gstatic.com/firebasejs/10.8.1/firebase-auth.js";
import { getFirestore, collection, onSnapshot, query, orderBy, doc, updateDoc, deleteDoc, getDocs } from "https://www.gstatic.com/firebasejs/10.8.1/firebase-firestore.js";

const firebaseConfig = {
  apiKey: "AIzaSyDuPkuqMA9mcQoYhHTBttz71X8HwjKTQQ0",
  authDomain: "graduates-de1c9.firebaseapp.com",
  projectId: "graduates-de1c9",
  storageBucket: "graduates-de1c9.firebasestorage.app",
  messagingSenderId: "1094090662082",
  appId: "1:1094090662082:web:732784f6bf94691fa0db5b",
  measurementId: "G-X8L9MB5YE7"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const auth = getAuth(app);
const db = getFirestore(app);

// DOM Elements
const loginSection = document.getElementById('loginSection');
const dashboardSection = document.getElementById('dashboardSection');
const loginForm = document.getElementById('loginForm');
const emailInput = document.getElementById('email');
const passwordInput = document.getElementById('password');
const loginError = document.getElementById('loginError');
const loginBtn = document.getElementById('loginBtn');
const logoutBtn = document.getElementById('logoutBtn');
const listContainer = document.getElementById('adminCommentsList');
const totalCount = document.getElementById('totalCount');

let unsubscribeSnapshot = null;

// Handle Auth State
onAuthStateChanged(auth, (user) => {
  if (user) {
    // Logged in
    loginSection.classList.add('hidden');
    dashboardSection.classList.remove('hidden');
    dashboardSection.classList.add('flex');
    logoutBtn.classList.remove('hidden');
    loadComments();
  } else {
    // Logged out
    loginSection.classList.remove('hidden');
    dashboardSection.classList.add('hidden');
    dashboardSection.classList.remove('flex');
    logoutBtn.classList.add('hidden');
    if (unsubscribeSnapshot) unsubscribeSnapshot();
  }
});

// Handle Login
loginForm.addEventListener('submit', async (e) => {
  e.preventDefault();
  const email = emailInput.value.trim();
  const password = passwordInput.value;
  
  loginBtn.disabled = true;
  loginBtn.innerHTML = '<i class="ph ph-spinner animate-spin"></i> جاري الدخول...';
  loginError.classList.add('hidden');

  try {
    await signInWithEmailAndPassword(auth, email, password);
  } catch (error) {
    loginError.textContent = "البريد الإلكتروني أو كلمة المرور غير صحيحة.";
    loginError.classList.remove('hidden');
    loginBtn.disabled = false;
    loginBtn.innerHTML = '<span>دخول</span><i class="ph ph-sign-in"></i>';
  }
});

// Handle Logout
logoutBtn.addEventListener('click', () => {
  signOut(auth);
  loginBtn.disabled = false;
  loginBtn.innerHTML = '<span>دخول</span><i class="ph ph-sign-in"></i>';
});

// Format date
function formatDate(date) {
  if (!date) return 'الآن';
  return new Intl.DateTimeFormat('ar-SA', { 
    year: 'numeric', month: 'long', day: 'numeric', 
    hour: 'numeric', minute: 'numeric'
  }).format(date);
}

// Global functions for buttons
window.toggleApproval = async (id, currentStatus) => {
  try {
    await updateDoc(doc(db, "guestbook", id), {
      approved: !currentStatus
    });
  } catch (e) {
    alert("حدث خطأ أثناء التحديث.");
    console.error(e);
  }
};

window.deleteComment = async (id) => {
  if(confirm('هل أنت متأكد من حذف هذه الرسالة نهائياً؟')) {
    try {
      await deleteDoc(doc(db, "guestbook", id));
    } catch (e) {
      alert("حدث خطأ أثناء الحذف.");
      console.error(e);
    }
  }
};

// Render Admin Comment
function createAdminCommentElement(id, comment) {
  const isApproved = comment.approved || false;
  const statusBadge = isApproved 
    ? '<span class="px-2 py-1 bg-green-500/20 text-green-400 text-xs rounded-full border border-green-500/30">معروض للجمهور ✅</span>'
    : '<span class="px-2 py-1 bg-yellow-500/20 text-yellow-400 text-xs rounded-full border border-yellow-500/30">مخفي 👁️‍🗨️</span>';

  const toggleBtnClass = isApproved 
    ? 'bg-yellow-500/10 text-yellow-400 hover:bg-yellow-500/20 border-yellow-500/20' 
    : 'bg-green-500/10 text-green-400 hover:bg-green-500/20 border-green-500/20';
  
  const toggleBtnText = isApproved ? 'إخفاء التعليق' : 'عرض للجمهور';
  const toggleIcon = isApproved ? 'ph-eye-slash' : 'ph-eye';

  return `
    <div class="bg-cardDark p-5 rounded-2xl border ${isApproved ? 'border-primaryTeal/30' : 'border-white/5'} animate-fade-in flex flex-col md:flex-row gap-4 justify-between items-start md:items-center">
      <div class="flex-1">
        <div class="flex items-center gap-3 mb-2">
          <h4 class="text-white font-bold text-lg">${comment.name}</h4>
          ${statusBadge}
        </div>
        <span class="text-xs text-textMuted block mb-2">${formatDate(comment.timestamp?.toDate())}</span>
        <p class="text-textLight leading-relaxed whitespace-pre-line">${comment.message}</p>
      </div>
      
      <div class="flex gap-2 w-full md:w-auto">
        <button onclick="toggleApproval('${id}', ${isApproved})" class="flex-1 md:flex-none px-4 py-2 rounded-lg border transition flex justify-center items-center gap-2 ${toggleBtnClass}">
          <span>${toggleBtnText}</span>
          <i class="ph ${toggleIcon}"></i>
        </button>
        <button onclick="deleteComment('${id}')" class="px-4 py-2 bg-red-500/10 text-red-400 hover:bg-red-500/20 border border-red-500/20 rounded-lg transition flex items-center justify-center">
          <i class="ph ph-trash"></i>
        </button>
      </div>
    </div>
  `;
}

// Load Comments
function loadComments() {
  const q = query(collection(db, "guestbook"), orderBy("timestamp", "desc"));
  
  unsubscribeSnapshot = onSnapshot(q, (snapshot) => {
    totalCount.textContent = snapshot.size;
    
    if (snapshot.empty) {
      listContainer.innerHTML = `
        <div class="text-center text-textMuted py-10 bg-cardDark/50 rounded-2xl border border-white/5">
          لا توجد أي رسائل حتى الآن.
        </div>
      `;
      return;
    }

    let html = '';
    snapshot.forEach((doc) => {
      html += createAdminCommentElement(doc.id, doc.data());
    });
    listContainer.innerHTML = html;
  }, (error) => {
    console.error("Error fetching comments:", error);
    listContainer.innerHTML = `
      <div class="text-center text-red-400 py-10 bg-red-900/10 rounded-2xl border border-red-500/20">
        خطأ في جلب البيانات. الرجاء التأكد من صلاحيات Firestore Rules.
      </div>
    `;
  });
}


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
        <div class="flex justify-between items-center bg-bgDark p-3 rounded-lg border border-white/5 group">
          <span class="text-sm font-semibold">${stat.name}</span>
          <div class="flex items-center gap-2">
            <span class="bg-primaryTeal/20 text-primaryTeal px-2 py-1 rounded text-xs font-bold">${stat.views} زيارة</span>
            <button data-action="delete" data-collection="students_analytics" data-id="${stat.id}" class="text-red-500/50 hover:text-red-500 hover:bg-red-500/10 p-1.5 rounded-lg transition-all opacity-0 group-hover:opacity-100" title="مسح الإحصائية">
              <i class="ph ph-trash text-lg"></i>
            </button>
          </div>
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
        <div class="flex justify-between items-center bg-bgDark p-3 rounded-lg border border-white/5 group">
          <span class="text-sm font-semibold truncate max-w-[60%]">${stat.name}</span>
          <div class="flex items-center gap-2">
            <span class="bg-primaryTeal/20 text-primaryTeal px-2 py-1 rounded text-xs font-bold whitespace-nowrap">${stat.views} زيارة</span>
            <button data-action="delete" data-collection="projects_analytics" data-id="${stat.id}" class="text-red-500/50 hover:text-red-500 hover:bg-red-500/10 p-1.5 rounded-lg transition-all opacity-0 group-hover:opacity-100" title="مسح الإحصائية">
              <i class="ph ph-trash text-lg"></i>
            </button>
          </div>
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
