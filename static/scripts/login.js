'use strict';

// Handle form submission
$('#loginForm').submit(function(event) {
    event.preventDefault(); // Prevent the form from submitting the default way (no args provided)

    const formData = {
        'email': $('input[name=email]').val(),
        'password': $('input[name=password]').val()
    };

    // Make an AJAX POST request to the backend
    $.ajax({
        type: 'POST',
        url: 'http://localhost:6969/login',
        data: formData,
        dataType: 'json',
        encode: true
    })
    .done(function(data) {
        if (data.status === 'success') {
            window.location.href = '/profile';  // Redirect to the profile page
        }
    })
    .fail(function(jqXHR, textStatus, errorThrown) {
        $('#error-message').text('An error occurred during the login process: ' + textStatus);
    });
});