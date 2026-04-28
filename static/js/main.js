// Shared UI behaviors
document.addEventListener('DOMContentLoaded', function() {
    // Auto-dismiss alerts after 5 seconds
    const alerts = document.querySelectorAll('.alert-dismissible');
    alerts.forEach(function(alert) {
        setTimeout(function() {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }, 5000);
    });

    // Material Design input focus effects
    const inputs = document.querySelectorAll('.input-group-static .form-control, .input-group-outline .form-control');
    inputs.forEach(function(input) {
        input.addEventListener('focus', function() {
            this.parentElement.classList.add('is-focused');
        });
        input.addEventListener('blur', function() {
            this.parentElement.classList.remove('is-focused');
        });
    });
});
