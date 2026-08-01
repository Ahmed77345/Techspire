import re

# Update index.html to use URL params instead of localStorage
with open('index.html', 'r', encoding='utf-8') as f:
    idx = f.read()

script = """
  <script>
    // Track clicks reliably using URL Parameters (to bypass Tracking Prevention)
    function attachTrackingUrl(selector, docId) {
      document.querySelectorAll(selector).forEach(btn => {
        btn.addEventListener('click', (e) => {
          e.preventDefault();
          const href = btn.getAttribute('href');
          window.location.href = href + (href.includes('?') ? '&' : '?') + 'tracked=' + docId;
        });
      });
    }

    document.addEventListener('DOMContentLoaded', () => {
        attachTrackingUrl('#viewGraduatesBtn', 'view_graduates_btn');
        attachTrackingUrl('a[href="graduates.html"]:not(#viewGraduatesBtn)', 'nav_graduates_btn');
        attachTrackingUrl('a[href="projects.html"]', 'nav_projects_btn');
    });
  </script>
"""

idx = re.sub(
    r'<script>\s*// Track clicks reliably using localStorage.*?</script>',
    script.strip(),
    idx,
    flags=re.DOTALL
)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(idx)

# Update analytics.js to read from URL and clean up localStorage logic
with open('analytics.js', 'r', encoding='utf-8') as f:
    analytics = f.read()

url_logic = """
// Process pending clicks from URL (Reliable tracking)
const urlParams = new URLSearchParams(window.location.search);
const tracked = urlParams.get('tracked');
if (tracked) {
    trackView('general_analytics', tracked);
    // Remove it from URL so it doesn't track again on refresh
    urlParams.delete('tracked');
    const newSearch = urlParams.toString() ? '?' + urlParams.toString() : '';
    window.history.replaceState({}, document.title, window.location.pathname + newSearch + window.location.hash);
}
"""

analytics = re.sub(
    r'// Process pending clicks from localStorage.*',
    url_logic.strip(),
    analytics,
    flags=re.DOTALL
)

with open('analytics.js', 'w', encoding='utf-8') as f:
    f.write(analytics)

print('URL tracking implemented')
