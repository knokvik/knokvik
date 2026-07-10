# knokvik profile README — setup guide

Self-updating **neofetch-style** SVG card for [github.com/knokvik](https://github.com/knokvik), inspired by [Andrew6rant](https://github.com/Andrew6rant/Andrew6rant).

## What’s in this repo

| File | Purpose |
| --- | --- |
| `README.md` | Profile page (embeds dark/light SVGs) |
| `dark_mode.svg` / `light_mode.svg` | The card (stats updated by the script) |
| `today.py` | Fetches GitHub stats + rewrites the SVGs |
| `.github/workflows/build.yaml` | Runs daily at 04:00 UTC |
| `cache/` | LOC cache + `requirements.txt` |

## One-time setup

### 1. Push this folder to your special profile repo

The repo **must** be named exactly `knokvik` under your account:

```bash
cd ~/Programming/knokvik
git init
git remote add origin https://github.com/knokvik/knokvik.git
# If the remote already has history (e.g. profile-3d-contrib):
git fetch origin
git checkout -b main origin/main   # or merge carefully
# Then add the new files and push
git add .
git commit -m "feat: neofetch-style self-updating profile card"
git push -u origin main
```

> Your GitHub account already has `knokvik/knokvik` with a 3D contrib graph.  
> Either replace the empty README with this setup, or copy these files into a local clone of that repo so you keep `profile-3d-contrib/`.

### 2. Create a Personal Access Token

1. GitHub → **Settings → Developer settings → Personal access tokens → Fine-grained tokens**
2. Create a token with **All repositories** (or at least public ones you want counted)
3. Permissions:
   - **Account**: `Followers: Read`, `Starring: Read`, `Watching: Read`
   - **Repository**: `Contents: Read`, `Metadata: Read`
4. Copy the token.

### 3. Add repository secrets

On `knokvik/knokvik` → **Settings → Secrets and variables → Actions**:

| Secret | Value |
| --- | --- |
| `ACCESS_TOKEN` | The fine-grained PAT from step 2 |
| `USER_NAME` | `knokvik` |

### 4. Set your real birthday

In `today.py`:

```python
BIRTHDAY = datetime.datetime(2004, 1, 1)  # change year, month, day
```

This drives the **Uptime** field.

### 5. Personalize static text (optional)

Edit both SVGs (`dark_mode.svg` and `light_mode.svg`) for:

- OS / Host / Kernel / IDE  
- Languages & hobbies  
- Contact lines  
- Left-side ASCII art  

Keep the `id="..."` attributes on stats (`age_data`, `repo_data`, `commit_data`, etc.) — the script targets those.

### 6. Run the workflow

- **Actions → README build → Run workflow**, or  
- Push to `main` (workflow runs on push too).

First run may take a few minutes while it walks all repos for LOC. Later runs use `cache/`.

## Local dry-run

```bash
cd ~/Programming/knokvik
python3 -m venv .venv && source .venv/bin/activate
pip install -r cache/requirements.txt
export ACCESS_TOKEN="ghp_..."   # or fine-grained token
export USER_NAME="knokvik"
python today.py
```

Open `dark_mode.svg` / `light_mode.svg` in a browser to preview.

## Dark / light mode

GitHub’s `<picture>` + `prefers-color-scheme` in `README.md` picks the right SVG automatically.

## Keeping the 3D contribution graph

If you still want the old 3D graph under the card, add this to `README.md`:

```markdown
![3D Contribution Graph](./profile-3d-contrib/profile-night-green.svg)
```

(Requires the existing `profile-3d-contrib/` folder and its workflow.)

## Troubleshooting

| Symptom | Fix |
| --- | --- |
| Workflow fails auth | Re-check `ACCESS_TOKEN` / `USER_NAME` secrets |
| Stats stay `0` | Run workflow once; confirm token can read your repos |
| 403 / rate limit on LOC | Wait and re-run; cache will resume from partial file |
| Age wrong | Fix `BIRTHDAY` in `today.py` |
| Card text misaligned | Re-balance dots/spaces in SVG after editing long values |

## Credits

Architecture adapted from [Andrew6rant/Andrew6rant](https://github.com/Andrew6rant/Andrew6rant).
