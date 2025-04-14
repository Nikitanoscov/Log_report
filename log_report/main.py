import argparse
from concurrent.futures import ThreadPoolExecutor
import os
import sys
from typing import Dict, List

from parser import LogParser, RequestLogParser
from report import HandlersReportGenerator, ReportGenerator


BUFFER_SIZE = 1024*1024


class ReportFactory:

    _parsers = {
        'handlers': RequestLogParser,
    }
    
    _generators = {
        'handlers': HandlersReportGenerator(),
    }
    
    @classmethod
    def get_parser(cls, report_type: str) -> type[LogParser] | None:
        return cls._parsers.get(report_type)
    
    @classmethod
    def get_generator(cls, report_type: str) -> ReportGenerator | None:
        return cls._generators.get(report_type)


class LogAnalyzer:

    def __init__(self):
        self.factory = ReportFactory()

    def _process_single_file(self, file_path: str, parser: 'LogParser') -> List[Dict]:
        """Обрабатывает один файл и возвращает распарсенные данные."""
        data = []
        try:
            with open(file_path, 'r', encoding='utf-8', buffering=BUFFER_SIZE) as file:
                for line in file:
                    if parsed := parser.parse_line(line.strip()):
                        data.append(parsed)
        except Exception as e:
            print(f"Error processing {file_path}: {str(e)}")
        return data

    def process_files(self, file_paths: List[str], report_type: str) -> str:
        """Обрабатывает файлы параллельно."""
        parser = self.factory.get_parser(report_type)
        if not parser:
            raise ValueError(f"Unknown report type: {report_type}")

        with ThreadPoolExecutor(max_workers=os.cpu_count()) as executor:
            results = list(executor.map(
                lambda fp: self._process_single_file(fp, parser),
                file_paths
            ))
        
        data = [item for sublist in results for item in sublist]
        
        generator = self.factory.get_generator(report_type)
        return generator.generate(data) if data else f"No data found for {report_type} report"


def main():
    parser = argparse.ArgumentParser(description='Анализ логов django')
    parser.add_argument(
        'log_files',
        nargs='+',
        help='Файлы с логами для анализа'
    )
    parser.add_argument(
        '--report',
        choices=['handlers'], 
        default='handlers',
        help='Тип отчета'
    )
    
    args = parser.parse_args()
    args.log_files = set(args.log_files)
    for f in args.log_files:
        if not os.path.exists(f) and not os.access(f, os.R_OK):
            print(f"Warning: Cannot access file {f}")
            sys.exit()

    analyzer = LogAnalyzer()
    print(analyzer.process_files(args.log_files, args.report))

if __name__ == '__main__':
    main()