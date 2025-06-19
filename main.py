#!/usr/bin/env python3

import os
import sys
import argparse
import subprocess
import json
import datetime

# Directories
REPORTS_DIR = "reports"
LOGS_DIR = "logs"
os.makedirs(REPORTS_DIR, exist_ok=True)
os.makedirs(LOGS_DIR, exist_ok=True)

def run_ffuf(url, wordlist, threads, header):
    timestamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    output_json = os.path.join(LOGS_DIR, f"ffuf_output_{timestamp}.json")
    
    cmd = [
        "ffuf",
        "-u", url,
        "-w", wordlist,
        "-t", str(threads),
        "-o", output_json,
        "-of", "json"
    ]

    if header:
        cmd += ["-H", header]

    print(f"\n[+] Running FFUF:\n{' '.join(cmd)}\n")
    
    subprocess.run(cmd, check=True)

    return output_json

def parse_ffuf_output(json_file):
    with open(json_file, 'r') as f:
        data = json.load(f)

    results = data.get("results", [])
    return results

def generate_html_report(results, url, wordlist, header, threads, output_file):
    html_content = f"""
    <html>
    <head>
        <title>FFUF Scan Report</title>
        <style>
            body {{ background-color: #121212; color: #e0e0e0; font-family: Arial, sans-serif; }}
            table {{ width: 100%; border-collapse: collapse; margin-top: 20px; }}
            th, td {{ border: 1px solid #444; padding: 8px; text-align: left; }}
            th {{ background-color: #222; }}
            tr:nth-child(even) {{ background-color: #1c1c1c; }}
            .status-200 {{ color: #00ff00; }}
            .status-403 {{ color: #ffcc00; }}
            .status-500 {{ color: #ff4444; }}
            .status-other {{ color: #999999; }}
        </style>
    </head>
    <body>
        <h1>FFUF Scan Report</h1>
        <p><b>Target:</b> {url}</p>
        <p><b>Wordlist:</b> {wordlist}</p>
        <p><b>Threads:</b> {threads}</p>
        <p><b>Header:</b> {header if header else 'None'}</p>
        <p><b>Total Results:</b> {len(results)}</p>

        <table>
            <tr>
                <th>URL</th>
                <th>Status Code</th>
                <th>Content Length</th>
                <th>Lines</th>
                <th>Redirect</th>
            </tr>
    """

    for result in results:
        status_class = (
            "status-200" if result["status"] == 200 else
            "status-403" if result["status"] == 403 else
            "status-500" if result["status"] == 500 else
            "status-other"
        )

        url_result = result["url"]

        html_content += f"""
            <tr>
                <td><a href="{url_result}" target="_blank">{url_result}</a></td>
                <td class="{status_class}">{result['status']}</td>
                <td>{result['length']}</td>
                <td>{result['lines']}</td>
                <td>{result.get('redirectlocation', '')}</td>
            </tr>
        """

    html_content += """
        </table>
    </body>
    </html>
    """

    with open(output_file, 'w') as f:
        f.write(html_content)

    print(f"\n[+] HTML report saved to {output_file}\n")

def main():
    parser = argparse.ArgumentParser(description="Automated FFUF Scanner with HTML Reporting")
    parser.add_argument("--url", required=True, help="Target URL (use FUZZ in place)")
    parser.add_argument("--wordlist", required=True, help="Path to wordlist")
    parser.add_argument("--threads", type=int, default=50, help="Number of threads (default: 50)")
    parser.add_argument("--header", help="Optional header (ex: 'Authorization: Bearer xxxxx')")

    args = parser.parse_args()

    try:
        output_json = run_ffuf(args.url, args.wordlist, args.threads, args.header)
        results = parse_ffuf_output(output_json)
        timestamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
        output_html = os.path.join(REPORTS_DIR, f"ffuf_report_{timestamp}.html")
        generate_html_report(results, args.url, args.wordlist, args.header, args.threads, output_html)
    except subprocess.CalledProcessError:
        print("[-] FFUF execution failed. Make sure FFUF is installed and the command is correct.")

if __name__ == "__main__":
    main()
