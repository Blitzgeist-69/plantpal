# PlantPal — Testing

**Live site:** https://plantpal-ic-25eab202cb1a.herokuapp.com/

**Repo:** https://github.com/Blitzgeist-69/plantpal  

**Tester:** Ian Clifford

**Dates tested:** 10th September 2026

**Browsers / devices:**  

Chrome 153 & Edge 152 on Windows 11 Desktop, Chrome Dev Tools Mobile emulation

This file records the **manual** testing undertaken. Automated Django testing coverage is out of scope for v1.

---

**Result key**

| Result | Meaning |
| --- | --- |
| Pass | Matches expected behaviour |
| Fail | Does not match — must be fixed or explained |
| Pass (after fix) | Failed first time; retested after a commit |
| N/A | Feature not in v1 (see README out of scope) |


## 1. Deployment smoke test

To confirm production matches local, static files load, and Django is not in debug mode.

| ID | What | Steps | Expected | Result | Evidence |
| --- | --- | --- | --- | --- | --- |
| D1 | Home loads over HTTPS | Open https://plantpal-ic-25eab202cb1a.herokuapp.com/ | 200, title includes PlantPal, no Heroku application error | Pass  | [D1 home desktop ](readme_images/testing/d1-home-https.png) [D1 200](readme_images/testing/d1b-network-200.png) |
| D2 | Custom CSS / WhiteNoise | DevTools → Network. Confirm `/static/css/style.css` is 200 (not 404). Nav is dark green, page background pale green, footer present | Styles match local | Pass | [D2 CSS 200 ](readme_images/testing/d2-css-200.png)  |
| D3 | DEBUG is off | Visit a missing URL such as `/this-page-does-not-exist-xyz` | Custom PlantPal 404 | Pass | [D3 Custom 404](readme_images/testing/d3-404.png) |
| D4 | Favicon | Check tab icon | No 404 | Pass | [D4 Favicon](readme_images/testing/d4-fav.png) |
| D5 | Admin is not advertised | From the public site, there is no Admin link in the nav | admin/ in not in nav and not advertised to user | Pass | [D5 No admin in Nav ](readme_images/testing/d5-no-admin.png) |
| D6 | Live matches README claim | Compare live URL in README to the Heroku hostname | README & Live Site match | Pass | [ D6 README & Live match ](readme_images/testing/d6-readme-live-match.png) |

---

## 2. Public pages (logged out)

| ID | What | Steps | Expected | Result | Evidence |
| --- | --- | --- | --- | --- | --- |
| P1 | Home purpose is obvious | Open `/` logged out | Explanatory text and cards | Pass | [ P1 Clear Purpose ](readme_images/testing/p1-purpose.png) |
| P2 | Home CTAs | Click **Create an account** then browser Back, click **Log in** | `/accounts/register/` and `/accounts/login/` | Pass | [ P2 Home CTAs ](readme_images/testing/p2-ctas.png) |
| P3 | Logged-out nav | Inspect navbar | Brand **PlantPal**, **Log in**, **Register**. No Dashboard / My Plants / Add Plant / Log out | Pass | [ P3 Logged Out Nav ](readme_images/testing/p3-logged-out-nav.png) |
| P4 | Brand link | Click **PlantPal** on home | Stays on or returns to `/` | Pass | N/A |
| P5 | Footer | Scroll to bottom on home, login, register | Footer text: “PlantPal — track care, keep plants alive.” Stays at the bottom of the viewport on short pages | Pass | [ P5 Footer ](readme_images/testing/p5-footer.png) |
| P6 | Login page | Open `/accounts/login/` | Fields Username, Password; button **Log in**; link “No account? Register” | Pass | [ P6 Log In ](readme_images/testing/p6-login.png) |
| P7 | Register page | Open `/accounts/register/` | Username, Password, Password confirmation; Django help text; button **Register**; link to Log in | Pass | [ P7 Register ](readme_images/testing/p7-register.png) |
| P8 | No Lorem Ipsum | Read home + auth pages | Real product copy only | Pass | See P6 & P7 Evidence |

---

## 3. Authentication

Using a **new** username that does not already exist on production.

