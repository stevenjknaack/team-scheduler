'use strict';
document.getElementById("createEvent").addEventListener("click", function() {
    window.location.href = window.eventCreateUrl; 
});

// Toggle the logout form
$(document).ready(function () {
    $("#welcomeButton").on("click", function () {
        $("#logoutForm").toggle();
    });
});

// Pop up modal functionality
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
