
// Function to handle random password reset for users
function randomPasswordReset(userId) {
    if (confirm('Are you sure you want to reset this user\'s password to a random value?')) {
        fetch(`/dashboard/users/${userId}/reset-password`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': document.querySelector('meta[name="csrf-token"]').getAttribute('content')
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert(`Password has been reset to: ${data.password}`);
                location.reload();
            } else {
                alert('Failed to reset password');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('An error occurred while trying to reset the password');
        });
    }
}

// Function to handle random password reset for teachers
function randomTeacherPasswordReset(teacherId) {
    if (confirm('Are you sure you want to reset this teacher\'s password to a random value?')) {
        fetch(`/dashboard/teachers/${teacherId}/reset-password`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': document.querySelector('meta[name="csrf-token"]').getAttribute('content')
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert(`Password has been reset to: ${data.password}`);
                location.reload();
            } else {
                alert('Failed to reset password');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('An error occurred while trying to reset the password');
        });
    }
}

