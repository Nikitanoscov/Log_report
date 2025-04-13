from report import HandlersReportGenerator

def test_report_format():
    data = [
        {"level": "INFO", "handler": "/api/v1/users/"},
        {"level": "ERROR", "handler": "/api/v1/users/"},
        {"level": "INFO", "handler": "/api/v1/orders/"}
    ]
    
    report = HandlersReportGenerator().generate(data)
    lines = report.split('\n')
    assert lines[0].startswith("Total requests:")
    assert "HANDLER" in lines[2]
    assert "DEBUG" in lines[2]
    assert "INFO" in lines[2]
    assert "WARNING" in lines[2]
    assert "ERROR" in lines[2]
    assert "CRITICAL" in lines[2]
    
    assert "\t" in lines[3]


def test_report_counts():
    data = [
        {"level": "INFO", "handler": "/api/v1/users/"},
        {"level": "INFO", "handler": "/api/v1/users/"},
        {"level": "ERROR", "handler": "/api/v1/users/"},
        {"level": "DEBUG", "handler": "/api/v1/orders/"}
    ]
    report = HandlersReportGenerator().generate(data)
    assert "Total requests: 4" in report
    assert "/api/v1/users/" in report
    assert "2" in report
    assert "1" in report
    assert "1" in report



def test_empty_report():
    report = HandlersReportGenerator().generate([])
    assert "Total requests: 0" in report
    