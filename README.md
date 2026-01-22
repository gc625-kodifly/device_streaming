# device_streaming
streaming local camera to WAN accesible nicegui based dashboard using Caddy and mediamtx 


# Setup 

## Configuration (.env)

Mandatory variables: 
- `RTSP_SOURCE`: RTSP input URL for MediaMTX to pull . 
- `LAN_HOST`: Device LAN IP to advertise for WebRTC ICE ( for LAN viewing).
- `PUBLIC_HOST`: Public IP/DNS to advertise for WebRTC ICE (optional; required for viewing from outside LAN with port forwarding).

Optional variables
- `MTX_PATH`: Stream name / URL path. Player will be at `http://<host>/${MTX_PATH}/`.
- `NICEGUI_PORT`: Internal NiceGUI listen port (optional; default `6969`).
- `CADDY_HTTP_PORT`: Host port to expose the dashboard (optional; default `80`).
- `WEBRTC_UDP_PORT`: WebRTC media UDP port to expose/forward (optional; default `8189`).

## Run
From repo root:

```bash
# to start
docker compose -f docker/compose.yaml --env-file .env up -d --build

# to end 
docker compose -f docker/compose.yaml --env-file .env down
```