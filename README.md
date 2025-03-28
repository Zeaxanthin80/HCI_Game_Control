# Hand Gesture Game Controller

A computer vision-based game controller that allows you to control games using hand gestures captured through your webcam. This project uses OpenCV for hand detection and converts hand positions into keyboard inputs for gaming.

## Features

- Real-time hand gesture detection
- Webcam-based input
- Conversion of hand gestures to keyboard commands
- Visual feedback with debug window
- Configurable gesture zones

## Tech Stack

- Python 3.x
- OpenCV (cv2) - For video capture and image processing
- NumPy - For numerical operations
- PyAutoGUI - For keyboard input simulation
- Jupyter Notebook - For analysis and demonstration

## Requirements

Install the required dependencies using:

```bash
pip install -r requirements.txt
```

## Usage

1. Run the main application:
   ```bash
   python app.py
   ```

2. Position yourself in front of your webcam
3. The camera view is divided into three sections (left, center, right)
4. Use the following gestures to control your game:
   - Left hand up: Triggers SPACE key (Jump)
   - Right hand up: Triggers D key (Move Right)
   - Right hand down: Triggers A key (Move Left)

## Controls Explanation

- The screen is divided into three vertical sections
- Hands are detected based on skin color in HSV color space
- The center section is ignored to prevent accidental triggers
- There is a 0.5-second cooldown between actions to prevent rapid-fire inputs

## Analysis and Demo

Check out `game_control_analysis.ipynb` for:
- Detailed analysis of the hand detection system
- Video sample demonstrations
- Visual explanations of the control zones

## Exiting the Application

Press 'q' in the debug window to quit the application.

## File Structure

- `app.py` - Main application file
- `game_control_analysis.ipynb` - Jupyter notebook with analysis and demos
- `requirements.txt` - Project dependencies
- `sample.mp4` - Sample video for demonstration

## Contributing

Feel free to open issues or submit pull requests to improve the project.