| ID | What | Steps | Expected | Result | Evidence |
| --- | --- | --- | --- | --- | --- |
| A1 | Register success | Submit valid username + matching strong passwords | Account created, auto-logged-in, flash “Welcome to PlantPal.”, redirect to `/dashboard/` | Pass | Username used: UserA [ User A ](readme_images/testing/a1-usera-logged-in.png)|
| A2 | Register — short password | Password `a123` | Form redisplays with Django validation errors; no account created | Pass | [ A2 Short Password ](readme_images/testing/a2-short-pass.png) |
| A3 | Register — mismatch | Password and confirmation differ | Form redisplays with Django validation errors; no account created | Pass | [ A3 Password Mismatch ](readme_images/testing/a3-pass-mismatch.png) |
| A4 | Register — duplicate username | Re-register User A’s name | Username already exists error | Pass | [ A4 Username Exists ](readme_images/testing/a4-dup-user.png) |
| A5 | Register while logged in | While logged in, visit `/accounts/register/` | Redirect to dashboard (no second account form) | Pass | [ A5 Logged in & Register ](readme_images/testing/a5a-logged-in-reg.png) - [ Directed to Dash ](readme_images/testing/a5b-logged-in-reg.png) |
| A6 | Login failure | Log out. Submit wrong password | Stay on login; error (e.g. “Please enter a correct username and password…”) | Pass | [ A6 Wrong Password ](readme_images/testing/a6-wrong-pass.png) |
| A7 | Login success | Correct User A credentials | Redirect to `/dashboard/`; nav shows Dashboard, My Plants, Add Plant, “Hi, {username}”, **Log out** | Pass | [ A7 Login Success ](readme_images/testing/a7-login-success.png) |
| A8 | Login `next` | Log out. Visit `/plants/` then log in | After login, land on `/plants/` | Pass | [ A8 Logged Out - Plants ](readme_images/testing/a8a-next.png) - [ A8 Plants displayed on Login ](readme_images/testing/a8b-next.png)|
| A9 | Logout | Click **Log out** | Redirect to home. Nav is logged-out again | Pass | [ A9 Log out to Home ](readme_images/testing/a9-log-out-to-home.png) |
| A10 | Session | Log in, close the tab, reopen the live URL | Still logged in unless private window | Pass | N/A |
| A11 | Logged-in home | While logged in, visit `/` | Redirect to `/dashboard/` — home is for guests | Pass | [ A11 Logged in `/` ](readme_images/testing/a11a-logged-in-home.png) - [ A11 Redirect to Dash ](readme_images/testing/a11b-logged-in-home.png) |

---

## 4. Auth gates (must log in)

**logged out**. Each protected URL should bounce to login with `?next=…`.

| ID | URL | Expected | Result | Evidence |
| --- | --- | --- | --- | --- |
| G1 | `/dashboard/` | Redirect to `/accounts/login/?next=/dashboard/` | Pass | [ G1 Dashboard ](readme_images/testing/g1-dashboard.png) |
| G2 | `/plants/` | Redirect to login with `next=/plants/` | Pass | [ G2 plants/ ](readme_images/testing/g2-plants.png) |
| G3 | `/plants/add/` | Redirect to login | Pass | [ G3 /plants/add/](readme_images/testing/g3-plants-add.png) |
| G4 | `/plants/1/` | Redirect to login (do not leak if id 1 exists) | Pass | [ G4 plants/1/ ](readme_images/testing/g4-plants-1.png) |
| G5 | `/plants/1/edit/` | Redirect to login | Pass | [ G5 plants/1/edit/ ](readme_images/testing/g5-plants-1-edit.png) |
| G6 | `/plants/1/delete/` | Redirect to login | Pass | [ G6 plants/1/delete ](readme_images/testing/g6-plants-1-delete.png) |

---

## 5. Empty states (User A, zero plants)

| ID | What | Steps | Expected | Result | Evidence |
| --- | --- | --- | --- | --- | --- |
| E1 | Empty dashboard | Log in as new User A. Open Dashboard | You are logged in. Plant lists will appear here once you add some. **Add Plant** button works | Pass | [ E1 Dashboard ](readme_images/testing/e1-dash.png) |
| E2 | Empty My Plants | Open My Plants | “You don't have any plants yet.” plus Add Plant | Pass | [ E2 My Plants ](readme_images/testing/e2-my-plants.png) |

---

## 6. Plant CREATE

