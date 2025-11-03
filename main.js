// Medical AI Platform - Main JavaScript
class MedicalAIPlatform {
    constructor() {
        this.initializeApp();
        this.setupEventListeners();
        this.initializeAnimations();
        this.startRealTimeUpdates();
    }

    initializeApp() {
        // Initialize state
        this.currentImage = null;
        this.isProcessing = false;
        this.predictions = [];
        
        // Sample prediction data for simulation
        this.samplePredictions = [
            { condition: 'Pneumonia', confidence: 94, description: 'AI model detected signs of pneumonia with high confidence. Recommend immediate clinical review.' },
            { condition: 'Normal', confidence: 96, description: 'No abnormalities detected. Chest X-ray appears normal.' },
            { condition: 'COVID-19', confidence: 87, description: 'Characteristics consistent with COVID-19 pneumonia detected.' },
            { condition: 'Pneumonia', confidence: 91, description: 'Bilateral pneumonia patterns identified in lower lobes.' },
            { condition: 'Normal', confidence: 98, description: 'Clear lung fields with normal cardiac silhouette.' }
        ];
        
        console.log('MediAI Platform initialized');
    }

    setupEventListeners() {
        // File upload handling
        const uploadZone = document.getElementById('upload-zone');
        const fileInput = document.getElementById('file-input');
        const analyzeBtn = document.getElementById('analyze-btn');
        const clearBtn = document.getElementById('clear-btn');
        const saveRecordBtn = document.getElementById('save-record-btn');
        const generateReportBtn = document.getElementById('generate-report-btn');

        // Upload zone interactions
        uploadZone.addEventListener('click', () => fileInput.click());
        uploadZone.addEventListener('dragover', this.handleDragOver.bind(this));
        uploadZone.addEventListener('dragleave', this.handleDragLeave.bind(this));
        uploadZone.addEventListener('drop', this.handleDrop.bind(this));
        fileInput.addEventListener('change', this.handleFileSelect.bind(this));

        // Button interactions
        if (analyzeBtn) analyzeBtn.addEventListener('click', this.analyzeImage.bind(this));
        if (clearBtn) clearBtn.addEventListener('click', this.clearImage.bind(this));
        if (saveRecordBtn) saveRecordBtn.addEventListener('click', this.saveToRecord.bind(this));
        if (generateReportBtn) generateReportBtn.addEventListener('click', this.generateReport.bind(this));

        // Navigation active state
        this.updateNavigation();
    }

    initializeAnimations() {
        // Initialize text splitting for animations
        if (typeof Splitting !== 'undefined') {
            Splitting();
            
            // Animate hero text
            anime({
                targets: '[data-splitting] .char',
                translateY: [100, 0],
                opacity: [0, 1],
                easing: 'easeOutExpo',
                duration: 1400,
                delay: anime.stagger(30)
            });
        }

        // Animate stats cards on load
        anime({
            targets: '.bg-white',
            translateY: [20, 0],
            opacity: [0, 1],
            easing: 'easeOutQuart',
            duration: 800,
            delay: anime.stagger(100)
        });

        // Initialize P5.js background
        this.initializeBackground();
    }

    initializeBackground() {
        // P5.js sketch for medical grid background
        const sketch = (p) => {
            let particles = [];
            
            p.setup = () => {
                const canvas = p.createCanvas(p.windowWidth, p.windowHeight);
                canvas.id('p5-background');
                canvas.parent(document.body);
                
                // Create particles
                for (let i = 0; i < 50; i++) {
                    particles.push({
                        x: p.random(p.width),
                        y: p.random(p.height),
                        vx: p.random(-0.5, 0.5),
                        vy: p.random(-0.5, 0.5),
                        size: p.random(2, 6)
                    });
                }
            };
            
            p.draw = () => {
                p.clear();
                p.stroke(37, 99, 235, 30);
                p.strokeWeight(1);
                p.noFill();
                
                // Draw connections
                for (let i = 0; i < particles.length; i++) {
                    for (let j = i + 1; j < particles.length; j++) {
                        const dist = p.dist(particles[i].x, particles[i].y, particles[j].x, particles[j].y);
                        if (dist < 100) {
                            p.line(particles[i].x, particles[i].y, particles[j].x, particles[j].y);
                        }
                    }
                }
                
                // Update and draw particles
                particles.forEach(particle => {
                    particle.x += particle.vx;
                    particle.y += particle.vy;
                    
                    // Wrap around edges
                    if (particle.x < 0) particle.x = p.width;
                    if (particle.x > p.width) particle.x = 0;
                    if (particle.y < 0) particle.y = p.height;
                    if (particle.y > p.height) particle.y = 0;
                    
                    p.fill(37, 99, 235, 60);
                    p.noStroke();
                    p.circle(particle.x, particle.y, particle.size);
                });
            };
            
            p.windowResized = () => {
                p.resizeCanvas(p.windowWidth, p.windowHeight);
            };
        };
        
        new p5(sketch);
    }

    handleDragOver(e) {
        e.preventDefault();
        e.currentTarget.classList.add('dragover');
    }

    handleDragLeave(e) {
        e.currentTarget.classList.remove('dragover');
    }

