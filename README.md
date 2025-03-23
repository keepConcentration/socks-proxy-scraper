# SOCKS 프록시 스크래퍼

SOCKS 프록시 서버 목록을 자동으로 스크래핑하여 JSON 형태로 제공합니다. 업타임을 기준으로 정렬된 SOCKS4 및 SOCKS5 프록시 정보를 수집할 수 있습니다.

## 설치 및 실행 방법

```shell script
git clone https://github.com/사용자명/socks-proxy-scraper.git
cd socks-proxy-scraper

python -m venv venv

# macOS / Linux
source venv/bin/activate
# Window
venv\Scripts\activate

pip install -r requirements.txt

python run.py
```

## 필요 라이브러리

- beautifulsoup4
- cloudscraper

### 결과 예시

```json
{
  "proxies": [
    {
      "protocol": "socks5",
      "ip": "192.168.1.1",
      "port": "1080",
      "uptime": 99
    },
    {
      "protocol": "socks4",
      "ip": "10.0.0.1",
      "port": "4145",
      "uptime": 95
    }
  ]
}
```

## 주의사항

- 프록시 서버는 자주 변경되거나 다운될 수 있습니다.
- 스크래핑 대상 웹사이트의 구조가 변경되면 이 라이브러리가 작동하지 않을 수 있습니다.
- 프록시 서버 사용 시 법적, 윤리적 규정을 준수해야 합니다.
- 과도한 요청은 스크래핑 대상 서버에 부하를 줄 수 있으므로 적절한 간격을 두고 사용하세요.

---

**참고**: 이 도구는 교육 및 연구 목적으로만 사용해야 합니다. 프록시 서버의 무단 사용은 법적 문제를 야기할 수 있습니다.