import os
import time
import requests
import xml.etree.ElementTree as ET

# This ensures the files go exactly where Member 1's AI is looking
DATASET_FOLDER = "dataset"
os.makedirs(DATASET_FOLDER, exist_ok=True)

# ⚠️ SETTING THE LIMIT:
# I have set this to 20 for your first test run so it finishes in a few minutes. 
# Once you see it working, change this number to 1000 and let it run overnight!
MAX_RESULTS = 999

# ArXiv API URL searching specifically for Computer Science & AI papers
API_URL = f"http://export.arxiv.org/api/query?search_query=cat:cs.AI&start=0&max_results={MAX_RESULTS}"

print(f"🔍 Connecting to arXiv to fetch {MAX_RESULTS} real research papers...")

response = requests.get(API_URL)
root = ET.fromstring(response.text)

# arXiv uses a specific XML format
ns = {'atom': 'http://www.w3.org/2005/Atom'}
entries = root.findall('atom:entry', ns)

print(f"📥 Found {len(entries)} papers. Starting background download...\n")

for i, entry in enumerate(entries):
    # Get the title and the PDF download link
    title = entry.find('atom:title', ns).text.strip().replace('\n', ' ')
    links = entry.findall('atom:link', ns)
    pdf_url = next((link.attrib['href'] for link in links if link.attrib.get('title') == 'pdf'), None)
    
    if pdf_url:
        # Add .pdf to the end of the URL to ensure it downloads as a file
        pdf_url = pdf_url + ".pdf"
        
        # Name the file simply so the AI can read it easily
        filename = f"arxiv_paper_{i+1}.pdf"
        filepath = os.path.join(DATASET_FOLDER, filename)
        
        print(f"[{i+1}/{len(entries)}] Downloading: {title[:50]}...")
        
        try:
            # Download the actual PDF file
            pdf_response = requests.get(pdf_url, stream=True)
            if pdf_response.status_code == 200:
                with open(filepath, 'wb') as f:
                    for chunk in pdf_response.iter_content(1024):
                        f.write(chunk)
            
            # 🛑 CRITICAL: We must pause for 3 seconds between downloads. 
            # If we don't, arXiv will think we are a cyber attack and block your IP!
            time.sleep(3)
            
        except Exception as e:
            print(f"⚠️ Failed to download {filename}: {e}")

print("\n✅ Dataset gathering complete! Your AI now has real data to scan against.")