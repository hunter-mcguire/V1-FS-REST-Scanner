import json
import logging
import os
import sys
import uuid
from datetime import datetime
from http import HTTPStatus
from typing import List, Optional

import amaas.grpc.aio as amaas
from amaas.grpc.util import SupportedV1Regions
from fastapi import FastAPI, Response, UploadFile
from pydantic import BaseModel

logger = logging.getLogger("V1-FS-REST-Scanner")
LOG_LEVEL = os.environ.get("LOG_LEVEL", "ERROR")
logger.setLevel(LOG_LEVEL)


class ScanResult(BaseModel):
    scannerVersion: Optional[str]
    scanResult: int
    scanId: uuid.UUID
    scanTimestamp: datetime
    fileName: str
    foundMalwares: List


region = os.getenv("REGION", default="us-1")
v1_api_key = os.getenv("V1_API_KEY")

if not v1_api_key:
    logging.error("Need To Provide API Key as env variable: 'V1_API_KEY'")
    sys.exit(4)


app = FastAPI()


@app.post("/scan")
async def scan_file(file: UploadFile, response: Response) -> ScanResult | None:
    try:
        handle = amaas.init_by_region(region, api_key=v1_api_key)
        file_contents = file.file.read()
        scan_results = json.loads(
            await amaas.scan_buffer(
                channel=handle,
                bytes_buffer=file_contents,
                uid=file.filename,
            )
        )
        await amaas.quit(handle)

        if not scan_results:
            response.status_code = HTTPStatus.UNPROCESSABLE_ENTITY

        return ScanResult(**scan_results)

    except amaas.AMaasException as error:
        if error.error_code == amaas.AMaasErrorCode.MSG_ID_ERR_INVALID_REGION:
            logging.error(f"Invalid Region.\nSupported Regions: {SupportedV1Regions}")
            response.status_code = HTTPStatus.BAD_REQUEST

        if error.error_code == amaas.AMaasErrorCode.MSG_ID_ERR_KEY_AUTH_FAILED:
            logging.error("Invalid token or Api Key.")
            response.status_code = HTTPStatus.UNAUTHORIZED

        if error.error_code == amaas.AMaasErrorCode.MSG_ID_ERR_RATE_LIMIT_EXCEEDED:
            response.status_code = HTTPStatus.TOO_MANY_REQUESTS
            logging.error("Rate Limit Exceeded.")

    finally:
        file.file.close()
