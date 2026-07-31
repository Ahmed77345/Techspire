import { initializeApp } from "https://www.gstatic.com/firebasejs/10.8.1/firebase-app.js";
import { getFirestore, doc, setDoc, increment } from "https://www.gstatic.com/firebasejs/10.8.1/firebase-firestore.js";

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

/**
 * Track a view in Firestore.
 * @param {string} collectionName - Collection name (e.g., 'students_analytics', 'projects_analytics', 'general_analytics')
 * @param {string} docId - Document ID to track (e.g., student ID, project ID, or 'view_graduates_btn')
 */
export async function trackView(collectionName, docId) {
    if (!docId) return;
    
    // Ensure docId is a string for Firestore
    const idString = String(docId);
    
    try {
        const docRef = doc(db, collectionName, idString);
        await setDoc(docRef, {
            views: increment(1),
            lastViewedAt: new Date()
        }, { merge: true });
        console.log(`Tracked view for ${collectionName}/${idString}`);
    } catch (error) {
        console.error("Error tracking view:", error);
    }
}

window.trackView = trackView; // make it globally available for easy access if needed
