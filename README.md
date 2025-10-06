# Nicholas Pipala — Personal Portfolio

This repository contains a multi-page personal portfolio website for Nicholas Pipala. It demonstrates semantic HTML, responsive CSS, accessibility practices, and a contact form with inline client-side validation. The project was built with AI assistance; prompts and reflections are logged in `.prompt/dev_notes.md`.

Files of interest
- `index.html` — Home page
- `about/about.html` — About / bio + contact info
- `resume/resume.html` — Full resume content (provided by Nicholas)
- `projects/projects.html` — Project showcase (with descriptions and repo links)
- `contact/contact.html` — Contact form (client-side validation, redirects to `thankyou.html`)
- `styles.css` — Shared CSS
- `.prompt/dev_notes.md` — AI prompts used and reflection

How to run locally (static server)
1. Open PowerShell in the project root (where `index.html` lives).
2. Run:
```powershell
python -m http.server 8000
```
3. Open http://localhost:8000/index.html in your browser.

Repository

- GitHub Repo: https://github.com/nppipala123/AIDD-Assignment-5

Notes & next steps
- Replace project repository links with specific repos and add real screenshots.
- For production form handling, add a server-side endpoint or service (e.g., Netlify Forms).
- Consider adding `.gitignore` to exclude `.venv/` and other local files.

Contact
- Email: nppipala@iu.edu
- GitHub: https://github.com/nppipala123
- LinkedIn: https://www.linkedin.com/in/nicholaspipala
