import json
import logging
import os
import sys
import uuid
from datetime import datetime
from http import HTTPStatus
from typing import List, Optional

import amaas.grpc.aio
from fastapi import FastAPI, Response, UploadFile
from pydantic import BaseModel


class ScanResult(BaseModel):
    scannerVersion: Optional[str]
    scanResult: int
    scanId: uuid.UUID
    scanTimestamp: datetime
    fileName: str
    foundMalwares: List


REGION = os.getenv("REGION", default="us-1")
V1_API_KEY = os.getenv("V1_API_KEY")

if not V1_API_KEY:
    logging.ERROR("Need To Provide API Key")
    sys.exit()

app = FastAPI()


@app.post("/scan")
async def scan_file(file: UploadFile, response: Response) -> ScanResult:
    handle = amaas.grpc.aio.init_by_region(REGION, api_key=V1_API_KEY)
    try:
        file_contents = file.file.read()
        scan_results = json.loads(
            await amaas.grpc.aio.scan_buffer(
                channel=handle,
                bytes_buffer=file_contents,
                uid=file.filename,
            )
        )

        if not scan_results:
            response.status_code = HTTPStatus.UNPROCESSABLE_ENTITY

        await amaas.grpc.aio.quit(handle)

        return ScanResult(**scan_results)
    except Exception:
        response.status_code = HTTPStatus.INTERNAL_SERVER_ERROR

    finally:
        file.file.close()
