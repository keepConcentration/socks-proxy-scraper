from proxy_scraper import get_proxy_list_json
import json

# 프록시 리스트 가져오기
proxies = json.loads(get_proxy_list_json())
proxy_list = proxies.get('proxies', [])

if proxy_list:
  print("\n=== SOCKS 프록시 서버 목록 ===")
  print("프로토콜\tIP\t\t포트\t업타임")
  print("-" * 50)
  for proxy in proxy_list:
    print(
      f"{proxy['protocol']}\t{proxy['ip']}\t{proxy['port']}\t{proxy['uptime']}%")
else:
  print("프록시 서버를 찾을 수 없습니다.")



