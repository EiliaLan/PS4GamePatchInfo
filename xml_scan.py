import hmac
import hashlib
import binascii
import requests
import xml.etree.ElementTree as ET
from tqdm import tqdm

# Function to generate URL using HMAC
def generate_url(GameID):
    byte_key = binascii.unhexlify("AD62E37F905E06BC19593142281C112CEC0E7EC3E97EFDCAEFCDBAAFA6378D84")
    hash = hmac.new(byte_key, ("np_" + GameID).encode('utf-8'), digestmod=hashlib.sha256)
    hash = hash.hexdigest()
    url = f"https://gs-sec.ww.np.dl.playstation.net/plo/np/{GameID}/{hash}/{GameID}-ver.xml"
    return url

# 将16进制的密钥转换为字节数组


# 循环遍历CUSA00001到CUSA01000的范围
for number in tqdm(range(1, 45000)):
    GameID = f"CUSA{number:05}"
    url = generate_url(GameID)

    try:
        # 发送HTTP请求获取XML内容
        response = requests.get(url,verify=False)
        response.raise_for_status()  # 抛出HTTP请求错误
        xml_content = response.content

        root = ET.fromstring(xml_content)
        # 解析XML内容
        title_id = root.attrib["titleid"]
        title = root.find(".//title").text
        version = root.find(".//package").attrib["version"]
        content_id = root.find(".//package").attrib["content_id"]

        # 将提取的信息写入文本文件
        with open("extracted_info.txt", "a", encoding="utf-8") as info_file:
            info_file.write(f"{title_id},{title},{version},{content_id}\n")

        print(f"{GameID} - Extraction completed!")
    except (requests.exceptions.RequestException, ET.ParseError) as e:
        print(f"{GameID} - Error: {e}")
        continue  # 出错时继续下一次循环

print("Extraction and writing completed!")