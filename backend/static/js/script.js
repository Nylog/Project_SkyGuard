// Grab references to all the dom elements we'll need to interract with

const loginView = document.getElementById("login-view");
const chatView = document.getElementById("chat-view");

const usernameInput = document.getElementById("username");
const passwordInput = document.getElementById("password");
const loginButton = document.getElementById("login-button");
const loginError = document.getElementById("login-error");

const loggedInAs = document.getElementById("logged-in-as");
const logoutButton = document.getElementById("logout-button");

const chatMessage = document.getElementById("chat-messages");
const chatInput = document.getElementById("chat-input");
const sendButton = document.getElementById("send-button");



// Sends the login request to the backend and switches views on success.
async function login() {
    const response = await fetch("/login", {
        method : "POST",
        headers : {"Content-Type" : "application/json"},
        body : JSON.stringify({
            username: usernameInput.value,
            password: passwordInput.value,
        }),
    });

    const data = await response.json();
    
    if (!data.success) {
        loginError.textContent = data.message;
        return
    }

    loginError.textContent = "";
    loggedInAs.textContent  = `Logged in as ${usernameInput.value} (${data.role})`;

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

// Adds a message bubble to the chat history.
// sender is either "user" or "agent", used to style the bubble accordingly.

function addMessage(text, sender){
    const messageDiv = document.createElement("div");
    messageDiv.classList.add("message", sender);
    messageDiv.textContent = text;
    chatMessage.appendChild(messageDiv);

    // Auto-scroll to the latest message.
    chatMessage.scrollTop = chatMessage.scrollHeight;
}

// Sends the current chat input to the backend and displays the response.

async function sendMessage(){
    const text = chatInput.value.trim();
    if (text == "") return;  // ignore empty text

    addMessage(text, "user");
    chatInput.value = "";

    const response = await fetch("/chat", {
        method : "POST",
        headers : {"Content-Type" : "application/json"},
        body : JSON.stringify({"message" : text}),

    });
    
    const data = await response.json();
    addMessage(data.response, "agent")

}

// --- Event ---

loginButton.addEventListener("click", login);
logoutButton.addEventListener("click", logout)
sendButton.addEventListener("click", sendMessage)

// Allow pressing Enter to log in (from either username or password field).

usernameInput.addEventListener("keydown", (e) => {if (e.key === "Enter") login(); })
passwordInput.addEventListener("keydown", (e) => {if (e.key === "Enter") login(); })

// Allow pressing Enter to send a chat message.

chatInput.addEventListener("keydown", (e) => {if (e.key === "Enter") sendMessage(); })
