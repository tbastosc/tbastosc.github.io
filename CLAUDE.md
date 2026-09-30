# CLAUDE.md

Hugo portfolio site using the [hugo-profile](https://github.com/gurusabarish/hugo-profile) theme. This file tells AI coding agents how to work with this repo.

## Commands

```bash
hugo server              # Dev server at localhost:1313
hugo --gc --minify       # Production build
```

## Structure

- `hugo.yaml` - All site config (hero, about, experience, projects, certifications, contact)
- `content/blogs/` - Blog posts in Markdown
- `static/images/` - Site images
- `themes/hugo-profile/` - Theme (git submodule, don't edit directly)
- `PORTFOLIO_SPEC.md` - User's portfolio spec (read this first if it has been filled out)

## Key Rules

- Theme uses YAML config (not TOML). All homepage sections live in `hugo.yaml` under `params`.
- Blog posts go in `content/blogs/`, not `content/posts/`.
- Don't edit anything inside `themes/`. Override by creating files at the site root level.
- Deployed via GitHub Pages using `.github/workflows/hugo.yml`.
- After making changes, run `hugo server` to verify the build works before committing.
- **Image paths must NOT start with `/`.** Use `images/hero.png` not `/images/hero.png`. The layout overrides pipe paths through Hugo's `relURL` filter, which only prepends the `baseURL` path for relative paths. Paths starting with `/` are treated as absolute and bypass `relURL`.

## Customization Workflow

When the user asks you to customize this portfolio:

1. **Read `PORTFOLIO_SPEC.md` first.** If the user filled it out, that's your source of truth. If they haven't, ask them the key questions: name, role, experience, projects, certifications.

2. **Update `hugo.yaml`.** This is where 90% of the work happens. Map the spec fields to config sections:
   - `params.hero` - name, subtitle, social links
   - `params.about` - bio text, skills list
   - `params.experience.items` - work history (each entry has `company`, `companyUrl`, `jobs` with `name`, `date`, `content`)
   - `params.education.items` - degrees (each has `title`, `school.name`, `school.url`, `date`, `GPA`, `content`)
   - `params.achievements.items` - certifications (each has `title`, `content`, `url`)
   - `params.projects.items` - portfolio projects (each has `title`, `content`, `image`, `badges`, `links`)
   - `params.contact` - email, FormSpree config
   - `params.footer.socialNetworks` - GitHub, LinkedIn, Twitter URLs
   - `params.navbar.brandName` - name shown in the nav bar

3. **Create blog posts** in `content/blogs/` with this front matter:
   ```yaml
   ---
   title: "Post Title"
   date: 2025-01-15
   draft: false
   tags: ["Security", "Cloud"]
   image: /images/post.jpg
   ---
   ```

4. **Handle images.** Remind the user to replace `static/images/me.png` with their photo. If they provide project screenshots, save them to `static/images/projects/`.

5. **Set `baseURL`** in `hugo.yaml` to match their deployment:
   - GitHub Pages: `https://USERNAME.github.io/REPO_NAME/`
   - Custom domain: `https://their-domain.com/`
   - For `username.github.io` repos: `https://USERNAME.github.io/`

6. **Verify the build.** Run `hugo server` and check for errors. Common issues:
   - Missing images referenced in config
   - YAML indentation errors in `hugo.yaml`
   - Wrong `baseURL` causing broken links

## Sections Reference

To hide a section, set `enable: false` in its config block. Available sections:

| Section | Config path | Purpose |
|---|---|---|
| Hero | `params.hero` | Landing section with name, tagline, social links |
| About | `params.about` | Bio and skills list |
| Experience | `params.experience` | Work history timeline |
| Education | `params.education` | Degrees and schools |
| Achievements | `params.achievements` | Certifications, awards |
| Projects | `params.projects` | Portfolio project cards |
| Contact | `params.contact` | Contact form or email link |

## Deployment

The GitHub Actions workflow at `.github/workflows/hugo.yml` auto-deploys on push to `main`. To set up:

1. Go to repo Settings > Pages > set Source to "GitHub Actions"
2. Push to `main`
3. The workflow builds and deploys automatically

For custom domains, add a `CNAME` file to `static/` with the domain name, and update `baseURL` in `hugo.yaml`.
