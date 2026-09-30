---
title: "Welcome to Your Security Portfolio"
date: 2025-01-01
draft: false
tags: ["Hugo", "Portfolio", "Getting Started"]
image: images/post.png
---

Congratulations on setting up your cybersecurity portfolio! This is a starter post to help you get familiar with the template. Feel free to delete it once you've added your own content.

## What to Write About

As a cybersecurity professional, your portfolio blog is a great place to share:

- **Technical writeups** from CTF competitions or lab exercises
- **Tool reviews** and comparisons of security software
- **Lessons learned** from real-world incidents (sanitized, of course)
- **How-to guides** for security tools and techniques
- **Career reflections** on certifications, interviews, and professional growth
- **Research findings** from vulnerability analysis or threat intelligence

## How to Create a New Post

Create a new Markdown file in the `content/blogs/` directory:

```bash
hugo new content content/blogs/my-new-post.md
```

Each post uses front matter at the top for metadata:

```yaml
---
title: "Your Post Title"
date: 2025-01-15
draft: false
tags: ["Security", "Cloud"]
image: images/post.png
---
```

Set `draft: true` to hide a post from the published site while you're still working on it.

## Customizing Your Site

All the main content on the homepage (hero section, about, experience, projects, certifications) is configured in `hugo.yaml`. Open that file and replace the placeholder content with your own information.

## Local Development

To preview your site locally:

```bash
hugo server
```

Visit `http://localhost:1313` to see your changes in real-time.

## Next Steps

1. Edit `hugo.yaml` with your real information
2. Replace the placeholder images in `static/images/`
3. Write your first real blog post
4. Push to GitHub and watch it deploy automatically

Happy building!
