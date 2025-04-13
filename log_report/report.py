from abc import abstractmethod
from collections import defaultdict
from typing import DefaultDict, Dict, List, Protocol



class ReportGenerator(Protocol):
    @abstractmethod
    def generate(self, data: List[Dict]) -> str:
        pass


class HandlersReportGenerator(ReportGenerator):
    
    def generate(self, data: List[Dict]) -> str:
        stats: DefaultDict[str, DefaultDict[str, int]] = defaultdict(lambda: defaultdict(int))
        total_request = len(data)
        
        for entry in data:
            stats[entry['handler']][entry['level']] += 1
        
        standard_levels = ('DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL')
        header = "HANDLER".ljust(25) + "\t" + "\t".join(level.ljust(10) for level in standard_levels)
        
        rows = []
        for handler in sorted(stats.keys()):
            row = handler.ljust(25) + "\t" + "\t".join(
                str(stats[handler].get(level, 0)).ljust(10)
                for level in standard_levels
            )
            rows.append(row)

        level_totals: Dict = defaultdict(int)
        for handler_data in stats.values():
            for level, count in handler_data.items():
                level_totals[level] += count

        totals_row = "".ljust(25) + "\t" + "\t".join(
            str(level_totals.get(level, 0)).ljust(10)
            for level in standard_levels
        )

        return "\n".join([
            f"Total requests: {total_request}\n",
            header,
            *rows,
            totals_row
        ])
