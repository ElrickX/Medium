import os
import reflex as rx
from pyreportjasper import PyReportJasper

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
RESOURCES_DIR = os.path.join(BASE_DIR, 'resources')
REPORTS_DIR = os.path.join(BASE_DIR, 'reports')

class ReportState(rx.State):
    report_html: str = ""  # Will store HTML content for preview
    report_file: str = ""  # File path to save

    def generate_report(self):
        """Generate HTML report from Jasper."""
        input_file = os.path.join(REPORTS_DIR, 'json.jrxml')   # You can use .jasper too
        output_file = os.path.join(REPORTS_DIR, 'json')
        conn = {
            'driver': 'json',
            'data_file': os.path.join(RESOURCES_DIR, 'contacts.json'),
            'json_query': 'contacts.person'
        }

        pyreportjasper = PyReportJasper()
        pyreportjasper.config(
            input_file,
            output_file,
            output_formats=["html", "pdf"],  # Generate both HTML and PDF
            db_connection=conn
        )
        pyreportjasper.process_report()

        # Load the generated HTML into state
        html_path = output_file + ".html"
        self.report_file = html_path
        with open(html_path, "r", encoding="utf-8") as f:
            self.report_html = f.read()

def index():
    return rx.vstack(
        rx.button("Generate & Preview Report", on_click=ReportState.generate_report),
        rx.cond(
            ReportState.report_html != "",
            rx.box(
                rx.html(ReportState.report_html),  # Show HTML content
                border="1px solid #ccc",
                padding="1em",
                width="100%",
                height="80vh",
                overflow="auto"
            )
        ),
        rx.cond(
            ReportState.report_html != "",
            rx.link(
                "Download PDF",
                href="/reports/json.pdf",  # Serve from static folder
                target="_blank",
                download="invoice.pdf",
                padding_top="1em"
            )
        )
    )

app = rx.App()
app.add_page(index)