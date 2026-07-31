import os

def insert_analytics(file_path, type_prefix):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if 'analytics.js' in content:
        return
        
    script_tag = f"""
  <!-- Analytics -->
  <script type="module" src="analytics.js"></script>
  <script type="module">
    import {{ trackView }} from './analytics.js';
    
    document.addEventListener('DOMContentLoaded', () => {{
      const params = new URLSearchParams(window.location.search);
      const id = params.get('id');
      if (id) {{
        trackView('{type_prefix}_analytics', id);
      }}
    }});
  </script>
"""
    
    # Insert before </body>
    content = content.replace('</body>', script_tag + '</body>')
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

insert_analytics(r'd:\flutter\project\flash\it_graduation_showcase\student.html', 'students')
insert_analytics(r'd:\flutter\project\flash\it_graduation_showcase\project.html', 'projects')
