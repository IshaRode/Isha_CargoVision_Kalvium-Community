import os
import glob
import re

# Fix imports in all pages
pages = glob.glob('pages/*.py')
for page in pages:
    with open(page, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # We want to remove all indentation inside the st.markdown HTML strings
    # We can do this by regex replacing lines that start with spaces or quotes inside st.markdown
    
    lines = content.split('\n')
    new_lines = []
    in_markdown = False
    for line in lines:
        if 'st.markdown(' in line and 'unsafe_allow_html=True' not in line:
            in_markdown = True
            new_lines.append(line)
        elif 'unsafe_allow_html=True' in line:
            in_markdown = False
            new_lines.append(line)
        elif in_markdown:
            # strip leading spaces but keep the quotes
            stripped = line.lstrip()
            # if it starts with quote, make sure we don't accidentally remove actual content
            new_lines.append(stripped)
        else:
            new_lines.append(line)
            
    with open(page, 'w', encoding='utf-8') as f:
        f.write('\n'.join(new_lines))

print("Fixed indentation in all pages!")
