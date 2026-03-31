import re
import urllib.request
import urllib.error
import time
import xml.etree.ElementTree as ET

def verify_arxiv_bib(filepath):
    with open(filepath, 'r') as f:
        bib_content = f.read()

    # Find all entries with arXiv IDs
    entries = []
    
    # Simple regex to extract title and arXiv ID pairs
    # This is a bit simplistic but works for well-formatted bibtex
    blocks = bib_content.split('@')
    for block in blocks[1:]:
        title_match = re.search(r'title\s*=\s*[\{"](.+?)[\}"]', block, re.IGNORECASE | re.DOTALL)
        arxiv_match = re.search(r'arXiv:(\d{4}\.\d{5})', block)
        
        if title_match and arxiv_match:
            title = title_match.group(1).replace('{', '').replace('}', '').replace('\n', ' ').strip()
            # clean up multiple spaces
            title = re.sub(r'\s+', ' ', title)
            arxiv_id = arxiv_match.group(1)
            entries.append((arxiv_id, title))

    print(f"Found {len(entries)} arXiv entries to check.")
    
    # Check next 8 unverified entries (from Round 1 we know 8 were checked)
    # We will pick a slice that haven't been mentioned in log.
    verified = ['2306.13649', '2306.08543', '2402.03898', '2501.12948', '2505.09388', '2601.02780', '2603.07079', '2410.11325']
    to_check = [e for e in entries if e[0] not in verified][:8]
    
    results = []
    for arxiv_id, local_title in to_check:
        url = f'http://export.arxiv.org/api/query?id_list={arxiv_id}'
        try:
            time.sleep(1) # rate limit
            req = urllib.request.Request(url)
            with urllib.request.urlopen(req) as response:
                xml_data = response.read()
                root = ET.fromstring(xml_data)
                
                # Arxiv API uses atom namespace
                ns = {'atom': 'http://www.w3.org/2005/Atom'}
                entry = root.find('atom:entry', ns)
                
                if entry is not None:
                    api_title = entry.find('atom:title', ns).text.replace('\n', ' ').strip()
                    api_title = re.sub(r'\s+', ' ', api_title)
                    
                    # Fuzzy match title (ignoring case and punctuation)
                    t1 = re.sub(r'[^a-z0-9]', '', local_title.lower())
                    t2 = re.sub(r'[^a-z0-9]', '', api_title.lower())
                    
                    match = t1 == t2 or t1 in t2 or t2 in t1
                    results.append((arxiv_id, local_title, api_title, match))
                    print(f"[{'PASS' if match else 'FAIL'}] {arxiv_id}")
                    if not match:
                        print(f"  Local: {local_title}")
                        print(f"  API:   {api_title}")
                else:
                    print(f"[FAIL] {arxiv_id} - Not found on arXiv")
                    results.append((arxiv_id, local_title, "NOT FOUND", False))
        except Exception as e:
            print(f"[ERROR] {arxiv_id} - {str(e)}")
            
    return results

verify_arxiv_bib('references.bib')
