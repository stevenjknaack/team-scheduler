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
    const emails = [];
    for (let i = 0; i < invitedParticipants.children.length; i++) {
        emails.push(invitedParticipants.children[i].innerText);
    }
    console.log(emails);
    modal.style.display = "none";
});
