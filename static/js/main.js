// Shared UI behaviors
document.addEventListener('DOMContentLoaded', function() {
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
