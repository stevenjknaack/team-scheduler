'use strict';

document.addEventListener('DOMContentLoaded', (event) => {

    // Event listener for checking/unchecking all checkboxes
    document.getElementById('checkAll').addEventListener('click', function () {
        const checkboxes = document.querySelectorAll('#peopleContainer .member input[type="checkbox"]');
        const allChecked = Array.from(checkboxes).every(checkbox => checkbox.checked);

        checkboxes.forEach((checkbox) => {
            checkbox.checked = !allChecked;
        });

        this.textContent = allChecked ? "Check All" : "Uncheck All";
    });



    // Function to filter and search people based on input
    window.searchPeople = function () {

        // Declare variables for input field, filter text, list of people, individual people entries, and loop index
        var input, filter, peopleList, peopleEntries, i, personName, txtValue;

        // Get the search input by its ID
        input = document.getElementById('searchPeople');
        // Get the search term and convert it to uppercase for case-insensitive comparison
        filter = input.value.toUpperCase();
        // Get the container that holds all people entries
        peopleList = document.getElementById("peopleContainer");
        // Get all people entry elements within the container
        peopleEntries = peopleList.getElementsByClassName('member');

        // Loop through all people entries in the list
        for (i = 0; i < peopleEntries.length; i++) {
            // For each entry, get the text content directly inside the label element
            personName = peopleEntries[i].textContent || peopleEntries[i].innerText;
            // Trim and convert the text content to uppercase for comparison
            txtValue = personName.trim().toUpperCase();
            // Check if the person's name contains the search term
            if (txtValue.indexOf(filter) > -1) {
                // If the name contains the search term, display the entry
                peopleEntries[i].style.display = "";
            } else {
                // If the name does not contain the search term, hide the entry
                peopleEntries[i].style.display = "none";
            }
        }
    };

    var durationInput = document.getElementById('eventDuration');

    durationInput.addEventListener('input', function (e) {
        var value = parseInt(e.target.value, 10);

        if (isNaN(value)) {
            e.target.setCustomValidity("Please enter a valid number.");
        } else {
            e.target.setCustomValidity("");
        }

        // This is important for some browsers to ensure the message shows
        e.target.reportValidity();
    });

});



function confirmParticipants() {
    // Retrieve the team name and description
    var teamName = document.getElementById('teamName').value.trim();
    var teamDescription = document.getElementById('teamDescription').value.trim();

    // Reference to the checkboxes and the selected participants container
    var checkboxes = document.querySelectorAll('#peopleContainer input[type="checkbox"]:checked');
    var selectedContainer = document.getElementById('selectedParticipants');

    // Check if team name or description is empty and alert the user
    if (!teamName || !teamDescription) {
        alert("Please enter both team name and description.");
        return;
    }

    // If no participants are selected, alert the user
    if (checkboxes.length === 0) {
        alert("Please select at least one participant.");
        return;
    }

    // Clear the container to remove any previous selections and set up for new content
    selectedContainer.innerHTML = '';
    selectedContainer.style.display = 'flex';
    selectedContainer.style.flexDirection = 'column'; // Ensure items are stacked vertically

    // Create and append the team information
    selectedContainer.appendChild(createTeamInfo(teamName, teamDescription));

    // Create and append the header for participants
    var participantsHeader = document.createElement('h3');
    participantsHeader.textContent = "Selected Participants:";
    selectedContainer.appendChild(participantsHeader);

    // Create a container for participants with flex row layout
    var participantsContainer = document.createElement('div');
    participantsContainer.className = 'selected-participant';
    participantsContainer.style.display = 'flex'; // Set up for flex row layout
    participantsContainer.style.flexWrap = 'wrap'; // Allow items to wrap
    participantsContainer.style.justifyContent = 'center'; // Align items to the start
    participantsContainer.style.overflowY = 'auto'; // Add scroll if the content overflows vertically

    // Iterate over each checked checkbox and add participants
    checkboxes.forEach(function (checkbox) {
        var participantDiv = document.createElement('div');
        participantDiv.className = 'participant';
        participantDiv.textContent = checkbox.value;
        participantsContainer.appendChild(participantDiv);
    });

    // Add the participants container to the selected container
    selectedContainer.appendChild(participantsContainer);

    // Hide the member selection panel
    toggleVisibility('memberSelection');
}


// Helper function to create team info elements
function createTeamInfo(teamName, teamDescription) {
    var teamInfoDiv = document.createElement('div');
    teamInfoDiv.innerHTML = `<strong>Team Name:</strong> ${teamName}<br><strong>Team Description:</strong> ${teamDescription}`;
    return teamInfoDiv;
}

// Helper function to toggle visibility of an element by id
function toggleVisibility(elementId) {
    var element = document.getElementById(elementId);
    element.style.display = (element.style.display === 'none') ? 'block' : 'none';
}

function createTeam() {
    // Retrieve the team name and description from input fields
    var teamName = document.getElementById('teamName').value.trim();
    var teamDescription = document.getElementById('teamDescription').value.trim();

    // Check if team name or description is empty and alert the user
    if (!teamName || !teamDescription) {
        alert("Please enter both team name and description.");
        return;
    }

    // Find all elements representing selected participants and extract their text content
    var selectedParticipantElements = document.querySelectorAll('#selectedParticipants .participant');
    var participants = Array.from(selectedParticipantElements).map(element => element.textContent);

    // Check if any participants are selected and alert if none are found
    if (participants.length === 0) {
        alert("Please select at least one participant.");
        return;
    }

    // Create a team object with the provided details
    var team = {
        name: teamName,
        description: teamDescription,
        participants: participants
    };

    // Log the created team for review or further processing
    console.log("Created Team:", team);
    
    // Optionally, here you can do something with the created team object,
    // such as displaying it on the page, or sending it to a server.
}

// The function is now ready to be called when needed, such as on a button click event.
