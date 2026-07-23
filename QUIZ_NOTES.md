# Quiz-day run order (mapped to Q1-Q10)

## 0. Before anything else -- get the password list file

The grading machine may have slow/no internet, and the whole DB init depends on this
file existing at build time. Download it now, on your own connection:

```bash
curl -L -o db/data/100k-most-used-passwords-NCSC.txt \
  https://raw.githubusercontent.com/danielmiessler/SecLists/master/Passwords/Common-Credentials/100k-most-used-passwords-NCSC.txt
```

Commit this file to git (don't gitignore it) -- it needs to travel with the zip so
`docker-compose up` on the marker's machine can load it with zero internet dependency.

Also pre-pull the big images tonight:
```bash
docker pull postgres:16-alpine
docker pull gitea/gitea:latest
docker pull sonarqube:community
docker pull python:3.12-slim
docker pull nginx:alpine
```

## 1. Make sure the literal command `sudo docker-compose up` works

The paper asks for the old hyphenated `docker-compose` command specifically. You have
the new `docker compose` (space) plugin. If the standalone binary isn't installed,
add a tiny wrapper so both forms work:

```bash
sudo tee /usr/local/bin/docker-compose > /dev/null <<'EOF'
#!/bin/bash
exec docker compose "$@"
EOF
sudo chmod +x /usr/local/bin/docker-compose
```
Test it: `sudo docker-compose up -d --build`

## 2. Bring the stack up

```bash
sudo docker-compose up -d --build
```
This starts `db`, `web`, `nginx`, `gitea`, `sonarqube`. First boot takes a few minutes
(SonarQube especially) -- give it time before checking each URL.

## 3. Q1 + Q2 -- webserver + HTTPS

- Web server is nginx, terminating TLS with a self-signed cert generated at image
  build time (`nginx/Dockerfile`).
- Visit **https://127.0.0.1/** -- your browser will warn "not secure" / "not private"
  because the cert is self-signed and untrusted. That warning is *expected and correct*
  for a self-signed cert -- click through it (Advanced -> Proceed). Don't try to make
  the warning disappear; that would mean you paid for a CA-signed cert, which isn't
  what was asked for.
- The "config username as admin / password 2301483@sit.singaporetech.edu.sg when
  necessary" instruction is used for the **gitea** admin account (Q3's identity is
  the *commit* identity, which is different) -- see step 4.

## 4. Q3 -- local git server + commit identity

Create the gitea admin login (the Q1 credentials):
```bash
./scripts/setup-gitea-admin.sh
```
Then set your **local repo's** git commit identity (not global, so it doesn't
touch your personal projects):
```bash
git init
git config user.name "Tan Tze Han"
git config user.email "2301483@sit.singaporetech.edu.sg"
```

## 5. Q4 -- the web app

Already built in `web/`. Quick self-check before moving on:
- `https://127.0.0.1/` -> login form (username + password)
- `https://127.0.0.1/register` -> account creation form
- Enter a common password (e.g. `password`) -> stays on the same page
- Enter something like `Zx9!Quartz-Meridian` -> Welcome page, shows the password,
  logout button returns to `/`
- After registering, confirm the row landed in the DB:
  ```bash
  docker exec -it db psql -U quizuser -d quizdb -c 'SELECT * FROM "2301483";'
  ```

Commit it:
```bash
git add .
git commit -m "Q4: password login + account creation app"
```

## 6. Q5 + Q6 -- GitHub Actions + committing everywhere

GitHub Actions only runs from a repo hosted on github.com -- your local gitea server
can't trigger it. So you push to **both** remotes:

```bash
# to your local git server (gitea) -- create an empty repo at http://localhost:3000 first
git remote add gitea http://localhost:3000/admin/<repo-name>.git
git push gitea main

# to GitHub -- create an empty repo on github.com first
git remote add origin https://github.com/<your-username>/<repo-name>.git
git push -u origin main
```
The workflow file `.github/workflows/ci.yml` is already in the repo, so pushing to
GitHub triggers it immediately -- check the **Actions** tab on your GitHub repo.

## 7. Q7 -- ESLint security in the pipeline

Already wired up as the `eslint-security` job in `ci.yml`, using
`eslint-plugin-security` against `web/static/validate.js`. Nothing extra to do
unless the workflow fails -- check the Actions log for the specific rule violated.

## 8. Q8 -- SonarQube credentials

```bash
./scripts/set-sonarqube-password.sh
```
Then confirm you can log in at **http://127.0.0.1:9000/** with
`admin / 2301483@sit.singaporetech.edu.sg`.

If the script's curl call fails (SonarQube enforces a password policy and may reject
this string), log in once via the browser with `admin/admin`, let it force a password
change, and set it there manually -- the UI tells you exactly which rule it violates.

## 9. Q9 -- local SonarQube scan

1. Log in to http://127.0.0.1:9000
2. My Account -> Security -> Generate Token (copy it)
3. Run:
   ```bash
   ./scripts/sonar-scan.sh <paste-token-here>
   ```
4. Refresh the SonarQube dashboard -- you should see Bugs / Vulnerabilities /
   Security Hotspots for the `web/` source.

`host.docker.internal` resolves correctly from inside a container on Mac Docker
Desktop with no extra flags -- this is one of the few things that's actually
*easier* on Mac than on Linux.

## 10. Q10 -- fix findings and rescan

The app here is intentionally short and avoids the classic culprits (no string-built
SQL, no `eval`, output is auto-escaped by Jinja2, no secrets hardcoded beyond the
required demo credentials) so it should come back close to clean. If SonarQube flags
anything:
1. Read what it flagged and why.
2. Fix it in the smallest way that addresses the actual issue (remember Q4-k: marks
   are deducted for unnecessarily long/complex code -- don't over-engineer the fix).
3. Re-run `./scripts/sonar-scan.sh <token>` and confirm the dashboard shows 0 open
   bugs/vulnerabilities and all hotspots reviewed.
4. Commit the fix and push to both remotes again (step 6).

## Final checklist before submission

- [ ] `db/data/100k-most-used-passwords-NCSC.txt` is committed (not gitignored)
- [ ] `sudo docker-compose up` works from a clean unzip
- [ ] https://127.0.0.1/ loads (self-signed warning is fine)
- [ ] gitea admin login works with the Q1 credentials
- [ ] Local git commit identity is Tan Tze Han / 2301483@sit.singaporetech.edu.sg
- [ ] GitHub Actions run is green (or at worst, its logs show a legitimate/explainable
      partial failure) on the Actions tab
- [ ] SonarQube reachable at http://127.0.0.1:9000/ with the Q8 credentials
- [ ] SonarQube dashboard shows 0 bugs / 0 vulnerabilities / hotspots reviewed
- [ ] Whole repo zipped as `StudentID.zip` (check the original paper's exact naming
      rule once you have it in front of you)
- [ ] Logout and restart the lab PC when done, if that's still a submission rule this year
