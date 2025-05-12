// Variables to track current question and selections
let currentQuestion = 1;
const totalQuestions = 15;
const userSelections = {};

// Initialize when DOM is ready
document.addEventListener('DOMContentLoaded', function () {
    console.log('DOM loaded - initializing form');

    // Get DOM elements
    const prevBtn = document.getElementById('prev-btn');
    const nextBtn = document.getElementById('next-btn');
    const questions = document.querySelectorAll('.question');
    const progressDots = document.querySelectorAll('.progress-dot');
    const options = document.querySelectorAll('.option');
    const closeBtn = document.querySelector('.close-btn');

    // --------- Add click handlers to options ---------
    if (options && options.length > 0) {
        console.log('Found', options.length, 'options - adding click handlers');

        options.forEach(function (option) {
            // Use inline style to debug
            option.style.cursor = 'pointer';

            option.addEventListener('click', function (e) {
                console.log('Option clicked:', this.textContent.trim());

                // Get question number
                const questionNumber = parseInt(this.closest('.question').dataset.question);

                // Get the actual text content based on question type
                let value;
                if (questionNumber === 13) {
                    // For mood (question 13), extract only the main word from <strong> tag
                    const strongTag = this.querySelector('strong');
                    value = strongTag ? strongTag.textContent.trim() : this.textContent.trim();
                } else {
                    // For other questions, get the full description
                    const textSpan = this.querySelector('.text-gray-600');
                    value = textSpan ? textSpan.textContent.trim() : this.textContent.trim();
                }

                console.log('Option data: Question', questionNumber, 'Value', value);

                // Save selection with actual text
                userSelections[questionNumber] = value;

                // Store the original data-value for UI purposes
                userSelections[`${questionNumber}_dataValue`] = this.dataset.value;

                // Unselect all options in this question
                const parentQuestion = this.closest('.question');
                parentQuestion.querySelectorAll('.option').forEach(function (opt) {
                    // Remove any inline styles 
                    opt.classList.remove('selected');
                    opt.style.backgroundColor = '';
                    opt.style.borderLeft = '';
                    opt.style.fontWeight = '';
                });

                // Apply styling directly to this option
                this.classList.add('selected');
                this.style.backgroundColor = '#f3f4f6';
                this.style.borderLeft = '4px solid #FA3980';
                this.style.fontWeight = 'bold';

                console.log('Option marked as selected');

                // If this is the last question, change Next to Submit
                if (currentQuestion === totalQuestions) {
                    nextBtn.textContent = 'Submit';
                }
            });
        });
    } else {
        console.error('No options found on the page!');
    }

    // --------- Add event listeners for text inputs ---------
    const textInputs = document.querySelectorAll('.text-input');
    if (textInputs && textInputs.length > 0) {
        console.log('Found', textInputs.length, 'text inputs - adding input handlers');

        textInputs.forEach(function (input) {
            input.addEventListener('input', function () {
                const questionNumber = parseInt(this.closest('.question').dataset.question);
                userSelections[questionNumber] = this.value;
                console.log('Text input updated for question', questionNumber);
            });
        });
    }

    // --------- Money spent input validation ---------
    const moneySpentInput = document.getElementById('money-spent');
    if (moneySpentInput) {
        // Simple input handler
        moneySpentInput.addEventListener('input', function (e) {
            // Get current value
            let value = this.value;

            // Remove any non-numeric characters except decimal point
            value = value.replace(/[^\d.]/g, '');

            // Split by decimal point
            let parts = value.split('.');

            // Only allow one decimal point
            if (parts.length > 2) {
                value = parts[0] + '.' + parts.slice(1).join('');
            }

            // Limit to 2 decimal places
            if (parts[1] && parts[1].length > 2) {
                value = parts[0] + '.' + parts[1].substr(0, 2);
            }

            // Update the input
            this.value = value;

            // Save to userSelections for form submission
            const questionNumber = 15;
            userSelections[questionNumber] = value;
        });

        // Format to 2 decimal places when user leaves the field
        moneySpentInput.addEventListener('blur', function () {
            let value = this.value;

            // Only format if there's a value
            if (value && value !== '.') {
                const numValue = parseFloat(value);
                if (!isNaN(numValue)) {
                    // Format to exactly 2 decimal places
                    this.value = numValue.toFixed(2);
                    userSelections[15] = this.value;
                }
            }
        });

        // Prevent invalid characters on key press
        moneySpentInput.addEventListener('keypress', function (e) {
            const charCode = e.which ? e.which : e.keyCode;

            // Allow: backspace, delete, tab, escape, enter
            if ([8, 9, 27, 13, 46].indexOf(charCode) !== -1 ||
                // Allow: Ctrl+A
                (charCode === 65 && e.ctrlKey === true) ||
                // Allow: home, end, left, right
                (charCode >= 35 && charCode <= 39)) {
                return;
            }

            // Ensure that it is a number or decimal point
            if (charCode !== 46 && (charCode < 48 || charCode > 57)) {
                e.preventDefault();
                return;
            }

            // Only allow one decimal point
            if (charCode === 46 && this.value.indexOf('.') !== -1) {
                e.preventDefault();
            }
        });
    }

    // --------- Next button ---------
    if (nextBtn) {
        nextBtn.addEventListener('click', function () {
            console.log('Next button clicked');

            if (currentQuestion === totalQuestions) {
                // This is the submit action
                submitForm();
            } else {
                // Move to next question
                moveToQuestion(currentQuestion + 1);
            }
        });
    } else {
        console.error('Next button not found!');
    }

    // --------- Previous button ---------
    if (prevBtn) {
        prevBtn.addEventListener('click', function () {
            console.log('Previous button clicked');

            if (currentQuestion > 1) {
                moveToQuestion(currentQuestion - 1);
            }
        });
    } else {
        console.error('Previous button not found!');
    }

    // --------- Close button ---------
    if (closeBtn) {
        closeBtn.addEventListener('click', function () {
            console.log('Close button clicked');

            if (confirm('Are you sure you want to exit? Your progress will be lost.')) {
                const introductoryUrl = document.getElementById('app-data').dataset.introductoryUrl;
                window.location.href = introductoryUrl;
            }
        });
    }

    // --------- Date picker setup ---------
    const dateInput = document.getElementById('survey-date');
    if (dateInput) {
        console.log('Initializing date picker');

        // Get today's date in local timezone
        const today = new Date();
        const year = today.getFullYear();
        const month = String(today.getMonth() + 1).padStart(2, '0');
        const day = String(today.getDate()).padStart(2, '0');
        const todayString = `${year}-${month}-${day}`;

        console.log('Today date string:', todayString); // Debug log

        // Set default value and max date
        dateInput.value = todayString;
        dateInput.setAttribute('max', todayString);

        // Add change listener
        dateInput.addEventListener('change', function () {
            console.log('Date changed to:', this.value);

            // Parse dates in local timezone to avoid timezone issues
            const selectedDateParts = this.value.split('-');
            const selectedDate = new Date(
                parseInt(selectedDateParts[0]),
                parseInt(selectedDateParts[1]) - 1,
                parseInt(selectedDateParts[2])
            );

            const currentDate = new Date();
            currentDate.setHours(0, 0, 0, 0); // Reset time for accurate comparison
            selectedDate.setHours(0, 0, 0, 0); // Reset time for accurate comparison

            console.log('Selected date:', selectedDate);
            console.log('Current date:', currentDate);

            if (selectedDate > currentDate) {
                alert("You cannot select future dates. Please select today or a past date.");
                this.value = todayString;
            } else {
                checkExistingData(this.value);
            }
        });

        // Also add an input event listener to handle manual typing
        dateInput.addEventListener('input', function () {
            console.log('Date input changed manually to:', this.value);
            // The change event will handle validation
        });

        // Check for existing data on page load
        checkExistingData(dateInput.value);
    } else {
        console.error('Date input not found!');
    }

    // Set initial button state
    updateButtonState();

    // Set initial progress indicator
    updateProgressIndicator();

    console.log('Form initialization complete');
});

