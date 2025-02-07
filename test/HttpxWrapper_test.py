import unittest
import sys
import os
import logging
import threading
import time

if os.name == "nt":
    sys.path.append (f'{os.path.dirname(__file__) }\\..\\requests-proxy-rotation')
else:
    sys.path.append (f'{os.path.dirname(__file__) }/..')

from httpx_proxy_rotation.httpx_proxy_rotation import HttpxWrapper

logging.basicConfig()
log = logging.getLogger("LOG")

class Test_limit_based(unittest.TestCase):
    def setUp(self):
        # Need setup proxy on 192,168,0.x first
        proxy_list = ["socks5h://192.168.0.100:30000","socks5h://192.168.0.100:30001","socks5h://192.168.0.100:30002"]
        self.rq = HttpxWrapper(http2=False, proxylist=proxy_list,verify_endpoint="https://example.com/", mode = HttpxWrapper.LIMIT_BASED)
        
    def test_get_limit_based(self):
        self.rq.remove_rotator("https://api.ipify.org?format=json")
        self.rq.add_rotator("https://api.ipify.org?format=json",2)
        for i in range(5):
            self.rq.get("https://api.ipify.org?format=json").json()
        self.assertEqual(1,self.rq.rotator_counter["api.ipify.org"])
        self.assertEqual(2,self.rq.current_proxy["api.ipify.org"])
        
    def test_post_limit_based(self):
        self.rq.remove_rotator("http://ip-api.com/batch")
        self.rq.add_rotator("http://ip-api.com/batch",2)
        for i in range(7):
            self.rq.post("http://ip-api.com/batch",data='[{"query": "208.80.152.201", "fields": "country"}, "8.8.8.8"]').json()
        self.assertEqual(1,self.rq.rotator_counter["ip-api.com"])
        self.assertEqual(0,self.rq.current_proxy["ip-api.com"])

    def test_request_limit_based(self):
        self.rq.remove_rotator("https://api.ipify.org?format=json")
        self.rq.add_rotator("https://api.ipify.org?format=json",2)
        for i in range(4):
            self.rq.request("get","https://api.ipify.org?format=json").json()
        self.assertEqual(2,self.rq.rotator_counter["api.ipify.org"])
        self.assertEqual(1,self.rq.current_proxy["api.ipify.org"])


class Test_time_based(unittest.TestCase):
    def setUp(self):
        # Need setup proxy on 192,168,0.x first
        proxy_list = ["socks5h://192.168.0.100:30000","socks5h://192.168.0.100:30001","socks5h://192.168.0.100:30002"]
        self.rq = HttpxWrapper(http2=False, proxylist=proxy_list,verify_endpoint="https://example.com/", mode = HttpxWrapper.TIME_BASED)

    def test_get_time_based(self):
        # Test counter
        self.rq.remove_rotator("http://ip-api.com")
        self.rq.add_rotator("http://ip-api.com/json/24.48.0.1",time_rate=(1,HttpxWrapper.UNIT_MIN),limit_times=2)
        start = time.time()
        for i in range(3):
            self.rq.get("http://ip-api.com/json/24.48.0.1").json()
        stop = time.time()
        self.assertEqual({"socks5h://192.168.0.100:30000":2,"socks5h://192.168.0.100:30001":1},self.rq.rotator_counter["ip-api.com"])
        self.assertEqual(1,self.rq.current_proxy["ip-api.com"])
        # After a unit of time
        time.sleep(60)
        self.rq.get("http://ip-api.com/json/24.48.0.1").json()
        self.assertEqual(1,self.rq.current_proxy["ip-api.com"])
        self.assertLessEqual(self.rq.rotator_counter["ip-api.com"]["socks5h://192.168.0.100:30000"],2)
        self.assertEqual(self.rq.rotator_counter["ip-api.com"]["socks5h://192.168.0.100:30001"],1)
    
    def test_get_multithread_time_based(self):
        pass
        
if __name__ == '__main__':
    unittest.main()