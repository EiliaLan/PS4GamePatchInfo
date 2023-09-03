import hmac
import hashlib
import binascii
import requests
import xml.etree.ElementTree as ET
from tqdm import tqdm
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def generate_url(GameID):
    byte_key = binascii.unhexlify("AD62E37F905E06BC19593142281C112CEC0E7EC3E97EFDCAEFCDBAAFA6378D84")
    hash = hmac.new(byte_key, ("np_" + GameID).encode('utf-8'), digestmod=hashlib.sha256)
    hash = hash.hexdigest()
    url = f"https://gs-sec.ww.np.dl.playstation.net/plo/np/{GameID}/{hash}/{GameID}-ver.xml"
    return url

for number in tqdm(range(1, 45000)):
    GameID = f"CUSA{number:05}"
    url = generate_url(GameID)

    try:
        
        response = requests.get(url,verify=False)
        response.raise_for_status()  
        xml_content = response.content

        root = ET.fromstring(xml_content)
        
        title_id = root.attrib["titleid"]
        title = root.find(".//title").text
        version = root.find(".//package").attrib["version"]
        #content_id = root.find(".//package").attrib["content_id"]

        
        with open("extracted_info.txt", "a", encoding="utf-8") as info_file:
            info_file.write(f"{title_id},{title},{version}\n")

        print(f"{GameID}:{title} - COMPLETE\n")
    except (requests.exceptions.RequestException, ET.ParseError) as e:
        print(f"{GameID} - Error: {e}")
        continue  
        
print("Extraction and writing completed!")