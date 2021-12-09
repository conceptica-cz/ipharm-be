import logging
from typing import Generator

import requests
from django.conf import settings

logger = logging.getLogger(__name__)


class ExternalReferenceError(Exception):
    pass


def patient_loader(url, **kwargs) -> Generator[dict, None, None]:
    """Get data from API

    :param url: url
    :return: generator yielding lists of results
    """
    headers = {"Authorization": f"Bearer {settings.REFERENCES_TOKEN}"}
    logger.debug(f"Getting url {url}")
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        logger.error(
            f"Error while getting data from {url} status_code={response.status_code} content={response.content}",
            extra={
                "url": url,
                "status_code": response.status_code,
                "content": response.content,
            },
        )
        raise ExternalReferenceError(
            f"Error while getting data from {url} status_code={response.status_code} content={response.content}"
        )
    data = response.json()
    results = data["result"]
    for result in results:
        yield result
