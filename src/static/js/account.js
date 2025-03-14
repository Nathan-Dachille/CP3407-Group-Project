function openModel(modelId) {
    document.getElementById(modelId).style.display = "flex";
}

function closeModel(modelId) {
    document.getElementById(modelId).style.display = "none";
}

function toggleEdit() {
    let displaySpan = document.getElementById("phone_display");
    let inputField = document.getElementById("phone_input");
    let button = document.querySelector(".toggle_edit");

    if (displaySpan.style.display === "none") {
        // Validate the input
        let phoneValue = inputField.value.trim();
        let phoneRegex = /^[\d\s\-\+\(\)]*$/; // Allows digits, spaces, dashes, plus, and parentheses

        if (phoneValue === "" || phoneRegex.test(phoneValue)) {
            // Valid input or blank, save and switch back to text mode
            displaySpan.textContent = phoneValue || "No phone number"; // Fallback text
            displaySpan.style.display = "inline";
            inputField.style.display = "none";
            button.textContent = "⇄"; // Reset button text
        } else {
            alert("Please enter a valid phone number.");
            inputField.focus();
        }
    } else {
        // Switching to edit mode
        inputField.style.display = "inline";
        inputField.focus();
        displaySpan.style.display = "none";
        button.textContent = "✔"; // Change button text to indicate save
    }
}