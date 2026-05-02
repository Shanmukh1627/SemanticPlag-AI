async function processAnalysis() {
    const btn = document.getElementById('scanBtn');
    const results = document.getElementById('resultSection');
    const circle = document.getElementById('scoreCircle');
    const scoreNum = document.getElementById('scoreNum');
    const downloadBtn = document.getElementById('downloadBtn');
    
    // --- 🚨 GRAB THE ACTUAL FILE ---
    const fileInput = document.querySelector('input[type="file"]');
    if (!fileInput || fileInput.files.length === 0) {
        alert("Please choose a PDF file first!");
        return;
    }
    
    // Package the file into a FormData object
    const formData = new FormData();
    formData.append('file', fileInput.files[0]);
    // ----------------------------------------

    btn.innerText = "Analyzing System...";
    btn.disabled = true;
    results.style.display = "grid";
    
    // Hide the download button while a new scan is processing
    if (downloadBtn) {
        downloadBtn.style.display = "none";
    }

    try {
        const response = await fetch('http://127.0.0.1:5000/analyze', {
            method: 'POST',
            body: formData 
        });
        
        const data = await response.json();

        // Safety Check
        if (data.error) {
            alert("Backend Error: " + data.error);
            btn.innerText = "Scan Failed";
            btn.style.background = "#ef4444";
            btn.disabled = false;
            return;
        }

        // 2-second delay to simulate "thinking"
        setTimeout(() => {
            const finalScore = data.score; 
            const offset = 314 - (314 * finalScore) / 100;
            
            // --- 🎨 UPGRADE 1: DYNAMIC THREAT COLORS ---
            let threatColor = "#10b981"; // Default Green (Original)
            if (finalScore >= 85) threatColor = "#ef4444"; // Red (Exact Plagiarism)
            else if (finalScore >= 70) threatColor = "#f59e0b"; // Orange (Paraphrased)
            else if (finalScore >= 50) threatColor = "#3b82f6"; // Blue (Idea Level)

            circle.style.stroke = threatColor; 
            scoreNum.style.color = threatColor; 
            document.getElementById('statusMsg').style.color = threatColor; 
            // -------------------------------------------
            
            circle.style.strokeDashoffset = offset;
            scoreNum.innerText = parseFloat(finalScore).toFixed(2);
            
            document.getElementById('statusMsg').innerText = data.status;
            document.getElementById('findingsText').innerHTML = `
                <p><strong>Verdict:</strong> <span style="color: ${threatColor}">${data.status}</span></p>
                <p>${data.details}</p>
            `;
            
            btn.innerText = "Analysis Complete";
            btn.style.background = "#059669";
            btn.disabled = false;

            // SHOW THE DOWNLOAD BUTTON
            if (downloadBtn) {
                downloadBtn.style.display = "block";
            }
            
        }, 2000);

    } catch (error) {
        console.error(error);
        btn.innerText = "Server Error";
        btn.style.background = "#ef4444";
        btn.disabled = false;
    }
} 

function downloadReport() {
    window.location.href = 'http://127.0.0.1:5000/download-report';
}

// --- 🌓 UPGRADE: LIGHT/DARK MODE TOGGLE ---
function toggleTheme() {
    const htmlElement = document.documentElement;
    const themeBtn = document.getElementById('themeToggle');
    
    // Check current theme
    if (htmlElement.getAttribute('data-theme') === 'light') {
        htmlElement.removeAttribute('data-theme');
        themeBtn.innerText = "☀️ Light Mode";
        localStorage.setItem('theme', 'dark'); // Save memory
    } else {
        htmlElement.setAttribute('data-theme', 'light');
        themeBtn.innerText = "🌙 Dark Mode";
        localStorage.setItem('theme', 'light'); // Save memory
    }
}

// --- 🖱️ ON PAGE LOAD: HANDLE DRAG & DROP AND SAVED THEME ---
document.addEventListener("DOMContentLoaded", () => {
    
    // 1. Load the user's saved theme from previous visits
    const savedTheme = localStorage.getItem('theme');
    const themeBtn = document.getElementById('themeToggle');
    
    if (savedTheme === 'light') {
        document.documentElement.setAttribute('data-theme', 'light');
        if (themeBtn) themeBtn.innerText = "🌙 Dark Mode";
    }

    // 2. Setup Drag and Drop logic
    const uploadBox = document.getElementById('uploadBox');
    const fileInput = document.getElementById('fileInput');
    const fileNameLabel = document.getElementById('fileNameLabel');

    if (uploadBox) {
        // Highlight box when dragging a file over it
        uploadBox.addEventListener('dragover', (e) => {
            e.preventDefault();
            uploadBox.classList.add('drag-active');
        });

        // Remove highlight when dragging away
        uploadBox.addEventListener('dragleave', () => {
            uploadBox.classList.remove('drag-active');
        });

        // Handle the actual drop
        uploadBox.addEventListener('drop', (e) => {
            e.preventDefault();
            uploadBox.classList.remove('drag-active');
            
            if (e.dataTransfer.files.length > 0) {
                fileInput.files = e.dataTransfer.files;
                fileNameLabel.innerText = 'Selected: ' + fileInput.files[0].name;
            }
        });
    }
});