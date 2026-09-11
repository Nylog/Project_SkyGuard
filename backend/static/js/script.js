// Grab references to all the dom elements we'll need to interract with

const loginView = document.getElementById("login-view");
const chatView = document.getElementById("chat-view");

const usernameInput = document.getElementById("username");
const passwordInput = document.getElementById("password");
const loginButton = document.getElementById("login-button");
const loginError = document.getElementById("login-error");

const loggedInAs = document.getElementById("logged-in-as");
const logoutButton = document.getElementById("logout-button");

const chatMessage = document.getElementById("chat-message");
const chatInput = document.getElementById("chat-input");
const sendButton = document.getElementById("send-button");



// Sends the login request to the backend and switches views on success.
async function login() {
    const response = await fetch("/login", {
        method : "POST",
        headers : {"Content-Type" : "application/json"}
        body : JSON.stringify({
            username: usernameInput.value,
            password: passwordInput.value,
        }),
    });

    loginError.textContent = "";
    loggedInAs.textContent  = 'Logged in as ${usernameInput.value} (${data.role})';

    loginView.classList.add("hidden");
    chatView.classList.remove("hidden");

}

// Logs the user out and switches back to the login view

async function logout() {
    await fetch ("/logout", {method : "POST"});

    chatView.classList.add("hidden");
    loginView.classList.remove("hidden");

    // Clear the chat history and login fields for a clean state on next login
    chatMessage.innerHTML = "";
    usernameInput.value = "";
    passwordInput.value = "";
}
