import glob

files = glob.glob('*.py') + glob.glob('pages/*.py')
for f in files:
    with open(f, 'r', encoding='utf-8') as file:
        content = file.read()
    
    new_content = content.replace('from components.top_navigation import get_top_nav_html', 'from components.top_navigation import get_top_nav_html')
    
    with open(f, 'w', encoding='utf-8') as file:
        file.write(new_content)
        
print("Successfully updated imports!")