    handleDrop(e) {
        e.preventDefault();
        e.currentTarget.classList.remove('dragover');
        const files = e.dataTransfer.files;
        if (files.length > 0) {
            this.processFile(files[0]);
        }
    }

    handleFileSelect(e) {
        const file = e.target.files[0];
        if (file) {
            this.processFile(file);
        }
    }

    processFile(file) {
        if (!file.type.startsWith('image/')) {
            this.showNotification('Please select a valid image file.', 'error');
            return;
        }

        const reader = new FileReader();
        reader.onload = (e) => {
            this.currentImage = {
                file: file,
                dataUrl: e.target.result,
                name: file.name
            };
            this.displayImagePreview();
        };
        reader.readAsDataURL(file);
    }

    displayImagePreview() {
        const previewImg = document.getElementById('preview-img');
        const uploadZone = document.getElementById('upload-zone');
        const imagePreview = document.getElementById('image-preview');
        
        if (previewImg && this.currentImage) {
            previewImg.src = this.currentImage.dataUrl;
            uploadZone.classList.add('hidden');
            imagePreview.classList.remove('hidden');
            
            // Animate preview appearance
            anime({
                targets: '#image-preview',
                opacity: [0, 1],
                translateY: [20, 0],
                duration: 500,
                easing: 'easeOutQuart'
            });
        }
    }

    analyzeImage() {
        if (!this.currentImage || this.isProcessing) return;
        
        this.isProcessing = true;
        const processingOverlay = document.getElementById('processing-overlay');
        const resultsPlaceholder = document.getElementById('results-placeholder');
        const resultsContent = document.getElementById('results-content');
        
        // Show processing overlay
        processingOverlay.classList.remove('hidden');
        
        // Simulate AI processing time
        setTimeout(() => {
            this.displayResults();
            this.isProcessing = false;
            processingOverlay.classList.add('hidden');
            resultsPlaceholder.classList.add('hidden');
            resultsContent.classList.remove('hidden');
            
            // Animate results
            anime({
                targets: '#results-content',
                opacity: [0, 1],
                translateY: [20, 0],
                duration: 600,
                easing: 'easeOutQuart'
            });
            
            // Animate confidence bars
            this.animateConfidenceBars();
            
        }, 2500);
    }

    displayResults() {
        // Get random prediction for simulation
        const prediction = this.samplePredictions[Math.floor(Math.random() * this.samplePredictions.length)];
        
        // Update UI elements
        const diagnosisResult = document.getElementById('diagnosis-result');
        const diagnosisDescription = document.getElementById('diagnosis-description');
        const confidenceBadge = document.getElementById('confidence-badge');
        
        if (diagnosisResult) {
            diagnosisResult.textContent = prediction.condition;
            diagnosisResult.className = `text-3xl font-bold mb-2 ${this.getConditionColor(prediction.condition)}`;
        }
        
        if (diagnosisDescription) {
            diagnosisDescription.textContent = prediction.description;
        }
        
        if (confidenceBadge) {
            confidenceBadge.textContent = `${prediction.confidence}% Confidence`;
            confidenceBadge.className = `px-3 py-1 rounded-full text-sm font-medium ${this.getConfidenceBadgeColor(prediction.confidence)}`;
        }
        
        // Update confidence bars
        this.updateConfidenceBars(prediction);
        
        // Add to recent predictions
        this.addToRecentPredictions(prediction);
    }

    updateConfidenceBars(primaryPrediction) {
        const conditions = ['Pneumonia', 'Normal', 'COVID-19'];
        const totalConfidence = 100;
        
        conditions.forEach(condition => {
            const bar = document.getElementById(`${condition.toLowerCase().replace('-', '')}-bar`);
            if (bar) {
                let confidence;
                if (condition === primaryPrediction.condition) {
                    confidence = primaryPrediction.confidence;
                } else {
                    confidence = Math.floor(Math.random() * 10) + 1; // Random low confidence for others
                }
                bar.style.width = `${confidence}%`;
            }
        });
    }

    animateConfidenceBars() {
        anime({
            targets: ['#pneumonia-bar', '#normal-bar', '#covid-bar'],
            width: (el) => el.style.width,
            duration: 1000,
            easing: 'easeOutQuart',
            delay: anime.stagger(200)
        });
    }

    getConditionColor(condition) {
        switch (condition) {
            case 'Pneumonia': return 'text-red-600';
            case 'Normal': return 'text-green-600';
            case 'COVID-19': return 'text-orange-600';
            default: return 'text-gray-900';
        }
    }

    getConfidenceBadgeColor(confidence) {
        if (confidence >= 90) return 'bg-green-100 text-green-800';
        if (confidence >= 80) return 'bg-yellow-100 text-yellow-800';
        return 'bg-red-100 text-red-800';
    }

    addToRecentPredictions(prediction) {
        this.predictions.unshift({
            ...prediction,
            timestamp: new Date(),
            patientId: `P${String(Math.floor(Math.random() * 9000) + 1000).padStart(4, '0')}`,
            image: this.currentImage?.dataUrl
        });
        
        // Keep only last 10 predictions
        if (this.predictions.length > 10) {
            this.predictions = this.predictions.slice(0, 10);
        }
    }

