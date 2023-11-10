'use strict';
document.getElementById("createEvent").addEventListener("click", function() {
    window.location.href = window.eventCreateUrl; 
});
3
// Toggle the logout form
$(document).ready(function () {
    $("#welcomeButton").on("click", function () {
        $("#logoutForm").toggle();
    });
});

// Invite pop up modal functionality
var modal = document.getElementById("inviteModal");
var btns = document.getElementsByClassName("invite-btn");
var span = document.getElementsByClassName("close-btn")[0];

for(let i = 0; i < btns.length; i++) {
    btns[i].onclick = function() {
        modal.style.display = "block";
        invitedParticipants.innerHTML = '';
    }
}

span.onclick = function() {
    modal.style.display = "none";
}

window.onclick = function(event) {
    if (event.target == modal) {
        modal.style.display = "none";
    }
}

// Edit pop up modal functionality
var editEventModal = document.getElementById("editEventModal");
var editBtn = document.getElementsByClassName("edit-btn");
var editClose = document.getElementsByClassName("edit-close-btn")[0];

for(let i = 0; i < editBtn.length; i++) {
    editBtn[i].onclick = function() {
        editEventModal.style.display = "block";
    }
}

editClose.onclick = function() {
    editEventModal.style.display = "none";
}

window.onclick = function(event) {
    if (event.target == editEventModal) {
        editEventModal.style.display = "none";
    }
}

// Invite participants functionality
const emailInput = document.getElementById("invite-email");
const invitedParticipants = document.getElementById("invited-participants");
const inviteSubmitBtn = document.querySelector(".invite-submit-btn");

emailInput.addEventListener("keyup", function(event) {
    if (event.key === "Enter") {
        if (emailInput.value.trim()) {
            const emailDiv = document.createElement("div");
            emailDiv.innerText = emailInput.value;
            invitedParticipants.appendChild(emailDiv);
            emailInput.value = ''; 
        }
    }
});

inviteSubmitBtn.addEventListener("click", function() {
    const emailsArray = [];
    for (let i = 0; i < invitedParticipants.children.length; i++) {
        emailsArray.push(invitedParticipants.children[i].innerText);
    }
    console.log(emailsArray);
    modal.style.display = "none";
    // ... existing code to get the list of emails ...

    // Convert the array of emails to JSON
    const payload = {
        emails: emailsArray
    };

    // Sending a POST request using fetch API
    fetch("/send-invitations", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(payload)
    })
    .then(response => response.json())
    .then(data => {
        console.log(data);  // This will print the response from the backend
        // You can also add some feedback to the user, such as an alert or a message.
        alert("Invitations sent successfully!");
    })
    .catch(error => {
        console.error("There was an error sending the invitations:", error);
        alert("Failed to send invitations.");
    });
});

// Event listener for the delete button
document.querySelectorAll(".delete-btn").forEach(function(btn) {
    btn.addEventListener("click", function() {
        var eventId = this.getAttribute("data-eventid");
        deleteEvent(eventId);
    });
});

// Function to delete an event
function deleteEvent(eventId) {
    // Send a request to the server to delete the event
    fetch("/delete-event/" + eventId, {
        method: "DELETE",
    })
        .then(function(response) {
            if (response.ok) {
                // Reload the page to reflect the changes
                location.reload();
            } else {
                console.log("Failed to delete the event.");
            }
        })
        .catch(function(error) {
            console.error("Error:", error);
        });
}

/**
 * Event listener for the edit button.
 *
 * This function adds a click event listener to all elements with the class "edit-btn."
 * When the edit button is clicked, it retrieves the event details from the associated data-eventid attribute,
 * fetches the event details, and populates the edit form modal fields with the event data for users to view.
 * If the event details are successfully fetched, it displays the edit event modal; otherwise, it logs an error message.
 *
 * @param {MouseEvent} event - The click event object.
 * @author Kyle Sung
 */
