import numpy as np

# Exercise definitions
EXERCISES = {
    'pushup': {'name': 'Push-ups', 'category': 'Calisthenics'},
    'squat': {'name': 'Squats', 'category': 'Calisthenics'},
    'curl': {'name': 'Bicep Curls', 'category': 'Dumbbell'},
    'plank': {'name': 'Plank Hold', 'category': 'Core'},
    'pullup': {'name': 'Pull-ups', 'category': 'Bar'},
    'lunge': {'name': 'Lunges', 'category': 'Calisthenics'},
    'press': {'name': 'Shoulder Press', 'category': 'Dumbbell'},
    'row': {'name': 'Rows', 'category': 'Dumbbell'}
}

def calculate_angle(a, b, c):
    """Calculate the angle between three points."""
    a = np.array([a.x, a.y])
    b = np.array([b.x, b.y])
    c = np.array([c.x, c.y])
    
    radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(a[1] - b[1], a[0] - b[0])
    angle = np.abs(radians * 180.0 / np.pi)
    
    if angle > 180.0:
        angle = 360 - angle
        
    return angle

def analyze_pushup(landmarks):
    """Analyze push-up form and provide feedback."""
    # Get relevant landmarks
    left_shoulder = landmarks[11]
    right_shoulder = landmarks[12]
    left_elbow = landmarks[13]
    right_elbow = landmarks[14]
    left_wrist = landmarks[15]
    right_wrist = landmarks[16]
    left_hip = landmarks[23]
    right_hip = landmarks[24]
    
    # Calculate angles
    left_arm_angle = calculate_angle(left_shoulder, left_elbow, left_wrist)
    right_arm_angle = calculate_angle(right_shoulder, right_elbow, right_wrist)
    
    # Calculate back alignment
    back_alignment = abs(left_hip.y - left_shoulder.y)
    
    # Determine state and provide feedback
    form_score = 100
    feedback = ""
    state = "ready"
    
    # Check arm angles for push-up position
    avg_arm_angle = (left_arm_angle + right_arm_angle) / 2
    
    if avg_arm_angle < 90:
        state = "down"
        if back_alignment > 0.1:
            feedback = "Keep your back straight"
            form_score -= 20
    elif avg_arm_angle > 160:
        state = "up"
        if back_alignment > 0.1:
            feedback = "Maintain proper back alignment"
            form_score -= 20
    else:
        state = "ready"
        feedback = "Lower your body until arms are at 90 degrees"
    
    return state, form_score, feedback

def analyze_squat(landmarks):
    """Analyze squat form and provide feedback."""
    # Get relevant landmarks
    left_hip = landmarks[23]
    right_hip = landmarks[24]
    left_knee = landmarks[25]
    right_knee = landmarks[26]
    left_ankle = landmarks[27]
    right_ankle = landmarks[28]
    
    # Calculate angles
    left_leg_angle = calculate_angle(left_hip, left_knee, left_ankle)
    right_leg_angle = calculate_angle(right_hip, right_knee, right_ankle)
    
    # Determine state and provide feedback
    form_score = 100
    feedback = ""
    state = "ready"
    
    avg_leg_angle = (left_leg_angle + right_leg_angle) / 2
    
    if avg_leg_angle < 90:
        state = "down"
        if abs(left_leg_angle - right_leg_angle) > 15:
            feedback = "Keep your knees aligned"
            form_score -= 20
    elif avg_leg_angle > 160:
        state = "up"
        if abs(left_leg_angle - right_leg_angle) > 15:
            feedback = "Maintain even weight distribution"
            form_score -= 20
    else:
        state = "ready"
        feedback = "Lower until thighs are parallel to ground"
    
    return state, form_score, feedback

def analyze_curl(landmarks):
    """Analyze bicep curl form and provide feedback."""
    # Get relevant landmarks
    left_shoulder = landmarks[11]
    right_shoulder = landmarks[12]
    left_elbow = landmarks[13]
    right_elbow = landmarks[14]
    left_wrist = landmarks[15]
    right_wrist = landmarks[16]
    
    # Calculate angles
    left_arm_angle = calculate_angle(left_shoulder, left_elbow, left_wrist)
    right_arm_angle = calculate_angle(right_shoulder, right_elbow, right_wrist)
    
    # Determine state and provide feedback
    form_score = 100
    feedback = ""
    state = "ready"
    
    avg_arm_angle = (left_arm_angle + right_arm_angle) / 2
    
    if avg_arm_angle < 60:
        state = "up"
        if abs(left_arm_angle - right_arm_angle) > 15:
            feedback = "Keep both arms moving together"
            form_score -= 20
    elif avg_arm_angle > 150:
        state = "down"
        if abs(left_arm_angle - right_arm_angle) > 15:
            feedback = "Maintain even curl motion"
            form_score -= 20
    else:
        state = "ready"
        feedback = "Full range of motion - extend arms fully"
    
    return state, form_score, feedback

def analyze_plank(landmarks):
    """Analyze plank form and provide feedback."""
    # Get relevant landmarks
    left_shoulder = landmarks[11]
    right_shoulder = landmarks[12]
    left_hip = landmarks[23]
    right_hip = landmarks[24]
    left_ankle = landmarks[27]
    right_ankle = landmarks[28]
    
    # Calculate back alignment
    back_alignment = abs((left_hip.y + right_hip.y)/2 - (left_shoulder.y + right_shoulder.y)/2)
    
    # Determine state and provide feedback
    form_score = 100
    feedback = ""
    state = "hold"
    
    if back_alignment > 0.1:
        feedback = "Keep your back straight"
        form_score -= 30
    elif abs(left_hip.y - right_hip.y) > 0.05:
        feedback = "Keep your hips level"
        form_score -= 20
    else:
        feedback = "Good form - maintain position"
    
    return state, form_score, feedback

