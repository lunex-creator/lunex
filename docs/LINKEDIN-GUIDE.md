# LUNEX LinkedIn — Maintenance Guide

**Scope of this document**: the LUNEX presence on LinkedIn — the Company Page, its assets, and (if created) the Group — how they were set up and how to keep them current. For the website, see `WEBSITE-GUIDE.md`. For the repository, see `GITHUB-GUIDE.md`.

---

## 1. Two separate things: Company Page vs. Group

LinkedIn has two distinct, unrelated features that are easy to conflate:

| | Company Page | Group |
|---|---|---|
| What it is | An organization's profile — one-way broadcast (posts, followers) | A discussion community — members post and reply to each other |
| Created from | Either a personal account or (once it exists) potentially delegated — but the *first* page for an org must come from a personal profile | **Always** a personal account — a Company Page cannot create a Group |
| LUNEX status at time of writing | Being set up | Deferred — see §5 |

---

## 2. Company Page setup

### Eligibility requirements (verified against LinkedIn's own Help documentation, not third-party guessing)

- Your personal LinkedIn account needs **more than one connection** (i.e., 2+) — third-party blog posts often cite much higher numbers (10, 30, even 500) but these are *recommendations for a page that looks established*, not the actual technical minimum to create one.
- Your personal account must be **at least one day old**.
- There's an anti-spam rate limit on how many pages one account can create in a short period — if page creation fails for no apparent reason, this could be why; wait a few days and retry.

### Creating the page

1. Navigate to `linkedin.com/company/setup/new` (no trailing slash — a trailing slash has caused a 404 before).
2. **If this 404s on mobile**: force the desktop site in your browser first (Chrome: ⋮ menu → "Desktop site"). This resolved the issue every time it came up — LinkedIn's page-creation flow does not reliably work on mobile web.
3. Select **"Company"** as the page type.
4. Fields and the values used for LUNEX:

| Field | Value used | Why |
|---|---|---|
| Page name | LUNEX | — |
| LinkedIn public URL | `linkedin.com/company/lunex-ot` (or similar) | Plain `lunex` was already taken by an unrelated organization — check availability live in the form, it validates as you type |
| Website | `lunex.cloud` | — |
| Industry | Automation Machinery Manufacturing | The closest match in LinkedIn's current taxonomy, despite LUNEX not manufacturing physical equipment — chosen because real peer organizations (e.g. ABB) are categorized here too, which matters for LinkedIn's own recommendation/discovery algorithm. Not a perfect semantic fit, but the best available and the one that puts the page among relevant company peers |
| Company size | 1–10 employees | — |
| Company type | **Self-employed** | Deliberately *not* "Non-profit" — that implies a registered legal entity (e.g. a Stichting) which doesn't exist yet. See `GITHUB-GUIDE.md` §9 on governance status. **Update this field if and when a foundation is actually incorporated** — not before |
| Tagline (max 120 chars) | "One object model for everything OT — process control, safety, security, alarms and AI." (86 characters) | Matches the website's hero headline for consistent messaging across channels |

5. Check the verification box and click **Create page**.


---

## 3. Page assets and content

### Images required, and their exact specifications

| Asset | Size | Notes |
|---|---|---|
| Logo | 300×300px | Circular crop applied by LinkedIn — keep the actual logo mark within the inner ~85% of the canvas (a margin of roughly 24px on all sides at this size) so nothing important gets clipped by the circle |
| Cover photo | 1128×191px | **Critical**: LinkedIn's profile photo overlaps the bottom-left corner of the cover photo on the rendered page. Keep all text and the logo mark in the top area and away from the bottom-left — this project's cover was deliberately laid out top-aligned with generous left padding specifically to clear this overlap zone |
| Featured post image | 1200×627px (standard LinkedIn feed image ratio) | Used when publishing the launch post, not uploaded directly to the page itself |

All three were generated from HTML/CSS (matching the exact brand colors and fonts documented in `WEBSITE-GUIDE.md` §3) rendered via headless browser screenshot, the same technique used for the website's favicon and OG image — not hand-designed in an image editor. **If the brand mark or colors ever change, regenerate these from the same HTML-source approach** rather than patching the PNGs directly, so they stay pixel-consistent with everything else.

### About / description text

The company description used:

