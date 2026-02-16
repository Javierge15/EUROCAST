1. EMISOR RTP

docker compose up --build

--

2. RECEPTOR RTP

ffplay -protocol_whitelist file,udp,rtp -i video.sdp

**LOW LATENCY**
ffplay -protocol_whitelist file,udp,rtp -fflags nobuffer -flags low_delay -framedrop -i video.sdp

--

3. HORA

watch -n 0.1 "date +'%H:%M:%S.%3N'"