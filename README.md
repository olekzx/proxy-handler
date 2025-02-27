# proxy-handler
A simple proxy class with built-in support for proxy authentication and connection testing

## Installation

    pip install proxy-handler

## Examples

#### Create a proxy

```python
from proxy import Proxy, ProxyType

# Proxy without authentication
proxy = Proxy.from_host_colon_port("host:port", ProxyType.SOCKS5)

# Proxy with authentication
proxy2 = Proxy.from_host_port_colon_user_pass("host:port:user:pass", ProxyType.HTTP)
```

#### Check connection

```python
from proxy import Proxy, ProxyType
import asyncio

proxy = Proxy.from_host_colon_port("host:port", ProxyType.SOCKS5)

# check_connection is an async method, so we use asyncio.run()
connection = asyncio.run(proxy.check_connection())

print(connection)
```

#### Flexible formats

```python
from proxy import Proxy, ProxyType
import asyncio

proxy = Proxy.from_host_colon_port("host:port", ProxyType.SOCKS5)

proxy.host_at_port() # e.g., 'socks5://host@port'
proxy.host_colon_port() # e.g., 'socks5://host:port'
proxy.host_port_at_user_pass() # e.g., 'socks5://host:port@user:pass'
```

#### Error handling

```python
from proxy import Proxy, ProxyType, InvalidProxyFormatException

try:
    proxy = Proxy.from_host_colon_port("host@port", ProxyType.SOCKS5)
except InvalidProxyFormatException as e:
    print(f"Error - {e}")

```


This project, **proxy-handler**, is licensed under the MIT License.  
See the [LICENSE](./LICENSE) file for details.