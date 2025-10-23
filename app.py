from flask import Flask, Response, render_template, request, redirect, url_for
from DAL import getAllProjects, saveProjectDB  # type: ignore

app = Flask(__name__, static_folder='.', static_url_path='')


# Home page HTML as a single string
INDEX_HTML = """<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Home - Personal Portfolio</title>
  <link rel="stylesheet" href="/css/styles.css">
 </head>
<body>
  <header>
    <div class="container">
  <h1>Nicholas Pipala</h1>
      <nav>
        <a href="/" class="active">Home</a>
        <a href="/about">About</a>
        <a href="/resume">Resume</a>
        <a href="/projects">Projects</a>
        <a href="/contact">Contact</a>
    </nav>
    </div>
  </header>

  <main class="container">
    <section class="hero">
  <div class="profile-wrapper"><img srcset="/images/Professional_Headshot_200.jpg 200w, /images/Professional_Headshot_400.jpg 400w, /images/Professional_Headshot_800.jpg 800w" sizes="(max-width:800px) 140px, 180px" src="/images/Professional_Headshot_400.jpg" alt="Nicholas Pipala professional headshot" class="profile-photo"></div>
      <div>
        <h2>Hi — I'm Nicholas Pipala</h2>
        <p class="lead">MS in Information Systems (Kelley School of Business). I build data-driven solutions, automate business processes, and apply AI to solve practical problems.</p>
      <p>
        <a class="btn" href="/projects">View Projects</a>
        <a class="btn ghost" href="/resume">View Resume</a>
      </p>
        <p class="lead">GitHub: <a href="https://github.com/nppipala123">github.com/nppipala123</a></p>
      </div>
    </section>

    <section class="featured">
      <h3>Featured Projects</h3>
      <div class="grid">
        <article class="card">
          <img src="/images/download.png" alt="Workday Reporting Automation screenshot">
          <div class="card-body">
            <h4>Workday Reporting Automation</h4>
            <p>Automated custom Workday reports and APIs to streamline HR data exchanges and eliminate manual processes.</p>
            <p><a href="/projects">Learn more →</a></p>
          </div>
        </article>
        <article class="card">
          <img src="/images/download.jpg" alt="Power BI Quality Dashboards screenshot">
          <div class="card-body">
            <h4>Power BI Quality Dashboards</h4>
            <p>Power BI dashboards built on SQL Server data to improve shop floor quality tracking and insights.</p>
            <p><a href="/projects">Learn more →</a></p>
          </div>
        </article>
      </div>
    </section>
  </main>

  <footer>
    <div class="container">
        <p>&copy; 2025 Nicholas Pipala • <a href="https://github.com/nppipala123">GitHub: nppipala123</a> • <a href="mailto:nppipala@iu.edu">nppipala@iu.edu</a> • assignment 5: <a href="https://github.com/nppipala123/AIDD-Assignment-5">https://github.com/nppipala123/AIDD-Assignment-5</a></p>
    </div>
  </footer>
</body>
</html>
"""


# About page HTML as a single string
ABOUT_HTML = """<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>About Me</title>
  <link rel="stylesheet" href="/css/styles.css">
</head>
<body>
  <header>
    <div class="container">
      <h1>About Me</h1>
      <nav>
        <a href="/">Home</a>
  <a href="/about" class="active">About</a>
        <a href="/resume">Resume</a>
        <a href="/projects">Projects</a>
        <a href="/contact">Contact</a>
      </nav>
    </div>
  </header>

  <main class="container">
    <section class="profile">
      <div class="profile-wrapper"><img srcset="/images/Professional_Headshot_200.jpg 200w, /images/Professional_Headshot_400.jpg 400w, /images/Professional_Headshot_800.jpg 800w" sizes="(max-width:800px) 140px, 120px" src="/images/Professional_Headshot_400.jpg" alt="Professional headshot of Nicholas Pipala" class="profile-photo"></div>
      <div>
        <h2>Nicholas Pipala</h2>
        <p>I am a graduate student in the MS Information Systems program at Indiana University’s Kelley School of Business, graduating May 2026. I’m passionate about designing data-driven solutions that automate workflows and turn information into decisions. I’ve delivered Workday API integrations, built Power BI dashboards on SQL Server, and partnered with cross‑functional teams to improve operational outcomes.</p>
        <p>Previously, I completed my B.S. in Information Systems with minors in Business Analytics and Spanish. I enjoy taking complex technical topics and communicating them clearly to stakeholders.</p>
        <p>Contact: <a href="mailto:nppipala@iu.edu">nppipala@iu.edu</a> • Phone: 630-240-3467 • <a href="https://www.linkedin.com/in/nicholaspipala">LinkedIn</a> • GitHub: <a href="https://github.com/nppipala123">github.com/nppipala123</a></p>
      </div>
    </section>

    <section>
      <h3>Interests & Goals</h3>
      <p>I’m especially interested in consulting, analytics, and AI‑assisted development. Short‑term, I’m seeking full‑time opportunities where I can contribute to workflow automation, data visualization, and integration projects. Long‑term, I aim to lead data and AI initiatives that deliver measurable business value.</p>
    </section>
  </main>

  <footer>
    <div class="container">
      <p>&copy; 2025 Nicholas Pipala • <a href="https://github.com/nppipala123">GitHub: nppipala123</a> • <a href="mailto:nppipala@iu.edu">nppipala@iu.edu</a> • assignment 5: <a href="https://github.com/nppipala123/AIDD-Assignment-5">https://github.com/nppipala123/AIDD-Assignment-5</a></p>
    </div>
  </footer>
</body>
</html>
"""


