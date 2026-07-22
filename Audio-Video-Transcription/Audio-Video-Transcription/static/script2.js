/* =========================================================
   AUDIO/VIDEO TRANSCRIPTION - DOCUMENT PAGE INTERACTION SCRIPT
   - Upper Right 3-Line Menu
   - Download as PDF / Docx with Rename Modal Popup
   - Mobile-Only Share Option (Hidden on Desktop)
   - 3-Way Translation (Hindi->English, English->Hindi, Mix)
========================================================= */

document.addEventListener("DOMContentLoaded", function () {
    checkDeviceShare();
});

// Toggle Main Hamburger Menu
function toggleMenu() {
    const menu = document.getElementById("menuDropdown");
    if (menu) {
        menu.classList.toggle("active");
    }
}

// Toggle Submenu (Download / Translate)
function toggleSubmenu(id) {
    const sub = document.getElementById(id);
    if (sub) {
        // Toggle current
        const isCurrentlyActive = sub.classList.contains("active");
        
        // Close all submenus first
        document.querySelectorAll(".submenu").forEach(el => {
            el.classList.remove("active");
        });

        if (!isCurrentlyActive) {
            sub.classList.add("active");
        }
    }
}

// Close menu when clicking outside
document.addEventListener("click", function (event) {
    const menuContainer = document.querySelector(".menu-container");
    if (menuContainer && !menuContainer.contains(event.target)) {
        const menu = document.getElementById("menuDropdown");
        if (menu) menu.classList.remove("active");
        document.querySelectorAll(".submenu").forEach(el => el.classList.remove("active"));
    }
});

// DEVICE DETECTION FOR SHARE OPTION
function checkDeviceShare() {
    const shareOption = document.getElementById("shareOption");
    if (!shareOption) return;

    const isMobile = /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent) 
                    || window.innerWidth <= 768;

    if (isMobile) {
        shareOption.style.display = "flex";
    } else {
        shareOption.style.display = "none";
    }
}

// MOBILE SHARE FUNCTION
function shareDocument() {
    const textContentEl = document.getElementById("textContent");
    const docTitleEl = document.getElementById("docTitle");

    const title = docTitleEl ? docTitleEl.innerText : "Audio/Video Transcription";
    const text = textContentEl ? textContentEl.innerText.substring(0, 500) + "..." : "";

    if (navigator.share) {
        navigator.share({
            title: title,
            text: text,
            url: window.location.href
        }).catch(err => console.log("Share cancelled or failed:", err));
    } else {
        alert("Native sharing is supported on mobile devices.");
    }
}

// DOWNLOAD WITH RENAME MODAL
let selectedFormat = 'pdf';

function openDownloadModal(format) {
    selectedFormat = format;
    const modal = document.getElementById("downloadModal");
    const downloadForm = document.getElementById("downloadForm");
    const formatLabel = document.getElementById("formatLabel");
    const filenameInput = document.getElementById("filenameInput");
    const docTitleEl = document.getElementById("docTitle");

    let defaultName = "Document";
    if (docTitleEl) {
        defaultName = docTitleEl.innerText.replace(/[^a-zA-Z0-9]/g, "_").replace(/_+/g, "_");
    }

    if (format === 'pdf') {
        formatLabel.innerText = "PDF Document (.pdf)";
        downloadForm.action = "/download-pdf";
        filenameInput.value = defaultName + ".pdf";
    } else {
        formatLabel.innerText = "Word Document (.docx)";
        downloadForm.action = "/download-docx";
        filenameInput.value = defaultName + ".docx";
    }

    if (modal) {
        modal.classList.add("active");
    }

    // Close dropdown menu
    const menu = document.getElementById("menuDropdown");
    if (menu) menu.classList.remove("active");
}

function closeDownloadModal() {
    const modal = document.getElementById("downloadModal");
    if (modal) {
        modal.classList.remove("active");
    }
}

// TRANSLATION FUNCTIONALITY
function translateDocument(targetLang) {
    const textContentEl = document.getElementById("textContent");
    if (!textContentEl) return;

    const currentText = textContentEl.innerText;
    if (!currentText || currentText.trim() === "") {
        alert("No content available to translate.");
        return;
    }

    showLoading("Translating content...");

    // Close menu
    const menu = document.getElementById("menuDropdown");
    if (menu) menu.classList.remove("active");

    fetch("/translate", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            language: targetLang,
            text: currentText
        })
    })
    .then(response => response.json())
    .then(data => {
        hideLoading();
        if (data.success && data.translated_text) {
            textContentEl.innerText = data.translated_text;
        } else {
            alert("Translation error: " + (data.error || "Failed to translate"));
        }
    })
    .catch(err => {
        hideLoading();
        console.error("Translation request failed:", err);
        alert("Translation process encountered an error.");
    });
}

function showLoading(message) {
    const overlay = document.getElementById("loadingOverlay");
    const textEl = document.getElementById("loadingText");
    if (textEl) textEl.innerText = message || "Processing...";
    if (overlay) overlay.classList.add("active");
}

function hideLoading() {
    const overlay = document.getElementById("loadingOverlay");
    if (overlay) overlay.classList.remove("active");
}