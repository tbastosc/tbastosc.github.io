# Hugo Portfolio Demo for Cybersecurity Professionals

A ready-to-deploy portfolio template built with [Hugo](https://gohugo.io/) and the [hugo-profile](https://github.com/gurusabarish/hugo-profile) theme. Designed for cybersecurity professionals who want a professional online presence without web development experience.

**[Live Demo](https://ethanolivertroy.github.io/hugo-portfolio-demo/)**

## Features

- Pre-configured sections for experience, projects, certifications, education, and blog
- Light/dark mode toggle
- Full-text search
- Mobile-responsive design
- Blog with tags and social sharing
- Contact form integration (FormSpree)
- Automatic deployment via GitHub Pages

## Quick Start

### Option A: Use a Coding Agent (Recommended)

The fastest way to make this your own is to fill out a spec and let an AI coding agent do the rest. This works with [Claude Code](https://docs.anthropic.com/en/docs/claude-code), GitHub Copilot, Cursor, Windsurf, or any agent that can read files and edit code.

1. Click **"Use this template"** > **"Create a new repository"** at the top of this page
2. Clone your new repo: `git clone --recursive https://github.com/YOUR_USERNAME/your-repo.git`
3. Open `PORTFOLIO_SPEC.md` and fill in your information (name, experience, projects, certs, etc.). Rough notes and bullet points are fine. You can even paste your resume.
4. Open a terminal in the repo and tell your agent:

   ```
   Read PORTFOLIO_SPEC.md and customize this portfolio site for me.
   ```

5. The agent reads your spec, updates `hugo.yaml`, creates blog posts, and sets up deployment. Review what it did, push, and your site is live.

The repo includes a `CLAUDE.md` that teaches agents how the site works, so they know which files to edit and how the config is structured.

### Option B: Manual Setup

1. Click **"Use this template"** > **"Create a new repository"**
2. Name your repo (e.g., `my-portfolio` or `username.github.io`)
3. In your new repo, go to **Settings** > **Pages** > set Source to **GitHub Actions**
4. Edit `hugo.yaml` with your information (name, bio, experience, projects, social links)
5. Push your changes. The site deploys automatically.

### Option C: Fork and Clone

```bash
# Fork this repo first, then:
git clone --recursive https://github.com/YOUR_USERNAME/hugo-portfolio-demo.git
cd hugo-portfolio-demo
hugo server
```

Visit `http://localhost:1313` to preview.

## Customization

Everything lives in `hugo.yaml`. Open it and replace the placeholder content:

| Section | What to Change |
|---|---|
| `hero` | Your name, tagline, and social links |
| `about` | Bio and skills list |
| `experience` | Work history with company names and descriptions |
| `education` | Degrees, schools, dates |
| `achievements` | Certifications (OSCP, CISSP, AWS, etc.) |
| `projects` | Your tools, repos, and writeups |
| `contact` | Email address or FormSpree form ID |
| `footer.socialNetworks` | GitHub, LinkedIn, Twitter URLs |

### Images

Replace the placeholder images in `static/images/`:

- `me.png` — Your profile photo (used in About section, displayed as a circle)
- `hero.png` — Hero section graphic (square, ~800x800)
- `projects/` — Project screenshots or thumbnails (landscape, ~1200x675)
- `post.png` — Default blog post featured image

#### Generate Custom Images with AI (Nano Banana Pro)

This repo includes `generate_images.py`, a script that uses Google's **Nano Banana Pro** (Gemini 3 Pro Image) to generate polished, cybersecurity-themed images for every slot in the portfolio. You can customize the prompts to match your personal brand.

**Setup:**

```bash
# 1. Get a free API key at https://aistudio.google.com/apikey
# 2. Install dependencies (if not already installed)
pip install google-genai Pillow

# 3. Set your API key
export GEMINI_API_KEY="your-key-here"
```

**Usage:**

```bash
# Preview what will be generated (no API calls)
python3 generate_images.py --dry-run

# Generate all 7 images (~90 seconds)
python3 generate_images.py

# Regenerate a single image
python3 generate_images.py --only hero
python3 generate_images.py --only avatar
python3 generate_images.py --only ctf
```

**Customize prompts:** Open `generate_images.py` and edit the `prompt` field in `IMAGE_SPECS` for each image. Tips for good prompts:

- Be specific about style: "isometric 3D", "flat design", "realistic screenshot", "infographic"
- Specify colors: "dark navy background with teal and cyan accents"
- Say "no text" or "no readable text" to avoid garbled lettering
- Include "professional portfolio quality" to bias toward polished output
- For avatars, use "stylized illustration" to avoid content policy blocks on photorealistic faces

**Available image slots:**

| Name | File | Description |
|---|---|---|
| `hero` | `static/images/hero.png` | Landing section graphic (1:1) |
| `avatar` | `static/images/me.png` | Profile photo / avatar (1:1, circular crop) |
| `cloud-scanner` | `static/images/projects/profile.png` | Project 1 card image (16:9) |
| `compliance` | `static/images/projects/profile2.png` | Project 2 card image (16:9) |
| `ctf` | `static/images/projects/converter.png` | Project 3 card image (16:9) |
| `blog-welcome` | `static/images/post.png` | Blog featured image (16:9) |
| `blog-homelab` | `static/images/post-homelab.png` | Blog featured image (16:9) |

Originals are automatically backed up to `static/images/backup/` before overwriting.

### Blog Posts

Create new posts in `content/blogs/`:

```bash
hugo new content content/blogs/my-post-title.md
```

## Local Development

Requirements: [Hugo](https://gohugo.io/installation/) (v0.87.0+)

```bash
# Start dev server with live reload
hugo server

# Build for production
hugo --gc --minify
```

## Deployment Options

### GitHub Pages (default)

Already configured. Push to `main` and the GitHub Actions workflow handles the rest.

### Netlify

[![Deploy to Netlify](https://www.netlify.com/img/deploy/button.svg)](https://app.netlify.com/start/deploy?repository=https://github.com/ethanolivertroy/hugo-portfolio-demo)

### Vercel

Import the repo at [vercel.com/new](https://vercel.com/new). Set the framework to Hugo and it auto-detects the config.

## Project Structure

```
.
├── .github/workflows/hugo.yml   # GitHub Pages deployment
├── content/blogs/               # Blog posts (Markdown)
├── static/images/               # Images and assets
├── themes/hugo-profile/         # Theme (git submodule)
├── hugo.yaml                    # All site configuration
├── PORTFOLIO_SPEC.md            # Fill this out, hand it to an AI agent
├── CLAUDE.md                    # Agent instructions (how to customize this site)
└── README.md
```

## Using AI Coding Agents

This repo is designed to work well with AI coding agents. Here's how the pieces fit together:

| File | Purpose |
|---|---|
| `PORTFOLIO_SPEC.md` | You fill this out with your career info. The agent reads it. |
| `CLAUDE.md` | Tells agents how the site works, what files to edit, and how the config is structured. |
| `hugo.yaml` | The agent updates this based on your spec. This is where all homepage content lives. |
| `content/blogs/` | The agent creates blog posts here based on your spec. |

### Workflow

```
Fill out PORTFOLIO_SPEC.md
        │
        ▼
Tell your agent: "Read PORTFOLIO_SPEC.md and customize this site for me"
        │
        ▼
Agent updates hugo.yaml, creates blog posts, sets baseURL
        │
        ▼
Agent runs `hugo server` to verify the build
        │
        ▼
You review, push to GitHub, site deploys automatically
```

### Tips

- **Start rough.** Your spec doesn't need to be polished. Bullet points, sentence fragments, even a pasted resume work. The agent will structure it.
- **Iterate.** After the first pass, tell the agent what to change: "make the about section shorter," "add another project," "write a blog post about X."
- **Ask for help.** The agent can help you write your bio, suggest project descriptions, draft blog posts, or set up a custom domain.
- **Preview first.** Always have the agent run `hugo server` before you push so you can check the result.

### Compatible Agents

- [Claude Code](https://docs.anthropic.com/en/docs/claude-code) (reads `CLAUDE.md` natively)
- GitHub Copilot (workspace mode)
- Cursor, Windsurf, Cline, Aider
- Any agent that can read files and edit code

## Credits

- [hugo-profile](https://github.com/gurusabarish/hugo-profile) theme by Gurusabarish
- [Hugo](https://gohugo.io/) static site generator
- [Bootstrap](https://getbootstrap.com/) and [Font Awesome](https://fontawesome.com/)

## License

MIT
