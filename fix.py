import os
import glob
import re

# 1. Fix imports in all pages
pages = glob.glob('pages/*.py')
for page in pages:
    with open(page, 'r', encoding='utf-8') as f:
        content = f.read()
    content = content.replace('render_sidebar', 'render_dashboard_sidebar')
    with open(page, 'w', encoding='utf-8') as f:
        f.write(content)

# 2. Function to strip indentation from HTML in python files
def fix_html_indentation(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    new_lines = []
    in_html = False
    for line in lines:
        if 'st.markdown("""' in line or 'st.markdown(\'\'\'' in line:
            in_html = True
            new_lines.append(line)
            continue
            
        if '""", unsafe_allow_html=True)' in line or "''', unsafe_allow_html=True)" in line:
            in_html = False
            new_lines.append(line)
            continue
            
        if in_html and line.strip().startswith('<'):
            new_lines.append(line.lstrip())
        else:
            new_lines.append(line)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.writelines(new_lines)

fix_html_indentation('pages/dashboard.py')
fix_html_indentation('pages/warehouse_intelligence.py')
fix_html_indentation('components/sidebar.py')

print('Fixed all pages')
