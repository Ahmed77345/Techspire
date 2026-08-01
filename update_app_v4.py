with open('app_v4.js', 'r', encoding='utf-8') as f:
    js = f.read()

tracking_logic = """
// Track Navbar clicks across all pages
document.addEventListener('DOMContentLoaded', () => {
    function attachTrackingUrl(selector, docId) {
      document.querySelectorAll(selector).forEach(btn => {
        btn.addEventListener('click', (e) => {
          e.preventDefault();
          const href = btn.getAttribute('href');
          window.location.href = href + (href.includes('?') ? '&' : '?') + 'tracked=' + docId;
        });
      });
    }
    
    // Navbar links
    attachTrackingUrl('a[href="graduates.html"]:not(#viewGraduatesBtn)', 'nav_graduates_btn');
    attachTrackingUrl('a[href="projects.html"]', 'nav_projects_btn');
});
"""

js = js + '\n' + tracking_logic

with open('app_v4.js', 'w', encoding='utf-8') as f:
    f.write(js)

print('app_v4.js updated')
