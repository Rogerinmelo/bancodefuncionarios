from __future__ import annotations

from uuid import uuid4

import boto3

from app.core.config import settings


class StorageService:
    def __init__(self) -> None:
        self.bucket = settings.storage_bucket
        self.client = boto3.client(
            "s3",
            endpoint_url=settings.storage_endpoint_url,
            region_name=settings.storage_region,
            aws_access_key_id=settings.storage_access_key,
            aws_secret_access_key=settings.storage_secret_key,
            use_ssl=settings.storage_use_ssl,
        )

    def upload_bytes(self, *, content: bytes, original_filename: str, content_type: str | None) -> str:
        key = f"employee-history/{uuid4()}-{original_filename}"
        extra_args = {}
        if content_type:
            extra_args["ContentType"] = content_type
        self.client.put_object(Bucket=self.bucket, Key=key, Body=content, **extra_args)
        return self.generate_presigned_url(key=key, expires_in=settings.signed_url_expires_seconds)

    def generate_presigned_url(self, *, key: str, expires_in: int = 3600) -> str:
        return self.client.generate_presigned_url(
            ClientMethod="get_object",
            Params={"Bucket": self.bucket, "Key": key},
            ExpiresIn=expires_in,
        )


storage_service = StorageService()