| ID | What | Steps | Expected | Result | Evidence |
| --- | --- | --- | --- | --- | --- |
| C1 | Open form | Nav **Add Plant** | `/plants/add/`, empty form, fields: Nickname, Species, Location, Acquired date, Water frequency days, Light needs, Notes | Pass | [ C1 Add Plant ](readme_images/testing/c1-add-plant.png) |
| C2 | Required fields | Submit empty form | Nickname and Species (and frequency if cleared) show errors; plant is **not** created | Pass | [ C2 Required fields ](readme_images/testing/c2-required.png) |
| C3 | Frequency minimum | Set water frequency to `0` or blank | Rejected (`PositiveIntegerField` / `min=1`) | **Fail** | [ C3 Min Days ](readme_images/testing/c3-min-days.png)|
| C4 | Happy path | Create **Fern** with Bathroom, 3 days, Medium light | Success message “Fern has been added to your collection.” Redirect to Fern’s detail URL `/plants/<id>/` | Pass | [ C4 Happy Path ](readme_images/testing/c4-happy-path.png) |
| C5 | Optional blanks | Create **Monty** with location and notes empty, no acquired date | Saves. Detail omits Location/Notes. Acquired default to 'Today' | Pass | [ C5 Optional Blanks ](readme_images/testing/c5-opt-blank.png) |
| C6 | Immediate UI | Open My Plants | Fern and Monty cards appear | Pass | [ C6 Plants Cards appear ](readme_images/testing/c6-my-plants.png) |
| C7 | Owner is hidden | View page source / form | No user-id field. Owner is set in the view | Pass | [ C7 Page Source ](readme_images/testing/c7-page-source.png) |
| C8 | Date widget | Acquired date is a date picker (`type="date"`) | Date picker available; accepts type `dd/mm/yyyy` | Pass | [ C8 Date Picker ](readme_images/testing/c8-date-picker.png) |


---

## 7. Plant READ (list, detail, search)

| ID | What | Steps | Expected | Result | Evidence |
| --- | --- | --- | --- | --- | --- |
| R1 | List cards | `/plants/` | Cards show nickname (link), species, location if set, watering days. Ordered by nickname | Pass | [ R1 List Cards ](readme_images/testing/r1-list-cards.png) |
| R2 | Detail fields | Open Fern | Species, Location, Water every N days, Light display name, Notes if any. **Edit** and **Delete**. “Back to My Plants” | Pass | [ R2 Details Fields ](readme_images/testing/r2-detail-fields.png) |
| R3 | Search nickname | Query `Spike` | Only Spike. URL has `?q=Spike` | Pass | [ R3 Search Nickname ](readme_images/testing/r3-search-nickname.png) |
| R4 | Search species | Query `Monstera` | Only Monty | Pass | [ R4 Search Species ](readme_images/testing/r4-search-species.png) |
| R5 | Search location | Query `Hallway` | Only Spike | Pass | [ R5 Search Location](readme_images/testing/r5-search-location.png) |
| R6 | Search case | Query `spike` | Case-insensitive match | Pass | [ R6 Case Insensitive ](readme_images/testing/r6-search-case.png) |
| R7 | Search miss | Query `zzzz` | “No plants match zzzz.” Clear-search link returns full list | Pass | [ R7 Search 'zzzz' ](readme_images/testing/r7-search-zzzz.png) |


---

## 8. Care logs + dashboard (CREATE related records)

Dashboard “needs attention” uses **last Watered log only** + `water_frequency_days`. Other actions do not reset the watering clock. A plant with **no** water log is due today.

