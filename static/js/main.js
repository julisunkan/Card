// Business Card Generator - Main JavaScript

document.addEventListener('DOMContentLoaded', function() {
    // Initialize components
    initializeTemplateGallery();
    initializeFormValidation();
    initializeFileUpload();
    initializeTooltips();
    
    console.log('Business Card Generator initialized');
});

// Social media counter
let socialMediaCount = 0;
const maxSocialMedia = 1;

// Social media platform options
const socialPlatforms = {
    linkedin: { name: 'LinkedIn', icon: '💼', placeholder: 'https://linkedin.com/in/yourname' },
    twitter: { name: 'Twitter/X', icon: '🐦', placeholder: '@yourusername' },
    instagram: { name: 'Instagram', icon: '📷', placeholder: '@yourusername' },
    github: { name: 'GitHub', icon: '💻', placeholder: 'github.com/yourusername' },
    facebook: { name: 'Facebook', icon: '📘', placeholder: 'https://facebook.com/yourname' },
    tiktok: { name: 'TikTok', icon: '🎵', placeholder: '@yourusername' }
};

function addSocialMedia() {
    if (socialMediaCount >= maxSocialMedia) {
        showToast('Maximum 1 social media account allowed', 'error');
        return;
    }
    
    const container = document.getElementById('social-media-container');
    const socialDiv = document.createElement('div');
    socialDiv.className = 'mb-3 social-media-entry';
    socialDiv.dataset.index = socialMediaCount;
    
    // Get available platforms (not already selected)
    const usedPlatforms = Array.from(container.querySelectorAll('select[name^="social_platform"]'))
        .map(select => select.value)
        .filter(value => value);
    
    const availablePlatforms = Object.keys(socialPlatforms)
        .filter(platform => !usedPlatforms.includes(platform));
    
    if (availablePlatforms.length === 0) {
        showToast('All social media platforms have been added', 'error');
        return;
    }
    
    socialDiv.innerHTML = `
        <div class="row">
            <div class="col-md-4">
                <select class="form-select" name="social_platform_${socialMediaCount}" onchange="updateSocialPlaceholder(this)">
                    <option value="">Select Platform</option>
                    ${availablePlatforms.map(platform => 
                        `<option value="${platform}">${socialPlatforms[platform].icon} ${socialPlatforms[platform].name}</option>`
                    ).join('')}
                </select>
            </div>
            <div class="col-md-7">
                <input type="text" class="form-control" name="social_value_${socialMediaCount}" 
                       placeholder="Select platform first" disabled>
            </div>
            <div class="col-md-1">
                <button type="button" class="btn btn-outline-danger btn-sm" onclick="removeSocialMedia(this)">
                    <i class="fas fa-times"></i>
                </button>
            </div>
        </div>
    `;
    
    container.appendChild(socialDiv);
    socialMediaCount++;
    
    updateAddButton();
}

function removeSocialMedia(button) {
    const socialDiv = button.closest('.social-media-entry');
    socialDiv.remove();
    socialMediaCount--;
    updateAddButton();
}

function updateSocialPlaceholder(selectElement) {
    const platform = selectElement.value;
    const inputElement = selectElement.closest('.row').querySelector('input[name^="social_value"]');
    
    if (platform && socialPlatforms[platform]) {
        inputElement.placeholder = socialPlatforms[platform].placeholder;
        inputElement.disabled = false;
    } else {
        inputElement.placeholder = 'Select platform first';
        inputElement.disabled = true;
        inputElement.value = '';
    }
}

function updateAddButton() {
    const button = document.getElementById('add-social-media');
    if (socialMediaCount >= maxSocialMedia) {
        button.style.display = 'none';
    } else {
        button.style.display = 'inline-block';
    }
}

// Template Gallery Functionality
function initializeTemplateGallery() {
    const templatePreviews = document.querySelectorAll('.template-preview');
    const templateSelect = document.getElementById('template');
    
    if (templatePreviews.length > 0 && templateSelect) {
        templatePreviews.forEach(preview => {
            preview.addEventListener('click', function() {
                const templateId = this.dataset.template;
                
                // Update select value
                templateSelect.value = templateId;
                
                // Update visual selection
                templatePreviews.forEach(p => p.classList.remove('selected'));
                this.classList.add('selected');
                
                // Add animation
                this.style.transform = 'scale(0.95)';
                setTimeout(() => {
                    this.style.transform = '';
                }, 150);
            });
        });
        
        // Sync initial selection
        const initialTemplate = templateSelect.value;
        const initialPreview = document.querySelector(`[data-template="${initialTemplate}"]`);
        if (initialPreview) {
            initialPreview.classList.add('selected');
        }
    }
}

