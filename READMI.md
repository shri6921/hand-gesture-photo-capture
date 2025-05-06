Hand Gesture Photo Capture
A Python-based computer vision project that uses OpenCV, MediaPipe, and Tkinter to capture photos automatically when a two-finger hand gesture is detected. Upon detecting two extended fingers (excluding the thumb), the program initiates a 5-second countdown and saves a photo to the local PC. The Tkinter GUI provides a user-friendly interface with a live webcam feed, start/stop controls, and status messages.
Features

Real-time Hand Tracking: Uses MediaPipe's hand detection to track hand landmarks and identify gestures.
Two-Finger Detection: Triggers a photo capture when exactly two fingers are extended (index, middle, ring, or pinky, excluding thumb).
Automatic Photo Capture: Captures and saves a photo after a 5-second countdown.
Tkinter GUI: Displays the webcam feed, status updates, and a start/stop button.
Error Handling: Includes webcam initialization checks and user feedback for issues like missing webcam.

Prerequisites

Python 3.7 or higher
A webcam (minimum 720p recommended)
Good lighting conditions for accurate hand detection

Installation

Clone the Repository:
git clone https://github.com/shri6921/hand-gesture-photo-capture.git
cd hand-gesture-photo-capture


Set Up a Virtual Environment (recommended):
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate


Install Dependencies:
pip install -r requirements.txt



Dependencies
See requirements.txt for the full list. Key libraries:

opencv-python: For webcam access and image processing
mediapipe: For hand landmark detection
pillow: For displaying images in Tkinter

Usage

Run the Program:
python hand_photo_capture.py


Interact with the GUI:

Click the "Start" button to initialize the webcam.
Show two extended fingers (e.g., index and middle) in front of the webcam.
Wait for the 5-second countdown displayed in the status bar.
The photo is automatically saved to the captured_photos directory with a timestamped filename (e.g., photo_20250506_173536.jpg).
Click "Stop" to close the webcam or show another two-finger gesture to capture another photo.
Close the GUI window to exit.


Troubleshooting:

If the webcam doesn't start, ensure it's connected and accessible (test with another app like Zoom).
Check the status bar for error messages (e.g., "No webcam found").
Verify dependencies are installed correctly.
For webcam index issues, modify the initialize_webcam method to use the correct index (see code comments).



Project Structure
hand-gesture-photo-capture/
├── hand_photo_capture.py    # Main script with GUI and gesture detection
├── requirements.txt         # List of Python dependencies
├── README.md               # Project documentation
├── LICENSE                 # License file (MIT License)
├── captured_photos/        # Directory where photos are saved (auto-created)

License
This project is licensed under the MIT License. See the LICENSE file for details.
Contributing
Contributions are welcome! Please fork the repository, create a new branch, and submit a pull request with your changes. Ensure your code follows PEP 8 style guidelines and includes appropriate comments.
Acknowledgments

OpenCV for computer vision tools
MediaPipe for hand tracking
Tkinter for the GUI
Inspired by gesture recognition projects on GitHub

Contact
For issues or suggestions, open an issue on GitHub or contact the maintainer at [shrinathshrimangale30@gmail.com].

Built with ❤️ using Python and computer vision