// Move to a specific question
function moveToQuestion(questionNumber) {
    console.log('Moving to question', questionNumber);

    // Hide current question
    document.querySelector(`.question[data-question="${currentQuestion}"]`).style.display = 'none';

    // Show new question
    document.querySelector(`.question[data-question="${questionNumber}"]`).style.display = 'block';

    // Update current question
    currentQuestion = questionNumber;

    // Update progress indicator
    updateProgressIndicator();

    // Update button state
    updateButtonState();
}

// Update progress indicator
function updateProgressIndicator() {
    // First reset all dots to gray
    document.querySelectorAll('[data-question]').forEach(dot => {
        dot.classList.remove('bg-pink-500');
        dot.classList.add('bg-white');
    });

    // Set the current question dot to pink
    const currentDot = document.querySelector(`[data-question="${currentQuestion}"]`);
    if (currentDot) {
        currentDot.classList.remove('bg-white');
        currentDot.classList.add('bg-pink-500');
    }

    // Mark previous questions as completed (optional)
    for (let i = 1; i < currentQuestion; i++) {
        const completedDot = document.querySelector(`[data-question="${i}"]`);
        if (completedDot && userSelections[i]) {
            completedDot.classList.remove('bg-white');
            completedDot.classList.add('bg-green-300');
        }
    }
}