// Form Validation
function initializeFormValidation() {
    const forms = document.querySelectorAll('form');
    
    forms.forEach(form => {
        form.addEventListener('submit', function(event) {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
                
                // Focus on first invalid field
                const firstInvalid = form.querySelector(':invalid');
                if (firstInvalid) {
                    firstInvalid.focus();
                    showToast('Please fill in all required fields', 'error');
                }
            }
            
            form.classList.add('was-validated');
        });
    });
    
    // Real-time validation for email
    const emailInput = document.getElementById('email');
    if (emailInput) {
        emailInput.addEventListener('blur', function() {
            if (this.value && !isValidEmail(this.value)) {
                this.setCustomValidity('Please enter a valid email address');
                this.classList.add('is-invalid');
            } else {
                this.setCustomValidity('');
                this.classList.remove('is-invalid');
            }
        });
    }
    
    // Real-time validation for phone
    const phoneInput = document.getElementById('phone');
    if (phoneInput) {
        phoneInput.addEventListener('input', function() {
            // Allow common phone number formats
            this.value = this.value.replace(/[^\d\s\-\(\)\+]/g, '');
        });
    }
    
    // Real-time validation for website
    const websiteInput = document.getElementById('website');
    if (websiteInput) {
        websiteInput.addEventListener('blur', function() {
            if (this.value && !isValidURL(this.value)) {
                this.setCustomValidity('Please enter a valid URL (e.g., https://example.com)');
                this.classList.add('is-invalid');
            } else {
                this.setCustomValidity('');
                this.classList.remove('is-invalid');
            }
        });
    }
}

// File Upload Handling
function initializeFileUpload() {
    const logoInput = document.getElementById('logo');
    const csvInput = document.getElementById('csv_file');
    
    if (logoInput) {
        logoInput.addEventListener('change', function() {
            const file = this.files[0];
            if (file) {
                validateImageFile(file, this);
            }
        });
    }
    
    if (csvInput) {
        csvInput.addEventListener('change', function() {
            const file = this.files[0];
            if (file) {
                validateCSVFile(file, this);
            }
        });
    }
}

// Initialize Bootstrap Tooltips
function initializeTooltips() {
    const tooltipTriggerList = document.querySelectorAll('[data-bs-toggle="tooltip"]');
    if (tooltipTriggerList.length > 0 && typeof bootstrap !== 'undefined') {
        const tooltipList = [...tooltipTriggerList].map(tooltipTriggerEl => 
            new bootstrap.Tooltip(tooltipTriggerEl)
        );
    }
}

// Utility Functions
function isValidEmail(email) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
}

function isValidURL(url) {
    try {
        new URL(url);
        return true;
    } catch {
        return false;
    }
}

function validateImageFile(file, input) {
    const maxSize = 16 * 1024 * 1024; // 16MB
    const allowedTypes = ['image/jpeg', 'image/jpg', 'image/png', 'image/gif', 'image/svg+xml'];
    
    if (file.size > maxSize) {
        showToast('File is too large. Maximum size is 16MB.', 'error');
        input.value = '';
        return false;
    }
    
    if (!allowedTypes.includes(file.type)) {
        showToast('Invalid file type. Please upload PNG, JPG, GIF, or SVG.', 'error');
        input.value = '';
        return false;
    }
    
    showToast('Logo uploaded successfully!', 'success');
    return true;
}

function validateCSVFile(file, input) {
    const maxSize = 5 * 1024 * 1024; // 5MB
    
    if (file.size > maxSize) {
        showToast('CSV file is too large. Maximum size is 5MB.', 'error');
        input.value = '';
        return false;
    }
    
    if (!file.name.toLowerCase().endsWith('.csv')) {
        showToast('Please upload a CSV file.', 'error');
        input.value = '';
        return false;
    }
    
    showToast('CSV file loaded successfully!', 'success');
    return true;
}

