# PyProxyList

*PyProxyList* — is a free proxy list generator, based on [OprahProxy](https://github.com/spaze/oprah-proxy).

## Usage

  1. [Download](https://github.com/bashkirtsevich/PyProxyList/archive/master.zip) or clone this repository via SSH (`git clone git@github.com:bashkirtsevich/PyProxyList.git`) or HTTPS (`git clone https://github.com/bashkirtsevich/PyProxyList.git`);
  2. Import `proxy_list.py` or `proxy_request.py` into your python project;
  3. Enjoy.

## Demos
### ProxyList demo
```python
#!/usr/bin/python
# -*- coding: utf-8 -*-

# import ProxyList
from proxy_list import ProxyList

# call ProxyList constructor
proxy_lit = ProxyList()
# print 
print proxy_lit.get_proxies()
# get_proxies returns dictionary of proxy list and authorization login & password
```
### ProxyRequest demo
```python
#!/usr/bin/python
# -*- coding: utf-8 -*-

# import ProxyRequest
from proxy_request import ProxyRequest

proxy = ProxyRequest()
print proxy.http_get('http://www.myipaddress.com/show-my-ip-address/')['data']

```

License
----

MIT
