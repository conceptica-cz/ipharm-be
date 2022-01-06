from reports.models import ReportFile


def report_to_string(report_file: ReportFile) -> str:
    path = report_file.file.path
    with open(path, "r") as file:
        return file.read()
