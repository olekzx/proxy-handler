import enum
from dataclasses import dataclass
from typing import Optional
import httpx


@dataclass(frozen=True)
class ProxyAuth:
    username: str
    password: str


class ProxyType(enum.Enum):
    HTTP = "http"
    SOCKS5 = "socks5"


class InvalidProxyFormatException(Exception):
    def __init__(self, message: str = f"Invalid proxy format"):
        self.message = message
        super().__init__(self.message)


class ProxyValidationException(Exception):
    def __init__(self, message: str = f"Validation went wrong"):
        self.message = message
        super().__init__(self.message)


@dataclass(frozen=True)
class Proxy:
    host: str
    port: int
    type: ProxyType
    auth: Optional[ProxyAuth] = None

    def __post_init__(self):
        if not (1 <= self.port <= 65535):
            raise ProxyValidationException("Post must be between 1 and 65535")

    async def check_connection(self):
        async with httpx.AsyncClient(proxy=self.user_pass_at_host_port()) as client:
            try:
                await client.get("https://httpbin.org/get")
            except httpx.ProxyError:
                return False
        return True

    def host_colon_port(self):
        return f"{self.type.value}://{self.host}:{self.port}"

    def host_at_port(self):
        return f"{self.type.value}://{self.host}@{self.port}"

    def host_port_colon_user_pass(self):
        if self.auth is None:
            return f"{self.type.value}://{self.host}:{self.port}"
        return f"{self.type.value}://{self.host}:{self.port}:{self.auth.username}:{self.auth.password}"

    def host_port_at_user_pass(self):
        if self.auth is None:
            return f"{self.type.value}://{self.host}:{self.port}"
        return f"{self.type.value}://{self.host}:{self.port}@{self.auth.username}:{self.auth.password}"

    def user_pass_colon_host_port(self):
        if self.auth is None:
            return f"{self.type.value}://{self.host}:{self.port}"
        return f"{self.type.value}://{self.auth.username}:{self.auth.password}:{self.host}:{self.port}"

    def user_pass_at_host_port(self):
        if self.auth is None:
            return f"{self.type.value}://{self.host}:{self.port}"
        return f"{self.type.value}://{self.auth.username}:{self.auth.password}@{self.host}:{self.port}"

    @staticmethod
    def from_host_port_colon_user_pass(proxy: str, type: ProxyType):
        try:
            print(proxy.split("@"))
            host, port, username, password = proxy.split(":")
            return Proxy(host, int(port), type, ProxyAuth(username, password))
        except ValueError:
            raise InvalidProxyFormatException(f"Expected host post colon user pass format - {proxy}")

    @staticmethod
    def from_host_port_at_user_pass(proxy: str, type: ProxyType):
        try:
            host_port, auth = proxy.split("@")
            host, port = host_port.split(":")
            username, password = auth.split(":")
            return Proxy(host, int(port), type, ProxyAuth(username, password))
        except ValueError:
            raise InvalidProxyFormatException(f"Expected host post at user pass format - {proxy}")

    @staticmethod
    def from_user_pass_colon_host_port(proxy: str, type: ProxyType):
        try:
            username, password, host, port = proxy.split(":")
            return Proxy(host, int(port), type, ProxyAuth(username, password))
        except ValueError:
            raise InvalidProxyFormatException(f"Expected user pass colon host port format - {proxy}")

    @staticmethod
    def from_user_pass_at_host_port(proxy: str, type: ProxyType):
        try:
            auth, proxy = proxy.split("@")
            username, password = auth.split(":")
            host, port = proxy.split(":")
            return Proxy(host, int(port), type, ProxyAuth(username, password))
        except ValueError:
            raise InvalidProxyFormatException(f"Expected user pass at host port format - {proxy}")

    @staticmethod
    def from_host_colon_port(proxy: str, type: ProxyType):
        try:
            host, port = proxy.split(":")
            return Proxy(host, int(port), type)
        except ValueError:
            raise InvalidProxyFormatException(f"Expected host colon port format - {proxy}")

    @staticmethod
    def from_host_at_port(proxy: str, type: ProxyType):
        try:
            host, port = proxy.split("@")
            return Proxy(host, int(port), type)
        except ValueError:
            raise InvalidProxyFormatException(f"Expected host at port format - {proxy}")

    def __str__(self):
        return self.host_port_colon_user_pass()
