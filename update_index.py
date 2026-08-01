import re

with open('index.html', 'r', encoding='utf-8') as f:
    idx_content = f.read()

analytics_script = """
  <script type="module" src="analytics.js"></script>
  <script type="module">
    import { trackView } from './analytics.js';
    
    function attachTracking(selector, docId) {
      document.querySelectorAll(selector).forEach(btn => {
        btn.addEventListener('click', (e) => {
          e.preventDefault();
          const href = btn.getAttribute('href');
          Promise.race([
            trackView('general_analytics', docId),
            new Promise(resolve => setTimeout(resolve, 500))
          ]).then(() => {
            window.location.href = href;
          });
        });
      });
    }

    // Hero Button
    attachTracking('#viewGraduatesBtn', 'view_graduates_btn');
    // Navbar links
    attachTracking('a[href="graduates.html"]:not(#viewGraduatesBtn)', 'nav_graduates_btn');
    attachTracking('a[href="projects.html"]', 'nav_projects_btn');
  </script>
"""

idx_content = re.sub(
    r'<script type="module" src="analytics\.js"></script>.*?</script>',
    analytics_script.strip(),
    idx_content,
    flags=re.DOTALL
)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(idx_content)

print('index.html updated')
