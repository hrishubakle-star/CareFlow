# CareFlow Unified

CareFlow Unified is a Flask-based healthcare assistant web app that processes medical documents and videos to generate actionable caretaker guidance, medical insights, and safety alerts.

## Features

- Upload medical documents and generate a caretaker-focused to-do list.
- Extract medication schedules, daily care tasks, diet guidance, warning signs, and follow-up recommendations.
- Support for medical image analysis using Gemini AI and structured response parsing.
- Web UI powered by Flask with separate modules for documentation, SOS, and computer vision.

## Requirements

- Python 3.11 or newer
- Windows / Linux / macOS

## Install

1. Clone the repository.

```powershell
cd "d:\CareFlow Unified"
```

2. Create and activate a Python virtual environment.

```powershell
python -m venv .careflow_env
.\.careflow_env\Scripts\Activate.ps1
```

3. Install dependencies.

```powershell
pip install -r requirements.txt
```

## Configuration

Create a `.env` file in the project root with the following variables:

```env
GEMINI_API_KEY=your_gemini_api_key_here
SECRET_KEY=careflow-secret-2024
```

- `GEMINI_API_KEY`: Required to call the Gemini API for medical document analysis. You can get the Gemini key from Google AI Studio, here: https://aistudio.google.com/api-keys
- `SECRET_KEY`: Used by Flask for session management and flash messages.

## Run

```powershell
python app.py
```

Open your browser at `http://127.0.0.1:5000/`.

## Project Structure

- `app.py` - Flask application entrypoint and blueprint registration.
- `requirements.txt` - Python dependency list.
- `modules/doc/` - Document upload, AI prompt handling, and result rendering.
  - `services.py` - Gemini client, schema definition, and document processing.
  - `routes.py` - Upload and result endpoints.
- `templates/doc/result.html` - Display patient insights and caretaker to-do list.
- `static/uploads/doc/` - Uploaded medical documents.
- `yolov8n-pose.pt` - Pretrained pose model used by the computer vision module.

## Usage

1. Start the app.
2. Navigate to the document upload page.
3. Upload a medical report or prescription image.
4. Review the generated caretaker to-do list and additional guidance.

### Testing with your own video

You can test the computer-vision streaming with your own video file. By default the app looks for a hard-coded test file in `static/cv_assets/`.

Steps:

- Copy your MP4 file into `static/cv_assets/` (for example `my_test_video.mp4`).
- Open `modules/cv/routes.py` and edit the `video_feed` handler to point to your filename. Locate this line:

```python
video_source = os.path.join(current_app.root_path, 'static', 'cv_assets', 'abc.mp4')
```

Replace `abc.mp4` with your file name, for example:

```python
video_source = os.path.join(current_app.root_path, 'static', 'cv_assets', 'my_test_video.mp4')
```

- Restart the Flask app and visit the dashboard at `http://127.0.0.1:5000/cv/` or directly stream the feed at:

```
http://127.0.0.1:5000/cv/video_feed/file
```

Note: passing any `<source>` other than `camera` will cause the route to use the hard-coded file path, so updating the filename in `modules/cv/routes.py` is required unless you modify the route logic.


## Notes

- If the app fails to read the image, confirm the file is a supported format: `png`, `jpg`, or `jpeg`.
- The current AI flow expects structured JSON from the Gemini response, so the schema must remain consistent.
- Flask is configured with `use_reloader=False` to avoid duplicate model loads in development.

## Troubleshooting

- `GEMINI_API_KEY` missing: verify `.env` exists and is loaded.
- OpenAI/Gemini errors: check internet access and API key validity.
- Upload errors: confirm file extension and that `static/uploads/doc/` is writable.


