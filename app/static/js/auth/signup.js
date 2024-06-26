'use strict';

// Handle form submission
$('#signup-form').submit(function(event) {
    event.preventDefault(); // Prevent the form from submitting the default way

    const formData = {
        'email': $('input[name=email]').val(),
        'username': $('input[name=username]').val(),
        'password': $('input[name=password]').val()
    };

    // Make an AJAX POST request to the backend
    $.ajax({
        type: 'POST',
        url: './signup',
        data: formData,
        dataType: 'json',
        encode: true
    })
    .done(function(data) {
        if (data.status === 'success') {
            window.location.href = './login';  // Redirect to the login page
        }
    })
    .fail(function(jqXHR, textStatus, errorThrown) {
        $('#error-message').text('An error occurred during the signup process: ' + textStatus);
    });
});