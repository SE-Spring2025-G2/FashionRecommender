document.addEventListener('DOMContentLoaded', function() {
    var anonCheckbox = document.getElementById('anon');
    var nameField = document.getElementById('feedback_name');

    anonCheckbox.addEventListener('change', function() {
        if (anonCheckbox.checked) {
            nameField.value = '';
            nameField.disabled = true;
            nameField.required = false;
        } else {
            nameField.disabled = false;
            nameField.required = true;
        }
    });
});