    clearImage() {
        this.currentImage = null;
        const uploadZone = document.getElementById('upload-zone');
        const imagePreview = document.getElementById('image-preview');
        const resultsPlaceholder = document.getElementById('results-placeholder');
        const resultsContent = document.getElementById('results-content');
        
        uploadZone.classList.remove('hidden');
        imagePreview.classList.add('hidden');
        resultsPlaceholder.classList.remove('hidden');
        resultsContent.classList.add('hidden');
        
        // Reset file input
        document.getElementById('file-input').value = '';
    }

    saveToRecord() {
        this.showNotification('Patient record saved successfully!', 'success');
        
        // Update patient count
        const patientsCount = document.getElementById('patients-count');
        if (patientsCount) {
            const currentCount = parseInt(patientsCount.textContent) || 0;
            this.animateCounter(patientsCount, currentCount, currentCount + 1);
        }
    }

    generateReport() {
        this.showNotification('Generating detailed report...', 'info');
        
        // Simulate report generation
        setTimeout(() => {
            this.showNotification('Report generated successfully!', 'success');
        }, 1500);
    }

    showNotification(message, type = 'info') {
        // Create notification element
        const notification = document.createElement('div');
        notification.className = `fixed top-4 right-4 z-50 px-6 py-3 rounded-lg shadow-lg text-white font-medium transform translate-x-full transition-transform duration-300 ${
            type === 'success' ? 'bg-green-600' :
            type === 'error' ? 'bg-red-600' :
            type === 'warning' ? 'bg-yellow-600' :
            'bg-blue-600'
        }`;
        notification.textContent = message;
        
        document.body.appendChild(notification);
        
        // Animate in
        setTimeout(() => {
            notification.style.transform = 'translateX(0)';
        }, 100);
        
        // Animate out and remove
        setTimeout(() => {
            notification.style.transform = 'translateX(100%)';
            setTimeout(() => {
                document.body.removeChild(notification);
            }, 300);
        }, 3000);
    }

    animateCounter(element, start, end) {
        anime({
            targets: { value: start },
            value: end,
            duration: 1000,
            easing: 'easeOutQuart',
            update: function(anim) {
                element.textContent = Math.floor(anim.animatables[0].target.value);
            }
        });
    }

    updateNavigation() {
        const currentPage = window.location.pathname.split('/').pop() || 'index.html';
        const navLinks = document.querySelectorAll('.nav-link');
        
        navLinks.forEach(link => {
            const href = link.getAttribute('href');
            if (href === currentPage) {
                link.classList.add('active');
            } else {
                link.classList.remove('active');
            }
        });
    }

    startRealTimeUpdates() {
        // Update stats periodically
        setInterval(() => {
            this.updateLiveStats();
        }, 5000);
        
        // Initial stats animation
        setTimeout(() => {
            this.animateInitialStats();
        }, 1000);
    }

    updateLiveStats() {
        // Simulate real-time accuracy updates
        const accuracyElement = document.getElementById('accuracy-percent');
        if (accuracyElement) {
            const currentAccuracy = parseFloat(accuracyElement.textContent);
            const newAccuracy = currentAccuracy + (Math.random() - 0.5) * 0.2;
            const clampedAccuracy = Math.max(94.0, Math.min(95.5, newAccuracy));
            
            anime({
                targets: { value: currentAccuracy },
                value: clampedAccuracy,
                duration: 1000,
                easing: 'easeOutQuart',
                update: function(anim) {
                    accuracyElement.textContent = anim.animatables[0].target.value.toFixed(1) + '%';
                }
            });
        }
        
        // Update queue count
        const queueElement = document.getElementById('queue-count');
        if (queueElement && Math.random() < 0.3) { // 30% chance to update
            const currentQueue = parseInt(queueElement.textContent);
            const newQueue = Math.max(0, currentQueue + Math.floor(Math.random() * 3) - 1);
            this.animateCounter(queueElement, currentQueue, newQueue);
        }
    }

    animateInitialStats() {
        // Animate initial counter values
        const patientsCount = document.getElementById('patients-count');
        if (patientsCount) {
            this.animateCounter(patientsCount, 0, 247);
        }
    }
}

// Initialize the application when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.medicalAI = new MedicalAIPlatform();
});

// Utility functions for other pages
window.MedicalAIUtils = {
    formatDate: (date) => {
        return new Intl.DateTimeFormat('en-US', {
            year: 'numeric',
            month: 'short',
            day: 'numeric',
            hour: '2-digit',
            minute: '2-digit'
        }).format(date);
    },
    
    getConditionColor: (condition) => {
        switch (condition) {
            case 'Pneumonia': return 'text-red-600 bg-red-100';
            case 'Normal': return 'text-green-600 bg-green-100';
            case 'COVID-19': return 'text-orange-600 bg-orange-100';
            default: return 'text-gray-600 bg-gray-100';
        }
    },
    
    showNotification: (message, type = 'info') => {
        if (window.medicalAI) {
            window.medicalAI.showNotification(message, type);
        }
    }
};