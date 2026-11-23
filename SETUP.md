# Setup guide: Ghost Protocol Labs organization profile

This turns the README at the top of `github.com/Ghost-Protocol-Lab` into the ghost-themed page. It takes about five minutes and needs **no tokens, secrets or workflows**. Everything is static.

## What you need first

- You must be an **owner** of the Ghost-Protocol-Lab organization (members cannot create this repo or edit the profile).
- A web browser is enough. Git is optional.

## 1. Create the repository

1. Go to <https://github.com/organizations/Ghost-Protocol-Lab/repositories/new>.
2. Name it exactly **`.github`** (a dot, then `github`, all lowercase).
3. Set visibility to **Public**. A private `.github` repo will not show on the profile.
4. Leave "Add a README" unticked. Create the repository.

## 2. Upload the files

Upload the contents of this folder so the repo looks like this:

```
.github/
├── profile/
│   ├── README.md          <- this is what visitors see
│   └── assets/*.svg
├── scripts/               <- optional, only for regenerating the art
├── README.md              <- describes the repo itself (not shown on the org page)
├── SETUP.md
└── .gitignore
```

The path **`profile/README.md`** matters. Put it anywhere else and the org page stays empty.

Browser route: on the new repo page choose **uploading an existing file**, drag the folders in, and commit. If you prefer git:

```bash
cd Ghost-Protocol-Lab-profile
git init -b main
git add .
git commit -m "Add organization profile"
git remote add origin https://github.com/Ghost-Protocol-Lab/.github.git
git push -u origin main
```

## 3. Check the branch name

Every image in `profile/README.md` uses an absolute URL that assumes the default branch is **`main`**:

```
https://raw.githubusercontent.com/Ghost-Protocol-Lab/.github/main/profile/assets/hero.svg
```

Absolute URLs are required here. Relative paths such as `assets/hero.svg` work on a repo page but **break on the organization page**.

If your default branch is not `main`, fix every URL in one go:

```bash
sed -i 's#/\.github/main/#/.github/YOUR_BRANCH/#g' profile/README.md
```

## 4. Check the result

Open <https://github.com/Ghost-Protocol-Lab>. You should see the hero banner, then the sections. If you see broken images:

- Make sure the repo is public and named exactly `.github`.
- Make sure the branch name matches step 3.
- Hard-refresh the page (Ctrl+Shift+R). GitHub caches images for a short while.

## 5. Placeholders to fill in

| Where | What | Status |
|---|---|---|
| `profile/README.md`, "Make contact" | A commented-out block of Discord, X, LinkedIn, Email and Newsletter badges with `TODO_` values. | The website's contact page says nothing is live yet, so no channels were invented. When a real channel exists, uncomment the block and replace the `TODO_` values. |
| `profile/README.md`, "Free for everyone" | Cyber Posts, Newsletter and Communities say **Coming soon**. | Taken from the placeholders on the website's free page. Replace "Coming soon" with a link once each one is live. |
| `profile/README.md`, "In the lab" | GHOSTGRID, GHOSTPROXY and GHOSTPROBE are marked **PLANNED**. | The website's homepage says "06 projects" but lists only three, and the roadmap page lists none. Update this table when you settle the real list. |

To find every unfinished spot: `grep -n "TODO_\|Coming soon\|PLANNED" profile/README.md`

## 6. Things that live elsewhere (not in this repo)

- **Organization avatar, description, website and location:** Organization **Settings -> Profile**. Set the website to `https://ghost-protocol-lab.github.io/Ghost-Protocol-Lab/`.
- **Pinned repositories:** on the org page, use **Customize pins** to show the five Damn_Practical repos first.
- **Members-only README (optional):** create a *private* repo named `.github-private` with `profile/README.md` inside. Members see it instead of the public one.

## 7. Changing the look

Edit the constants at the top of `scripts/make_assets.py`:

- `NAME`, `TAGLINE`: hero text.
- `TITLES`: the rotating lines under the name on the hero.
- `HEADERS`: the six section banners (id, title, subtitle).

Then regenerate and commit:

```bash
python3 scripts/make_assets.py
git add profile/assets && git commit -m "Refresh art" && git push
```

Colours and fonts are in `scripts/theme.py`. The art uses only system monospace fonts and has no scripts or external references, so GitHub renders it safely.

## Good to know

- The profile README is plain Markdown plus a little HTML. GitHub strips scripts and styles, which is why the animation lives inside the SVG files.
- The org page shows `profile/README.md` only. The root `README.md` is for people browsing the `.github` repo.
- A `.github` repo can also hold default community health files (`CODE_OF_CONDUCT.md`, `CONTRIBUTING.md`, `SECURITY.md`, issue templates) that apply to every org repo without its own. The five code-of-the-crypt rules in the README would make a good start for `CODE_OF_CONDUCT.md`.
- `SECURITY.md` is worth adding for a security org. Tell researchers where to send reports once you have a contact channel.
