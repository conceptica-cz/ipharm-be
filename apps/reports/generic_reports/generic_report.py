import importlib
import logging
from typing import Callable

from django.conf import settings

from . import common

logger = logging.getLogger(__name__)


class GenericReport:
    def __init__(
        self,
        data_loader: Callable,
        data_loader_kwargs: dict,
        renderer: Callable,
        renderer_kwargs: dict,
        **kwargs,
    ):
        self.data_loader = data_loader
        self.data_loader_kwargs = data_loader_kwargs
        self.renderer = renderer
        self.renderer_kwargs = renderer_kwargs
        self.kwargs = kwargs

    def render(self):
        data = self.data_loader(**self.data_loader_kwargs | self.kwargs)
        logger.debug(f"Report data was generated", extra={"data": data})
        content = self.renderer(data=data, **self.renderer_kwargs | self.kwargs)
        return content


class GenericReportFactory:
    def create(
        self, report_type: "GenericReportType", report_format: str, **kwargs
    ) -> GenericReport:
        data_loader = common.get_func_from_path(
            settings.GENERIC_REPORTS[report_type.name]["data_loader"]
        )

        data_loader_kwargs = settings.GENERIC_REPORTS[report_type.name].get(
            "data_loader_kwargs", {}
        )

        renderer = common.get_func_from_path(
            settings.GENERIC_REPORTS[report_type.name]["renderers"][report_format][
                "renderer"
            ]
        )

        renderer_kwargs = settings.GENERIC_REPORTS[report_type.name]["renderers"][
            report_format
        ].get("renderer_kwargs", {})

        kwargs["report_type"] = report_type

        return GenericReport(
            data_loader=data_loader,
            data_loader_kwargs=data_loader_kwargs,
            renderer=renderer,
            renderer_kwargs=renderer_kwargs,
            **kwargs,
        )