// Update button state
function updateButtonState() {
    const prevBtn = document.getElementById('prev-btn');
    const nextBtn = document.getElementById('next-btn');

    // Disable Previous button on first question
    if (currentQuestion === 1) {
        prevBtn.disabled = true;
        prevBtn.classList.add('opacity-50', 'cursor-not-allowed');
    } else {
        prevBtn.disabled = false;
        prevBtn.classList.remove('opacity-50', 'cursor-not-allowed');
    }

    // Change Next to Submit on last question
    if (currentQuestion === totalQuestions) {
        nextBtn.textContent = 'Submit';
        // Keep the pink color for Submit
    } else {
        nextBtn.textContent = 'Next';
    }

    // Ensure button styling is correct
    prevBtn.style.backgroundColor = prevBtn.disabled ? '#E5E7EB' : 'white';
    nextBtn.style.backgroundColor = '#FA3980';
}

// Process form submission
function submitForm() {
    console.log('Submitting form');

    // Check if all questions have been answered
    let allAnswered = true;

    for (let i = 1; i <= totalQuestions; i++) {
        if (userSelections[i] === undefined || userSelections[i] === '') {
            allAnswered = false;
            alert(`Please answer question ${i} before submitting.`);
            moveToQuestion(i);
            return;
        }
    }

    if (allAnswered) {
        // Get the selected date
        const dateInput = document.getElementById('survey-date');
        const selectedDate = dateInput ? dateInput.value : new Date().toISOString().split('T')[0];

        // Prepare form data - only send the actual text values, not the data-value helpers
        const formData = {
            date: selectedDate
        };

        // Add only the actual question responses (exclude the helper data-value entries)
        for (let i = 1; i <= totalQuestions; i++) {
            if (userSelections[i] !== undefined) {
                formData[i] = userSelections[i];
            }
        }

        // Get URL and CSRF token from the data-attributes
        const appData = document.getElementById('app-data').dataset;
        const submitUrl = appData.submitUrl;
        const csrfToken = appData.csrfToken;
        const introductoryUrl = appData.introductoryUrl;

        console.log('Sending data to server:', formData);

        // Send data to server via fetch API
        fetch(submitUrl, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken
            },
            body: JSON.stringify(formData)
        })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    // Show success message
                    alert('Thank you for submitting your data!');
                    // Redirect to introduction page
                    window.location.href = introductoryUrl;
                } else {
                    // Show error message
                    alert('Error: ' + (data.message || 'Something went wrong.'));
                }
            })
            .catch(error => {
                console.error('Error:', error);
                alert('An error occurred while submitting your data.');
            });
    }
}

