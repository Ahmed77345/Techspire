import { initializeApp } from "https://www.gstatic.com/firebasejs/10.8.1/firebase-app.js";
import { getFirestore, collection, addDoc, onSnapshot, query, orderBy, where, serverTimestamp } from "https://www.gstatic.com/firebasejs/10.8.1/firebase-firestore.js";

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
const db = getFirestore(app);

// Form Elements
const form = document.getElementById('guestbookForm');
const nameInput = document.getElementById('gbName');
const messageInput = document.getElementById('gbMessage');
const submitBtn = document.getElementById('gbSubmitBtn');
const statusText = document.getElementById('gbStatus');
const listContainer = document.getElementById('guestbookList');

// Format date nicely
function formatDate(date) {
  if (!date) return 'الآن';
  return new Intl.DateTimeFormat('ar-SA', { 
    year: 'numeric', month: 'long', day: 'numeric', 
    hour: 'numeric', minute: 'numeric'
  }).format(date);
}

// Render a single comment
function createCommentElement(comment) {
  return `
    <div class="bg-cardDark p-5 rounded-2xl border border-white/5 animate-fade-in">
      <div class="flex items-center gap-3 mb-3">
        <div class="w-10 h-10 rounded-full bg-primaryTeal/20 flex items-center justify-center text-primaryTeal font-bold text-lg">
          ${comment.name.charAt(0)}
        </div>
        <div>
          <h4 class="text-white font-bold">${comment.name}</h4>
          <span class="text-xs text-textMuted">${formatDate(comment.timestamp?.toDate())}</span>
        </div>
      </div>
      <p class="text-textLight leading-relaxed whitespace-pre-line">${comment.message}</p>
    </div>
  `;
}

// Listen to approved messages in real-time
if (listContainer) {
  const q = query(collection(db, "guestbook"), where("approved", "==", true));
  onSnapshot(q, (snapshot) => {
    if (snapshot.empty) {
      listContainer.innerHTML = `
        <div class="text-center text-textMuted py-10 flex flex-col items-center gap-3 bg-cardDark/50 rounded-2xl border border-white/5">
          <i class="ph ph-chat-teardrop text-4xl text-primaryTeal/50"></i>
          <span>لا توجد آراء معروضة حالياً. كن أول من يكتب! 🎓</span>
        </div>
      `;
      return;
    }

    // Sort documents client-side to avoid needing a Firestore Composite Index
    const docs = [];
    snapshot.forEach((doc) => docs.push(doc.data()));
    
    docs.sort((a, b) => {
      const timeA = a.timestamp?.toMillis() || 0;
      const timeB = b.timestamp?.toMillis() || 0;
      return timeB - timeA; // Descending (newest first)
    });

    let html = '';
    docs.forEach((data) => {
      html += createCommentElement(data);
    });
    
    listContainer.innerHTML = html;
  }, (error) => {
    console.error("Error fetching comments:", error);
    // If it fails (e.g. permission error), just show empty gracefully
    listContainer.innerHTML = `
      <div class="text-center text-red-400 py-10 bg-cardDark/50 rounded-2xl border border-white/5">
        جاري تهيئة الآراء، يرجى المحاولة لاحقاً.
      </div>
    `;
  });
}

// Handle form submission
if (form) {
  form.addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const name = nameInput.value.trim();
    const message = messageInput.value.trim();
    
    if (!name || !message) return;

    // Loading state
    submitBtn.disabled = true;
    submitBtn.innerHTML = '<i class="ph ph-spinner animate-spin"></i> جاري الإرسال...';
    
    try {
      await addDoc(collection(db, "guestbook"), {
        name: name,
        message: message,
        approved: false, // Default to false (hidden from public)
        timestamp: serverTimestamp()
      });
      
      // Success
      form.reset();
      statusText.textContent = "تم إرسال رسالتك بنجاح! شكراً لك ❤️ (سيتم مراجعتها قبل النشر)";
      statusText.className = "text-sm text-center text-green-400 mt-2 block animate-fade-in";
      
      setTimeout(() => {
        statusText.classList.add('hidden');
      }, 3000);
      
    } catch (e) {
      console.error("Error adding document: ", e);
      statusText.textContent = "حدث خطأ أثناء الإرسال، يرجى المحاولة لاحقاً.";
      statusText.className = "text-sm text-center text-red-400 mt-2 block animate-fade-in";
    } finally {
      // Reset button
      submitBtn.disabled = false;
      submitBtn.innerHTML = '<span>إرسال التهنئة</span><i class="ph ph-paper-plane-right"></i>';
    }
  });
}