> An open, object-oriented reference model spanning process control, functional safety, industrial cybersecurity, alarm management, and the AI/data layer — one consistent model instead of five separate standards. Draft v0.1, authored by a single contributor so far, and built specifically to be argued with. If you work in OT, process safety, or industrial cybersecurity: this group is for exactly that — pointing at what's wrong, missing, or overcomplicated. Full specification: lunex.cloud · Repository: github.com/lunex-creator/lunex

This deliberately matches the humble, invite-critique tone used in `README.md` and the GitHub Discussions welcome post — not corporate marketing language. **If this text is ever revised, keep that tone consistent across all three places** (LinkedIn, `README.md`, GitHub Discussions) rather than letting LinkedIn drift toward more promotional phrasing, which is the platform's cultural default.

**Specialties field** (up to 20 keywords): OT reference architecture, industrial automation, functional safety, IEC 61508, IEC 61511, industrial cybersecurity, IEC 62443, alarm management, ISA-18.2, digital twin, predictive maintenance, closed-loop AI control, ISA-88, ISA-95, PackML.

---

## 4. Publishing a post and using "Featured"

This is the part of LinkedIn's interface most likely to confuse someone unfamiliar with the platform: **Company Pages cannot feature a raw external link directly.** The Featured section only lets you promote a post that has *already been published* on the page.

### Correct order of operations

1. **Publish the post first.** From the Company Page, click "Start a post," paste the announcement text, attach the 1200×627 image (§3) via the photo icon in the composer, then publish.
2. **Then feature it.** Go to **Edit page → Featured** (in the left-hand sidebar of the page admin view) → **Manage featured → Feature a Post** → select the post you just published.

Trying to do this the other way around (looking for a way to feature `lunex.cloud` or the GitHub repo directly as a link) will not work — there is no such option on a Company Page.

### Mobile web caveat

Attaching an image to a post composer has, in the past, failed to open the file picker correctly in mobile Chrome. **Fix**: same as the page-creation issue — force desktop site mode, or use the LinkedIn mobile app instead of the mobile browser, which doesn't have this limitation.


---

## 5. LinkedIn Group — deferred, but planned

A Group was discussed as a possible addition (a discussion-oriented community, complementing the Company Page's one-way posts and GitHub Discussions' developer-oriented audience) but **not yet created**, pending the Company Page being finished first — a Group with no page to anchor it to looks less established.

If and when it's created, the plan (from earlier discussion, preserved here so it isn't lost):

- **Must be created from a personal account**, not the Company Page (LinkedIn does not allow Pages to create or own Groups).
- **Suggested name**: `LUNEX — Open OT Reference Model` — not bare "LUNEX," since a Group name should be discoverable by people who don't already know the term (LinkedIn's own guidance).
- **Privacy**: Public (not Private) — consistent with the project's "invite scrutiny" positioning; note this **cannot be changed after creation**, so confirm it's the right call before finalizing.
- **Discoverability**: Listed (so it appears in LinkedIn search).
- **Suggested industries** (up to 3): Industrial Automation, Machinery, Computer & Network Security.
- **Suggested group rules**: mirror `CODE_OF_CONDUCT.md`'s tone — disagreement about the model is welcome, contempt for the person is not.

**One open question, deliberately left for whoever sets this up**: whether to actually commit to keeping a third community channel alive (GitHub Discussions, the Company Page's comments, and now a Group) — an abandoned Group looks worse than no Group. Don't create it reflexively; create it when there's a realistic plan to seed and monitor it.

---

## 6. General maintenance notes

- **Keep the tagline in sync with the website.** If the website's hero headline (`WEBSITE-GUIDE.md` §2) changes, update LinkedIn's tagline field to match — they were deliberately written to be identical.
- **Company type** should move from "Self-employed" to whatever's accurate the moment a legal entity exists (see `GITHUB-GUIDE.md` §9 for the governance staging this depends on).
- **Contact**: general inquiries route to `info@lunex.cloud`, matching the website footer — don't introduce a separate LinkedIn-only contact address.
- **Posting cadence**: no fixed schedule was established — the priority was getting the page and its first post right, not committing to a publishing rhythm prematurely. If a cadence is adopted later, document it here.

---

*For why these specific choices were made (Self-employed vs. Non-profit, the industry-category tradeoff, deferring the Group), see `docs/PROJECT-RECORD.md` in the repository — this guide tells you *how* to operate the LinkedIn presence; that document tells you *why* it's set up this way.*