def analyze_pullup(landmarks):
    """Analyze pull-up form and provide feedback."""
    # Get relevant landmarks
    left_shoulder = landmarks[11]
    right_shoulder = landmarks[12]
    left_elbow = landmarks[13]
    right_elbow = landmarks[14]
    left_wrist = landmarks[15]
    right_wrist = landmarks[16]
    chin = landmarks[7]
    
    # Calculate angles
    left_arm_angle = calculate_angle(left_shoulder, left_elbow, left_wrist)
    right_arm_angle = calculate_angle(right_shoulder, right_elbow, right_wrist)
    
    # Determine state and provide feedback
    form_score = 100
    feedback = ""
    state = "ready"
    
    avg_arm_angle = (left_arm_angle + right_arm_angle) / 2
    
    if chin.y > (left_shoulder.y + right_shoulder.y)/2:
        state = "down"
        if abs(left_arm_angle - right_arm_angle) > 15:
            feedback = "Keep arms even during descent"
            form_score -= 20
    elif avg_arm_angle < 90:
        state = "up"
        if abs(left_arm_angle - right_arm_angle) > 15:
            feedback = "Pull evenly with both arms"
            form_score -= 20
    else:
        state = "ready"
        feedback = "Pull until chin is over the bar"
    
    return state, form_score, feedback

def analyze_lunge(landmarks):
    """Analyze lunge form and provide feedback."""
    # Get relevant landmarks
    left_hip = landmarks[23]
    right_hip = landmarks[24]
    left_knee = landmarks[25]
    right_knee = landmarks[26]
    left_ankle = landmarks[27]
    right_ankle = landmarks[28]
    
    # Calculate angles
    left_leg_angle = calculate_angle(left_hip, left_knee, left_ankle)
    right_leg_angle = calculate_angle(right_hip, right_knee, right_ankle)
    
    # Determine state and provide feedback
    form_score = 100
    feedback = ""
    state = "ready"
    
    if min(left_leg_angle, right_leg_angle) < 90:
        state = "down"
        if abs(left_hip.y - right_hip.y) > 0.1:
            feedback = "Keep hips level during lunge"
            form_score -= 20
    elif min(left_leg_angle, right_leg_angle) > 160:
        state = "up"
        if abs(left_hip.y - right_hip.y) > 0.1:
            feedback = "Stand tall between lunges"
            form_score -= 20
    else:
        state = "ready"
        feedback = "Lower until back knee nearly touches ground"
    
    return state, form_score, feedback

def analyze_press(landmarks):
    """Analyze shoulder press form and provide feedback."""
    # Get relevant landmarks
    left_shoulder = landmarks[11]
    right_shoulder = landmarks[12]
    left_elbow = landmarks[13]
    right_elbow = landmarks[14]
    left_wrist = landmarks[15]
    right_wrist = landmarks[16]
    
    # Calculate angles
    left_arm_angle = calculate_angle(left_shoulder, left_elbow, left_wrist)
    right_arm_angle = calculate_angle(right_shoulder, right_elbow, right_wrist)
    
    # Determine state and provide feedback
    form_score = 100
    feedback = ""
    state = "ready"
    
    avg_arm_angle = (left_arm_angle + right_arm_angle) / 2
    
    if avg_arm_angle > 160:
        state = "up"
        if abs(left_arm_angle - right_arm_angle) > 15:
            feedback = "Press evenly with both arms"
            form_score -= 20
    elif avg_arm_angle < 90:
        state = "down"
        if abs(left_arm_angle - right_arm_angle) > 15:
            feedback = "Keep arms even during lowering"
            form_score -= 20
    else:
        state = "ready"
        feedback = "Press weights straight overhead"
    
    return state, form_score, feedback

def analyze_row(landmarks):
    """Analyze dumbbell row form and provide feedback."""
    # Get relevant landmarks
    left_shoulder = landmarks[11]
    right_shoulder = landmarks[12]
    left_elbow = landmarks[13]
    right_elbow = landmarks[14]
    left_wrist = landmarks[15]
    right_wrist = landmarks[16]
    left_hip = landmarks[23]
    right_hip = landmarks[24]
    
    # Calculate angles
    left_arm_angle = calculate_angle(left_shoulder, left_elbow, left_wrist)
    right_arm_angle = calculate_angle(right_shoulder, right_elbow, right_wrist)
    
    # Determine state and provide feedback
    form_score = 100
    feedback = ""
    state = "ready"
    
    avg_arm_angle = (left_arm_angle + right_arm_angle) / 2
    back_alignment = abs((left_shoulder.y + right_shoulder.y)/2 - (left_hip.y + right_hip.y)/2)
    
    if avg_arm_angle < 60:
        state = "up"
        if back_alignment > 0.1:
            feedback = "Keep your back straight during the row"
            form_score -= 20
    elif avg_arm_angle > 150:
        state = "down"
        if back_alignment > 0.1:
            feedback = "Maintain back position while lowering"
            form_score -= 20
    else:
        state = "ready"
        feedback = "Pull weights toward your chest"
    
    return state, form_score, feedback 