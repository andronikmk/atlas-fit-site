#!/usr/bin/env python3
"""Builds the atlas-fit.fit site: home, support, privacy and about pages.

    python3 build.py "/path/to/WorkoutLogApp/docs/privacy-policy.md"

The privacy page is generated from the app's policy file, so the site and the
copy bundled in the app say the same thing. Re-run this and publish whenever
that file changes. No dependencies beyond Python 3.
"""
import html
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DOMAIN = "atlas-fit.fit"
EMAIL = "support@atlas-fit.fit"
# The company that publishes Atlas Fit: its exact legal name as registered on
# Sunbiz (Florida's business register). Apple compares this site with the
# D-U-N-S record, so it must match letter for letter, including "LLC".
COMPANY = "Andronik Capital LLC"
YEAR = 2026


def page(title: str, description: str, body: str, path: str) -> str:
    def nav(href: str, label: str) -> str:
        current = ' aria-current="page"' if href == path else ""
        return f'<a href="{href}"{current}>{label}</a>'

    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(description)}">
<link rel="canonical" href="https://{DOMAIN}{path}">
<link rel="icon" href="/icon-180.png">
<link rel="apple-touch-icon" href="/icon-180.png">
<link rel="stylesheet" href="/styles.css">
</head>
<body>
<header class="site">
  <a class="brand" href="/"><img src="/icon-180.png" alt="" width="32" height="32"><span>Atlas Fit</span></a>
  <nav>{nav("/support/", "Support")}{nav("/privacy/", "Privacy")}{nav("/about/", "About")}</nav>
</header>
<main>
{body}
</main>
<footer class="site">
  <p>Atlas Fit is a strength-training log for iPhone and Apple Watch, made by {html.escape(COMPANY)}.</p>
  <p><a href="/about/">About</a> · <a href="/support/">Support</a> · <a href="/privacy/">Privacy policy</a> · <a href="mailto:{EMAIL}">{EMAIL}</a></p>
  <p>© {YEAR} {html.escape(COMPANY)}</p>
</footer>
</body>
</html>
"""


def inline(text: str) -> str:
    text = html.escape(text, quote=False)
    text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"(?<![\w@])_(.+?)_(?!\w)", r"<em>\1</em>", text)
    text = re.sub(r"([\w.+-]+@[\w-]+(?:\.[\w-]+)+)", r'<a href="mailto:\1">\1</a>', text)
    return text


def markdown(source: str) -> str:
    """The small subset the policy uses: #, ##, bullets, paragraphs, bold, italics."""
    out, bullets = [], []

    def flush():
        if bullets:
            out.append("<ul>\n" + "\n".join(f"  <li>{b}</li>" for b in bullets) + "\n</ul>")
            bullets.clear()

    for raw in source.splitlines():
        line = raw.strip()
        if line.startswith("- "):
            bullets.append(inline(line[2:]))
            continue
        flush()
        if not line:
            continue
        if line.startswith("## "):
            out.append(f"<h2>{inline(line[3:])}</h2>")
        elif line.startswith("# "):
            out.append(f"<h1>{inline(line[2:])}</h1>")
        elif line.startswith("_") and line.endswith("_"):
            out.append(f'<p class="meta">{inline(line[1:-1])}</p>')
        else:
            out.append(f"<p>{inline(line)}</p>")
    flush()
    return "\n".join(out)


HOME = f"""<section class="hero">
  <img src="/icon-180.png" alt="Atlas Fit app icon" width="96" height="96">
  <h1>Atlas Fit</h1>
  <p class="lede">A strength-training log for iPhone and Apple Watch. Log sets fast, follow your routines, and see what is getting stronger.</p>
  <p class="note">Coming to the App Store.</p>
</section>
<section class="points">
  <div><h2>Yours, on your iPhone</h2><p>No account and no sign-in. Your workouts stay on your iPhone, and Atlas has no servers to send them to.</p></div>
  <div><h2>Built for the gym floor</h2><p>Routines, supersets, warm-ups, a rest timer on your Lock Screen, a plate calculator, and your Apple Watch on your wrist.</p></div>
  <div><h2>Progress you can read</h2><p>History, personal records and trends for every exercise, plus recovery, sleep and weight from Apple Health if you connect it.</p></div>
</section>
<section class="links">
  <a class="button" href="/support/">Get help</a>
  <a class="button quiet" href="/privacy/">Read the privacy policy</a>
</section>
"""

