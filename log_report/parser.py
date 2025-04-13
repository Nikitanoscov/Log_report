from abc import abstractmethod
import re
from typing import Dict, Protocol


class LogParser(Protocol):
    @staticmethod
    @abstractmethod
    def parse_line(line: str) -> Dict:
        pass


class RequestLogParser:
    @staticmethod
    def parse_line(line: str) -> Dict | None:
        pattern = (
            r'^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2},\d{3}\s+'
            r'(?P<level>INFO|ERROR|WARNING|DEBUG|CRITICAL)\s+'
            r'django\.request:\s+'
            r'.*?'
            r'(?P<handler>/[^\s]+)'
        )
        
        match = re.match(pattern, line)
        if not match:
            return None
        
        return {
            "level": match.group("level"),
            "handler": match.group("handler")
        }


class SecurityLogParser:
    @staticmethod
    def parse_line(line: str) -> Dict | None:
        match = re.match(
            r'^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2},\d{3}\s+'
            r'(?P<level>\w+)\s+'
            r'django\.security:\s+'
            r'(?P<message>.*)$',
            line
        )
        return {
            'level': match.group('level').upper(),
            'message': match.group('message')
        } if match else None

