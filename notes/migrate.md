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


rule FastRegexExample
{
  meta:
    description = "Match 32‑char hex strings only in small files"
  strings:
    $hex_prefilter = /[0-9A-Fa-f]{4}/    // quick 4‑hex nibble match
    $full_hex     = /^[0-9A-Fa-f]{32}$/  // full 32 hex chars
  condition:
    filesize < 50KB and                   // 1) small file?
    $hex_prefilter and                    // 2) does it even have hex?
    $full_hex                             // 3) run the full regex
}

yara --benchmark my_rules.yar samples/
