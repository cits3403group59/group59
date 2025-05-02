// Form submission handler
document.getElementById('signin-form').addEventListener('submit', function(event) {
    event.preventDefault();
    
    // Get form values
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;
    
    // If any required field is left empty, show an alert
    if (!email || !password) {
        alert('Please fill in all required fields');
        return;
    }
    
    // Here you would typically send the form data to your server for authentication
    // For now, we'll just simulate success and redirect
    alert('Signed in successfully!');
    window.location.href = '{{url_for("introductory")}}';
});

        // Set DOB date constraints
        window.addEventListener('DOMContentLoaded', () => {
            const today = new Date();
            const year = today.getFullYear();
            const month = String(today.getMonth() + 1).padStart(2, '0');
            const day = String(today.getDate()).padStart(2, '0');
            const maxDate = `${year}-${month}-${day}`;
            const minYear = year - 120;
            const minDate = `${minYear}-${month}-${day}`;

            document.getElementById('dob').setAttribute('max', maxDate);
            document.getElementById('dob').setAttribute('min', minDate);
        });

// Handle form submission
document.getElementById('signup-form').addEventListener('submit', function (event) {
    event.preventDefault();

    const firstName = document.getElementById('name').value.trim();
    const lastName = document.getElementById('lastName').value.trim();
    const email = document.getElementById('email').value.trim();
    const dob = document.getElementById('dob').value;
    const password = document.getElementById('password').value;
    const confirmPassword = document.getElementById('confirm-password').value;
    const termsAccepted = document.getElementById('terms').checked;

    if (!firstName || !lastName || !email || !password || !dob) {
        alert('Please fill in all fields');
        return;
    }

    if (password !== confirmPassword) {
        alert('Passwords do not match');
        return;
    }

    if (!termsAccepted) {
        alert('You must accept the Terms of Service and Privacy Policy');
        return;
    }

    // Use the full URL to your Flask API
    const apiUrl = 'http://127.0.0.1:5000/api/auth/register';
    console.log('Submitting to:', apiUrl);

    fetch(apiUrl, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            first_name: firstName,
            last_name: lastName,
            email: email,
            password: password,
            dob: dob,
            terms_accepted: termsAccepted
        }),
        credentials: 'include' // Important for session cookies
    })
        .then(response => {
            console.log('Response status:', response.status);
            return response.json().catch(error => {
                console.error('Error parsing JSON:', error);
                return { error: 'Failed to parse server response' };
            });
        })
        .then(data => {
            console.log('Registration response:', data);
            if (data.error) {
                alert(data.error);
            } else if (data.errors) {
                let errorMessage = '';
                for (const [field, message] of Object.entries(data.errors)) {
                    errorMessage += `${field}: ${message}\n`;
                }
                alert('Registration failed:\n' + errorMessage);
            } else {
                alert('Account created successfully! Redirecting to login...');
                window.location.href = '{{url_for("login_page")}}';
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('An error occurred. Please try again.');
        });
});