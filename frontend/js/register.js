/**
 * Registration form handler for kodbank1 banking application.
 * 
 * This module handles user registration with client-side validation,
 * form submission to the backend API, and error handling.
 * 
 * Requirements: 1.1, 1.5, 1.6
 * 
 * @module register
 */

// API Base URL - automatically detects environment
const API_BASE_URL = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1'
    ? '' // Use relative URLs for local development
    : ''; // Use relative URLs for Vercel (routes are configured in vercel.json)

document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('registerForm');
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
     * Validate registration form data on the client side.
     * 
     * Validates:
     * - uid: Required, non-empty
     * - uname: Required, non-empty
     * - password: Required, minimum 8 characters
     * - email: Required, valid email format
     * - phone: Required, non-empty
     * 
     * @param {Object} formData - The form data to validate
     * @param {string} formData.uid - User ID
     * @param {string} formData.uname - Username
     * @param {string} formData.password - Password
     * @param {string} formData.email - Email address
     * @param {string} formData.phone - Phone number
     * @returns {boolean} True if all validations pass, false otherwise
     */
    const validateForm = (formData) => {
        clearErrors();
        let isValid = true;

        console.log('Validating form data...');

        // Validate uid - must be non-empty
        if (!formData.uid || formData.uid.trim() === '') {
            console.log('Validation failed: User ID is empty');
            showFieldError('uid', 'User ID is required');
            isValid = false;
        } else {
            console.log('✓ User ID is valid');
        }

        // Validate username - must be non-empty
        if (!formData.uname || formData.uname.trim() === '') {
            console.log('Validation failed: Username is empty');
            showFieldError('uname', 'Username is required');
            isValid = false;
        } else {
            console.log('✓ Username is valid');
        }

        // Validate password - minimum 6 characters
        if (!formData.password || formData.password.length < 6) {
            console.log('Validation failed: Password length is', formData.password ? formData.password.length : 0, '(minimum 6 required)');
            showFieldError('password', 'Password must be at least 6 characters');
            isValid = false;
        } else {
            console.log('✓ Password is valid (length:', formData.password.length, ')');
        }

        // Validate email - basic email format check
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!formData.email || !emailRegex.test(formData.email)) {
            console.log('Validation failed: Email format is invalid');
            showFieldError('email', 'Please enter a valid email address');
            isValid = false;
        } else {
            console.log('✓ Email is valid');
        }

        // Validate phone - must be non-empty
        if (!formData.phone || formData.phone.trim() === '') {
            console.log('Validation failed: Phone is empty');
            showFieldError('phone', 'Phone number is required');
            isValid = false;
        } else {
            console.log('✓ Phone is valid');
        }

        console.log('Overall validation result:', isValid);
        return isValid;
    };

    /**
     * Handle registration form submission.
     * 
     * Process:
     * 1. Prevent default form submission
     * 2. Collect and validate form data
     * 3. Send POST request to /api/register endpoint
     * 4. Handle success (redirect to login) or error (display message)
     * 
     * Security considerations:
     * - Password is sent over HTTPS (enforced by backend)
     * - Form data is validated both client-side and server-side
     * - Submit button is disabled during request to prevent double submission
     * 
     * Requirements: 1.1, 1.5, 1.6
     */
    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        clearErrors();

        console.log('Registration form submitted');

        // Collect form data from input fields
        const formData = {
            uid: document.getElementById('uid').value.trim(),
            uname: document.getElementById('uname').value.trim(),
            password: document.getElementById('password').value,
            email: document.getElementById('email').value.trim(),
            phone: document.getElementById('phone').value.trim()
        };

        console.log('Form data collected:', { ...formData, password: '***' });

        // Validate form data before sending to server
        if (!validateForm(formData)) {
            console.log('Form validation failed');
            return;
        }

        console.log('Form validation passed');

        // Disable submit button to prevent double submission
        const submitButton = form.querySelector('button[type="submit"]');
        const originalText = submitButton.textContent;
        submitButton.disabled = true;
        submitButton.textContent = 'Registering...';

        try {
            console.log('Sending registration request to /api/register');
            console.log('API Base URL:', API_BASE_URL);
            
            // Send registration request to backend API
            const response = await fetch(`${API_BASE_URL}/api/register`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(formData)
            });

            console.log('Response status:', response.status);

            const data = await response.json();
            console.log('Response data:', data);

            if (response.ok && data.status === 'success') {
                // Registration successful - redirect to login page (Requirement 1.5)
                console.log('Registration successful, redirecting to login page');
                window.location.href = 'login.html';
            } else {
                // Handle error response from server (e.g., duplicate user)
                const errorMessage = data.message || 'Registration failed. Please try again.';
                console.log('Registration failed:', errorMessage);
                showFormError(errorMessage);
            }
        } catch (error) {
            // Handle network errors or server unavailability
            console.error('Registration error:', error);
            showFormError('Unable to connect to server. Please try again later.');
        } finally {
            // Re-enable submit button regardless of outcome
            submitButton.disabled = false;
            submitButton.textContent = originalText;
        }
    });
});