| ID | What | Steps | Expected | Result | Evidence |
| --- | --- | --- | --- | --- | --- |
| L1 | Empty history | Open a new plant | “No care has been logged for this plant yet.” Date field defaults to today | Pass | [ L1 Empty History ](readme_images/testing/l1-no-care.png) |
| L2 | Care required fields | Submit log with Action unset | Validation message; no row added | Pass | [ L2 Required Field ](readme_images/testing/l2-care-req.png) |
| L3 | Log Watered today on Fern | Action Watered, date today, optional note | Message “Logged Watered for Fern.” History shows `DD-MM-YYYY — Watered — notes` | Pass | [ L3 Watered ](readme_images/testing/l3-care-logged.png) |
| L4 | Other actions | On Monty, log Fertilized then Health check | Both rows appear. Display names (Fertilized, Health check) not raw keys | Pass | [ L4 Care Actions ](readme_images/testing/l4-care-actions.png) |
| L5 | Newest first | Add two logs on different dates | List ordered by date descending | Pass | [ L5 Newest Care First ](readme_images/testing/l5-care-date-order.png) |
| L6 | Dashboard after water | Fern watered today, frequency 3 | Fern in **Doing fine** with “next watering {today+3}” | Pass | [ L6 Fern Watered](readme_images/testing/l6-fern-watered.png) |
| L7 | Never watered | Spike has no water log | Spike in **Needs attention**, due date = today | Pass | [ L7 Never Watered ](readme_images/testing/l7-never-watered.png) |
| L8 | Overdue | On Orchid, log Watered with date **20 days ago**, frequency 7 | Orchid in **Needs attention**, “watering due {that date + 7}” | Pass | [ L8 Water > 20days ago](readme_images/testing/l8a-water-in-past.png) — [ L8 Still  in Dashboard ](readme_images/testing/l8b-in-dash.png) |
| L9 | Non-water does not clear due | Plant due + log only “Pruned” | Still needs attention (watering clock unchanged) | Pass | [ L9 Pruned ](readme_images/testing/l9a-pruned.png) — [ L9 Needs Attention ](readme_images/testing/l9b-in-dash.png) |


---

## 9. Plant UPDATE

| ID | What | Steps | Expected | Result | Evidence |
| --- | --- | --- | --- | --- | --- |
| U1 | Form is pre-filled | Edit Fern | All current values present; page is the shared plant form in edit mode | Pass | [ U1 Edit ](readme_images/testing/u1-edit.png) |
| U2 | Change location + frequency | Bathroom to Hallway, 3 to 7. Save | Message “Fern has been updated.” Detail shows new values | Pass | [ U2 Amend ](readme_images/testing/u2-amend.png) |
| U3 | List reflects edit | My Plants | Card shows Hallway / 7 days immediately | Pass | [ U3 Cards Updated ](readme_images/testing/u3-cards.png) |
| U4 | Invalid edit | Clear nickname, submit | Errors; previous nickname still in the database (reload detail) | Pass | [ U4 Amend with Missing Field ](readme_images/testing/u4-amend-missing-nickname.png) |

---

## 10. Plant DELETE

| ID | What | Steps | Expected | Result | Evidence |
| --- | --- | --- | --- | --- | --- |
| X1 | Confirm page | Click Delete on Orchid | Confirm page names the plant and is not an instant delete | Pass | [ X1 Delete Warning ](readme_images/testing/x1-delete-warning.png) |
| X2 | Cancel | Use Back / My Plants without posting | Orchid still exists | Pass | [ X2 Cancel Delete ](readme_images/testing/x2-orchid-remains.png) |
| X3 | Confirm delete | POST Delete | Message “Orchid has been deleted.” Redirect to My Plants. Card gone | Pass | [ X3 Plant Deleted ](readme_images/testing/x3-plant-deleted.png) |
| X4 | CASCADE | Before delete, add a care log. After delete, open the old `/plants/<id>/` | 404. Logs are gone with the plant (no orphan admin rows) | Pass | [ X4 Plant to Delete ](readme_images/testing/x4a-delete-plant-53.png) — [ X4 Plant Deleted ](readme_images/testing/x4b-deleted.png)|

---

## 11. Owner isolation (User A vs User B)

This is a **security** test using two browsers — Chrome for UserA & Edge for UserB.

| ID | What | Steps | Expected | Result | Evidence |
| --- | --- | --- | --- | --- | --- |
| S1 | List isolation | User B opens `/plants/` | Only Ficus — none of A’s nicknames | Pass | [ S1 List Isolation ](readme_images/testing/s1-list-isolation.png) |
| S2 | Guess detail | User B visits User A’s `/plants/<Fern id>/` | Custom 404 (“That page does not exist or you do not have access to it.”) | Pass | [ S2 Guess Detail ](readme_images/testing/s2-guess-id.png) |
| S3 | Guess edit GET | B opens A’s `/plants/<id>/edit/` | 404 | Pass | [ S3 Gues Edit ](readme_images/testing/s3-guess-edit.png) |
| S4 | Guess delete GET | B opens A’s `/plants/<id>/delete/` | 404 | Pass | [ S4 Guess Delete ](readme_images/testing/s4-guess-delete.png) |

---

## 12. Validation and defensive design

