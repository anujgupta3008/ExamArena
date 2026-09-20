import glob
import re

def fix_toast_syntax():
    for file in glob.glob('src/**/*.jsx', recursive=True):
        with open(file, 'r') as f:
            content = f.read()
        
        # We want to replace toast.('message', 'error') with toast.error('message')
        # We want to replace toast.('message', 'success') with toast.success('message')
        # We want to replace toast.('message', 'info') with toast('message')
        
        # Use regex to find `toast.\((.*?),\s*['"](.*?)['"]\)` or `toast\((.*?),\s*['"](.*?)['"]\)`
        content = re.sub(r'toast\.\((.*?),\s*[\'"]error[\'"]\)', r'toast.error(\1)', content)
        content = re.sub(r'toast\.\((.*?),\s*[\'"]success[\'"]\)', r'toast.success(\1)', content)
        content = re.sub(r'toast\.\((.*?),\s*[\'"]info[\'"]\)', r'toast(\1)', content)
        content = re.sub(r'toast\.\((.*?),\s*[\'"]warning[\'"]\)', r'toast(\1, { icon: "⚠️" })', content)
        
        # Also catch toast('msg', 'error')
        content = re.sub(r'toast\((.*?),\s*[\'"]error[\'"]\)', r'toast.error(\1)', content)
        content = re.sub(r'toast\((.*?),\s*[\'"]success[\'"]\)', r'toast.success(\1)', content)
        content = re.sub(r'toast\((.*?),\s*[\'"]info[\'"]\)', r'toast(\1)', content)
        content = re.sub(r'toast\((.*?),\s*[\'"]warning[\'"]\)', r'toast(\1, { icon: "⚠️" })', content)

        # Catch remaining toast.(
        content = content.replace('toast.(', 'toast(')
        
        with open(file, 'w') as f:
            f.write(content)

if __name__ == '__main__':
    fix_toast_syntax()
