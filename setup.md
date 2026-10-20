# Lab Setup & Reproduction Guide (`setup.md`)

![Environment](https://img.shields.io/badge/OS-Kali%20Linux%202025%2F2026-557C94?style=flat-square&logo=kalilinux&logoColor=white)
![Tools](https://img.shields.io/badge/Stack-Burp%20Suite%20%7C%20Wireshark%20%7C%20Aircrack--ng%20%7C%20DVWA%20%7C%20Python%203-blue?style=flat-square)

This guide provides step-by-step instructions to configure the laboratory environment, install required dependencies, verify repository image assets, and reproduce all four modules of the **VA Initiatives Ethical Hacking Project**.

---

## Table of Contents
- [1. System Prerequisites & Repository Cloning](#1-system-prerequisites--repository-cloning)
- [2. Image Assets Directory Mapping (`./assets/images/`)](#2-image-assets-directory-mapping-assetsimages)
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
```

---

## 2. Image Assets Directory Mapping (`./assets/images/`)

The `./assets/images/` directory contains 16 lab screenshots captured on February 18, 2026. Below is the complete mapping of each file in `./assets/images/` to its corresponding project phase:

| Project Module | Filename in `./assets/images/` | URL-Encoded Markdown Link | Description |
| :--- | :--- | :--- | :--- |
| **Project 1 (IDOR)** | `Screenshot 2026-02-18 002334.png` | `./assets/images/Screenshot%202026-02-18%20002334.png` | `My account` Login page & initial reconnaissance (`12:23 AM`) |
| **Project 1 (IDOR)** | `Screenshot 2026-02-18 002704.png` | `./assets/images/Screenshot%202026-02-18%20002704.png` | Online retail store home page (`WE LIKE TO SHOP`, `12:27 AM`) |
| **Project 1 (IDOR)** | `Screenshot 2026-02-18 013226.png` | `./assets/images/Screenshot%202026-02-18%20013226.png` | Live chat with Hal Pline & sequential `3.txt` / `4.txt` downloads (`1:32 AM`) |
| **Project 1 (IDOR)** | `Screenshot 2026-02-18 013203.png` | `./assets/images/Screenshot%202026-02-18%20013203.png` | Burp Suite Repeater capturing `GET /download-transcript/4.txt` (`1:32 AM`) |
| **Project 1 (IDOR)** | `Screenshot 2026-02-18 013122.png` | `./assets/images/Screenshot%202026-02-18%20013122.png` | Burp Suite Repeater exploiting `GET /download-transcript/1.txt` (`1:31 AM`) |
| **Project 1 (IDOR)** | `Screenshot 2026-02-18 013406.png` | `./assets/images/Screenshot%202026-02-18%20013406.png` | Post-exploitation credential verification (`1:34 AM`) |
| **Project 2 (PCAP)** | `Screenshot 2026-02-18 151153.png` | `./assets/images/Screenshot%202026-02-18%20151153.png` | Initial Wireshark inspection of `wpa.cap` (`3:11 PM`) |
| **Project 2 (PCAP)** | `Screenshot 2026-02-18 151251.png` | `./assets/images/Screenshot%202026-02-18%20151251.png` | Wireshark unfiltered view of `wpa.cap` (13 packets, `SSID="test"`, `3:12 PM`) |
| **Project 2 (PCAP)** | `Screenshot 2026-02-18 151321.png` | `./assets/images/Screenshot%202026-02-18%20151321.png` | Wireshark filtered by `eapol` isolating the 4-way WPA handshake (`3:13 PM`) |
| **Project 2 (PCAP)** | `Screenshot 2026-02-18 155443.png` | `./assets/images/Screenshot%202026-02-18%20155443.png` | Terminal: `aircrack-ng wpa.cap` confirming `WPA (1 handshake)` (`3:54 PM`) |
| **Project 2 (PCAP)** | `Screenshot 2026-02-18 163409.png` | `./assets/images/Screenshot%202026-02-18%20163409.png` | Cloning `aircrack-ng/test/password.lst` from GitHub (`4:34 PM`) |
| **Project 2 (PCAP)** | `Screenshot 2026-02-18 163522.png` | `./assets/images/Screenshot%202026-02-18%20163522.png` | Aircrack-ng `1.7` cracking `wpa.cap` -> `KEY FOUND! [ biscotte ]` (`4:35 PM`) |
| **Project 3 (SQLi)** | `Screenshot 2026-02-18 015043.png` | `./assets/images/Screenshot%202026-02-18%20015043.png` | DVWA SQL Injection configuration & PHP source code inspection (`1:50 AM`) |
| **Project 3 (SQLi)** | `Screenshot 2026-02-18 015500.png` | `./assets/images/Screenshot%202026-02-18%20015500.png` | Burp Suite Proxy intercepting `POST /DVWA/vulnerabilities/sqli/` (`1:55 AM`) |
| **Project 3 (SQLi)** | `Screenshot 2026-02-18 015846.png` | `./assets/images/Screenshot%202026-02-18%20015846.png` | Testing SQLi payloads & analyzing `mysqli_real_escape_string` (`1:58 AM`) |
| **Project 3 (SQLi)** | `Screenshot 2026-02-18 020140.png` | `./assets/images/Screenshot%202026-02-18%20020140.png` | Successful `1 OR 1=1` SQL Injection execution & user table dump (`2:01 AM`) |

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
   * In **Repeater**, change the request line to `GET /download-transcript/1.txt HTTP/2` and click **Send** to retrieve `carlos`'s plaintext password (`uz6rp2rnyf0eyv52awL`).

![Burp Suite Repeater Capturing Transcript Download](./assets/images/Screenshot%202026-02-18%20013203.png)
*Figure 1: Verifying the `/download-transcript/4.txt` request in Burp Suite Repeater during Project 1 setup.*

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

![Aircrack-ng Setup and Dictionary Verification](./assets/images/Screenshot%202026-02-18%20155443.png)
*Figure 2: Verifying `wpa.cap` handshake detection (`1 potential targets`) in Aircrack-ng prior to supplying `-w passwad.txt`.*

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