# Contact page HTML as a single string
CONTACT_HTML = """<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Contact</title>
  <link rel="stylesheet" href="/css/styles.css">
  <script>
    function showError(input, message){
      const msg = input.parentElement.querySelector('.error-message');
      if(msg){ msg.textContent = message || ''; }
      input.classList.toggle('invalid', Boolean(message));
      if(message){ input.setAttribute('aria-invalid','true'); }
      else{ input.removeAttribute('aria-invalid'); }
    }

    function validateForm(e){
      const form = e.target;
      let valid = true;

      const first = form.first;
      const last = form.last;
      const email = form.email;
      const pw = form.password;
      const pw2 = form.confirm_password;

      if(!first.value.trim()) { showError(first, 'First name is required.'); valid = false; } else { showError(first); }
      if(!last.value.trim()) { showError(last, 'Last name is required.'); valid = false; } else { showError(last); }
      if(!email.validity.valid) { showError(email, 'Enter a valid email address.'); valid = false; } else { showError(email); }
      if(pw.value.length < 8) { showError(pw, 'Password must be at least 8 characters.'); valid = false; } else { showError(pw); }
      if(pw2.value !== pw.value) { showError(pw2, 'Passwords must match.'); valid = false; } else { showError(pw2); }

      if(!valid){ e.preventDefault(); }
      return valid;
    }

    document.addEventListener('DOMContentLoaded', ()=>{
      const form = document.getElementById('contactForm');
      if(!form) return;
      form.addEventListener('submit', validateForm);

      // Live validation
      ['first','last','email','password','confirm_password'].forEach(id =>{
        const input = document.getElementById(id);
        if(!input) return;
        input.addEventListener('input', ()=>{
          if(id === 'confirm_password'){
            showError(input, input.value === document.getElementById('password').value ? '' : 'Passwords must match.');
          } else if(id === 'email'){
            showError(input, input.validity.valid ? '' : 'Enter a valid email address.');
          } else if(id === 'password'){
            showError(input, input.value.length >= 8 ? '' : 'Password must be at least 8 characters.');
          } else {
            showError(input, input.value.trim() ? '' : 'This field is required.');
          }
        });
      });
    })
  </script>
</head>
<body>
  <header>
    <div class="container">
      <h1>Contact</h1>
      <nav>
        <a href="/">Home</a>
  <a href="/about">About</a>
        <a href="/resume">Resume</a>
        <a href="/projects">Projects</a>
        <a href="/contact" class="active">Contact</a>
      </nav>
    </div>
  </header>

  <main class="container">
    <section>
      <form id="contactForm" action="/thankyou" method="get" novalidate aria-describedby="formHelp">
        <div class="form-group">
          <label for="first">First Name</label>
          <input id="first" name="first" type="text" required aria-required="true">
          <div class="error-message" aria-live="polite"></div>
        </div>
        <div class="form-group">
          <label for="last">Last Name</label>
          <input id="last" name="last" type="text" required aria-required="true">
          <div class="error-message" aria-live="polite"></div>
        </div>
        <div class="form-group">
          <label for="email">Email</label>
          <input id="email" name="email" type="email" required pattern=".+@.+\..+" aria-required="true">
          <div class="error-message" aria-live="polite"></div>
        </div>
        <div class="form-group">
          <label for="password">Password</label>
          <input id="password" name="password" type="password" required minlength="8" aria-required="true">
          <div class="error-message" aria-live="polite"></div>
        </div>
        <div class="form-group">
          <label for="confirm_password">Confirm Password</label>
          <input id="confirm_password" name="confirm_password" type="password" required minlength="8" aria-required="true">
          <div class="error-message" aria-live="polite"></div>
        </div>
        <div class="form-group">
          <button type="submit" class="btn">Send</button>
        </div>
      </form>
    </section>
  </main>

  <footer>
    <div class="container">
      <p>&copy; 2025 Nicholas Pipala • <a href="https://github.com/nppipala123">GitHub: nppipala123</a> • <a href="mailto:nppipala@iu.edu">nppipala@iu.edu</a> • assignment 5: <a href="https://github.com/nppipala123/AIDD-Assignment-5">https://github.com/nppipala123/AIDD-Assignment-5</a></p>
    </div>
  </footer>
</body>
</html>
"""


