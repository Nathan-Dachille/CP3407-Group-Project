document.addEventListener("DOMContentLoaded", function() {
        // Trigger the AJAX request when the page loads
        updateWeekInfo();
});

function updateWeekInfo() {
    // Get today's date (you can change this to any date logic you prefer)
    const userDate = new Date().toISOString().split('T')[0];  // Formats date as YYYY-MM-DD

    // Send the new date via AJAX to the server
    fetch(`/profile/?user_date=${userDate}`, {
        method: 'GET',
        headers: {
            'X-Requested-With': 'XMLHttpRequest'
        }
    })
    .then(response => response.json())

    .catch(error => console.error("Error fetching week data:", error));
}

function openModel(modelId) {
    document.getElementById(modelId).style.display = "flex";
}

function closeModel(modelId) {
    document.getElementById(modelId).style.display = "none";
}

function toggleAvailable(togType, target) {
    if (togType === 'hour')
    {
        if (true === true)// target is toggled unavailable
        {
            document.getElementById(target).style.color = "white";
        } else
        {
            document.getElementById(target).style.color = "red";
        }

    } else if (togType === 'week')
    {

    }

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