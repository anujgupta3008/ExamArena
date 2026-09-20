import os
import glob

def refactor_toasts():
    for file in glob.glob('src/**/*.jsx', recursive=True):
        with open(file, 'r') as f:
            content = f.read()
        
        if 'addToast' in content:
            print(f"Refactoring {file}...")
            # Remove addToast from component props
            content = content.replace('{ addToast }', '{}')
            content = content.replace('addToast?.', 'toast.')
            content = content.replace('addToast(', 'toast(')
            content = content.replace('if (addToast) toast(', 'toast(')
            content = content.replace('if (addToast) {', '{')
            content = content.replace('addToast:', 'toast:')
            
            # Add import toast from 'react-hot-toast'; at the top
            if "import toast from 'react-hot-toast';" not in content:
                content = "import toast from 'react-hot-toast';\n" + content
                
            with open(file, 'w') as f:
                f.write(content)

if __name__ == '__main__':
    refactor_toasts()
