# Local AI Desktop Companion

A fully private, locally-run AI desktop companion that uses a 3D avatar for interaction. This project combines local Large Language Models (LLMs), Text-to-Speech (TTS), and 3D rendering to create an interactive and engaging desktop experience.

![Screenshot of the AI companion in action](https://i.imgur.com/your-image-url.png)

*(Suggestion: Replace the image URL above with a link to a real screenshot or GIF of your application!)*

## ⚠️ Important Note on Performance

This project is **highly resource-intensive**. It runs several demanding processes simultaneously:
* **A Large Language Model (LLM)** via Ollama.
* **A Text-to-Speech (TTS) Engine** via Coqui TTS.
* **A 3D Rendering Scene** via Electron and Three.js.

Loading the AI and TTS models requires a significant amount of **RAM** and **VRAM**. On systems with less powerful hardware or without a dedicated GPU, you may experience:
* **Long Initial Loading Times**: The first time you run the backend, it will download several gigabytes of model data. Subsequent launches will still take time to load these models into memory.
* **Slow Performance or Crashes**: If your system runs out of memory, the application may become unresponsive or crash.

Please be patient during startup, and ensure you are running this on a machine that meets the resource demands.

## Features

* **3D Avatar Display**: Renders any VRM model in a transparent, borderless, and draggable window that stays on top of other applications.
* **Local AI Chat**: Utilizes Ollama to run local language models, ensuring all conversations remain private and offline.
* **Text-to-Speech (TTS)**: Integrates Coqui TTS to give the avatar a voice, synthesizing responses in real-time.
* **Lip-Sync Animation**: The avatar's mouth moves in sync with the generated speech, creating a more lifelike interaction.
* **Gaze Tracking**: The avatar's head and eyes follow the mouse cursor, making her feel more aware and interactive.

## Project Architecture

The application is built on a client-server architecture, with the frontend (Electron) and backend (Python/Flask) running as two separate processes that communicate via a local REST API.

+--------------------------+      1. User sends message      +--------------------------+
|      Frontend (UI)       | ------------------------------> |      Backend (API)       |
| (Electron, Three.js)     |                                 |   (Python, Flask)        |
| - Renders VRM model      |      2. Gets AI response       +--------------------------+
| - Captures user input    | <------------------------------ | - Ollama for LLM logic   |
| - Plays audio & animates |      3. Requests speech         | - Coqui for TTS          |
+--------------------------+ ------------------------------> |                          |
4. Returns audio data      +--------------------------+
<------------------------------

## Tech Stack

### Backend
* **Framework**: Python 3.11+ with Flask
* **AI Engine**: Ollama
* **LLM Model**: `phi-3:mini` (for fast, local responses)
* **TTS Engine**: Coqui TTS

### Frontend
* **Framework**: Electron
* **Bundler**: Vite
* **3D Rendering**: Three.js
* **VRM Loading**: `@pixiv/three-vrm`

---

## Getting Started

Follow these instructions to get the project running on your local machine.

### Prerequisites

* **Git**: To clone the repository.
* **Python & Conda**: Python 3.11+ installed, preferably managed via Anaconda or Miniconda.
* **Node.js**: Version 18.x or later, which includes `npm`.
* **Ollama**: You must have the [Ollama desktop application](https://ollama.com/) installed and running.
* **A VRM Model**: You need a 3D avatar model in the `.vrm` format. You can create your own using [VRoid Studio](https://vroid.com/en/studio) or download one from a platform like [VRoid Hub](https://hub.vroid.com/).

### Installation

1.  **Clone the Repository**
    ```bash
    git clone https://github.com/tejeshwarv16/Local-AI-Desktop-Companion.git
    cd Local-AI-Desktop-Companion
    ```

2.  **Add Your VRM Model**
    * Take the `.vrm` file you downloaded.
    * Place it inside the `frontend/public/` directory.
    * Rename the file to **`model.vrm`**. The final path should be `frontend/public/model.vrm`.

3.  **Set Up the Backend (Python)**
    * Create and activate the Conda environment:
        ```bash
        conda create --name miku python=3.11 -y
        conda activate miku
        ```
    * Install all required Python packages:
        ```bash
        pip install flask flask-cors ollama TTS torch
        ```
    * Pull the required AI model via Ollama:
        ```bash
        ollama pull phi-3:mini
        ```

4.  **Set Up the Frontend (Electron)**
    * Navigate to the `frontend` directory:
        ```bash
        cd frontend
        ```
    * Install all Node.js dependencies:
        ```bash
        npm install
        ```
    * **Important**: If the `npm install` fails due to a `three` and `@pixiv/three-vrm` version conflict, run the following commands to fix it:
        ```bash
        npm uninstall three
        npm install three@0.164.1
        npm install
        ```

### Usage

To run the application, you must start both the backend and frontend servers in two separate terminals.

**Terminal 1: Start the Backend**
```bash
# Navigate to the project's root directory
# (Activate conda environment if you haven't already: conda activate miku)
python app.py
```
Wait until you see the message "TTS engine ready." This may take a while on the first run as models are downloaded.
**Terminal 2: Start the Frontend**
```bash
# Navigate to the frontend directory
cd frontend
npm run dev
```
The desktop companion application should now launch on your screen, displaying the VRM model you provided.

**Future Improvements**
This project serves as a strong foundation. Future enhancements could include:

Re-enabling Powerful LLMs: Modify app.py to use larger models like Llama 2 or Mistral on systems with sufficient VRAM.

Advanced Animations: Implement idle animations (blinking, breathing) and emotion-based facial expressions.

Persistent Memory: Integrate a simple database like SQLite or a vector store to give the companion long-term memory of past conversations.

Packaging: Use electron-builder to package the application into a distributable .exe file for easy installation on other machines.
