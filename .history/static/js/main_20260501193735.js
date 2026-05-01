// Professional Confirmation Popups using SweetAlert2
function confirmRegistration(event, url) {
    event.preventDefault();
    Swal.fire({
        title: 'Confirm Registration',
        text: 'Are you sure you want to register for this event?',
        icon: 'question',
        showCancelButton: true,
        confirmButtonColor: '#1a365d',
        cancelButtonColor: '#718096',
        confirmButtonText: 'Yes, Register Now',
        background: '#f7fafc',
        borderRadius: '15px'
    }).then((result) => {
        if (result.isConfirmed) {
            window.location.href = url;
        }
    });
}

function confirmAction(event, title, message, confirmText, color = '#1a365d') {
    event.preventDefault();
    const form = event.target;
    Swal.fire({
        title: title,
        text: message,
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: color,
        cancelButtonColor: '#718096',
        confirmButtonText: confirmText,
        background: '#f7fafc',
        borderRadius: '15px'
    }).then((result) => {
        if (result.isConfirmed) {
            form.submit();
        }
    });
}
