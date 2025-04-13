from main import LogAnalyzer

def test_log_analyzer(sample_log_file):
    analyzer = LogAnalyzer()
    report = analyzer.process_files([sample_log_file], "handlers")
    assert "Total requests: 2" in report
    assert "/api/v1/reviews/" in report
    assert "/api/v1/support/" in report