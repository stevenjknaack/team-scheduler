"use strict";

/**
 * Global variable to store the generated invitation code.
 * @type {string|null}
 */
var invitationCodeGenerated = null;

document.addEventListener('DOMContentLoaded', (event) => {


    /**
     * Functionality: Team box click
     * Attaches click event listeners to all elements with class 'team-box'.
     * On click, redirects to the team's page based on the data attribute 'data-team-url'.
     */
    var teamBoxes = document.querySelectorAll('.team-box');
    teamBoxes.forEach(function (box) {
        box.addEventListener('click', function () {
            var teamUrl = box.getAttribute('data-team-url');
            console.log('this is url', teamUrl)
            window.location.href = teamUrl;
        });
    });

    /**
     * Functionality: Inivte Button click
     * Handle 1: closing modal when click (x) or "esc" button
     * Handle 2: generating a unique invitation code for each group
     * Handle 3: inserting email inputs
     * Handle 4: sending emails functionality 
     */

    var inviteModal = document.getElementById('inviteModal');
    var btn = document.getElementById('invite-btn');
    var span = document.getElementsByClassName('close')[0];
    var invitationCodeInput = document.getElementById('invitationCode');

    /**
     * Handle 1
     * Closes the invite modal when the close button (span) is clicked.
     */
    span.onclick = function () {
        inviteModal.style.display = 'none';
    };

    /**
     * Handle 1
     * Closes the invite modal when the Escape key is pressed, provided the modal is currently displayed.
     * @param {object} event - an KeyBoardEvent
     */
    document.addEventListener('keydown', function (event) {
        // Check if the key pressed is the Escape key and if the modal is displayed
        if (event.key === 'Escape' && inviteModal.style.display === 'block') {
            inviteModal.style.display = 'none';
        }
    });

    /**
     * Handle 2
     * Opens the inviteModal and sets the invitation code as the group ID for the specific group the user has navigated to
     * 
     * @author Kyle
     */
    btn.onclick = function () {
        // display the inviteModal
        inviteModal.style.display = 'block';

        // get current URL
        var currentURL = window.location.href;

        // extract the group ID from the URL using regex
        var match = currentURL.match(/\/groups\/(\d+)/);

        // check if a match is found
        if (match) {
            var groupId = match[1];
            invitationCodeInput.value = groupId; // set value of invitation code to extracted group ID
        } else {
            console.error('Group ID not found in the URL');
        }
    };

    // Inviting participants
    const emailInput = document.getElementById("invite-email");
    const invitedParticipants = document.getElementById("invited-participants");
    const inviteSubmitBtn = document.querySelector(".invite-submit-btn");

    /**
     * Handle 3
     * Allows adding participant emails by pressing the Enter key.
     * Appends entered emails to the 'invited-participants' element.
     * @param {object} event - an KeyBoardEvent
     */
    if (emailInput) {
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
    }

    /**
     * Handle 4
     * Gathers and logs the emails of all invited participants when the submit button is clicked.
     * Closes the invite modal afterwards.
     * 
     * @author Kyle
     */
    if (inviteSubmitBtn) {
        inviteSubmitBtn.addEventListener("click", function () {
            const emails = [];
            for (let i = 0; i < invitedParticipants.children.length; i++) {
                emails.push(invitedParticipants.children[i].innerText);
            }

            var currentUrl = window.location.href;
            var eventId = this.getAttribute("data-event-id");
            console.log("EVENT ID: " + eventId);
            var groupId = currentUrl.match(/\/groups\/(\d+)/);
            console.log("GROUP ID: " + groupId[1]);

            // make HTTP request to the Flask backend
            fetch(`../groups/send-invitations/${groupId[1]}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ emails: emails }),
            })
                .then(response => response.json())
                .then(data => {
                    console.log(data); // return JSON response
                })
                .catch(error => {
                    console.error('Error: ', error); // if error, print out error
                });
            // console.log(emails);
            inviteModal.style.display = "none"; // close the invite modal
        });
    }


    /**
     * Functionality: People modal 
     * Handle 1: opening the modal when people button clicked
     * Handle 2: closing modal when click (x) or "esc" button
     * Handle 3: search function
     * Handle 4: TODO promote and demote functionality
     */


    // People modal handling
    var peopleModal = document.getElementById('peopleModal');
    var peopleBtn = document.getElementById('people-btn');
    var spanClosePeople = peopleModal.getElementsByClassName('close')[0];

    /**
     * Handle 1
     * Opens the people modal when the 'people-btn' is clicked.
     */
    peopleBtn.onclick = function () {
        peopleModal.style.display = 'block';
    };

    /**
     * Handle 2
     * Closes the people modal when the close button (span) is clicked.
     */
    spanClosePeople.onclick = function () {
        peopleModal.style.display = 'none';
    };

    /**
     * Handle 2
     * Closes the people modal when the Escape key is pressed
     * @param {object} event - an KeyBoardEvent
     */
    document.addEventListener('keydown', function (event) {
        // Check if the key pressed is the Escape key and if the modal is displayed
        if (event.key === 'Escape' && peopleModal.style.display === 'block') {
            peopleModal.style.display = 'none';
        }
    });

    /**
     * Handle 3
     * Filters and displays email entries in 'emailList' that match the search criteria entered in 'searchEmail'.
     * Performs a case-insensitive search.
     */
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
    // Creates Modal for creating event button
    $("#createEventButton").click(function () {
        $("#createEventModal").css("display", "block");
    });

    // Close create event modal
    $(".close").click(function () {
        $("#createEventModal").css("display", "none");
    });

    // Close create event modal if clicked outside the modal
    window.onclick = function (event) {
        if (event.target === $("#createEventModal")[0]) {
            $("#createEventModal").css("display", "none");
        }
    };

    document.querySelectorAll(".delete-event-btn").forEach(function (btn) {
        btn.addEventListener("click", function () {
            console.log("button clicked")
            var eventId = this.getAttribute("data-event-id");
            delete_event(eventId);
        });
    });
    // Function to delete an event
    function delete_event(eventId) { // TODO THIS IS SO FUCKING BROKEN BRO
        // Extract the group ID from the current URL
        var currentUrl = window.location.href;
        // Extract from the url 'group/id' (localhost:6969/group/id)
        var groupIdMatch = currentUrl.match(/\/groups\/(\d+)/);
        // Make sure that there is an element there and that there is an id element
        let groupId = null;
        if (groupIdMatch && groupIdMatch[1]) {
            groupId = groupIdMatch[1];
            // Redirect to create-event with the extracted group ID
        }
        // Send a request to the server to delete the event
        fetch(`../events/delete-event/${eventId}/${groupId}`, {
            method: "DELETE",
        })
            .then(function (response) {
                if (response.ok) {
                    // Reload the page to reflect the changes
                    location.reload();
                } else {
                    console.log("Failed to delete the event.");
                }
            })
            .catch(function (error) {
                console.error("Error:", error);
            });
    }
    
    
    var createTeamButton = document.getElementById('createTeamButton');
    var createTeamOptions = document.getElementById('createTeamOptions');
    var partitionTeamButton = document.getElementById('partitionTeamButton');
    var manualCreateTeamButton = document.getElementById('manualCreateTeamButton');
    if (createTeamButton && createTeamOptions && partitionTeamButton && manualCreateTeamButton) {
    createTeamButton.addEventListener('click', function(event) {
        // Toggle the dropdown display
        createTeamOptions.style.display = createTeamOptions.style.display === 'block' ? 'none' : 'block';
        event.stopPropagation(); // Prevent the click from propagating to the window
    });

    partitionTeamButton.addEventListener('click', function() {
        var currentUrl = window.location.href;
        var groupIdMatch = currentUrl.match(/\/groups\/(\d+)/);

        if (groupIdMatch && groupIdMatch[1]) {
            var groupId = groupIdMatch[1];
            window.location.href = '../teams/partition_team_page?group_id=' + groupId;
        } else {
            console.error('Group ID not found in the URL');
        }
        createTeamOptions.style.display = 'none'; // Hide the options
    });

    manualCreateTeamButton.addEventListener('click', function() {
        var currentUrl = window.location.href;
        var groupIdMatch = currentUrl.match(/\/groups\/(\d+)/);

        if (groupIdMatch && groupIdMatch[1]) {
            var groupId = groupIdMatch[1];
            window.location.href = '../teams/manual_create_team_page?group_id=' + groupId;
        } else {
            console.error('Group ID not found in the URL');
        }
        createTeamOptions.style.display = 'none'; // Hide the options
    });

    // Optional: Hide the dropdown if clicked outside
    window.addEventListener('click', function(event) {
        if (event.target !== createTeamButton && event.target !== createTeamOptions) {
            createTeamOptions.style.display = 'none';
        }
    });
}

    // TODO: Add functionality for promote and demote buttons
    /*
        var promoteButtons = document.getElementsByClassName('promotion-btn');
        var demoteButtons = document.getElementsByClassName('demotion-btn');
        // Loop through buttons and assign event handlers
    */

});
