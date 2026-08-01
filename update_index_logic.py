import re

with open('index.html', 'r', encoding='utf-8') as f:
    idx = f.read()

script = """
  <!-- Swiper JS -->
  <script src="https://cdn.jsdelivr.net/npm/swiper@11/swiper-bundle.min.js"></script>
  
  <script>
    // Track clicks reliably using localStorage
    function attachTrackingStorage(selector, storageKey) {
      document.querySelectorAll(selector).forEach(btn => {
        btn.addEventListener('click', () => {
          localStorage.setItem(storageKey, 'true');
        });
      });
    }

    document.addEventListener('DOMContentLoaded', () => {
        // Hero Button
        attachTrackingStorage('#viewGraduatesBtn', 'track_view_graduates_btn');
        // Navbar links
        attachTrackingStorage('a[href="graduates.html"]:not(#viewGraduatesBtn)', 'track_nav_graduates_btn');
        attachTrackingStorage('a[href="projects.html"]', 'track_nav_projects_btn');
    });
  </script>
"""

idx = re.sub(
    r'<!-- Swiper JS -->.*?</script>\s*</script>',
    script.strip(),
    idx,
    flags=re.DOTALL
)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(idx)

print('index.html updated')
