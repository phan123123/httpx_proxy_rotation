# requests-proxy-rotation
A wrapped version of httpx. Help bypassing limitation of API by automatic rotating proxy.

## How to install
```bash
pip install git+https://github.com/phan123123/httpx_proxy_rotation
```

## How to use
### Limit based mode
Wrapped httpx client will be sent with proxies one by one with a limit number
```python
from httpx_proxy_rotation import HttpxWrapper

proxylist = ["socks5://123.123.123.123:8080","socks4://1.2.3.4:1234"]
verify_endpoint = "http://example.com" # using this endpoint to check proxy is alive or not
client = HttpxWrapper(http2=True ,proxylist=proxy_list,verify_endpoint=verify_endpoint, mode = RequestsWrapper.LIMIT_BASED)

client.add_rotator("domain_01",limit_times = 5) # domain_01 API with limit 5 times for each IP.
response = client.get("http://domain_01/get_endpoint")
response = client.post("http://domain_01/post_endpoint", data="test")
response = client.request("method","http://domain_01", ...)
```
### Time based mode
Wrapped httpx client will be sent a limit of number with each limit times during a number of unit time.
```python
from requests_proxy_rotation import RequestsWrapper

proxylist = ["socks5://123.123.123.123:8080","socks4://1.2.3.4:1234"]
verify_endpoint = "http://example.com"
client = HttpxWrapper(http2= True,proxylist=proxy_list,verify_endpoint=verify_endpoint, mode = RequestsWrapper.TIME_BASED)

client.add_rotator("domain_01",limit_times = 5, time_rate=(2,RequestsWrapper.UNIT_MIN)) # domain_01 API with limit 5 times for each IP in 2 minutes.
response = client.get("http://domain_01/get_endpoint")
response = client.post("http://domain_01/post_endpoint", data="test")
response = client.request("method","http://domain_01", ...)
```