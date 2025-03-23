from bs4 import BeautifulSoup
import re
import logging
import cloudscraper
import json

logger = logging.getLogger(__name__)

def get_proxy_list():
  """
    SOCKS 프록시 목록을 JSON 형태로 가져오는 함수
    반환값: {"proxies": [{"protocol": "socks5", "ip": "127.0.0.1", "port": "1080", "uptime": 99}, ...]}
    """
  url = 'https://spys.one/en/socks-proxy-list/'

  scraper = cloudscraper.create_scraper(
      browser={
        'browser': 'firefox',
        'platform': 'windows',
        'mobile': False
      },
      delay=5
  )

  # 랜덤 user agent
  headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Referer': 'https://spys.one/',
    'DNT': '1',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
  }

  data = {"xpp": "5", "xf1": "0", "xf2": "0", "xf4": "0", "xf5": "2"}

  try:
    logger.info("프록시 목록을 가져오는 중...")
    r = scraper.post(url, data=data, headers=headers)

    if r.status_code != 200:
      logger.error(f"웹사이트 접근 실패. 상태 코드: {r.status_code}")
      return {"proxies": []}

    soup = BeautifulSoup(r.content, 'html.parser')

    result = []

    ports = {}
    script = soup.select_one("body > script")
    if script:
      for row in script.text.split(";"):
        if "^" in row:
          line = row.split("=")
          if len(line) >= 2:
            ports[line[0]] = line[1].split("^")[0]

    trs = soup.select("tr[onmouseover]")

    for tr in trs:
      e_ip = tr.select_one("font.spy14")
      ip = ""

      # 포트번호
      e_port = tr.select_one("script")
      port = ""
      if e_port is not None:
        re_port = re.compile(r'\(([a-zA-Z0-9]+)\^[a-zA-Z0-9]+\)')
        match = re_port.findall(e_port.text)
        for item in match:
          if item in ports:
            port = port + ports[item]
      else:
        continue

      # IP 주소
      if e_ip is not None:
        for item in e_ip.findAll('script'):
          item.extract()
        ip = e_ip.text
      else:
        continue

      # 업타임
      tds = tr.select("td")
      is_skip = False
      pct = "0"
      for td in tds:
        e_pct = td.select_one("font > acronym")
        if e_pct is not None:
          pct = re.sub('([0-9]+)%.*', r'\1', e_pct.text)
          if not pct.isdigit():
            is_skip = True
            break
      if is_skip:
        continue

      # SOCKS 프록시만 필터링
      if "SOCKS" in tr.text:
        protocol = "socks5" if "SOCKS5" in tr.text else "socks4"
        # JSON 형태로 저장
        proxy_data = {
          "protocol": protocol,
          "ip": ip,
          "port": port,
          "uptime": int(pct)
        }
        result.append(proxy_data)

    # 업타임 기준 정렬
    result.sort(key=lambda element: element["uptime"], reverse=True)

    if result:
      logger.info(f"{len(result)}개의 프록시를 찾았습니다.")
      return {"proxies": result}
    else:
      logger.warning("프록시를 찾지 못했습니다.")
      return {"proxies": []}

  except Exception as e:
    logger.error(f"프록시 목록 가져오기 오류: {str(e)}")
    return {"proxies": []}

def get_proxy_list_json():
  """
    SOCKS 프록시 목록을 JSON 문자열로 가져오는 함수
    """
  proxy_data = get_proxy_list()
  return json.dumps(proxy_data, ensure_ascii=False, indent=2)
