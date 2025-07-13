import React, { useState, useRef, useEffect, useCallback } from 'react';
import { Camera, Settings, Play, Pause, RotateCcw, Target, AlertTriangle, CheckCircle, Info } from 'lucide-react';

const FitnessTrainer = () => {
  const videoRef = useRef(null);
  const canvasRef = useRef(null);
  const [isRunning, setIsRunning] = useState(false);
  const [selectedExercise, setSelectedExercise] = useState('pushup');
  const [repCount, setRepCount] = useState(0);
  const [setCount, setSetCount] = useState(1);
  const [feedback, setFeedback] = useState('');
  const [formScore, setFormScore] = useState(100);
  const [showSettings, setShowSettings] = useState(false);
  const [confidence, setConfidence] = useState(0.7);
  const [feedbackSensitivity, setFeedbackSensitivity] = useState(0.8);
  const [poses, setPoses] = useState([]);
  const [exerciseState, setExerciseState] = useState('ready');
  const [lastRepTime, setLastRepTime] = useState(0);
  const [avgRepTime, setAvgRepTime] = useState(0);
  const [totalReps, setTotalReps] = useState(0);

  const exercises = {
    pushup: { name: 'Push-ups', category: 'Calisthenics' },
    squat: { name: 'Squats', category: 'Calisthenics' },
    curl: { name: 'Bicep Curls', category: 'Dumbbell' },
    plank: { name: 'Plank Hold', category: 'Core' },
    pullup: { name: 'Pull-ups', category: 'Bar' },
    lunge: { name: 'Lunges', category: 'Calisthenics' },
    press: { name: 'Shoulder Press', category: 'Dumbbell' },
    row: { name: 'Rows', category: 'Dumbbell' }
  };

  const exerciseStates = {
    ready: { color: 'text-blue-500', bg: 'bg-blue-100' },
    down: { color: 'text-orange-500', bg: 'bg-orange-100' },
    up: { color: 'text-green-500', bg: 'bg-green-100' },
    hold: { color: 'text-purple-500', bg: 'bg-purple-100' }
  };

  // Mock pose detection - in real implementation, this would use MediaPipe
  const mockPoseDetection = useCallback(() => {
    if (!videoRef.current || !canvasRef.current) return;

    const canvas = canvasRef.current;
    const ctx = canvas.getContext('2d');
    const video = videoRef.current;

    // Clear canvas
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    // Mock pose landmarks for demonstration
    const mockPoses = [
      {
        landmarks: [
          { x: 0.5, y: 0.2, z: 0, visibility: 0.9 }, // nose
          { x: 0.48, y: 0.25, z: 0, visibility: 0.9 }, // left eye
          { x: 0.52, y: 0.25, z: 0, visibility: 0.9 }, // right eye
          { x: 0.45, y: 0.3, z: 0, visibility: 0.9 }, // left ear
          { x: 0.55, y: 0.3, z: 0, visibility: 0.9 }, // right ear
          { x: 0.4, y: 0.4, z: 0, visibility: 0.9 }, // left shoulder
          { x: 0.6, y: 0.4, z: 0, visibility: 0.9 }, // right shoulder
          { x: 0.35, y: 0.55, z: 0, visibility: 0.9 }, // left elbow
          { x: 0.65, y: 0.55, z: 0, visibility: 0.9 }, // right elbow
          { x: 0.3, y: 0.7, z: 0, visibility: 0.9 }, // left wrist
          { x: 0.7, y: 0.7, z: 0, visibility: 0.9 }, // right wrist
          { x: 0.45, y: 0.6, z: 0, visibility: 0.9 }, // left hip
          { x: 0.55, y: 0.6, z: 0, visibility: 0.9 }, // right hip
          { x: 0.43, y: 0.8, z: 0, visibility: 0.9 }, // left knee
          { x: 0.57, y: 0.8, z: 0, visibility: 0.9 }, // right knee
          { x: 0.41, y: 0.95, z: 0, visibility: 0.9 }, // left ankle
          { x: 0.59, y: 0.95, z: 0, visibility: 0.9 }, // right ankle
        ]
      }
    ];

    setPoses(mockPoses);

    // Draw skeleton
    drawSkeleton(ctx, mockPoses[0], canvas.width, canvas.height);

    // Analyze exercise
    analyzeExercise(mockPoses[0]);
  }, [selectedExercise, exerciseState, repCount]);

  const drawSkeleton = (ctx, pose, width, height) => {
    if (!pose || !pose.landmarks) return;

    const landmarks = pose.landmarks;
    
    // Draw connections
    const connections = [
      [0, 1], [1, 2], [2, 3], [3, 7], [0, 4], [4, 5], [5, 6], [6, 8],
      [9, 10], [11, 12], [11, 13], [12, 14], [13, 15], [14, 16],
      [11, 23], [12, 24], [23, 24], [23, 25], [24, 26], [25, 27], [26, 28],
      [5, 6], [11, 12]
    ];

    ctx.strokeStyle = '#00ff00';
    ctx.lineWidth = 2;

    connections.forEach(([start, end]) => {
      if (landmarks[start] && landmarks[end] && 
          landmarks[start].visibility > confidence && 
          landmarks[end].visibility > confidence) {
        ctx.beginPath();
        ctx.moveTo(landmarks[start].x * width, landmarks[start].y * height);
        ctx.lineTo(landmarks[end].x * width, landmarks[end].y * height);
        ctx.stroke();
      }
    });

    // Draw landmarks
    ctx.fillStyle = '#ff0000';
    landmarks.forEach(landmark => {
      if (landmark.visibility > confidence) {
        ctx.beginPath();
        ctx.arc(landmark.x * width, landmark.y * height, 4, 0, 2 * Math.PI);
        ctx.fill();
      }
    });
  };

  const analyzeExercise = (pose) => {
    if (!pose || !pose.landmarks) return;

    const landmarks = pose.landmarks;
    let newFeedback = '';
    let newFormScore = 100;
    let newState = exerciseState;

    // Mock exercise analysis based on selected exercise
    switch (selectedExercise) {
      case 'pushup':
        newState = analyzePushup(landmarks);
        break;
      case 'squat':
        newState = analyzeSquat(landmarks);
        break;
      case 'curl':
        newState = analyzeCurl(landmarks);
        break;
      case 'plank':
        newState = analyzePlank(landmarks);
        break;
      default:
        newState = 'ready';
    }

    // Generate feedback based on form
    if (newFormScore < 70) {
      newFeedback = 'Focus on maintaining proper form';
    } else if (newFormScore < 85) {
      newFeedback = 'Good form, minor adjustments needed';
    } else {
      newFeedback = 'Excellent form!';
    }

    // Update state and count reps
    if (newState !== exerciseState) {
      if (newState === 'up' && exerciseState === 'down') {
        const currentTime = Date.now();
        if (currentTime - lastRepTime > 1000) { // Prevent double counting
          setRepCount(prev => prev + 1);
          setTotalReps(prev => prev + 1);
          setLastRepTime(currentTime);
          
          // Calculate average rep time
          if (repCount > 0) {
            setAvgRepTime(prev => (prev + (currentTime - lastRepTime)) / 2);
          }
        }
      }
      setExerciseState(newState);
    }

    setFeedback(newFeedback);
    setFormScore(newFormScore);
  };

  const analyzePushup = (landmarks) => {
    // Mock pushup analysis
    const shoulderY = (landmarks[5].y + landmarks[6].y) / 2;
    const hipY = (landmarks[11].y + landmarks[12].y) / 2;
    const kneeY = (landmarks[13].y + landmarks[14].y) / 2;

    if (shoulderY > hipY + 0.1) return 'down';
    if (shoulderY < hipY - 0.05) return 'up';
    return 'ready';
  };

  const analyzeSquat = (landmarks) => {
    // Mock squat analysis
    const hipY = (landmarks[11].y + landmarks[12].y) / 2;
    const kneeY = (landmarks[13].y + landmarks[14].y) / 2;

    if (hipY > kneeY + 0.05) return 'down';
    if (hipY < kneeY - 0.1) return 'up';
    return 'ready';
  };

  const analyzeCurl = (landmarks) => {
    // Mock curl analysis
    const elbowY = (landmarks[7].y + landmarks[8].y) / 2;
    const wristY = (landmarks[9].y + landmarks[10].y) / 2;

    if (wristY < elbowY - 0.1) return 'up';
    if (wristY > elbowY + 0.1) return 'down';
    return 'ready';
  };

  const analyzePlank = (landmarks) => {
    // Mock plank analysis
    return 'hold';
  };

  const startCamera = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ 
        video: { width: 640, height: 480 } 
      });
      if (videoRef.current) {
        videoRef.current.srcObject = stream;
        videoRef.current.play();
      }
    } catch (err) {
      console.error('Error accessing camera:', err);
    }
  };

  const stopCamera = () => {
    if (videoRef.current && videoRef.current.srcObject) {
      const tracks = videoRef.current.srcObject.getTracks();
      tracks.forEach(track => track.stop());
      videoRef.current.srcObject = null;
    }
  };

  const toggleTracking = () => {
    if (isRunning) {
      setIsRunning(false);
      stopCamera();
    } else {
      setIsRunning(true);
      startCamera();
    }
  };

  const resetWorkout = () => {
    setRepCount(0);
    setSetCount(1);
    setExerciseState('ready');
    setFeedback('');
    setFormScore(100);
    setTotalReps(0);
  };

  const completeSet = () => {
    setSetCount(prev => prev + 1);
    setRepCount(0);
    setExerciseState('ready');
  };

  // Animation loop
  useEffect(() => {
    let animationId;
    
    if (isRunning) {
      const animate = () => {
        mockPoseDetection();
        animationId = requestAnimationFrame(animate);
      };
      animate();
    }

    return () => {
      if (animationId) {
        cancelAnimationFrame(animationId);
      }
    };
  }, [isRunning, mockPoseDetection]);

  const getFeedbackIcon = () => {
    if (formScore >= 85) return <CheckCircle className="w-5 h-5 text-green-500" />;
    if (formScore >= 70) return <Info className="w-5 h-5 text-orange-500" />;
    return <AlertTriangle className="w-5 h-5 text-red-500" />;
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900 text-white p-4">
      <div className="max-w-6xl mx-auto">
        {/* Header */}
        <div className="text-center mb-8">
          <h1 className="text-4xl font-bold mb-2 bg-gradient-to-r from-purple-400 to-pink-400 bg-clip-text text-transparent">
            AI Fitness Trainer
          </h1>
          <p className="text-slate-300">Real-time pose estimation and form correction</p>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Video Feed */}
          <div className="lg:col-span-2">
            <div className="bg-slate-800 rounded-lg p-4 border border-slate-700">
              <div className="relative">
                <video
                  ref={videoRef}
                  className="w-full h-96 bg-black rounded-lg"
                  playsInline
                  muted
                />
                <canvas
                  ref={canvasRef}
                  width={640}
                  height={480}
                  className="absolute top-0 left-0 w-full h-full rounded-lg"
                />
                
                {/* Exercise State Indicator */}
                <div className={`absolute top-4 left-4 px-3 py-1 rounded-full text-sm font-medium ${exerciseStates[exerciseState].bg} ${exerciseStates[exerciseState].color}`}>
                  {exerciseState.charAt(0).toUpperCase() + exerciseState.slice(1)}
                </div>
              </div>

              {/* Controls */}
              <div className="flex justify-center gap-4 mt-4">
                <button
                  onClick={toggleTracking}
                  className={`flex items-center gap-2 px-6 py-3 rounded-lg font-medium transition-all ${
                    isRunning
                      ? 'bg-red-600 hover:bg-red-700 text-white'
                      : 'bg-green-600 hover:bg-green-700 text-white'
                  }`}
                >
                  {isRunning ? <Pause className="w-5 h-5" /> : <Play className="w-5 h-5" />}
                  {isRunning ? 'Stop' : 'Start'}
                </button>
                <button
                  onClick={resetWorkout}
                  className="flex items-center gap-2 px-4 py-3 rounded-lg bg-slate-600 hover:bg-slate-700 text-white font-medium transition-all"
                >
                  <RotateCcw className="w-5 h-5" />
                  Reset
                </button>
                <button
                  onClick={() => setShowSettings(!showSettings)}
                  className="flex items-center gap-2 px-4 py-3 rounded-lg bg-purple-600 hover:bg-purple-700 text-white font-medium transition-all"
                >
                  <Settings className="w-5 h-5" />
                  Settings
                </button>
              </div>
            </div>
          </div>

          {/* Stats Panel */}
          <div className="space-y-6">
            {/* Exercise Selection */}
            <div className="bg-slate-800 rounded-lg p-4 border border-slate-700">
              <h3 className="text-lg font-semibold mb-3 text-purple-300">Exercise</h3>
              <select
                value={selectedExercise}
                onChange={(e) => setSelectedExercise(e.target.value)}
                className="w-full p-3 bg-slate-700 border border-slate-600 rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-purple-500"
              >
                {Object.entries(exercises).map(([key, exercise]) => (
                  <option key={key} value={key}>
                    {exercise.name} ({exercise.category})
                  </option>
                ))}
              </select>
            </div>

            {/* Rep Counter */}
            <div className="bg-slate-800 rounded-lg p-4 border border-slate-700">
              <h3 className="text-lg font-semibold mb-3 text-purple-300">Progress</h3>
              <div className="grid grid-cols-2 gap-4">
                <div className="text-center">
                  <div className="text-3xl font-bold text-green-400">{repCount}</div>
                  <div className="text-sm text-slate-400">Reps</div>
                </div>
                <div className="text-center">
                  <div className="text-3xl font-bold text-blue-400">{setCount}</div>
                  <div className="text-sm text-slate-400">Sets</div>
                </div>
              </div>
              <button
                onClick={completeSet}
                className="w-full mt-4 px-4 py-2 bg-blue-600 hover:bg-blue-700 rounded-lg font-medium transition-all"
              >
                Complete Set
              </button>
            </div>

            {/* Form Score */}
            <div className="bg-slate-800 rounded-lg p-4 border border-slate-700">
              <h3 className="text-lg font-semibold mb-3 text-purple-300">Form Score</h3>
              <div className="flex items-center gap-3">
                <div className="flex-1">
                  <div className="w-full bg-slate-700 rounded-full h-3">
                    <div
                      className={`h-3 rounded-full transition-all duration-300 ${
                        formScore >= 85 ? 'bg-green-500' : 
                        formScore >= 70 ? 'bg-orange-500' : 'bg-red-500'
                      }`}
                      style={{ width: `${formScore}%` }}
                    />
                  </div>
                </div>
                <span className="text-xl font-bold">{formScore}%</span>
              </div>
            </div>

            {/* Feedback */}
            <div className="bg-slate-800 rounded-lg p-4 border border-slate-700">
              <h3 className="text-lg font-semibold mb-3 text-purple-300">Feedback</h3>
              <div className="flex items-center gap-3">
                {getFeedbackIcon()}
                <span className="text-sm">{feedback || 'Ready to start!'}</span>
              </div>
            </div>

            {/* Quick Stats */}
            <div className="bg-slate-800 rounded-lg p-4 border border-slate-700">
              <h3 className="text-lg font-semibold mb-3 text-purple-300">Session Stats</h3>
              <div className="space-y-2 text-sm">
                <div className="flex justify-between">
                  <span className="text-slate-400">Total Reps:</span>
                  <span className="font-medium">{totalReps}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-slate-400">Avg Rep Time:</span>
                  <span className="font-medium">{avgRepTime > 0 ? `${(avgRepTime / 1000).toFixed(1)}s` : '0s'}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-slate-400">Exercise:</span>
                  <span className="font-medium">{exercises[selectedExercise].name}</span>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Settings Panel */}
        {showSettings && (
          <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
            <div className="bg-slate-800 rounded-lg p-6 max-w-md w-full mx-4 border border-slate-700">
              <h3 className="text-xl font-semibold mb-4 text-purple-300">Settings</h3>
              
              <div className="space-y-4">
                <div>
                  <label className="block text-sm font-medium mb-2">Confidence Threshold</label>
                  <input
                    type="range"
                    min="0.1"
                    max="1"
                    step="0.1"
                    value={confidence}
                    onChange={(e) => setConfidence(parseFloat(e.target.value))}
                    className="w-full"
                  />
                  <span className="text-xs text-slate-400">{confidence}</span>
                </div>
                
                <div>
                  <label className="block text-sm font-medium mb-2">Feedback Sensitivity</label>
                  <input
                    type="range"
                    min="0.1"
                    max="1"
                    step="0.1"
                    value={feedbackSensitivity}
                    onChange={(e) => setFeedbackSensitivity(parseFloat(e.target.value))}
                    className="w-full"
                  />
                  <span className="text-xs text-slate-400">{feedbackSensitivity}</span>
                </div>
              </div>
              
              <div className="flex justify-end gap-3 mt-6">
                <button
                  onClick={() => setShowSettings(false)}
                  className="px-4 py-2 bg-slate-600 hover:bg-slate-700 rounded-lg font-medium transition-all"
                >
                  Close
                </button>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default FitnessTrainer;