var xhr = null;

getXmlHttpRequestObject = function () {
    if (!xhr) {
        // Create a new XMLHttpRequest object --> exchange data with a web server behind the scenes
        xhr = new XMLHttpRequest();
    }
    return xhr;
};

function dataCallback() {
    // Check response is ready or not
    if (xhr.readyState == 4 && xhr.status == 200) {
        console.log("User data received!");
        //getDate();
        dataDiv = document.getElementById('result-container');
        // Set current data text
        dataDiv.innerHTML = xhr.responseText;
    }
}
function getUsers() {
    console.log("Get users...");
    xhr = getXmlHttpRequestObject();
    
    xhr.onreadystatechange = dataCallback;
    // asynchronous requests
    xhr.open("GET", "http://localhost:6969/users", true); //get the reqeust from 6969/users
    // Send the request over the network
    xhr.send(null);
}
/*
function getDate() {
    date = new Date().toString();

    document.getElementById('time-container').textContent
        = date;
}*/


// the call back function checks the state of xhr 
// we need to check before processing the data
function sendDataCallback() {
    // Check response is ready or not
    if (xhr.readyState == 4 && xhr.status == 201) {
        console.log("Data creation response received!");
        //getDate();
        //dataDiv = document.getElementById('sent-data-container');
        // Set current data text
        //dataDiv.innerHTML = xhr.responseText;
    }
}

function sendData() {
    email = document.getElementById('email').value; // Assuming the email input has id 'email-input'
    password = document.getElementById('password').value; // Assuming the password input has id 'password-input'

    if (!email || !password) {
        console.log("Email or password is empty.");
        return;
    }
    console.log("Sending email: " + email + " and password " + password);
    xhr = getXmlHttpRequestObject();
    xhr.onreadystatechange = sendDataCallback;
    // Asynchronous requests
    xhr.open("POST", "http://localhost:6969/login", true); // Assuming your login route is '/login'
    xhr.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
    // Send the request over the network
    xhr.send(JSON.stringify({"email": email, "password": password}));
}