## Remove hardcoded Projects HTML; use templates instead


# Resume page HTML as a single string
RESUME_HTML = """<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Resume</title>
  <link rel="stylesheet" href="/css/styles.css">
</head>
<body>
  <header>
    <div class="container">
      <h1>Resume</h1>
      <nav>
        <a href="/">Home</a>
  <a href="/about">About</a>
        <a href="/resume" class="active">Resume</a>
        <a href="/projects">Projects</a>
        <a href="/contact">Contact</a>
      </nav>
    </div>
  </header>

  <main class="container">
    <section class="resume">
      <h2>NICHOLAS PIPALA</h2>
      <p>nickpipala@gmail.com | 630-240-3467 | <a href="https://www.linkedin.com/in/nicholaspipala">www.linkedin.com/in/nicholaspipala</a></p>

      <h3>EDUCATION</h3>
      <p><strong>Indiana University, Kelley School of Business</strong> – Bloomington, IN <em>May 2026</em><br>
      Master of Science in Information Systems<br>
      • Graduate Assistantship: Awarded based on academic excellence in undergraduate coursework</p>

      <p><strong>Indiana University, Kelley School of Business</strong> – Bloomington, IN <em>May 2025</em><br>
      Bachelor of Science in Business; Major: Information Systems; Minors: Business Analytics; Spanish GPA: 3.72/4.00<br>
      • Deans Scholarship: Awarded $4,000/semester merit-based scholarship for academic achievements</p>

      <h3>EXPERIENCE</h3>
      <h4>Options Clearing Corporation – Chicago, IL</h4>
      <p><em>Enterprise Technology Solutions Intern (May 2025 – August 2025)</em></p>
      <ul>
        <li>Configured custom Workday reports as APIs to automate data transfers between internal teams, eliminating manual workflows and potential errors for cross-system integrations</li>
        <li>Led migration of employee photo storage from Active Directory to Workday using custom Workday Studio integrations, achieving $30,000/year in cost savings and streamlining HR and Facilities Management processes</li>
        <li>Coordinated and resolved diverse ServiceNow tickets across multiple Workday HCM modules, collaborating with a variety of stakeholders to deliver timely solutions that enhanced system performance and user satisfaction</li>
      </ul>

      <h4>Dover Corporation – Houston, TX</h4>
      <p><em>IT Leadership Development Program (June 2024 – August 2024)</em></p>
      <ul>
        <li>Built Power BI dashboards leveraging SQL Server data to improve quality tracking, enabling shop floor teams to recognize material issues 35% more effectively</li>
        <li>Standardized NTFS-based access controls across 11 sites, ensuring 100% compliance with internal and federal contract requirements</li>
        <li>Performed a gap analysis of on-prem ERP processes to support migration to cloud-based Syteline 10.0</li>
      </ul>

      <h4>Glanbia Performance Nutrition – Downers Grove, IL</h4>
      <p><em>Ecommerce Sales Intern (June 2023 – August 2023)</em></p>
      <ul>
        <li>Developed an AI-powered workflow utilizing ChatGPT and Jasper AI to enhance Amazon product pages, increasing conversion rates by 20-30% across three top brands</li>
        <li>Partnered with external media agency to recommend an increase of $50,000 in advertising and promotional spending, driving growth for high-priority product groups</li>
      </ul>

      <h3>LEADERSHIP</h3>
      <h4>Digital Transformation & AI Club – Bloomington, IN</h4>
      <p><em>President (March 2025 – Present)</em></p>
      <ul>
        <li>Support fellow leadership in alumni outreach and logging to both bolster the club’s external reputation as well as secure future participation for club events</li>
        <li>Direct executive decision-making for club activities, ensuring alignment with leadership and member interests</li>
        <li>Manage communications between current and incoming MSIS cohorts near 200 total students regarding information of upcoming club activities including networking events, distinguished speakers and social outings</li>
      </ul>

      <h3>TECHNICAL</h3>
      <ul>
        <li>Methodologies: Agile, Waterfall, UML</li>
        <li>Business Intelligence & Reporting: Power BI, Tableau, Excel, SQL</li>
        <li>Programming: Python, R, HTML/CSS, XML, MVEL</li>
      </ul>

      <h3>ADDITIONAL</h3>
      <p>Computer Building, Golfing, AI Strategy, Consulting, Spanish, Language Learning</p>
    </section>

    <section class="resume-download">
      <h3>Download Resume</h3>
      <div class="resume-actions">
        <a href="/resume/Pipala_Nicholas_Resume_Final.pdf" download class="btn">
          📄 Download PDF Resume
        </a>
      </div>
    </section>

    <section class="resume-embed">
      <h3>Resume Preview</h3>
      <iframe 
        src="/resume/Pipala_Nicholas_Resume_Final.pdf" 
        width="100%" 
        height="600px"
        style="border: 1px solid #ddd; margin-top: 1rem; border-radius: 8px;">
        <p>Your browser doesn't support PDFs. 
        <a href="/resume/Pipala_Nicholas_Resume_Final.pdf">Download the resume instead</a></p>
      </iframe>
    </section>
  </main>

  <footer>
    <div class="container">
      <p>&copy; 2025 Nicholas Pipala • <a href="https://github.com/nppipala123">GitHub: nppipala123</a> • <a href="mailto:nppipala@iu.edu">nppipala@iu.edu</a> • assignment 5: <a href="https://github.com/nppipala123/AIDD-Assignment-5">https://github.com/nppipala123/AIDD-Assignment-5</a></p>
    </div>
  </footer>
</body>
 
</html>
"""


