#!/usr/bin/env python3
"""
MediAI Platform - Flask Backend API
Advanced Medical Diagnosis System
"""

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
import json
import random
import time
from datetime import datetime, timedelta
import base64
from io import BytesIO
from PIL import Image
import numpy as np

app = Flask(__name__)
CORS(app)

# Configuration
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
app.config['UPLOAD_FOLDER'] = 'uploads'

# Ensure upload directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Sample data for simulation
SAMPLE_CONDITIONS = ['Pneumonia', 'Normal', 'COVID-19']
SAMPLE_SYMPTOMS = [
    'Cough', 'Fever', 'Chest Pain', 'Shortness of Breath', 'Fatigue',
    'Weight Loss', 'Night Sweats', 'Difficulty Breathing', 'Chest Tightness',
    'Chronic Cough', 'Blood in Sputum', 'Wheezing', 'Rapid Breathing'
]

# Mock patient database
MOCK_PATIENTS = [
    {
        'id': 'P2847',
        'name': 'Sarah Johnson',
        'age': 34,
        'gender': 'Female',
        'image': 'https://kimi-web-img.moonshot.cn/img/img.freepik.com/1dae55c5462bc294f8629bfd0538e967301ff5ed.jpg',
        'lastVisit': datetime.now().isoformat(),
        'totalScans': 2,
        'symptoms': ['Cough', 'Fever', 'Chest Pain'],
        'medicalHistory': 'No significant respiratory conditions',
        'allergies': ['Penicillin'],
        'predictions': [
            {
                'date': (datetime.now() - timedelta(hours=2)).isoformat(),
                'condition': 'Pneumonia',
                'confidence': 91,
                'image': 'https://kimi-web-img.moonshot.cn/img/www.cvmg.com/ca547d2ab192e1be85ddc467146365fff53f63f5.jpg',
                'notes': 'Bilateral pneumonia detected in lower lobes',
                'processingTime': 2.3,
                'modelVersion': 'MediAI v2.1'
            }
        ]
    },
    {
        'id': 'P2846',
        'name': 'Michael Chen',
        'age': 28,
        'gender': 'Male',
        'image': 'https://kimi-web-img.moonshot.cn/img/media.istockphoto.com/c6ab48b27b3311b0d399df06468070e546ee2fd3.jpg',
        'lastVisit': (datetime.now() - timedelta(hours=5)).isoformat(),
        'totalScans': 1,
        'symptoms': ['Routine Checkup'],
        'medicalHistory': 'Healthy individual',
        'allergies': [],
        'predictions': [
            {
                'date': (datetime.now() - timedelta(hours=5)).isoformat(),
                'condition': 'Normal',
                'confidence': 96,
                'image': 'https://kimi-web-img.moonshot.cn/img/brettmollard.com/bcff4ae29ce5bd1b19e56f2c87979fda8fcab9a3.jpg',
                'notes': 'Clear lung fields, normal cardiac silhouette',
                'processingTime': 1.8,
                'modelVersion': 'MediAI v2.1'
            }
        ]
    },
    {
        'id': 'P2845',
        'name': 'Emily Rodriguez',
        'age': 42,
        'gender': 'Female',
        'image': 'https://kimi-web-img.moonshot.cn/img/media.istockphoto.com/a2a74530386bb9e80979af6604300c945b455f20.jpg',
        'lastVisit': (datetime.now() - timedelta(hours=8)).isoformat(),
        'totalScans': 3,
        'symptoms': ['Shortness of Breath', 'Fatigue', 'Fever'],
        'medicalHistory': 'Recent travel history',
        'allergies': ['Sulfa drugs'],
        'predictions': [
            {
                'date': (datetime.now() - timedelta(hours=8)).isoformat(),
                'condition': 'COVID-19',
                'confidence': 87,
                'image': 'https://kimi-web-img.moonshot.cn/img/static01.nyt.com/ec45b08a90a293a4b27ea2e5dc4c00ba15c2d1a3.jpg',
                'notes': 'Ground-glass opacities consistent with COVID-19',
                'processingTime': 2.7,
                'modelVersion': 'MediAI v2.1'
            }
        ]
    }
]

