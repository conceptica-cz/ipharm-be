import logging
from typing import Generator

import requests
from django.conf import settings
from django.utils import timezone

logger = logging.getLogger(__name__)


def references_loader(url, **kwargs) -> Generator[dict, None, None]:
    """Get data from 3rd-party API

    :param url: start url
    :return: generator yielding lists of results
    """
    latest_update = kwargs.get("latest_update", None)
    if latest_update:
        url = (
            url
            + "?updated_since="
            + (latest_update.started_at - timezone.timedelta(minutes=10))
            .replace(tzinfo=None)
            .isoformat()
        )
    headers = {"Authorization": f"Bearer {settings.REFERENCES_TOKEN}"}
    logger.debug(f"Get {url}")
    response = requests.get(url, headers=headers)
    data = response.json()
    if response.status_code != 200:
        logger.error(
            f"Error while getting data from {url} status_code={response.status_code} data={data}",
            extra={"url": url, "status_code": response.status_code, "data": data},
        )
    results = data["results"]
    for result in results:
        yield result
    if (next_url := data.get("next")) is not None:
        yield from references_loader(url=next_url)
