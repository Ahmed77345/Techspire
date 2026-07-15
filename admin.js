import { initializeApp } from "https://www.gstatic.com/firebasejs/10.8.1/firebase-app.js";
import { getAuth, signInWithEmailAndPassword, signOut, onAuthStateChanged } from "https://www.gstatic.com/firebasejs/10.8.1/firebase-auth.js";
import { getFirestore, collection, onSnapshot, query, orderBy, doc, updateDoc, deleteDoc } from "https://www.gstatic.com/firebasejs/10.8.1/firebase-firestore.js";

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
