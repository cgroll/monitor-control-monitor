# API Controlled Image Display

This project provides a simple server that allows you to control which image is displayed on a fullscreen web page, using API calls. The server is built with Flask and Flask-SocketIO, and communicates with connected web clients in real-time using WebSockets.

## How it Works

- The server (`server.py`) exposes an API endpoint that lets you select which image to display by sending a POST request.
- Images are hosted in the `static/` directory and displayed in a fullscreen HTML page (`index.html`).
- When an image is changed via the API, all connected clients are instantly updated using WebSockets.

## Features
- Real-time image switching for all connected clients
- Simple API for changing images
- Fullscreen, responsive image display in the browser

## Development Setup

1. **Clone the repository**
2. **Create a virtual environment:**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```
3. **Install dependencies using [uv](https://github.com/astral-sh/uv):**
   ```bash
   uv pip sync
   ```
   Or, if you prefer pip:
   ```bash
   pip install flask flask-socketio
   ```
4. **Add your images** to the `static/` directory. The default supported images are:
   - `layout1_1920x1080.png`
   - `layout2_1920x1080.png`
   - `layout3_1920x1080.png`
   - `layout4_1920x1080.png`

## Running the Project

Start the server with:
```bash
python server.py
```

By default, the server listens on **port 8080** and all interfaces (`0.0.0.0`).

- Access the image display at: [http://localhost:8080/](http://localhost:8080/)
- The main page will show the current image in fullscreen mode.

## Changing the Displayed Image

Send a POST request to the API endpoint to change the image. For example:

```bash
curl -X POST http://localhost:8080/display/1
curl -X POST http://localhost:8080/display/2
curl -X POST http://localhost:8080/display/3
curl -X POST http://localhost:8080/display/4
```

The number corresponds to the image as defined in `server.py`.

## How it Works (Technical)
- The server uses Flask to serve the HTML page and static images.
- Flask-SocketIO is used to push image change events to all connected clients in real-time via WebSockets.
- When a client connects, it immediately receives the current image to display.

## Customization
- To add more images, place them in the `static/` directory and update the `VALID_IMAGES` dictionary in `server.py`.