// Function to check if data exists for a date
function checkExistingData(date) {
    console.log('Checking for existing data on', date);

    fetch(`/check-survey-data?date=${date}`)
        .then(response => response.json())
        .then(data => {
            if (data.exists) {
                console.log('Found existing data for', date);

                // Populate form with existing data
                for (let i = 1; i <= totalQuestions; i++) {
                    if (data.survey[i] !== null) {
                        userSelections[i] = data.survey[i].toString();
                    }
                }

                // Update the UI to reflect loaded data
                updateSelectedOptions();
                updateTextInputs();
            } else {
                console.log('No existing data for', date);

                // Reset form for new entry
                resetForm();
            }
        })
        .catch(error => {
            console.error('Error checking existing data:', error);
        });
}

// Function to update the UI for selected options
function updateSelectedOptions() {
    console.log('Updating selected options in UI');

    // First, deselect all options
    document.querySelectorAll('.option').forEach(option => {
        option.classList.remove('selected');
        option.style.backgroundColor = '';
        option.style.borderLeft = '';
        option.style.fontWeight = '';
    });

    // Then mark selected options based on userSelections
    for (const questionNum in userSelections) {
        if (parseInt(questionNum) <= 13 && userSelections[questionNum]) { // Up to question 13 are now multiple choice
            const selectedText = userSelections[questionNum];
            const question = document.querySelector(`.question[data-question="${questionNum}"]`);

            if (question) {
                // Find the option that contains this text
                const options = question.querySelectorAll('.option');
                options.forEach(option => {
                    let optionText;

                    // For mood (question 13), compare with the strong tag text
                    if (parseInt(questionNum) === 13) {
                        const strongTag = option.querySelector('strong');
                        optionText = strongTag ? strongTag.textContent.trim() : '';
                    } else {
                        // For other questions, use the description text
                        const textSpan = option.querySelector('.text-gray-600');
                        optionText = textSpan ? textSpan.textContent.trim() : option.textContent.trim();
                    }

                    if (optionText === selectedText || optionText.includes(selectedText)) {
                        option.classList.add('selected');
                        option.style.backgroundColor = '#f3f4f6';
                        option.style.borderLeft = '4px solid #FA3980';
                        option.style.fontWeight = 'bold';
                        console.log('Marked option selected for question', questionNum);
                    }
                });
            }
        }
    }
}

// Function to update text inputs with loaded data
function updateTextInputs() {
    console.log('Updating text inputs with loaded data');

    // Update wake-up time
    const wakeUpInput = document.getElementById('wake-up-time');
    if (wakeUpInput && userSelections[11]) {
        wakeUpInput.value = userSelections[11];
    }

    // Update transportation
    const transportationInput = document.getElementById('transportation');
    if (transportationInput && userSelections[12]) {
        transportationInput.value = userSelections[12];
    }

    // Update bed time
    const bedTimeInput = document.getElementById('bed-time');
    if (bedTimeInput && userSelections[14]) {
        bedTimeInput.value = userSelections[14];
    }

    // Update money spent
    const moneySpent = document.getElementById('money-spent');
    if (moneySpent && userSelections[15]) {
        moneySpent.value = userSelections[15];
    }
}

// Function to reset the form
function resetForm() {
    console.log('Resetting form');

    // Clear userSelections
    for (let i = 1; i <= totalQuestions; i++) {
        delete userSelections[i];
        delete userSelections[`${i}_dataValue`]; // Also clear the data-value helpers
    }

    // Deselect all options
    document.querySelectorAll('.option').forEach(option => {
        option.classList.remove('selected');
        option.style.backgroundColor = '';
        option.style.borderLeft = '';
        option.style.fontWeight = '';
    });

    // Clear all text inputs
    document.querySelectorAll('.text-input').forEach(input => {
        input.value = '';
    });
}