| ID | What | Steps | Expected | Result | Evidence |
| --- | --- | --- | --- | --- | --- |
| V1 | CSRF | Register/login/plant/care/delete forms | Hidden `csrfmiddlewaretoken` on every POST | Pass | [ V1 Register ](readme_images/testing/v1-register.png) [ V1 Login ](readme_images/testing/v1-login.png) [ V1 Add Plant ](readme_images/testing/v1-add-plant.png) [ V1 Care Log ](readme_images/testing/v1-care-log.png) [ V1 Delete ](readme_images/testing/v1-delete.png)|
| V2 | Logout CSRF | Log out button is inside a POST form with CSRF | GET `/accounts/logout/` does not silently log you out | Pass | [ V2 Logout CSRF ](readme_images/testing/v2-logout.png) |
| V3 | Huge nickname | 200+ character nickname | Max 100 | Pass | Field max is 100 characters and truncates pasted text |
| V4 | Negative frequency | `-5` | Rejected | Pass | [ V4 Negative Frequency ](readme_images/testing/v4-neg-freq.png) |
| V5 | Invalid pk | `/plants/99999/` as owner | 404 custom page | Pass | [ V5 Invalid pk ](readme_images/testing/v5-invalid-pk.png) |
| V6 | Invalid pk type | `/plants/abc/` | 404 (URL does not match int converter) | Pass | [ V6 Invalid pk Type ](readme_images/testing/v6-invalid-pk-type.png) |
| V7 | Back / Forward | Create a plant, go Back to the form, Forward | No crash; no duplicate | Pass | No crash or duplicate created |

---

## 13. Responsiveness

Use Chrome DevTools device mode. Do **not** only stretch a desktop window.

| ID | Viewport | Pages to open | Expected | Result | Evidence |
| --- | --- | --- | --- | --- | --- |
| M1 | 375 × 812 (iPhone) | Home, login, dashboard, list, detail, add form, delete | Hamburger toggles. No horizontal scroll. Forms usable with one thumb. Footer not covering the primary button | Pass | [ M1 Home ](readme_images/testing/m1-375px-home.png)  [ M1 Dashboard ](readme_images/testing/m1-375px-dash.png)  [ M1 Add Plant ](readme_images/testing/m1-375px-plant.png)  [ M1 My Plants ](readme_images/testing/m1-375px-my-plants.png) |
| M2 | 768 × 1024 (tablet) | Same set | Cards wrap; nav may expand; readable measure | Pass | [ M2 Home ](readme_images/testing/m2-768px-home.png)  [ M2 Dashboard ](readme_images/testing/m2-768px-dash.png)  [ M2 Add Plant ](readme_images/testing/m2-768px-plant.png) [ M2 My Plants ](readme_images/testing/m2-768px-my-plants.png)|
| M3 | 1280+ desktop | Same set | Nav inline; cards in a row on home; footer full width | Pass | [ M3 Home ](readme_images/testing/m3-1280px-home.png) [ M3 My Plants ](readme_images/testing/m3-1280px-my-plants.png) |
| M4 | Hamburger | Mobile: open menu, follow Dashboard, reopen | Menu works after navigation | Pass | N/A |

---

### Lighthouse / WAVE notes

| Page | Tool | Score / issues | Action |
| --- | --- | --- | --- |
| Home `/` | Lighthouse | 98 | [ Lighthouse Home ](readme_images/testing/lighthouse-home.png) |
| Dashboard | Lighthouse | 97 | [ Lighthouse Dashboard ](readme_images/testing/lighthouse-dash.png) |
| Add plant | Lighthouse | 98 | [ Lighthouse Add Plant ](readme_images/testing/lighthouse-add-plant.png) |
| My Plants | Lighthouse | 96 | [ Lighthouse My Plants ](readme_images/testing/lighthouse-my-plants.png) |
| Home `/` | WAVE | 10 | [ WAVE Home ](readme_images/testing/wave-home.png) |
| Dashboard | WAVE | 10 | [ WAVE Dashboard](readme_images/testing/wave-dash.png) |
| Add Plant | WAVE | 9.4 | [ WAVE Add Plant ](readme_images/testing/wave-add-plant.png) |
| My Plants | WAVE | 10 | [ WAVE My Plants ](readme_images/testing/wave-my-plants.png) |

---

## 14. Code quality validators

### HTML (W3C Markup Validation Service)

Validate **View Source** of rendered pages (not the raw template). Unauthenticated pages can use the live URL; logged-in pages: save HTML or use the “direct input” tab.

