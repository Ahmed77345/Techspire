with open('admin.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Replace the flex justify-end mb-6 to include the new button
old_flex = '<div class="flex justify-end mb-6">'
new_flex = """
        <div class="flex justify-end mb-6 gap-3">
          <button id="openClearStatsModalBtn" class="inline-flex items-center gap-2 bg-red-600/20 hover:bg-red-600/40 text-red-400 border border-red-500/30 px-4 py-2 rounded-lg font-bold transition-all shadow-[0_0_15px_rgba(220,38,38,0.2)]">
            <i class="ph ph-trash"></i>
            مسح البيانات
          </button>
"""
html = html.replace(old_flex, new_flex)

# Add Modal at the end of the body
modal_html = """
  <!-- Clear Stats Modal -->
  <div id="clearStatsModal" class="fixed inset-0 bg-black/80 backdrop-blur-sm z-[100] hidden flex items-center justify-center opacity-0 transition-opacity duration-300">
    <div class="bg-bgDark border border-white/10 p-8 rounded-2xl w-full max-w-md transform scale-95 transition-transform duration-300">
      <h3 class="text-2xl font-bold text-white mb-2">مسح الإحصائيات</h3>
      <p class="text-textMuted mb-6 text-sm">اختر البيانات التي تريد تصفيرها. لا يمكن التراجع عن هذا الإجراء.</p>
      
      <div class="flex flex-col gap-3 mb-8">
        <button id="clearGeneralBtn" class="w-full text-right bg-white/5 hover:bg-white/10 border border-white/5 p-4 rounded-xl text-white font-semibold transition-all flex justify-between items-center group">
          <span>إحصائيات الأزرار (الرئيسية والقائمة)</span>
          <i class="ph ph-trash text-red-400 opacity-0 group-hover:opacity-100 transition-opacity"></i>
        </button>
        <button id="clearStudentsBtn" class="w-full text-right bg-white/5 hover:bg-white/10 border border-white/5 p-4 rounded-xl text-white font-semibold transition-all flex justify-between items-center group">
          <span>زيارات الخريجين</span>
          <i class="ph ph-trash text-red-400 opacity-0 group-hover:opacity-100 transition-opacity"></i>
        </button>
        <button id="clearProjectsBtn" class="w-full text-right bg-white/5 hover:bg-white/10 border border-white/5 p-4 rounded-xl text-white font-semibold transition-all flex justify-between items-center group">
          <span>زيارات المشاريع</span>
          <i class="ph ph-trash text-red-400 opacity-0 group-hover:opacity-100 transition-opacity"></i>
        </button>
        <button id="clearAllBtn" class="w-full text-right bg-red-600/20 hover:bg-red-600/30 border border-red-500/20 p-4 rounded-xl text-red-400 font-semibold transition-all flex justify-between items-center mt-2">
          <span>مسح جميع الإحصائيات بالكامل!</span>
          <i class="ph ph-warning-circle text-xl"></i>
        </button>
      </div>
      
      <div class="flex justify-end">
        <button id="closeClearStatsModalBtn" class="bg-white/10 hover:bg-white/20 text-white px-6 py-2 rounded-lg font-bold transition-all">
          إلغاء
        </button>
      </div>
    </div>
  </div>
"""

# Increase cache buster for admin.js
html = html.replace('admin.js?v=4', 'admin.js?v=6')

html = html.replace('</body>', modal_html + '\n</body>')

with open('admin.html', 'w', encoding='utf-8') as f:
    f.write(html)
print('HTML updated')
