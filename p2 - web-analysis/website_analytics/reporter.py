from typing import TextIO
import sys
from urllib.parse import urlparse
from website_analytics.models import ReportData


def render_terminal_report(report: ReportData, output: TextIO = sys.stdout) -> None:
    """Render summary and detailed link tables in ASCII format matching spec design."""
    summary = report.summary
    links = report.links

    # Summary Report Box
    border = "+------------------------------------------------------------------------+"
    output.write(f"{border}\n")
    output.write("| Summary report:                                                        |\n")
    output.write(f"{border}\n")
    line1 = f"    Total Links: {summary.total_links}, Internal: {summary.internal_links}, External: {summary.external_links}, Broken: {summary.broken_links}"
    output.write(f"| {line1:<70} |\n")
    line2 = f"    Max latency: {int(round(summary.max_latency_ms))}ms, Max bytes transferred: {summary.max_bytes_transferred:,} bytes"
    output.write(f"| {line2:<70} |\n")
    output.write(f"{border}\n")

    # Detailed Report Table
    output.write("| Detailed report:                                                       |\n")

    table_border = "+----------------+-----+----------+---------+-------------+--------------+"
    output.write(f"{table_border}\n")
    output.write("|  Link          | E/I | Response | Latency | Bytes       | Content      |\n")
    output.write("|                |     | Code     | in ms   | Transferred | Type         |\n")
    output.write(f"{table_border}\n")

    for link in links:
        parsed = urlparse(link.url)
        path_str = parsed.path if parsed.path else link.url
        if len(path_str) > 14:
            path_display = path_str[:11] + "..."
        else:
            path_display = path_str

        e_i = "I" if link.link_type == "Internal" else "E"
        resp_code = str(link.status_code) if link.status_code is not None else "ERR"
        latency_str = str(int(round(link.latency_ms)))
        bytes_str = f"{link.bytes_transferred:,}"
        c_type = link.content_type[:12]

        output.write(
            f"| {path_display:<14} | {e_i:^3} | {resp_code:<8} | {latency_str:<7} | {bytes_str:<11} | {c_type:<12} |\n"
        )

    output.write(f"{table_border}\n")
