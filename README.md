# 🚀 ffuf_auto – Automated FFUF Scanner with HTML Reporting

`ffuf_auto` is a Python automation wrapper for [FFUF](https://github.com/ffuf/ffuf) that makes content discovery scans faster, easier, and beautiful.  
It performs a scan, stores logs in JSON, and generates a **clean HTML report** with clickable results and status-code color indicators.

---

## 🛠 Features

- ✅ Fully automated FFUF scan
- ✅ Generates professional HTML report
- ✅ Clickable links + status colors (200 green, 403 yellow, etc)
- ✅ Saves raw FFUF JSON output
- ✅ Easy to customize and extend

---

## 💻 Usage

```bash
python3 ffuf_auto.py --url https://target.com/FUZZ --wordlist wordlists/sample_wordlist.txt --threads 50