// Toast Notification System
function showToast(message, type = 'info') {
    // Create toast container if it doesn't exist
    let toastContainer = document.getElementById('toast-container');
    if (!toastContainer) {
        toastContainer = document.createElement('div');
        toastContainer.id = 'toast-container';
        toastContainer.className = 'toast-container position-fixed top-0 end-0 p-3';
        toastContainer.style.zIndex = '1055';
        document.body.appendChild(toastContainer);
    }
    
    // Create toast element
    const toastId = 'toast-' + Date.now();
    const toastHtml = `
        <div id="${toastId}" class="toast align-items-center text-bg-${type === 'error' ? 'danger' : type === 'success' ? 'success' : 'primary'} border-0" role="alert">
            <div class="d-flex">
                <div class="toast-body">
                    <i class="fas fa-${type === 'error' ? 'exclamation-circle' : type === 'success' ? 'check-circle' : 'info-circle'} me-2"></i>
                    ${message}
                </div>
                <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button>
            </div>
        </div>
    `;
    
    toastContainer.insertAdjacentHTML('beforeend', toastHtml);
    
    // Initialize and show toast
    const toastElement = document.getElementById(toastId);
    if (typeof bootstrap !== 'undefined') {
        const toast = new bootstrap.Toast(toastElement, {
            autohide: true,
            delay: type === 'error' ? 5000 : 3000
        });
        toast.show();
        
        // Remove toast element after it's hidden
        toastElement.addEventListener('hidden.bs.toast', function() {
            this.remove();
        });
    } else {
        // Fallback if Bootstrap is not available
        setTimeout(() => {
            toastElement.remove();
        }, 3000);
    }
}

// Form Auto-save (localStorage)
function initializeAutoSave() {
    const form = document.getElementById('cardForm');
    if (!form) return;
    
    const formData = {};
    const inputs = form.querySelectorAll('input, select, textarea');
    
    // Load saved data
    const savedData = localStorage.getItem('businessCardForm');
    if (savedData) {
        try {
            const parsed = JSON.parse(savedData);
            inputs.forEach(input => {
                if (parsed[input.name] && input.type !== 'file') {
                    input.value = parsed[input.name];
                }
            });
        } catch (e) {
            console.warn('Failed to load saved form data');
        }
    }
    
    // Save data on change
    inputs.forEach(input => {
        input.addEventListener('change', function() {
            if (this.type !== 'file') {
                formData[this.name] = this.value;
                localStorage.setItem('businessCardForm', JSON.stringify(formData));
            }
        });
    });
}

// Clear saved form data
function clearSavedData() {
    localStorage.removeItem('businessCardForm');
    showToast('Saved form data cleared', 'info');
}

// Export button loading states
function initializeExportButtons() {
    const exportButtons = document.querySelectorAll('a[href*="export"]');
    
    exportButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            const icon = this.querySelector('i');
            const originalClass = icon.className;
            const originalText = this.textContent;
            
            // Show loading state
            icon.className = 'fas fa-spinner fa-spin me-2';
            
            // Reset after delay
            setTimeout(() => {
                icon.className = originalClass;
            }, 2000);
        });
    });
}

// Keyboard shortcuts
document.addEventListener('keydown', function(e) {
    // Ctrl/Cmd + Enter to submit form
    if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
        const form = document.querySelector('form');
        if (form) {
            form.submit();
        }
    }
    
    // Escape to clear form
    if (e.key === 'Escape') {
        const clearButton = document.querySelector('button[onclick="clearForm()"]');
        if (clearButton && confirm('Clear the form?')) {
            clearForm();
        }
    }
});

// Global clear form function
function clearForm() {
    const form = document.getElementById('cardForm');
    if (form) {
        form.reset();
        form.classList.remove('was-validated');
        
        // Clear template selection
        document.querySelectorAll('.template-preview').forEach(p => {
            p.classList.remove('selected');
        });
        
        // Clear saved data
        clearSavedData();
        
        showToast('Form cleared successfully', 'info');
    }
}

// Initialize auto-save when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    initializeAutoSave();
    initializeExportButtons();
});

// Page visibility API for auto-save
document.addEventListener('visibilitychange', function() {
    if (document.visibilityState === 'hidden') {
        // Save form data when user leaves the page
        const form = document.getElementById('cardForm');
        if (form) {
            const formData = {};
            const inputs = form.querySelectorAll('input, select, textarea');
            inputs.forEach(input => {
                if (input.type !== 'file') {
                    formData[input.name] = input.value;
                }
            });
            localStorage.setItem('businessCardForm', JSON.stringify(formData));
        }
    }
});

// Responsive helpers
function checkMobile() {
    return window.innerWidth <= 768;
}

// Handle responsive layout changes
window.addEventListener('resize', function() {
    const isMobile = checkMobile();
    
    // Adjust template gallery height on mobile
    const gallery = document.querySelector('.template-gallery');
    if (gallery) {
        gallery.style.maxHeight = isMobile ? '250px' : '400px';
    }
});

// Initialize on load
document.addEventListener('DOMContentLoaded', function() {
    // Set initial responsive states
    if (checkMobile()) {
        document.body.classList.add('mobile-view');
    }
});
