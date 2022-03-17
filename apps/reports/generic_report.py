import importlib
import logging
from typing import Callable

from django.conf import settings
from django.template.loader import render_to_string
from weasyprint import HTML

logger = logging.getLogger(__name__)


def to_pdf(content):
    html = HTML(string=content)
    rendered = html.write_pdf()
    return rendered


def to_text(content):
    return content


class GenericReport:
    CONVERTERS = {
        "txt": to_text,
        "pdf": to_pdf,
    }

    def __init__(
        self,
        data_loader: Callable,
        template: str,
        report_format: str = "pdf",
        **kwargs,
    ):
        self.data_loader = data_loader
        self.template = template
        self.report_format = report_format
        self.kwargs = kwargs

    def render(self):
        data = self.data_loader(**self.kwargs)
        logger.debug(f"Report data was generated", extra={"data": data})
        content = render_to_string(self.template, data)
        return self.CONVERTERS[self.report_format](content)


class GenericReportFactory:
    @staticmethod
    def _get_func(dotted_path: str) -> Callable:
        module_name, func_name = dotted_path.rsplit(".", 1)
        module = importlib.import_module(module_name)
        return getattr(module, func_name)

    def create(
        self, report_type: "GenericReportType", report_format: str, **kwargs
    ) -> GenericReport:
        data_loader = self._get_func(
            settings.GENERIC_REPORTS[report_type.name]["data_loader"]
        )
        template = settings.GENERIC_REPORTS[report_type.name]["templates"][
            report_format
        ]
        kwargs["report_type"] = report_type
        return GenericReport(
            data_loader=data_loader,
            template=template,
            report_format=report_format,
            **kwargs,
        )