SUPPORT = f"""<h1>Support</h1>
<p class="lede">Something not working, or a question about Atlas? Email <a href="mailto:{EMAIL}">{EMAIL}</a>.</p>
<p>It helps to include your iPhone model, your iOS version, the Atlas version (Settings › About) and what you were doing when the problem appeared. A screenshot is welcome.</p>

<h2>Your data</h2>
<details><summary>Where is my data kept?</summary>
<p>On your iPhone, and on your Apple Watch during a workout. Atlas has no accounts and no servers, and this version does not sync through iCloud. If you back up your iPhone with iCloud Backup or to a computer, Atlas's data is included in that backup like any other app's.</p></details>
<details><summary>How do I move my workouts to a new iPhone?</summary>
<p>Restore the new iPhone from a backup of the old one and Atlas's data comes with it. You can also make a copy of your workouts yourself: Settings › Data › Export workout data saves CSV files wherever you choose.</p></details>
<details><summary>Can I bring my history from Strong or Hevy?</summary>
<p>Yes. Export a CSV file from that app, then in Atlas open Settings › Data › Import workout data and pick the file. It is read on your iPhone and is not uploaded anywhere. You can remove an import later in Settings › Data › Imports.</p></details>
<details><summary>How do I delete my data?</summary>
<p>Settings › Data › Delete all data erases everything Atlas holds on that iPhone and returns it to the welcome screen. Deleting the app does the same. Workouts Atlas already saved to Apple Health stay in the Health app, where you can delete them.</p></details>

<h2>Atlas Pro</h2>
<details><summary>I bought Pro but the app shows Free</summary>
<p>Open Settings › Atlas Pro and tap Restore purchases. Make sure you are signed in to the App Store with the Apple Account that made the purchase.</p></details>
<details><summary>How do I cancel or change my subscription?</summary>
<p>Subscriptions are managed by Apple: open iPhone Settings, tap your name, then Subscriptions. Deleting the app does not cancel a subscription. If you subscribe and later buy Lifetime, cancel the subscription there so it does not renew.</p></details>
<details><summary>What happens to my data if Pro ends?</summary>
<p>Nothing is deleted or locked. You keep every workout and routine; only creating routines beyond the Free limit needs Pro.</p></details>
<details><summary>Can I get a refund?</summary>
<p>Apple handles all payments and refunds. Request one at <a href="https://reportaproblem.apple.com">reportaproblem.apple.com</a>.</p></details>

<h2>Coach</h2>
<details><summary>Why does the Coach show sample workouts?</summary>
<p>The Coach uses Apple Intelligence, which runs on your iPhone. It needs an iPhone that supports Apple Intelligence, with Apple Intelligence turned on in iPhone Settings. Without it, Atlas shows built-in sample workouts, labelled as samples.</p></details>
<details><summary>Is the Coach medical advice?</summary>
<p>No. It gives general training suggestions, and Atlas is not a medical device. If you are injured, unwell or unsure, see a qualified professional.</p></details>

<h2>Apple Health and Apple Watch</h2>
<details><summary>How do I connect Apple Health, or change what Atlas can read?</summary>
<p>Connect in Settings › Health &amp; Devices. Apple shows its permission screen only once, so to change access later open the Health app, tap your picture, then Apps › Atlas.</p></details>
<details><summary>My Today screen is empty</summary>
<p>Recovery, sleep and the other panels are built from Apple Health data, usually recorded by an Apple Watch. If Apple Health is connected and the panels are still empty, check in the Health app that Atlas is allowed to read those types.</p></details>
<details><summary>The Watch app is missing</summary>
<p>Open the Watch app on your iPhone, scroll to Available Apps and install Atlas. Keep your iPhone nearby the first time you open it so your routines can copy across.</p></details>

<h2>Privacy and lock</h2>
<details><summary>How do I lock Atlas with Face ID?</summary>
<p>Turn it on in Settings › Profile &amp; privacy.</p></details>
<details><summary>What does Atlas do with my data?</summary>
<p>It keeps it on your iPhone. The <a href="/privacy/">privacy policy</a> has the detail.</p></details>
"""


def about() -> str:
    company = html.escape(COMPANY)
    return f"""<h1>About</h1>
<p class="lede">Atlas Fit is made by {company}, an independent software company based in Florida.</p>
<p>{company} designs and publishes Atlas Fit, a strength-training log for iPhone and Apple Watch, and is its seller on the App Store.</p>
<p>Atlas Fit is built to keep your training private. There are no accounts and no servers: workouts are stored on your iPhone, and Apple Health data is read on your device. The <a href="/privacy/">privacy policy</a> has the detail.</p>

<h2>Contact</h2>
<p>For help with the app, questions about privacy, or anything else, email <a href="mailto:{EMAIL}">{EMAIL}</a>. The <a href="/support/">support page</a> answers the most common questions.</p>
"""


def main() -> None:
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    if not COMPANY.strip():
        sys.exit("Set COMPANY in build.py to the company's exact legal name; not building.")
    policy = Path(sys.argv[1]).read_text(encoding="utf-8")
    if re.search(r"\[[^\]\n]*\]", policy):
        sys.exit("The policy still has a bracketed placeholder in it; not building.")

    pages = {
        "index.html": page("Atlas Fit: strength-training log for iPhone and Apple Watch",
                           "Atlas Fit is a private strength-training log for iPhone and Apple Watch. No account, no servers.",
                           HOME, "/"),
        "support/index.html": page("Atlas Fit support",
                                   "Help with Atlas Fit: your data, Atlas Pro, the Coach, Apple Health and Apple Watch.",
                                   '<article class="doc">\n' + SUPPORT + "</article>", "/support/"),
        "privacy/index.html": page("Atlas Fit privacy policy",
                                   "What data Atlas Fit handles, where it is kept and what you can do with it.",
                                   '<article class="doc policy">\n' + markdown(policy) + "\n</article>", "/privacy/"),
        "about/index.html": page("About Atlas Fit",
                                 f"Atlas Fit is made by {COMPANY}. Contact details for the company and the app.",
                                 '<article class="doc">\n' + about() + "</article>", "/about/"),
        "404.html": page("Page not found · Atlas Fit", "Page not found.",
                         '<article class="doc"><h1>Page not found</h1><p>Try <a href="/support/">Support</a> or the <a href="/privacy/">privacy policy</a>.</p></article>',
                         "/404.html"),
    }
    for name, content in pages.items():
        target = ROOT / name
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8")
        print("wrote", name)


if __name__ == "__main__":
    main()
