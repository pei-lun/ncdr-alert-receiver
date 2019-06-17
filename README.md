# NCDR Alert Receiver

部署時，需要創個 `instance` 資料夾，在裡面新增 `config.py`，內容為：

```Python
# Required
S3_BUCKET = 'S3 BUCKET'

# Optional
S3_PREFIX = 'S3 PREFIX
```