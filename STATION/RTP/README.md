## 1. RTP SENDER
```
docker compose up --build
```


## 2. RTP RECEIVER
```
ffplay -protocol_whitelist file,udp,rtp -i video.sdp
```

### LOW LATENCY VERSION
```
ffplay -protocol_whitelist file,udp,rtp -fflags nobuffer -flags low_delay -framedrop -i video.sdp
```

### TIME VISUALIZATION 
```
watch -n 0.1 "date +'%H:%M:%S.%3N'"
```