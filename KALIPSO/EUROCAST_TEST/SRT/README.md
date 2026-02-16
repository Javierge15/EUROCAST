1. RECEPTOR SRT

ffplay -i "srt://127.0.0.1:5000?mode=listener"

**LOW LATENCY**

ffplay -fflags nobuffer -flags low_delay -framedrop -i "srt://127.0.0.1:5000?mode=listener&latency=200000"

--

2. EMISOR SRT

docker compose up --build

--

3. HORA

watch -n 0.1 "date +'%H:%M:%S.%3N'"
