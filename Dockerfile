FROM alpine:3.18

# 安裝 sqlite3 與 bash
RUN apk add --no-cache sqlite bash

# 建立 /data 目錄作為 volume
VOLUME ["/data"]
WORKDIR /data

# 保持容器運行
CMD ["sh", "-c", "while true; do sleep 3600; done"]