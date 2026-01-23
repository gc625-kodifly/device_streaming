# device_streaming
streaming local camera to WAN accesible nicegui based dashboard using Caddy and mediamtx 

https://www.tldraw.com/f/VM7fj2yrXblICyd-BBfxP?d=v63.-282.2386.1412.page

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
# start services (reverse proxy + mediamtx + dev container)
docker compose -f docker/compose.yaml --profile dev --env-file .env up -d --build

# in another terminal: start the NiceGUI ROS node inside the dev container
docker exec -it docker-rosdev-1 bash -lc 'cd /home/kodifly/ros2_ws && source /opt/ros/humble/setup.bash && source install/setup.bash && ros2 launch gui main_launch.py'

# to end 
docker compose -f docker/compose.yaml --profile dev --env-file .env down
```

Then open the dashboard at `http://localhost/` (or `http://localhost:${CADDY_HTTP_PORT}` if you override it).

Notes:
- In the **dev** profile, NiceGUI is **not** published to the host; it is reached through Caddy. So `http://localhost:6969/` will not work unless you add a `ports:` mapping for `rosdev`.
- If you open `http://localhost/` *before* running the `ros2 launch ...`, Caddy will return **502 Bad Gateway** because nothing is listening on `rosdev:6969` yet.