# Operational Runbook & Troubleshooting Guide (`troubleshooting.md`)

![Diagnostics](https://img.shields.io/badge/Runbook-Troubleshooting%20%26%20Diagnostics-critical?style=flat-square)
![Coverage](https://img.shields.io/badge/Scope-Projects%201%E2%80%934-blue?style=flat-square)

This troubleshooting guide documents common failure modes, error codes, and operational roadblocks encountered across all four modules of the **VA Initiatives Ethical Hacking Project**, along with step-by-step resolutions.

---

## Table of Contents
- [1. Project 1 Troubleshooting: IDOR & Burp Suite HTTP/2 Interception](#1-project-1-troubleshooting-idor--burp-suite-http2-interception)
- [2. Project 2 Troubleshooting: Wireshark EAPOL Filtering & Aircrack-ng](#2-project-2-troubleshooting-wireshark-eapol-filtering--aircrack-ng)
- [3. Project 3 Troubleshooting: DVWA Medium SQLi & HTTP 500 Errors](#3-project-3-troubleshooting-dvwa-medium-sqli--http-500-errors)
- [4. Project 4 Troubleshooting: Python SQLite3 Parameter Binding](#4-project-4-troubleshooting-python-sqlite3-parameter-binding)

---

## 1. Project 1 Troubleshooting: IDOR & Burp Suite HTTP/2 Interception

### Issue 1.1: PortSwigger Lab Subdomain Returns `504 Gateway Timeout` or `Lab Expired`
* **Symptom:** Navigating to `https://0aaa00cc04df2f8e83d138b2006600ee.web-security-academy.net/` returns a timeout or "Lab session has expired" message.
* **Root Cause:** PortSwigger Web Security Academy generates ephemeral lab subdomains per session that automatically terminate after inactivity.
* **Resolution:**
  1. Log in to PortSwigger Academy and launch a fresh instance of the lab at `https://portswigger.net/web-security/access-control/lab-insecure-direct-object-references`.
  2. Capture the new `/download-transcript/{N}.txt` request in Burp Suite Proxy and update the `Host` header in Repeater to match your active lab instance.

### Issue 1.2: Clicking "View transcript" Downloads the File Without Appearing in Burp Proxy
* **Symptom:** The browser downloads `3.txt` or `4.txt`, but the `GET /download-transcript/4.txt` request does not pause in Burp Suite Proxy.
* **Root Cause:** Burp Suite's default **Intercept Client Requests** rules often exclude certain file extensions or only intercept requests with parameters (`URL Via Proxy` filter).
* **Resolution:**
  1. Even if the request was not paused by live Intercept, navigate to **Proxy** -> **HTTP history** in Burp Suite.
  2. Locate the `GET /download-transcript/4.txt` entry, right-click it, and select **Send to Repeater** (`Ctrl+R`).
  3. Alternatively, go to **Proxy** -> **Proxy settings** -> **Request interception rules** and uncheck exclusions for file extensions.

![Locating GET /download-transcript/4.txt in Burp Suite Repeater](./assets/images/Screenshot%202026-02-18%20013203.png)
*Figure 1: Inspecting `GET /download-transcript/4.txt` in Burp Suite Repeater after forwarding from HTTP history.*

---

## 2. Project 2 Troubleshooting: Wireshark EAPOL Filtering & Aircrack-ng

### Issue 2.1: Aircrack-ng Prompts `Please specify a dictionary (option -w)` and Exits
* **Symptom:** Running `aircrack-ng wpa.cap` identifies `1 potential targets` (`BSSID: 00:0D:93:EB:B0:8C`, `ESSID: test`, `WPA (1 handshake)`), prints `Please specify a dictionary (option -w).`, and quits.
* **Root Cause:** For WPA/WPA2-Personal captures, Aircrack-ng cannot crack the 4-way handshake without a wordlist file passed via the `-w` flag.
* **Resolution:**
  Provide the path to your downloaded wordlist (`passwad.txt` or `/usr/share/wordlists/rockyou.txt`):
  ```bash
  aircrack-ng wpa.cap -w passwad.txt
  ```

![Aircrack-ng Prompting for Dictionary Option -w](./assets/images/Screenshot%202026-02-18%20155443.png)
*Figure 2: Diagnostic screenshot showing `Please specify a dictionary (option -w)` when running `aircrack-ng wpa.cap` without `-w`.*

### Issue 2.2: `Passphrase not in dictionary` When Using an Incomplete or Corrupted Wordlist
* **Symptom:** Aircrack-ng finishes testing all keys in the file and outputs `Passphrase not in dictionary`.
* **Root Cause:** If the GitHub HTML page for `password.lst` was saved instead of the **Raw** text file, or if `passwad.txt` was truncated when pasting into `nano`, the word `biscotte` (located at line 2,293 of 2,294) may be missing.
* **Resolution:**
  Verify that `passwad.txt` contains `biscotte` and has 2,294 lines:
  ```bash
  wc -l ~/Downloads/passwad.txt
  grep -n "biscotte" ~/Downloads/passwad.txt
  ```
  If missing, re-download the raw file directly:
  ```bash
  curl -sSL [https://raw.githubusercontent.com/aircrack-ng/aircrack-ng/master/test/password.lst](https://raw.githubusercontent.com/aircrack-ng/aircrack-ng/master/test/password.lst) -o ~/Downloads/passwad.txt
  ```

### Issue 2.3: Wireshark Does Not Display the 4-Way Handshake Frames
* **Symptom:** Filtering in Wireshark returns zero packets.
* **Root Cause:** Using an uppercase filter (such as `EAPOL` or `WPA`) in Wireshark's display filter bar throws a syntax error (red filter bar).
* **Resolution:**
  Use the lowercase protocol filter `eapol` (filter bar turns green) to isolate Frames `2`, `4`, `6`, and `8`.

![Wireshark Green Filter Bar Using Lowercase eapol Filter](./assets/images/Screenshot%202026-02-18%20151321.png)
*Figure 3: Using the lowercase `eapol` display filter in Wireshark to isolate the 4-way handshake frames.*

---

## 3. Project 3 Troubleshooting: DVWA Medium SQLi & HTTP 500 Errors

### Issue 3.1: Quote-Based SQLi Payloads (`1'`, `1' OR '1'='1`) Return `HTTP/1.1 500 Internal Server Error`
* **Symptom:** Sending `id=1'&Submit=Submit` or `id=1' OR '1'='1&Submit=Submit` to `POST /DVWA/vulnerabilities/sqli/` in Burp Suite Repeater returns `HTTP/1.1 500 Internal Server Error` (Apache/2.4.65 Debian).
* **Root Cause:** At the `Medium` security level, DVWA sanitizes `$_POST['id']` using `mysqli_real_escape_string()`, which escapes single and double quotes (`\'` and `\"`). Because the backend SQL query does **not** wrap `$id` in quotes (`SELECT first_name, last_name FROM users WHERE user_id = $id;`), the escaped backslash (`WHERE user_id = 1\'`) causes a fatal MySQL syntax error.
* **Resolution:**
  Use a **quote-less numeric/boolean SQLi payload**:
  ```text
  id=1 OR 1=1&Submit=Submit
  ```
  Because there are no quotes in `1 OR 1=1`, `mysqli_real_escape_string()` leaves the payload unaltered, and MySQL evaluates `WHERE user_id = 1 OR 1=1;` as `TRUE` for all rows.

### Issue 3.2: Burp Suite Proxy Does Not Intercept `http://localhost/DVWA/` Traffic in Firefox
* **Symptom:** Submitting the DVWA form in Firefox bypasses Burp Suite Proxy completely.
* **Root Cause:** By default, Firefox's `network.proxy.allow_hijacking_localhost` preference is set to `false`, causing Firefox to bypass configured proxies for `localhost` and `127.0.0.1` traffic.
* **Resolution:**
  1. Open a new tab in Firefox and type `about:config` in the address bar.
  2. Search for `network.proxy.allow_hijacking_localhost`.
  3. Double-click the setting to toggle it to **`true`**.

### Issue 3.3: DVWA Redirects Back to `login.php` When Replaying Requests in Burp Repeater
* **Symptom:** Sending a request in Burp Repeater returns `HTTP/1.1 302 Found` with `Location: ../../login.php`.
* **Root Cause:** The `PHPSESSID` cookie expired or the `security=medium` cookie is missing from the `Cookie:` header.
* **Resolution:**
  Ensure your Repeater request includes both the active `PHPSESSID` and `security=medium` cookies:
  ```http
  Cookie: security=medium; PHPSESSID=<YOUR_ACTIVE_SESSION_ID>
  ```

---

## 4. Project 4 Troubleshooting: Python SQLite3 Parameter Binding

### Issue 4.1: `sqlite3.ProgrammingError: Incorrect number of bindings supplied`
* **Symptom:** Calling `cursor.execute(query, (id))` with a string like `"1 OR 1=1;"` throws:
  ```text
  Database error: Incorrect number of bindings supplied. The current statement uses 1, and there are 9 supplied.
  ```
* **Root Cause:** In Python, `(id)` without a trailing comma is evaluated as a parenthesized string (which is a sequence of 9 characters) rather than a 1-element tuple.
* **Resolution:**
  Always include the trailing comma `(id,)` when passing a single parameter tuple to `cursor.execute()`, exactly as implemented in `SQL_remediation.py`:
  ```python
  cursor.execute(query, (id,))
  ```

### Issue 4.2: `No user found with that ID.` Returned for All Inputs (Including Valid IDs)
* **Symptom:** Calling `get_user_info(1)` prints `No user found with that ID.` or `Database error: no such table: users`.
* **Root Cause:** `sqlite3.connect('users_database.db')` automatically creates an empty database file if `users_database.db` does not exist in the current working directory.
* **Resolution:**
  Run the database initialization snippet in [`setup.md` (Section 6)](./setup.md#6-project-4-setup-python-sqlite3-database--sql_remediationpy-verification) to create and seed the `users` table before testing `get_user_info()`.