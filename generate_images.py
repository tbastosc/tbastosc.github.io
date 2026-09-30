#!/usr/bin/env python3
"""Generate portfolio images using Google Nano Banana Pro (Gemini 3 Pro Image Preview).

Usage:
    export GEMINI_API_KEY="your-key-here"
    python3 generate_images.py              # Generate all images
    python3 generate_images.py --dry-run    # Preview prompts without calling API
    python3 generate_images.py --only hero  # Generate a single image by name
"""

import os
import sys
import time
import shutil
import argparse
from pathlib import Path

from google import genai
from google.genai import types
from PIL import Image

# ── Paths ────────────────────────────────────────────────────────

REPO_ROOT = Path(__file__).parent
STATIC_IMAGES = REPO_ROOT / "static" / "images"
BACKUP_DIR = STATIC_IMAGES / "backup"

MODEL = "gemini-3-pro-image-preview"
DELAY_BETWEEN_REQUESTS = 10  # seconds

# ── Image Specifications ─────────────────────────────────────────

IMAGE_SPECS = [
    {
        "name": "hero",
        "label": "Hero Image",
        "output": STATIC_IMAGES / "hero.png",
        "target_size": (800, 800),
        "prompt": (
            "A polished digital illustration of a cybersecurity workspace, isometric 3D style. "
            "The scene shows a glowing terminal screen with green code scrolling, surrounded by "
            "floating holographic shields, lock icons, and network topology diagrams. A dark navy "
            "blue and deep teal color palette with bright cyan and electric green accent highlights. "
            "Clean, modern, minimal aesthetic. No people, no text. Professional portfolio-quality "
            "illustration with subtle gradients and soft shadows. Dark background that works well "
            "on both light and dark website themes."
        ),
    },
    {
        "name": "avatar",
        "label": "Profile Avatar",
        "output": STATIC_IMAGES / "me.png",
        "target_size": (512, 512),
        "prompt": (
            "A stylized, professional avatar illustration of a cybersecurity professional. "
            "Gender-neutral, modern flat design with subtle 3D depth. The person wears a dark "
            "hoodie, has short hair, and is shown from the chest up against a dark gradient "
            "background with subtle digital circuit board patterns. A faint glow of teal and "
            "electric blue emanates from behind. Clean vector-art style, similar to a premium "
            "Dribbble or Behance avatar. No text, centered composition, suitable for a circular crop."
        ),
    },
    {
        "name": "cloud-scanner",
        "label": "Project: Cloud Security Scanner",
        "output": STATIC_IMAGES / "projects" / "profile.png",
        "target_size": (1200, 675),
        "prompt": (
            "A clean, professional UI mockup screenshot of a cloud security scanning dashboard. "
            "Dark theme interface showing a table of findings with severity badges (Critical in red, "
            "High in orange, Medium in yellow, Low in green). A sidebar with AWS, GCP, and Azure "
            "cloud provider icons. The top section has a summary bar chart showing vulnerabilities "
            "by category. Modern design language similar to a real SaaS product. Realistic software "
            "screenshot aesthetic, not an illustration. Dark navy background with muted accent colors. "
            "No real company logos, no readable text strings."
        ),
    },
    {
        "name": "compliance",
        "label": "Project: Compliance Automation",
        "output": STATIC_IMAGES / "projects" / "profile2.png",
        "target_size": (1200, 675),
        "prompt": (
            "A professional diagram showing a compliance automation workflow. Clean, modern "
            "infographic style on a dark background. The flow shows interconnected nodes: a code "
            "repository icon on the left, connecting through arrows to a control mapping engine "
            "in the center depicted as interlocking gears, then flowing to document icons labeled "
            "with compliance frameworks (SOC 2, FedRAMP, ISO 27001) on the right. Teal and cyan "
            "accent colors on a dark navy background. Professional technical diagram aesthetic, "
            "minimal and elegant. No photographs, no readable fine text."
        ),
    },
    {
        "name": "ctf",
        "label": "Project: CTF Writeups",
        "output": STATIC_IMAGES / "projects" / "converter.png",
        "target_size": (1200, 675),
        "prompt": (
            "A dramatic, atmospheric illustration of a capture-the-flag cybersecurity competition "
            "scene. A glowing terminal window in the center shows stylized command-line output with "
            "a flag being captured. Surrounding the terminal are abstract representations of "
            "challenges: a binary cascade, a padlock being picked, a web exploitation payload, and "
            "a cryptographic key. Dark background with neon green, electric blue, and purple glow "
            "effects. Hacker aesthetic but professional and polished, not cartoonish. No readable "
            "text, no real code. Moody cinematic lighting."
        ),
    },
    {
        "name": "blog-welcome",
        "label": "Blog: Welcome Post",
        "output": STATIC_IMAGES / "post.png",
        "target_size": (1200, 675),
        "prompt": (
            "A sleek isometric illustration of a cybersecurity home lab setup. The scene shows a "
            "desk with a monitor displaying a terminal, a rack server with blinking LEDs, a network "
            "switch with ethernet cables, and a laptop running a purple desktop. Small floating "
            "icons represent virtual machines. Clean, modern illustration style with a dark navy "
            "background and teal, cyan, and soft purple accents. Professional portfolio blog header "
            "aesthetic. No people, no readable text, minimal and elegant."
        ),
    },
    {
        "name": "blog-homelab",
        "label": "Blog: Home Lab Post",
        "output": STATIC_IMAGES / "post-homelab.png",
        "target_size": (1200, 675),
        "prompt": (
            "A clean technical illustration showing layers of security architecture. From bottom "
            "to top: a server rack base layer, a network firewall layer with shield icons, a cloud "
            "layer with abstract cloud shapes, and a monitoring layer with graphs and alert icons "
            "at the top. Vertical connecting lines between layers glow with data flowing upward. "
            "Dark background with teal and cyan highlights. Modern infographic style, suitable as "
            "a blog post header image for a cybersecurity professional's portfolio."
        ),
    },
]

