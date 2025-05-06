// document.addEventListener('DOMContentLoaded', function () {
//     // Define the confirmRemove function
//     function confirmRemove(friendId) {
//         // Show the confirmation modal
//         document.getElementById('confirm-modal').classList.remove('hidden');

//         // Handle the confirmation action
//         document.getElementById('confirm-remove-btn').onclick = function() {
//             // Set the form action to the correct URL with the friend ID
//             var form = document.getElementById('remove-friend-form-' + friendId);
//             form.action = '/friend/remove/' + friendId; // Ensure the correct URL

//             // Submit the form (this sends the POST request)
//             form.submit();
//         };

//         // Close the modal if cancel is clicked
//         document.getElementById('cancel-remove-btn').onclick = function() {
//             document.getElementById('confirm-modal').classList.add('hidden');
//         };
//     }

//     // Expose the confirmRemove function globally
//     window.confirmRemove = confirmRemove;
// });
