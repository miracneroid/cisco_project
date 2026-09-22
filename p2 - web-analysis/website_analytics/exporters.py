import json
import csv
import sys
from typing import TextIO
from website_analytics.models import ReportData


def export_json(report: ReportData, output: TextIO = sys.stdout) -> None:
    """Export report summary and link details as JSON."""
    data = {
        "summary": report.summary.to_dict(),
        "links": [link.to_dict() for link in report.links],
    }
    json.dump(data, output, indent=2)
    output.write("\n")


def export_csv(report: ReportData, output: TextIO = sys.stdout) -> None:
    """Export link details as CSV."""
    fieldnames = [
        "url",
        "type",
        "status_code",
        "latency_ms",
        "bytes_transferred",
        "content_type",
        "error",
    ]
    writer = csv.DictWriter(output, fieldnames=fieldnames)
    writer.writeheader()

    for link in report.links:
        writer.writerow(link.to_dict())
