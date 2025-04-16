// Drowsiness Detector JavaScript

document.addEventListener('DOMContentLoaded', function() {
    // Check if we're on the detection page
    const videoFeed = document.getElementById('videoFeed');
    if (!videoFeed) return;

    const statusOverlay = document.getElementById('status-overlay');
    const statusMessage = document.getElementById('statusMessage');
    const detectionStatus = document.getElementById('detectionStatus');
    const detectionMessage = document.getElementById('detectionMessage');

    // Function to poll status from the server
    function pollStatus() {
        fetch('/get_status')
            .then(response => response.json())
            .then(data => {
                updateStatusDisplay(data.status, data.message);
            })
            .catch(error => {
                console.error('Error fetching status:', error);
            });
    }

    // Update the UI based on detection status
    function updateStatusDisplay(status, message) {
        detectionStatus.textContent = formatStatus(status);
        detectionMessage.textContent = message;

        // Remove all status classes
        detectionStatus.classList.remove('status-awake', 'status-drowsy', 'status-no-face');
        statusOverlay.classList.remove('warning');

        // Add appropriate class based on status
        if (status === 'drowsy') {
            detectionStatus.classList.add('status-drowsy');
            statusOverlay.classList.add('warning');
            statusMessage.textContent = message;
        } else if (status === 'awake') {
            detectionStatus.classList.add('status-awake');
            statusMessage.textContent = 'Eyes Open - Looking Good!';
        } else if (status === 'no_face') {
            detectionStatus.classList.add('status-no-face');
            statusMessage.textContent = 'No Face Detected - Please Position Yourself in Frame';
        } else {
            statusMessage.textContent = 'Initializing...';
        }
    }

    // Format status text for display
    function formatStatus(status) {
        switch(status) {
            case 'awake':
                return 'Awake';
            case 'drowsy':
                return 'DROWSY - WAKE UP!';
            case 'no_face':
                return 'No Face Detected';
            case 'no_camera':
                return 'Camera Not Available';
            default:
                return 'Initializing...';
        }
    }

    // Request permission for camera if needed
    function requestCameraPermission() {
        navigator.mediaDevices.getUserMedia({ video: true })
            .then(stream => {
                // We don't need to use the stream here since Flask handles the camera
                console.log('Camera permission granted');
                stream.getTracks().forEach(track => track.stop());
            })
            .catch(error => {
                console.error('Camera permission denied:', error);
                detectionStatus.textContent = 'Camera Access Denied';
                detectionMessage.textContent = 'Please allow camera access to use this application';
            });
    }

    // Set up polling for status updates
    let statusInterval = setInterval(pollStatus, 1000);

    // Clean up when leaving the page
    window.addEventListener('beforeunload', function() {
        clearInterval(statusInterval);
    });

    // Request camera permission on page load
    requestCameraPermission();
});