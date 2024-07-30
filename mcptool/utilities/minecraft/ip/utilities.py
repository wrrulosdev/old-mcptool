import socket
from typing import Union

from loguru import logger


class IPUtilities:
    @staticmethod
    @logger.catch
    def is_valid_ip(ip: str) -> bool:
        """
        Check if the IP address is valid.
        :param ip: The IP address to check.
        :return: True if the IP address is valid, otherwise False.
        """
        try:
            socket.inet_aton(ip)
            return True

        except OSError:
            return False

    @staticmethod
    @logger.catch
    def resolve(domain: str) -> Union[str, None]:
        """
        Resolve the IP address of a domain.
        :param domain:  The domain to resolve.
        :return: The IP address of the domain.
        """
        ip_address: Union[str, None] = None

        try:
            ip_address = socket.gethostbyname(domain)

        except (socket.gaierror, OSError, UnicodeError):
            pass

        return ip_address
