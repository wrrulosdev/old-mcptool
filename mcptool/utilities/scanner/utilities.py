import subprocess

from loguru import logger


class ScannerUtilities:
    @staticmethod
    @logger.catch
    def nmap_installed() -> bool:
        """
        Check if Nmap is installed.
        :return: True if Nmap is installed, False otherwise.
        """
        return subprocess.call(f'nmap --version >nul 2>&1', shell=True) == 0

    @staticmethod
    @logger.catch
    def masscan_installed() -> bool:
        """
        Check if Masscan is installed.
        :return: True if Masscan is installed, False otherwise.
        """
        return subprocess.call(f'masscan --version >nul 2>&1', shell=True) == 0
