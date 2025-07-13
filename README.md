# AI Fitness Trainer

A real-time fitness trainer application that uses computer vision to track exercises, count repetitions, and provide form feedback.

## Features

- Real-time pose estimation using MediaPipe
- Support for multiple exercises:
  - Push-ups
  - Squats
  - Bicep Curls
  - Plank Hold
  - Pull-ups
  - Lunges
  - Shoulder Press
  - Rows
- Automatic rep counting
- Real-time form feedback
- Form score tracking
- Exercise statistics
- Live skeleton overlay
- Adjustable settings for confidence threshold and feedback sensitivity

## Requirements

- Python 3.8+
- Webcam
- The required Python packages are listed in `requirements.txt`

## Installation

1. Clone this repository:
```bash
git clone https://github.com/yourusername/ai-fitness-trainer.git
cd ai-fitness-trainer
```

2. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install the required packages:
```bash
pip install -r requirements.txt
```

## Usage

1. Run the Streamlit app:
```bash
streamlit run app.py
```

2. Allow webcam access when prompted by your browser.

3. Select an exercise from the dropdown menu in the sidebar.

4. Adjust the confidence threshold and feedback sensitivity if needed.

5. Position yourself in front of the camera so your full body is visible.

6. Start exercising! The app will automatically:
   - Track your movements
   - Count repetitions
   - Provide real-time form feedback
   - Display your form score

## Exercise Tips

- **Push-ups**: Keep your back straight and lower until arms are at 90 degrees
- **Squats**: Keep knees aligned and lower until thighs are parallel to ground
- **Bicep Curls**: Maintain even motion and full range of movement
- **Plank**: Keep back straight and hips level
- **Pull-ups**: Pull until chin is over the bar, maintain even arm movement
- **Lunges**: Keep hips level and lower until back knee nearly touches ground
- **Shoulder Press**: Press weights straight overhead with even arm movement
- **Rows**: Maintain straight back while pulling weights toward chest

## Extending the App

To add new exercises:

1. Add the exercise definition to `EXERCISES` in `exercise_utils.py`
2. Create an analysis function following the pattern of existing exercises
3. Add the analysis function to the analysis_funcs dictionary in `app.py`

## Troubleshooting

- If the webcam doesn't start, check your browser's camera permissions
- For better pose detection, ensure good lighting and clear view of your full body
- Adjust the confidence threshold if pose detection is unstable

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details. 