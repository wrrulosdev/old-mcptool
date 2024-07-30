import dns
from loguru import logger


class PortUtilities:
    @staticmethod
    @logger.catch
    def get_minecraft_port(domain: str) -> int:
        """
        Get the port of the Minecraft server.
        :param domain: The domain of the server.
        :return: The port of the server.
        """
        hostname: str = f'_minecraft._tcp.{domain}'
        port: int = 25565
        try:
            # Use the dns.resolver to query SRV DNS records for the server.
            answers = dns.resolver.resolve(hostname, 'SRV')
            # Extract the target port information from the SRV DNS record.
            port = answers[0].port

        except (dns.resolver.NXDOMAIN, dns.resolver.NoAnswer, dns.resolver.NoNameservers, dns.exception.Timeout,
                dns.name.EmptyLabel) as e:
            logger.debug(f"Failed to get the port for {domain} - using default port 25565. Error: {e}")

        return port
