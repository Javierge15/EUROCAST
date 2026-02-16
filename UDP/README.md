# HOW TO USE

## 1. VEHICLE - RECEIVER
```bash
docker compose up --build receiver
```

## 2. STATION - SENDER
Edit ```docker-compose.yaml```:

Change TARGET_IP with the vehicle's PC ```NETBIRD IP```

```bash
docker compose up --build sender
```


Check the ```.csv``` saved on the vehicle PC
