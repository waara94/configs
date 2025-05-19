svn export https://svn.example.com/repo/path/trunk project-folder

svn export: Checks out the latest code without version control metadata.

project-folder: Destination folder for the exported code.

cd project-folder
git init
git add .
git commit -m "Initial import from SVN (no history)"

Create an empty GitHub repository first (no README or .gitignore), then:

bash
Kopiera
Redigera
git remote add origin https://github.com/your-username/your-repo.git
git branch -M main  # Optional, to set 'main' as default
git push -u origin main