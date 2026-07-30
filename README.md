# Lamia SOS Map App

A FastAPI-based SOS reporting app with a Leaflet map frontend.

## Run the app

Start the server from the repository root:

```bash
mkdir -p Lamia/certs
openssl req -x509 -nodes -newkey rsa:2048 -keyout Lamia/certs/key.pem -out Lamia/certs/cert.pem -days 365 -subj '/CN=localhost'
python -m uvicorn Lamia.main:app --host 0.0.0.0 --port 8443 --ssl-keyfile Lamia/certs/key.pem --ssl-certfile Lamia/certs/cert.pem
```

## Access the app

Open this link in your browser:

- `https://0.0.0.0:8443`

If you are on another device on the same network, use the host machine IP with `https://<HOST_IP>:8443`.

## Purpose

This app is designed to let one user send a quick SOS report with a short message and their current location, while other users can open the same app URL and see that SOS on a shared map.

- A user can submit an SOS report from their device.
- The backend stores reports in a local SQLite database.
- The map page polls the backend and displays all active reports as markers.
- HTTPS is used so mobile browsers can request location permission securely.

## Limitations

- This is a demo/prototype, not a production system.
- It uses a self-signed certificate, so browsers will warn and mobile users must accept the insecure certificate.
- The app stores data locally in `sos.db`; it does not support multi-server or cloud persistence.
- There is no user authentication, authorization, or session management.
- Location depends on the browser/device and may not be accurate on all Android devices.
- The map and API are designed for small-scale local network use only.

## Notes

- The app uses a self-signed certificate, so the browser may warn about security.
- If using a mobile device, accept the certificate warning or install the cert to trust it.
