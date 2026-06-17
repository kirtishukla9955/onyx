import os
import boto3
from botocore.client import Config

class S3Client:
    def __init__(self):
        self.endpoint_url = os.getenv("S3_ENDPOINT", "http://localhost:9000")
        self.access_key = os.getenv("S3_ACCESS_KEY", "minioadmin")
        self.secret_key = os.getenv("S3_SECRET_KEY", "minioadmin")
        self.bucket = os.getenv("S3_BUCKET", "onyx-assets")

        # Initialize boto3 client
        self.s3 = boto3.client(
            "s3",
            endpoint_url=self.endpoint_url,
            aws_access_key_id=self.access_key,
            aws_secret_access_key=self.secret_key,
            config=Config(signature_version="s3v4"),
            region_name="us-east-1"  # Default region for MinIO compatibility
        )

    def upload_file(self, file_obj, filename: str, content_type: str) -> str:
        """
        Uploads a file-like object to S3/MinIO and returns the public file URL.
        """
        self.s3.upload_fileobj(
            file_obj,
            self.bucket,
            filename,
            ExtraArgs={"ContentType": content_type}
        )
        
        # Construct public URL
        # For development inside Docker, the backend refers to 'minio:9000'
        # but the frontend running in the host browser needs to request 'localhost:9000'.
        public_endpoint = self.endpoint_url
        if "minio:" in public_endpoint:
            public_endpoint = public_endpoint.replace("minio:", "localhost:")
            
        file_url = f"{public_endpoint}/{self.bucket}/{filename}"
        return file_url

    def upload_protected_file(self, file_content: bytes, filename: str, content_type: str) -> str:
        """
        Uploads raw bytes to S3/MinIO (useful for storing the output of the protection pipeline)
        and returns the public file URL.
        """
        self.s3.put_object(
            Bucket=self.bucket,
            Key=filename,
            Body=file_content,
            ContentType=content_type
        )
        
        public_endpoint = self.endpoint_url
        if "minio:" in public_endpoint:
            public_endpoint = public_endpoint.replace("minio:", "localhost:")
            
        file_url = f"{public_endpoint}/{self.bucket}/{filename}"
        return file_url

# Singleton instance
s3_storage = S3Client()
