/**
 * Login form handler for kodbank1 banking application.
 * 
 * This module handles user authentication with client-side validation,
 * form submission to the backend API, JWT token management via cookies,
 * and error handling.
 * 
 * Security considerations:
 * - JWT token is stored as HTTP-only cookie (set by backend)
 * - Credentials are sent over HTTPS
 * - credentials: 'include' ensures cookies are sent with requests
 * 
 * Requirements: 2.1, 2.6, 2.7, 2.8
 * 
 * @module login
 */

document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('loginForm');
    const formError = document.getElementById('form-error');

    /**
     * Clear all error messages from the form.
     * Removes both general form errors and field-specific errors.
     */
    const clearErrors = () => {
        formError.textContent = '';
        document.querySelectorAll('.error-message').forEach(el => {
            el.textContent = '';
        });
    };

    /**
     * Display an error message for a specific form field.
     * 
     * @param {string} fieldId - The ID of the form field
     * @param {string} message - The error message to display
     */
    const showFieldError = (fieldId, message) => {
        const errorElement = document.getElementById(`${fieldId}-error`);
        if (errorElement) {
            errorElement.textContent = message;
        }
    };

    /**
     * Display a general form error message.
     * 
     * @param {string} message - The error message to display
     */
    const showFormError = (message) => {
        formError.textContent = message;
    };

    /**
     * Validate login form data on the client side.
     * 
     * Validates:
     * - username: Required, non-empty
     * - password: Required, non-empty
     * 
     * @param {Object} formData - The form data to validate
     * @param {string} formData.username - Username
     * @param {string} formData.password - Password
     * @returns {boolean} True if all validations pass, false otherwise
     */
    const validateForm = (formData) => {
        clearErrors();
        let isValid = true;

        // Validate username - must be non-empty
        if (!formData.username || formData.username.trim() === '') {
            showFieldError('username', 'Username is required');
            isValid = false;
        }

        // Validate password - must be non-empty
        if (!formData.password || formData.password.trim() === '') {
            showFieldError('password', 'Password is required');
            isValid = false;
        }

        return isValid;
    };

    /**
     * Handle login form submission.
     * 
     * Process:
     * 1. Prevent default form submission
     * 2. Collect and validate form data
     * 3. Send POST request to /api/login endpoint with credentials
     * 4. Backend sets JWT token as HTTP-only cookie on success
     * 5. Redirect to dashboard on success or display error
     * 
     * Security considerations:
     * - credentials: 'include' ensures cookies are sent and received
     * - JWT token is stored as HTTP-only cookie (prevents XSS attacks)
     * - Password is sent over HTTPS (enforced by backend)
     * - Submit button is disabled during request to prevent double submission
     * 
     * Requirements: 2.1, 2.5, 2.6, 2.7, 2.8
     */
    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        clearErrors();

        // Collect credentials from form
        const formData = {
            username: document.getElementById('username').value.trim(),
            password: document.getElementById('password').value
        };

        // Validate form data before sending to server
        if (!validateForm(formData)) {
            return;
        }

        // Disable submit button to prevent double submission
        const submitButton = form.querySelector('button[type="submit"]');
        const originalText = submitButton.textContent;
        submitButton.disabled = true;
        submitButton.textContent = 'Logging in...';

        try {
            // Send login request to backend API
            // credentials: 'include' ensures cookies are sent and received
            const response = await fetch('/api/login', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                credentials: 'include', // Required for cookie-based authentication
                body: JSON.stringify(formData)
            });

            const data = await response.json();

            if (response.ok && data.status === 'success') {
                // Login successful - JWT token is now stored as HTTP-only cookie
                // Store username in localStorage for display purposes
                localStorage.setItem('username', formData.username);
                // Redirect to dashboard (Requirement 2.7)
                window.location.href = 'dashboard.html';
            } else {
                // Handle authentication failure (invalid credentials)
                const errorMessage = data.message || 'Login failed. Please check your credentials.';
                showFormError(errorMessage);
            }
        } catch (error) {
            // Handle network errors or server unavailability
            showFormError('Unable to connect to server. Please try again later.');
            console.error('Login error:', error);
        } finally {
            // Re-enable submit button regardless of outcome
            submitButton.disabled = false;
            submitButton.textContent = originalText;
        }
    });
});
