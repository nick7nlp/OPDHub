import re
import urllib.request
import urllib.error
import time
import xml.etree.ElementTree as ET

def verify_arxiv_bib(filepath):
    with open(filepath, 'r') as f:
        bib_content = f.read()

    blocks = bib_content.split('@')
    entries = []
    for block in blocks[1:]:
        title_match = re.search(r'title\s*=\s*[\{"](.+?)[\}"]', block, re.IGNORECASE | re.DOTALL)
        arxiv_match = re.search(r'arXiv:(\d{4}\.\d{5})', block)
        if title_match and arxiv_match:
            title = title_match.group(1).replace('{', '').replace('}', '').replace('\n', ' ').strip()
            title = re.sub(r'\s+', ' ', title)
            arxiv_id = arxiv_match.group(1)
            entries.append((arxiv_id, title))

    # Just pick the next 10 for this round
    verified_so_far = [
        '2306.13649', '2306.08543', '2402.03898', '2501.12948', '2505.09388', 
        '2601.02780', '2603.07079', '2410.11325',
        '2305.02301', '2305.12870', '2305.15717', '2305.20050', '2307.15190', 
        '2310.16944', '2401.01335', '2402.11890',
        '2402.13116', '2404.02657', '2407.14679', '2408.00118'
    ]
    
    to_check = [e for e in entries if e[0] not in verified_so_far][:10]
    
    for arxiv_id, local_title in to_check:
        url = f'http://export.arxiv.org/api/query?id_list={arxiv_id}'
        try:
            time.sleep(2)
            req = urllib.request.Request(url)
            with urllib.request.urlopen(req) as response:
                xml_data = response.read()
                root = ET.fromstring(xml_data)
                ns = {'atom': 'http://www.w3.org/2005/Atom'}
                entry = root.find('atom:entry', ns)
                if entry is not None:
                    api_title = entry.find('atom:title', ns).text.replace('\n', ' ').strip()
                    api_title = re.sub(r'\s+', ' ', api_title)
                    t1 = re.sub(r'[^a-z0-9]', '', local_title.lower())
                    t2 = re.sub(r'[^a-z0-9]', '', api_title.lower())
                    match = t1 == t2 or t1 in t2 or t2 in t1
                    print(f"[{'PASS' if match else 'FAIL'}] {arxiv_id}")
                    if not match:
                        print(f"  Local: {local_title}")
                        print(f"  API:   {api_title}")
                else:
                    print(f"[FAIL] {arxiv_id} - Not found on arXiv")
        except Exception as e:
            print(f"[ERROR] {arxiv_id} - {str(e)}")

verify_arxiv_bib('/apdcephfs_cq8/share_1324356/nickmysong/daily_search/on-policy-distillation-survey/references.bib')
