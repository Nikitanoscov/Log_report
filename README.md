# Log-report - приложение составляющие отчеты по django логам

  Возможность создать отчет на основе нескольких файлов.

## Команда

  python main.py <путь к файлу или нескольким файлам> --report <Название отчета>

## Добавление новых отчетов

  Для создания нового отчета:     
  Создайте новый класс для представления отчета наследованный от класса ReportGenerator.    
  ```
class ReportGenerator(Protocol):
    @abstractmethod
    def generate(self, data: List[Dict]) -> str:
        pass


class NewReportGenerator(ReportGenerator):
    
    def generate(self, data: List[Dict]) -> str:
        new logic_view
  ```
  Для создания нового обработчика логов создайте новый класс наследованный LogParser dв файле parser.py.   
```
class LogParser(Protocol):
    @staticmethod
    @abstractmethod
    def parse_line(line: str) -> Dict | None:
        pass


class NewLogParser(LogParser):
    @staticmethod
    def parse_line(line: str) -> Dict | None:
        new logic parce
```
  

## Регистрация новых отчетов.

  В файле main.py в функции main укажите название нового отчета в этой строке ```parser.add_argument('--report', choices=['handlers'], default='handlers', help='Report type')``` в поле choise затем в классе ReportFactory в полях _report и _generator поставте соответсвие команды с парсеров и генератором отчета.
```
class ReportFactory:
      // Добавить новый парсер: Команда: парсер
    _parsers = {
        'handlers': RequestLogParser,
    }
    // Добавить новый генератор: Команда: генератор
    _generators = {
        'handlers': HandlersReportGenerator(),
    }
    
    @classmethod
    def get_parser(cls, report_type: str) -> type[LogParser] | None:
        return cls._parsers.get(report_type)
    
    @classmethod
    def get_generator(cls, report_type: str) -> ReportGenerator | None:
        return cls._generators.get(report_type)
```
    
## Создание отчета
  ```
  cd log_report/
  ```

  ```
  python main.py file.log --report handlers
  ```
