document.addEventListener('DOMContentLoaded', function () {
    console.log("CONNECTED TO JS FILE");

    // Sign-in form handler
    const signinForm = document.getElementById('signin-form');
    if (signinForm) {
        signinForm.addEventListener('submit', function (event) {
            event.preventDefault();

            const email = document.getElementById('email').value;
            const password = document.getElementById('password').value;

            if (!email || !password) {
                alert('Please fill in all required fields');
                return;
            }

            alert('Signed in successfully!');
            window.location.href = "/";
        });
    }

    // Set DOB date constraints
    const dobInput = document.getElementById('dob');
    if (dobInput) {
        const today = new Date();
        const year = today.getFullYear();
        const month = String(today.getMonth() + 1).padStart(2, '0');
        const day = String(today.getDate()).padStart(2, '0');
        const maxDate = `${year}-${month}-${day}`;
        const minDate = `${year - 120}-${month}-${day}`;

        dobInput.setAttribute('max', maxDate);
        dobInput.setAttribute('min', minDate);
    }

    // Sign-up form handler
    const signupForm = document.getElementById('signup-form');
    if (signupForm) {
        signupForm.addEventListener('submit', function (event) {
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
                credentials: 'include'
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
                        window.location.href = '../static/login_page.html';
                    }
                })
                .catch(error => {
                    console.error('Error:', error);
                    alert('An error occurred. Please try again.');
                });
        });
    }
});