| Page | URL | Errors | Warnings | Result | Notes |
| --- | --- | --- | --- | --- | --- |
| Home | `/` | None | Section lacks heading | Pass | [ Home ](readme_images/testing/w3c-html-home.png) |
| Login | `/accounts/login/` | None | None | Pass | [ Login ](readme_images/testing/w3c-html-login.png) |
| Register | `/accounts/register/` | Stray Tags | None | **Fail** | [ Registration ](readme_images/testing/w3c-html-register-fail.png) |
| Dashboard | `/dashboard/` | None | None | Pass | [ Dashboard ](readme_images/testing/w3c-html-dash.png) |
| My Plants | `/plants/` | None | None | Pass | [ My Plants ](readme_images/testing/w3c-html-my-plants.png) |
| Plant detail | `/plants/<id>/` | None | None | Pass | [ Plant Detail](readme_images/testing/w3c-html-plant-detail.png) |
| Add plant | `/plants/add/` | None | None | Pass | [ Add Plant ](readme_images/testing/w3c-html-add-plant.png) |
| Delete confirm | `/plants/<id>/delete/` | None | None | Pass | [ Delete Confirm ](readme_images/testing/w3c-html-delete-confirm.png) |
| 404 | `/this-page-does-not-exist-xyz` | None | None | Pass | [ 404 ](readme_images/testing/w3c-html-404.png) |

### CSS (W3C Jigsaw)

| File | Errors | Warnings | Result | Evidence |
| --- | --- | --- | --- | --- |
| `/static/css/style.css` | None | None | Pass | [ style.css ](readme_images/testing/w3c-css.png) |



### Python (PEP 8)

[ PEP8 Flake8 ](readme_images/testing/pep8-flake8.png)

---

## 15. User story acceptance

### Must have

| Story | Covered by | Pass? |  |
| --- | --- | --- | --- |
| Create an account | A1–A4 | Pass |  |
| Log in and log out | A6–A9 | Pass |  |
| Clear home + nav before register | P1–P3 | Pass |  |
| Add a plant with nickname, species, frequency | C4 | Pass |  |
| See all plants and search | R1–R7 | Pass |  |
| Open one plant + care history | R2, L1–L5 | Pass |  |
| Change a plant | U1–U3 | Pass |  |
| Delete a plant | X1–X4 | Pass |  |
| Record watering / care | L3–L4 | Pass |  |
| Dashboard due / overdue | L6–L9 | Pass |  |
| Nobody else can read or change my plants | S1–S4 | Pass |  |

### Should have

| Story | Covered by | Pass? |  |
| --- | --- | --- | --- |
| Works on a small screen | M1, M4 | Pass |  |
| Success / error message after every save | C2, A2 | Pass |  |

### Could have (out of scope)

| Story | Status |
| --- | --- |
| Plant photo | N/A — not in v1 |
| Edit / delete a care log row | N/A — create-only history |
| Email reminders | N/A |

---

## Bugs found

| ID | Found in test | Description | Severity | Status | Fix / commit | Why left unfixed (if any) |
| --- | --- | --- | --- | --- | --- | --- |
| B1 | C3  | Min days can be 0 | Low  | Open | N/A | Time contraints prevent fix in v1. Issue is low severity and risk in 'fixing' outweighs benefit |
| B2 | V3 | Very long Nickname overflows cards | Low | Open | N/A | Time contraints prevent fix in v1. Issue is low severity and risk in 'fixing' outweighs benefit |
| B3 | Code Quality Validation - HTML Registration | Stray Tags [ Registration Fail ](readme_images/testing/w3c-html-register-fail.png) | Low | Open | N/A | Time contraints prevent fix in v1. Issue is low severity and risk in 'fixing' outweighs benefit |

### Severity

- **High** — data loss, 500, owner leak, cannot complete CRUD
- **Medium** — wrong dashboard bucket, broken link, validation missing
- **Low** — copy typo, spacing, validator warning

---

## Known limitations (not bugs)

- Dashboard due-date uses the latest **Watered** log only. Fertilize / prune / check do not move the watering due date or move plants out of 'Needs Attention'.
- Care history is append-only. A mistyped log cannot be edited or deleted in v1.
- No password-reset email.
- No plant photographs in v1.
- Manual testing only — no pytest / `TestCase` suite.


