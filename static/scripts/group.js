"use strict";

// Variable outside to store the invitation code
var invitationCodeGenerated = null;

document.addEventListener('DOMContentLoaded', (event) => {

    // ... other code ...

    // Get all team boxes
    var teamBoxes = document.querySelectorAll('.team-box');

    // Add click event listener to each team box
    teamBoxes.forEach(function (box) {
        box.addEventListener('click', function () {
            // Redirect to the team's page
            var teamUrl = box.getAttribute('data-team-url');
            window.location.href = teamUrl;
        });
    });
    

    var modal = document.getElementById('inviteModal');
    var btn = document.getElementById('invite-btn');
    var span = document.getElementsByClassName('close-btn')[0];
    var invitationCodeInput = document.getElementById('invitationCode');

    // When the user clicks the button, open the modal and generate code if not already generated
    btn.onclick = function () {
        modal.style.display = 'block';
        if (!invitationCodeGenerated) {
            invitationCodeGenerated = Math.random().toString(36).substring(2, 10);
            invitationCodeInput.value = invitationCodeGenerated;
        }
    };

    // When the user clicks on <span> (x), close the modal
    span.onclick = function () {
        modal.style.display = 'none';
    };


    // Invite participants functionality
    const emailInput = document.getElementById("invite-email");
    const invitedParticipants = document.getElementById("invited-participants");
    const inviteSubmitBtn = document.querySelector(".invite-submit-btn");

    emailInput.addEventListener("keyup", function (event) {
        if (event.key === "Enter") {
            if (emailInput.value.trim()) {
                const emailDiv = document.createElement("div");
                emailDiv.innerText = emailInput.value;
                invitedParticipants.appendChild(emailDiv);
                emailInput.value = '';
            }
        }
    });

    inviteSubmitBtn.addEventListener("click", function () {
        const emails = [];
        for (let i = 0; i < invitedParticipants.children.length; i++) {
            emails.push(invitedParticipants.children[i].innerText);
        }
        console.log(emails);
        modal.style.display = "none";
    });



    // Get the People modal
    var peopleModal = document.getElementById('peopleModal');

    // Get the People button
    var peopleBtn = document.getElementById('people-btn');

    // Get the span element that closes the People modal
    var spanClosePeople = peopleModal.getElementsByClassName('close-btn')[0];

    // When the user clicks the People button, open the People modal
    peopleBtn.onclick = function () {
        peopleModal.style.display = 'block';
    };

    // When the user clicks on <span> (x), close the People modal
    spanClosePeople.onclick = function () {
        peopleModal.style.display = 'none';
    };


    // Function for searching emails
    window.searchEmails = function () {

        // Declare variables for input field, filter text, list of emails, individual email entries, and loop index
        var input, filter, emailList, emailEntries, i, emailText, txtValue;

        // Get the search input by its ID
        input = document.getElementById('searchEmail');
        // Get the search term and convert it to uppercase for case-insensitive comparison
        filter = input.value.toUpperCase();
        // Get the container that holds all email entries
        emailList = document.getElementById("emailList");
        // Get all email entry elements within the container
        emailEntries = emailList.getElementsByClassName('email-entry');

        // Loop through all email entries in the list
        for (i = 0; i < emailEntries.length; i++) {
            // For each entry, get the span element that contains the email text
            emailText = emailEntries[i].getElementsByClassName('email-text')[0];
            // Get the text content of the email span element
            txtValue = emailText.textContent || emailText.innerText;
            // Check if the email text contains the search term
            if (txtValue.toUpperCase().indexOf(filter) > -1) {
                // If the email text contains the search term, display the email entry
                emailEntries[i].style.display = "";
            } else {
                // If the email text does not contain the search term, hide the email entry
                emailEntries[i].style.display = "none";
            }
        }
    };

    // Add functionality for promote and demote buttons
    // This pseudocode needs to be linked to actual event handlers that perform the promotion/demotion
    /*
    var promoteButtons = document.getElementsByClassName('promotion-btn');
    var demoteButtons = document.getElementsByClassName('demotion-btn');
    // Loop through buttons and assign event handlers
    */

});