# System statistics
SYSTEM_STATS = {
    'patientsToday': 247,
    'averageWaitTime': 2.3,
    'aiAccuracy': 94.7,
    'activeQueue': 3,
    'totalScans': 1847,
    'processingTime': {
        'average': 2.3,
        'min': 1.2,
        'max': 4.8
    }
}

# Model performance metrics
MODEL_PERFORMANCE = {
    'accuracy': 94.7,
    'precision': 92.1,
    'recall': 89.5,
    'f1Score': 90.7,
    'aucScores': {
        'Normal': 0.95,
        'Pneumonia': 0.92,
        'COVID-19': 0.89
    },
    'confusionMatrix': [
        [45, 3, 2],
        [2, 38, 4],
        [1, 2, 28]
    ]
}

def generate_prediction_result(image_data=None):
    """Generate a simulated AI prediction result"""
    condition = random.choice(SAMPLE_CONDITIONS)
    confidence = random.randint(85, 98)
    
    # Generate confidence breakdown for all conditions
    confidences = {}
    for cond in SAMPLE_CONDITIONS:
        if cond == condition:
            confidences[cond.lower().replace('-', '')] = confidence
        else:
            remaining = 100 - confidence
            confidences[cond.lower().replace('-', '')] = random.randint(1, remaining // 2)
    
    # Normalize confidences to sum to 100
    total = sum(confidences.values())
    for key in confidences:
        confidences[key] = int(confidences[key] * 100 / total)
    
    # Ensure the primary condition has the highest confidence
    confidences[condition.lower().replace('-', '')] = max(confidences.values())
    
    descriptions = {
        'Pneumonia': 'AI model detected signs of pneumonia with high confidence. Recommend immediate clinical review.',
        'Normal': 'No abnormalities detected. Chest X-ray appears normal.',
        'COVID-19': 'Characteristics consistent with COVID-19 pneumonia detected.'
    }
    
    return {
        'condition': condition,
        'confidence': confidence,
        'description': descriptions[condition],
        'confidences': confidences,
        'processingTime': round(random.uniform(1.5, 3.5), 1),
        'modelVersion': 'MediAI v2.1',
        'timestamp': datetime.now().isoformat()
    }

def process_image_simulation(image_file):
    """Simulate AI image processing"""
    # Simulate processing delay
    time.sleep(random.uniform(2.5, 4.0))
    
    # Generate prediction
    result = generate_prediction_result()
    
    # Save uploaded file (simulate)
    if image_file:
        filename = f"upload_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{image_file.filename}"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        image_file.save(filepath)
        result['imagePath'] = filepath
    
    return result

@app.route('/')
def index():
    """Serve the main application"""
    return send_from_directory('.', 'index.html')

@app.route('/<path:filename>')
def serve_static(filename):
    """Serve static files"""
    return send_from_directory('.', filename)

# API Endpoints

@app.route('/api/analyze-image', methods=['POST'])
def analyze_image():
    """Analyze medical image and return AI prediction"""
    try:
        if 'image' not in request.files:
            return jsonify({'error': 'No image file provided'}), 400
        
        image_file = request.files['image']
        if image_file.filename == '':
            return jsonify({'error': 'No image file selected'}), 400
        
        # Validate file type
        allowed_extensions = {'png', 'jpg', 'jpeg', 'gif', 'bmp', 'dicom'}
        file_extension = image_file.filename.rsplit('.', 1)[1].lower()
        
        if file_extension not in allowed_extensions:
            return jsonify({'error': 'Invalid file type. Please upload an image file.'}), 400
        
        # Process image and get prediction
        result = process_image_simulation(image_file)
        
        # Update system stats
        SYSTEM_STATS['patientsToday'] += 1
        SYSTEM_STATS['totalScans'] += 1
        
        return jsonify({
            'success': True,
            'prediction': result,
            'status': 'completed',
            'message': 'Image analysis completed successfully'
        })
        
    except Exception as e:
        return jsonify({
            'error': 'Image analysis failed',
            'message': str(e)
        }), 500

@app.route('/api/patients', methods=['GET'])
def get_patients():
    """Get patient list with optional filtering"""
    try:
        search = request.args.get('search', '').lower()
        condition = request.args.get('condition', '')
        date_range = request.args.get('date_range', '')
        limit = int(request.args.get('limit', 50))
        offset = int(request.args.get('offset', 0))
        
        # Filter patients
        filtered_patients = MOCK_PATIENTS.copy()
        
        if search:
            filtered_patients = [
                p for p in filtered_patients
                if search in p['id'].lower() or
                   search in p['name'].lower() or
                   any(search in symptom.lower() for symptom in p['symptoms']) or
                   any(search in pred['condition'].lower() for pred in p['predictions'])
            ]
        
        if condition:
            filtered_patients = [
                p for p in filtered_patients
                if any(pred['condition'] == condition for pred in p['predictions'])
            ]
        
        # Apply pagination
        total = len(filtered_patients)
        patients = filtered_patients[offset:offset + limit]
        
        return jsonify({
            'success': True,
            'patients': patients,
            'total': total,
            'limit': limit,
            'offset': offset
        })
        
    except Exception as e:
        return jsonify({
            'error': 'Failed to retrieve patients',
            'message': str(e)
        }), 500

@app.route('/api/patients/<patient_id>', methods=['GET'])
def get_patient(patient_id):
    """Get specific patient details"""
    try:
        patient = next((p for p in MOCK_PATIENTS if p['id'] == patient_id), None)
        
        if not patient:
            return jsonify({'error': 'Patient not found'}), 404
        
        return jsonify({
            'success': True,
            'patient': patient
        })
        
    except Exception as e:
        return jsonify({
            'error': 'Failed to retrieve patient',
            'message': str(e)
        }), 500

@app.route('/api/patients/<patient_id>', methods=['PUT'])
def update_patient(patient_id):
    """Update patient information"""
    try:
        data = request.get_json()
        patient = next((p for p in MOCK_PATIENTS if p['id'] == patient_id), None)
        
        if not patient:
            return jsonify({'error': 'Patient not found'}), 404
        
        # Update patient fields
        allowed_fields = ['name', 'age', 'gender', 'symptoms', 'medicalHistory', 'allergies']
        for field in allowed_fields:
            if field in data:
                patient[field] = data[field]
        
        patient['lastVisit'] = datetime.now().isoformat()
        
        return jsonify({
            'success': True,
            'message': 'Patient updated successfully',
            'patient': patient
        })
        
    except Exception as e:
        return jsonify({
            'error': 'Failed to update patient',
            'message': str(e)
        }), 500

@app.route('/api/analytics/metrics', methods=['GET'])
def get_analytics_metrics():
    """Get model performance metrics"""
    try:
        time_range = request.args.get('time_range', '30d')
        
        # Generate historical data based on time range
        historical_data = []
        days = 30 if time_range == '30d' else 7 if time_range == '7d' else 90
        
        for i in range(days):
            date = datetime.now() - timedelta(days=i)
            historical_data.append({
                'date': date.isoformat(),
                'accuracy': 94.7 + random.uniform(-2, 2),
                'precision': 92.1 + random.uniform(-1.5, 1.5),
                'recall': 89.5 + random.uniform(-2.5, 2.5),
                'f1Score': 90.7 + random.uniform(-2, 2),
                'processedScans': random.randint(20, 100)
            })
        
        return jsonify({
            'success': True,
            'currentMetrics': MODEL_PERFORMANCE,
            'historicalData': historical_data[::-1],  # Reverse to get chronological order
            'systemStats': SYSTEM_STATS
        })
        
    except Exception as e:
        return jsonify({
            'error': 'Failed to retrieve analytics',
            'message': str(e)
        }), 500

@app.route('/api/analytics/usage', methods=['GET'])
def get_usage_analytics():
    """Get system usage analytics"""
    try:
        time_range = request.args.get('time_range', '30d')
        
        # Generate usage data
        usage_data = []
        if time_range == '7d':
            # Daily data for last 7 days
            for i in range(7):
                date = datetime.now() - timedelta(days=i)
                usage_data.append({
                    'date': date.isoformat(),
                    'scansProcessed': random.randint(30, 90),
                    'averageProcessingTime': round(random.uniform(1.8, 3.2), 1),
                    'peakHour': random.randint(9, 17),
                    'queueLength': random.randint(1, 8)
                })
        else:
            # Weekly data for longer ranges
            for i in range(4):
                week_start = datetime.now() - timedelta(weeks=i)
                usage_data.append({
                    'date': week_start.isoformat(),
                    'scansProcessed': random.randint(200, 500),
                    'averageProcessingTime': round(random.uniform(2.0, 2.8), 1),
                    'peakHour': random.randint(9, 17),
                    'queueLength': random.randint(2, 12)
                })
        
        return jsonify({
            'success': True,
            'usageData': usage_data[::-1]
        })
        
    except Exception as e:
        return jsonify({
            'error': 'Failed to retrieve usage data',
            'message': str(e)
        }), 500

@app.route('/api/system/status', methods=['GET'])
def get_system_status():
    """Get system health and status"""
    try:
        return jsonify({
            'success': True,
            'status': 'healthy',
            'timestamp': datetime.now().isoformat(),
            'version': 'MediAI v2.1',
            'uptime': '99.8%',
            'services': {
                'aiModel': 'active',
                'database': 'active',
                'storage': 'active',
                'api': 'active'
            },
            'systemStats': SYSTEM_STATS
        })
        
    except Exception as e:
        return jsonify({
            'error': 'Failed to retrieve system status',
            'message': str(e)
        }), 500

@app.route('/api/system/stats', methods=['GET'])
def get_real_time_stats():
    """Get real-time system statistics"""
    try:
        # Simulate real-time updates
        stats = SYSTEM_STATS.copy()
        stats['patientsToday'] += random.randint(0, 3)
        stats['activeQueue'] = max(0, stats['activeQueue'] + random.randint(-2, 2))
        stats['aiAccuracy'] = round(94.5 + random.uniform(-0.5, 0.5), 1)
        stats['averageWaitTime'] = round(2.3 + random.uniform(-0.5, 0.5), 1)
        
        return jsonify({
            'success': True,
            'stats': stats,
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({
            'error': 'Failed to retrieve real-time stats',
            'message': str(e)
        }), 500

@app.route('/api/predictions/<prediction_id>', methods=['GET'])
def get_prediction(prediction_id):
    """Get specific prediction details"""
    try:
        # Simulate prediction lookup
        prediction = generate_prediction_result()
        prediction['id'] = prediction_id
        
        return jsonify({
            'success': True,
            'prediction': prediction
        })
        
    except Exception as e:
        return jsonify({
            'error': 'Failed to retrieve prediction',
            'message': str(e)
        }), 500

@app.route('/api/export', methods=['POST'])
def export_data():
    """Export patient data and analytics"""
    try:
        data = request.get_json()
        export_type = data.get('type', 'patients')
        format_type = data.get('format', 'json')
        
        if export_type == 'patients':
            export_data = MOCK_PATIENTS
        elif export_type == 'analytics':
            export_data = {
                'modelPerformance': MODEL_PERFORMANCE,
                'systemStats': SYSTEM_STATS,
                'exportTimestamp': datetime.now().isoformat()
            }
        else:
            return jsonify({'error': 'Invalid export type'}), 400
        
        if format_type == 'json':
            return jsonify({
                'success': True,
                'data': export_data,
                'message': f'{export_type} data exported successfully'
            })
        else:
            return jsonify({'error': 'Format not supported'}), 400
            
    except Exception as e:
        return jsonify({
            'error': 'Export failed',
            'message': str(e)
        }), 500

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)