document.querySelectorAll(".edit-btn").forEach(function (btn) {
    btn.addEventListener("click", function () {
        // Get the event details from the current saved event
        var eventId = this.getAttribute("data-eventid");

        // Fetch the event details and handle it when the promise resolves
        getEventDetails(eventId).then(function (event) {
            if (event) {
                console.log("This is the event printed: ", event);

                // Populate edit form modal fields with the saved event details
                document.getElementById("editEventName").value = event.event_name;
                document.getElementById("editStartDate").value = event.start_date;
                document.getElementById("editEndDate").value = event.end_date;
                document.getElementById("editEventDescription").value = event.event_description;

                // Display the edit event modal
                document.getElementById("editEventModal").style.display = "block";
            } else {
                console.log("Failed to fetch event details.");
            }
        });
    });
});

/**
 * Function to call API and get the saved event details from database when editing.
 *
 * This function makes a request to the server to fetch event details based on the provided `eventId`,
 * returning the details as an object in the form of a Promise.
 *
 * @param {string} eventId - The unique identifier of the event to be fetched.
 * @returns {Promise<Object|null>} A Promise that resolves with the event details as an object when the request is successful,
 * or with `null` if there is an error or the request fails.
 *
 * @throws {Error} An error may be thrown if there are network or other issues during the request.
 * 
 * @author Kyle Sung
 */
function getEventDetails(eventId) {
    // Make request to server to fetch event details based on eventId, return details as an object as a promise
    return fetch("/get-event/" + eventId, {
        method: "GET", 
    })
        .then(function(response) {
            if (response.ok) {
                // Parse response as JSON and return event details
                return response.json();
            } else {
                // Error handling
                console.log("Failed to fetch event details.");
                return null;
            }
        })
        // Error handling
        .catch(function(error) {
            console.error("Error:", error);
            return null;
        });
}

/**
 * Event listener for saving event changes.
 *
 * This function adds a click event listener to the element with the ID "saveEventChanges."
 * When the save button is clicked, it retrieves the edited event details from the Edit Event Modal form
 * and prepares an object with the edited event information to make a PUT request using saveEventChanges function.
 * Lastly, it hides the Edit Event Modal form when the save event changes button is clicked.
 *
 * @param {MouseEvent} event - The click event object.
 * @author Kyle Sung
 */
document.getElementById("saveEventChanges").addEventListener("click", function() {

    let eventId = editBtn.getAttribute("data-eventid");

    // Get the edited event details from the Edit Event Modal form
    let editedEvent = {
        name: document.getElementById("editEventName").value,
        startDate: document.getElementById("editStartDate").value,
        endDate: document.getElementById("editEndDate").value,
        description: document.getElementById("editEventDescription").value
    };

    // Save the changes to the event
    saveEventChanges(eventId, editedEvent);

    console.log("I am being clicked!"); // debug comment

    // Close the Edit Event Modal form
    document.getElementById("editEventModal").style.display = "none";
});

/**
 * Function to save event changes.
 *
 * This function sends a PUT request to the server to save the changes made to an event with the specified `eventId`.
 * The edited event details are provided in the `editedEvent` object and sent as JSON in the request body.
 * The function handles the response from the server and logs success or error messages accordingly.
 *
 * @param {string} eventId - The unique identifier of the event to be updated.
 * @param {Object} editedEvent - An object containing the edited event details.
 * @return {void}
 *
 * @throws {Error} An error may be thrown if there are network or other issues during the request.
 * 
 * @author Kyle Sung
 */
function saveEventChanges(eventId, editedEvent) {
    fetch("/save-event-changes/" + eventId, {
        method: "PUT",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify(editedEvent),
    }).then(function (response) {
        if (response.ok) {
            // handle success
            console.log("Event changes saved successfully");
        } else {
            // handle error
            console.log("Failed to save event changes");
        }
    }).catch(function (error) {
        console.log("Error: ", error);
    });
}
