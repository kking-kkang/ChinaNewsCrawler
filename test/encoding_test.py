from charset_normalizer import from_bytes
import requests

url = "http://world.people.com.cn/n1/2017/0216/c1002-29085153.html"
response = requests.get(url)
detected = from_bytes(response.content).best()
response.encoding = detected.encoding  # 실제 감지된 인코딩 설정
html_content = response.text
print(f"감지된 인코딩: {detected.encoding}")