# Thank you page HTML as a single string
THANKYOU_HTML = """<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Thank You</title>
  <link rel="stylesheet" href="/css/styles.css">
</head>
<body>
  <main class="container">
    <section class="center">
      <h1>Thank you!</h1>
      <p>Your submission has been received.</p>
      <p><a href="/">Return Home</a></p>
    </section>
  </main>
  <footer>
    <div class="container">
      <p>&copy; 2025 Nicholas Pipala • <a href="https://github.com/nppipala123">GitHub: nppipala123</a> • <a href="mailto:nppipala@iu.edu">nppipala@iu.edu</a> • assignment 5: <a href="https://github.com/nppipala123/AIDD-Assignment-5">https://github.com/nppipala123/AIDD-Assignment-5</a></p>
    </div>
  </footer>
</body>
</html>
"""


def _html_response(html: str) -> Response:
    return Response(html, mimetype='text/html')


@app.route('/')
def index() -> Response:
    return _html_response(INDEX_HTML)


@app.route('/index.html')
def index_html() -> Response:
    return _html_response(INDEX_HTML)


@app.route('/about')
def about() -> Response:
    return _html_response(ABOUT_HTML)


@app.route('/about/about.html')
def about_html() -> Response:
    return _html_response(ABOUT_HTML)


@app.route('/projects')
def projects() -> Response:
    projects_list = getAllProjects()
    return Response(render_template('projects.html', projects=projects_list), mimetype='text/html')


@app.route('/projects/projects.html')
def projects_html() -> Response:
    return redirect(url_for('projects'))


@app.route('/projects/add', methods=['GET','POST'])
def add_project() -> Response:
    if request.method == 'GET':
        return Response(render_template('add_project.html'), mimetype='text/html')
    # POST
    title = request.form.get('title', '').strip()
    description = request.form.get('description', '').strip()
    image = request.form.get('image', '').strip()
    if title and description:
        saveProjectDB(title, description, image)
    return redirect(url_for('projects'))


@app.route('/resume')
def resume() -> Response:
    return _html_response(RESUME_HTML)


@app.route('/resume/resume.html')
def resume_html() -> Response:
    return _html_response(RESUME_HTML)


@app.route('/contact')
def contact() -> Response:
    return _html_response(CONTACT_HTML)


@app.route('/contact/contact.html')
def contact_html() -> Response:
    return _html_response(CONTACT_HTML)


@app.route('/thankyou')
def thankyou() -> Response:
    return _html_response(THANKYOU_HTML)


@app.route('/thankyou.html')
def thankyou_html() -> Response:
    return _html_response(THANKYOU_HTML)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
