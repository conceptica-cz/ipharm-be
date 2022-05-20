import logging
from typing import Generator

import requests
from django.conf import settings
from django.utils import timezone

logger = logging.getLogger(__name__)


class ExternalReferenceError(Exception):
    pass


def references_loader(url, **kwargs) -> Generator[dict, None, None]:
    """Get data from 3rd-party API

    :param url: start url
    :return: generator yielding lists of results
    """
    latest_update_id = kwargs.get("latest_update_id", None)
    if latest_update_id:
        from updates.models import Update

        latest_update = Update.ojbects.get(id=latest_update_id)
        url = (
            url
            + "?updated_since="
            + (latest_update.started_at - timezone.timedelta(minutes=10))
            .replace(tzinfo=None)
            .isoformat()
        )
    headers = {"Authorization": f"Bearer {settings.ICISELNIKY_TOKEN}"}
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
    results = data["results"]
    for result in results:
        yield result
    if (next_url := data.get("next")) is not None:
        yield from references_loader(url=next_url)
