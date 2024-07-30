from typing import Union

from loguru import logger

from .ip.utilities import IPUtilities
from .port.utilities import PortUtilities


class GetMCIPPort:
    def __init__(self, server):
        self.server = server

    @logger.catch
    def get_ip_port(self) -> Union[tuple[str, int], None]:
        """
        Get the IP and port of the server.
        :return: The IP and port of the server.
        """
        if ':' in self.server:  # Example: localhost:25565
            ip, port = self.server.split(':')

            try:
                return ip, int(port)

            except ValueError:
                logger.warning(f'Invalid port in server: {self.server} ({port}) - using default port 25565')
                return ip, 25565

        if IPUtilities.is_valid_ip(self.server):  # Example: 127.0.0.1:25565
            ipaddress: str = self.server
            port: int = PortUtilities.get_minecraft_port(ipaddress)
            return ipaddress, port

        # Example: localhost
        ipaddress: str = IPUtilities.resolve(self.server)

        if ipaddress is None:
            logger.error(f"Failed to resolve IP address for {self.server}")
            return None

        port: int = PortUtilities.get_minecraft_port(self.server)
        return ipaddress, port
