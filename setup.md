# Lab Setup & Reproduction Guide (`setup.md`)

![Environment](https://img.shields.io/badge/OS-Kali%20Linux%202025%2F2026-557C94?style=flat-square&logo=kalilinux&logoColor=white)
![Tools](https://img.shields.io/badge/Stack-Burp%20Suite%20%7C%20Wireshark%20%7C%20Aircrack--ng%20%7C%20DVWA%20%7C%20Python%203-blue?style=flat-square)

This guide provides step-by-step instructions to configure the laboratory environment, install required dependencies, organize repository assets, and reproduce all four modules of the **VA Initiatives Ethical Hacking Project**.

---

## Table of Contents
- [1. System Prerequisites & Repository Cloning](#1-system-prerequisites--repository-cloning)
- [2. Image Assets Directory Mapping](#2-image-assets-directory-mapping)
- [3. Project 1 Setup: PortSwigger IDOR Lab & Burp Suite](#3-project-1-setup-portswigger-idor-lab--burp-suite)
- [4. Project 2 Setup: Wireshark, Aircrack-ng & Wordlist Acquisition](#4-project-2-setup-wireshark-aircrack-ng--wordlist-acquisition)
- [5. Project 3 Setup: Local DVWA Deployment (Medium Security Level)](#5-project-3-setup-local-dvwa-deployment-medium-security-level)
- [6. Project 4 Setup: Python SQLite3 Database & `SQL_remediation.py` Verification](#6-project-4-setup-python-sqlite3-database--sql_remediationpy-verification)

---

## 1. System Prerequisites & Repository Cloning

### Recommended Virtual Machine Specifications
* **Host Hypervisor:** Oracle VirtualBox (or VMware Workstation / WSL2)
* **Guest OS:** Kali Linux (`x86_64`, 2 vCPUs, 4 GB RAM minimum)
* **Required Packages:** `burpsuite`, `wireshark`, `aircrack-ng`, `apache2`, `mariadb-server`, `php`, `php-mysqli`, `python3`, `sqlite3`, `git`, `curl`

### Clone the Repository
```bash
git clone [https://github.com/ch1n4x4/VA-Mentorship-project.git](https://github.com/ch1n4x4/VA-Mentorship-project.git)
cd VA-Mentorship-project
mkdir -p assets/images
```

---

## 2. Image Assets Directory Mapping

Ensure the 22 screenshots extracted from `assets/CHINAZA_NNAMANI_VA_INITIATIVES_ETHICAL_HACKING_PROJECT.pdf` are placed in `./assets/images/` using the following filenames referenced in `README.md`:

| Project Module | Image Path in Repository | Description in Documentation PDF |
| :--- | :--- | :--- |
| **Project 1 (IDOR)** | `./assets/images/page1_img1.png` | Page 1: Online retail store home page (`WE LIKE TO SHOP`) |
| **Project 1 (IDOR)** | `./assets/images/page2_img1.png` | Page 2 (Top): `My account` Login page |
| **Project 1 (IDOR)** | `./assets/images/page2_img2.png` | Page 2 (Bottom): Live chat with Hal Pline & `3.txt` / `4.txt` downloads |
| **Project 1 (IDOR)** | `./assets/images/page3_img1.png` | Page 3: Burp Suite Repeater capturing `GET /download-transcript/4.txt` |
| **Project 1 (IDOR)** | `./assets/images/page4_img1.png` | Page 4: Burp Suite Repeater exploiting `GET /download-transcript/1.txt` (leaking `carlos` password) |
| **Project 2 (PCAP)** | `./assets/images/page6_img1.png` | Page 6 (Top): Wireshark displaying all 13 packets of `wpa.cap` |
| **Project 2 (PCAP)** | `./assets/images/page6_img2.png` | Page 6 (Bottom): Wireshark filtered by `eapol` showing the 4-way WPA handshake |
| **Project 2 (PCAP)** | `./assets/images/page7_img1.png` | Page 7: Aircrack-ng `1.7` showing `KEY FOUND! [ biscotte ]` |
| **Project 2 (PCAP)** | `./assets/images/page8_img1.png` | Page 8 (Top): Running `aircrack-ng wpa.cap` to confirm handshake presence |
| **Project 2 (PCAP)** | `./assets/images/page8_img2.png` | Page 8 (Bottom): Aircrack-ng GitHub repo (`aircrack-ng/test/password.lst`) |
| **Project 2 (PCAP)** | `./assets/images/page9_img1.png` | Page 9: Executing `aircrack-ng wpa.cap -w passwad.txt` |
| **Project 3 (SQLi)** | `./assets/images/page11_img1.png` | Page 11 (Top): DVWA SQL Injection page with `User ID` dropdown |
| **Project 3 (SQLi)** | `./assets/images/page11_img2.png` | Page 11 (Bottom): DVWA status confirming `Security Level: medium` |
| **Project 3 (SQLi)** | `./assets/images/page12_img1.png` | Page 12 (Top): DVWA `Low` security PHP source code |
| **Project 3 (SQLi)** | `./assets/images/page12_img2.png` | Page 12 (Bottom): DVWA `Medium` security PHP source code (`mysqli_real_escape_string`) |
| **Project 3 (SQLi)** | `./assets/images/page13_img1.png` | Page 13: Burp Suite Proxy intercepting `POST /DVWA/vulnerabilities/sqli/` |
| **Project 3 (SQLi)** | `./assets/images/page14_img1.png` | Page 14: Burp Suite Repeater returning `HTTP 500` on `id=1'&Submit=Submit` |
| **Project 3 (SQLi)** | `./assets/images/page15_img1.png` | Page 15 (Top): Burp Suite Repeater returning `HTTP 200 OK` on `id=1 OR 1=1&Submit=Submit` |
| **Project 3 (SQLi)** | `./assets/images/page15_img2.png` | Page 15 (Bottom): Burp Suite Proxy intercepting request prior to injection |
| **Project 3 (SQLi)** | `./assets/images/page16_img1.png` | Page 16 (Top): Burp Suite Proxy injecting `id=1 OR 1=1&Submit=Submit` |
| **Project 3 (SQLi)** | `./assets/images/page16_img2.png` | Page 16 (Bottom): DVWA browser page dumping all 5 user records |
| **Project 4 (Code)** | `./assets/images/page20_img1.png` | Page 20: Specification for building the secure Python backend module |

---

## 3. Project 1 Setup: PortSwigger IDOR Lab & Burp Suite

1. **Launch Burp Suite:**
   ```bash
   burpsuite &
   ```
   * Select **Temporary Project** -> **Use Burp Defaults** -> **Start Burp**.
   * Navigate to **Proxy** -> **Proxy settings** and confirm the listener is active on `127.0.0.1:8080`.
2. **Access the PortSwigger IDOR Lab:**
   * Open Burp's built-in Chromium browser (or Firefox configured with FoxyProxy pointing to `127.0.0.1:8080`).
   * Navigate to the PortSwigger Lab: `https://portswigger.net/web-security/access-control/lab-insecure-direct-object-references` and click **Access the lab**.
3. **Reproduce the IDOR Exploitation:**
   * Click the **Live chat** tab, send a test message, and click **View transcript**.
   * In Burp Suite, navigate to **Proxy** -> **HTTP history**, locate `GET /download-transcript/4.txt` (or `2.txt`/`3.txt`), right-click, and select **Send to Repeater** (`Ctrl+R`).
   * In **Repeater**, change the request line to `GET /download-transcript/1.txt HTTP/2` and click **Send** to retrieve `carlos`'s plaintext password.

---

## 4. Project 2 Setup: Wireshark, Aircrack-ng & Wordlist Acquisition

1. **Install Wireshark and Aircrack-ng:**
   ```bash
   sudo apt update && sudo apt install -y wireshark aircrack-ng curl
   ```
2. **Download the Sample `wpa.cap` Capture and `password.lst` Wordlist:**
   ```bash
   mkdir -p ~/Downloads && cd ~/Downloads

   # Download the official Aircrack-ng test WPA capture file (wpa.cap)
   curl -sSL [https://raw.githubusercontent.com/aircrack-ng/aircrack-ng/master/test/wpa.cap](https://raw.githubusercontent.com/aircrack-ng/aircrack-ng/master/test/wpa.cap) -o wpa.cap

   # Download Solar Designer's 2,294-line password list into passwad.txt
   curl -sSL [https://raw.githubusercontent.com/aircrack-ng/aircrack-ng/master/test/password.lst](https://raw.githubusercontent.com/aircrack-ng/aircrack-ng/master/test/password.lst) -o passwad.txt
   ```
3. **Inspect the Handshake in Wireshark:**
   ```bash
   wireshark ~/Downloads/wpa.cap &
   ```
   * In the Wireshark display filter bar, type `eapol` and press `Enter` to view the 4-way handshake between `Apple_eb:b0:8c` (`00:0d:93:eb:b0:8c`) and `Netgear_91:53:5d` (`00:09:5b:91:53:5d`).
4. **Crack the Handshake with Aircrack-ng:**
   ```bash
   aircrack-ng ~/Downloads/wpa.cap -w ~/Downloads/passwad.txt
   ```

---

## 5. Project 3 Setup: Local DVWA Deployment (Medium Security Level)

1. **Install and Start DVWA on Kali Linux:**
   ```bash
   sudo apt update && sudo apt install -y dvwa
   sudo dvwa-start
   ```
   *(Alternatively, if running DVWA via Apache & MariaDB manually under `/var/www/html/DVWA`, ensure `sudo systemctl start apache2 mariadb` is running).*
2. **Initialize the DVWA Database & Set Security Level to `Medium`:**
   * Open Firefox and navigate to `http://localhost/DVWA/login.php`.
   * Log in with default credentials:
     * **Username:** `admin`
     * **Password:** `password`
   * Click **Setup / Reset DB** -> **Create / Reset Database**.
   * Navigate to **DVWA Security** on the left sidebar, select **`Medium`** from the dropdown menu, and click **Submit**.
3. **Reproduce the Medium SQLi Bypass:**
   * Navigate to **SQL Injection** (`http://localhost/DVWA/vulnerabilities/sqli/`).
   * Enable **Intercept is on** in Burp Suite Proxy, select `1` from the `User ID` dropdown, and click **Submit**.
   * In Burp Suite Proxy (or Repeater), change the request body from `id=1&Submit=Submit` to:
     ```text
     id=1 OR 1=1&Submit=Submit
     ```
   * Click **Forward** to view all 5 user records dumped in the browser.

---

## 6. Project 4 Setup: Python SQLite3 Database & `SQL_remediation.py` Verification

To test `SQL_remediation.py` locally against both legitimate user IDs and malicious SQL injection payloads (`"1 OR 1=1;"`), run the following initialization and verification commands:

1. **Initialize `users_database.db` with Sample DVWA User Records:**
   ```bash
   python3 -c "
   import sqlite3
   conn = sqlite3.connect('users_database.db')
   cur = conn.cursor()
   cur.execute('CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, first_name TEXT, last_name TEXT)')
   cur.executemany('INSERT OR REPLACE INTO users (id, first_name, last_name) VALUES (?, ?, ?)', [
       (1, 'admin', 'admin'),
       (2, 'Gordon', 'Brown'),
       (3, 'Hack', 'Me'),
       (4, 'Pablo', 'Picasso'),
       (5, 'Bob', 'Smith')
   ])
   conn.commit()
   conn.close()
   print('Database initialized successfully.')
   "
   ```
2. **Test Legitimate Lookup vs. Malicious SQL Injection Payload:**
   ```bash
   python3 -c "
   from SQL_remediation import get_user_info

   print('--- Test 1: Legitimate User Lookup (id = 1) ---')
   get_user_info(1)

   print('\n--- Test 2: Malicious SQLi Payload (id = \"1 OR 1=1;\") ---')
   malicious_input = '1 OR 1=1;'
   get_user_info(malicious_input)
   "
   ```
   **Expected Output:**
   ```text
   --- Test 1: Legitimate User Lookup (id = 1) ---
   ID: 1
   First Name: admin
   Surname: admin

   --- Test 2: Malicious SQLi Payload (id = "1 OR 1=1;") ---
   No user found with that ID.
   ```