# ── Core Functions ───────────────────────────────────────────────


def backup_originals():
    """Back up existing images before overwriting."""
    BACKUP_DIR.mkdir(parents=True, exist_ok=True)
    (BACKUP_DIR / "projects").mkdir(exist_ok=True)

    for spec in IMAGE_SPECS:
        output = spec["output"]
        # Check for any existing file with the same stem (could be .svg, .jpg, .png)
        for ext in [".png", ".jpg", ".jpeg", ".svg"]:
            candidate = output.with_suffix(ext)
            if candidate.exists():
                dest = BACKUP_DIR / candidate.relative_to(STATIC_IMAGES)
                dest.parent.mkdir(parents=True, exist_ok=True)
                if not dest.exists():
                    shutil.copy2(candidate, dest)
                    print(f"  Backed up: {candidate.name} → backup/{candidate.relative_to(STATIC_IMAGES)}")


def resize_image(path: Path, target_size: tuple[int, int]):
    """Resize image to target dimensions using high-quality resampling."""
    img = Image.open(path)
    if img.size != target_size:
        img = img.resize(target_size, Image.LANCZOS)
        img.save(path, quality=95)


def generate_image(client, spec: dict, max_retries: int = 3) -> bool:
    """Generate a single image with retry logic."""
    config = types.GenerateContentConfig(
        response_modalities=["TEXT", "IMAGE"],
    )

    for attempt in range(max_retries):
        try:
            response = client.models.generate_content(
                model=MODEL,
                contents=[spec["prompt"]],
                config=config,
            )

            for part in response.candidates[0].content.parts:
                if part.inline_data is not None:
                    # Ensure output directory exists
                    spec["output"].parent.mkdir(parents=True, exist_ok=True)

                    # Save the generated image
                    image = part.as_image()
                    image.save(spec["output"])

                    # Resize to target dimensions
                    resize_image(spec["output"], spec["target_size"])

                    print(f"  ✓ Saved: {spec['output'].relative_to(REPO_ROOT)} ({spec['target_size'][0]}x{spec['target_size'][1]})")
                    return True

            print(f"  ⚠ No image in response (text-only output)")
            return False

        except Exception as e:
            wait = 2**attempt * 5
            print(f"  ✗ Attempt {attempt + 1}/{max_retries} failed: {e}")
            if attempt < max_retries - 1:
                print(f"    Retrying in {wait}s...")
                time.sleep(wait)

    return False


# ── Main ─────────────────────────────────────────────────────────


def main():
    parser = argparse.ArgumentParser(description="Generate portfolio images with Nano Banana Pro")
    parser.add_argument("--dry-run", action="store_true", help="Print prompts without calling API")
    parser.add_argument("--only", type=str, help="Generate only a specific image (by name)")
    parser.add_argument("--no-backup", action="store_true", help="Skip backing up originals")
    parser.add_argument("--delay", type=int, default=DELAY_BETWEEN_REQUESTS, help="Seconds between API calls")
    args = parser.parse_args()

    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key and not args.dry_run:
        print("Error: Set GEMINI_API_KEY environment variable")
        print("  Get a key at: https://aistudio.google.com/apikey")
        sys.exit(1)

    # Filter specs if --only is used
    specs = IMAGE_SPECS
    if args.only:
        specs = [s for s in specs if args.only.lower() in s["name"].lower()]
        if not specs:
            print(f"No image matching '{args.only}'. Available names:")
            for s in IMAGE_SPECS:
                print(f"  {s['name']:20s} — {s['label']}")
            sys.exit(1)

    print(f"Nano Banana Pro Image Generator")
    print(f"Model: {MODEL}")
    print(f"Images: {len(specs)}")
    print(f"{'=' * 50}")

    # Backup originals
    if not args.no_backup and not args.dry_run:
        print("\nBacking up originals...")
        backup_originals()

    # Generate images
    client = None if args.dry_run else genai.Client(api_key=api_key)
    results = []

    for i, spec in enumerate(specs):
        print(f"\n[{i + 1}/{len(specs)}] {spec['label']}")
        print(f"  Output: {spec['output'].relative_to(REPO_ROOT)}")

        if args.dry_run:
            print(f"  Prompt: {spec['prompt'][:120]}...")
            results.append((spec["label"], "SKIPPED"))
            continue

        success = generate_image(client, spec)
        results.append((spec["label"], "OK" if success else "FAILED"))

        # Delay between requests to respect rate limits
        if i < len(specs) - 1:
            print(f"  Waiting {args.delay}s before next request...")
            time.sleep(args.delay)

    # Summary
    print(f"\n{'=' * 50}")
    print("Summary:")
    for label, status in results:
        icon = "✓" if status == "OK" else "○" if status == "SKIPPED" else "✗"
        print(f"  {icon} {label}: {status}")

    failed = sum(1 for _, s in results if s == "FAILED")
    if failed:
        print(f"\n{failed} image(s) failed. Re-run with --only <name> to retry.")
        sys.exit(1)


if __name__ == "__main__":
    main()
