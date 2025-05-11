// Variables to track current question and selections
let currentQuestion = 1;
const totalQuestions = 15;
const userSelections = {};

// Initialize when DOM is ready
document.addEventListener('DOMContentLoaded', function() {
    console.log('DOM loaded - initializing form');
    
    // Get DOM elements
    const prevBtn = document.getElementById('prev-btn');
    const nextBtn = document.getElementById('next-btn');
    const questions = document.querySelectorAll('.question');
    const progressDots = document.querySelectorAll('.progress-dot');
    const options = document.querySelectorAll('.option');
    const closeBtn = document.querySelector('.close-btn');
    
    // Force the styles in case they're not being picked up from CSS
    if (prevBtn) {
        prevBtn.style.backgroundColor = 'white';
        prevBtn.style.color = '#4B5563';
        prevBtn.style.border = '1px solid #E5E7EB';
        prevBtn.style.boxShadow = '0 1px 3px rgba(0, 0, 0, 0.1)';
    }
    
    if (nextBtn) {
        nextBtn.style.backgroundColor = '#FA3980';
        nextBtn.style.color = 'white';
        nextBtn.style.boxShadow = '0 1px 3px rgba(0, 0, 0, 0.1)';
    }
    
    // --------- Add click handlers to options ---------
    if (options && options.length > 0) {
        console.log('Found', options.length, 'options - adding click handlers');
        
        options.forEach(function(option) {
            // Use inline style to debug
            option.style.cursor = 'pointer';
            
            option.addEventListener('click', function(e) {
                console.log('Option clicked:', this.textContent.trim());
                
                // Get question number and value
                const questionNumber = parseInt(this.closest('.question').dataset.question);
                const value = this.dataset.value;
                console.log('Option data: Question', questionNumber, 'Value', value);
                
                // Save selection
                userSelections[questionNumber] = value;
                
                // Unselect all options in this question
                const parentQuestion = this.closest('.question');
                parentQuestion.querySelectorAll('.option').forEach(function(opt) {
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
        
        textInputs.forEach(function(input) {
            input.addEventListener('input', function() {
                const questionNumber = parseInt(this.closest('.question').dataset.question);
                userSelections[questionNumber] = this.value;
                console.log('Text input updated for question', questionNumber);
            });
        });
    }
    
    // --------- Next button ---------
    if (nextBtn) {
        nextBtn.addEventListener('click', function() {
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
        prevBtn.addEventListener('click', function() {
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
        closeBtn.addEventListener('click', function() {
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
        
        // Set default date to today
        const today = new Date().toISOString().split('T')[0];
        dateInput.value = today;
        
        // Set max date to today to prevent future date selection
        dateInput.setAttribute('max', today);
        
        // Add change listener
        dateInput.addEventListener('change', function() {
            console.log('Date changed:', this.value);
            
            // Validate the selected date isn't in the future
            const selectedDate = new Date(this.value);
            const currentDate = new Date();
            
            // Reset time for accurate comparison
            selectedDate.setHours(0, 0, 0, 0);
            currentDate.setHours(0, 0, 0, 0);
            
            if (selectedDate > currentDate) {
                alert("You cannot select future dates. Please select today or a past date.");
                this.value = today;
            } else {
                checkExistingData(this.value);
            }
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

        // Add date to the data being sent
        const formData = {
            ...userSelections,
            date: selectedDate
        };

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
        if (parseInt(questionNum) <= 10) { // Only for multiple choice questions
            const selectedValue = userSelections[questionNum];
            const question = document.querySelector(`.question[data-question="${questionNum}"]`);

            if (question) {
                const option = question.querySelector(`.option[data-value="${selectedValue}"]`);
                if (option) {
                    option.classList.add('selected');
                    option.style.backgroundColor = '#f3f4f6';
                    option.style.borderLeft = '4px solid #FA3980';
                    option.style.fontWeight = 'bold';
                    console.log('Marked option selected for question', questionNum);
                }
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

    // Update mood
    const moodInput = document.getElementById('mood');
    if (moodInput && userSelections[13]) {
        moodInput.value = userSelections[13];
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