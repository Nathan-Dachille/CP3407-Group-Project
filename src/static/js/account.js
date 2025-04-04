document.addEventListener("DOMContentLoaded", function () {
    // Retrieve the last focused date from sessionStorage or default to today
    let storedDate = sessionStorage.getItem("focusDate");
    let focusDate = storedDate ? new Date(storedDate) : new Date(); // Start with the user's current date

    function updateWeekInfo() {
        // Get today's date (you can change this to any date logic you prefer)
        const formatDate = focusDate.toISOString().split('T')[0]; // Formats date as YYYY-MM-DD

        // Send the new date via AJAX to the server
        fetch(`/profile/?user_date=${formatDate}`, {
            method: 'GET',
            headers: {
                'X-Requested-With': 'XMLHttpRequest'
            }
        })
        .then(response => response.json())
        .then(data => {
            if (!data || !data.week_dates || !data.week_number) {
                console.error("Invalid data received:", data);
                return;
            }

            // Subheader Section:
            document.getElementById("week-number").textContent = ` ${data.week_number} `;
            // Apply the ordinal formatting
            const formattedStartDate = formatDateWithOrdinal(data.week_dates[0]);
            const formattedEndDate = formatDateWithOrdinal(data.week_dates[6]);

            document.getElementById("week-range").textContent =
                `${formattedStartDate} - ${formattedEndDate}`;

            const startYear = new Date(Date.parse(data.week_dates[0])).getFullYear();
            const endYear = new Date(Date.parse(data.week_dates[6])).getFullYear();

            document.getElementById("year-display").textContent =
                (startYear !== endYear) ? ` ${startYear} - ${endYear} ` : ` ${startYear} `;

            // Table Section:
            const timetableContainer = document.getElementById("timetable")
            let timetableHTML = '<table class="timetable">';

            // Add table headers
            timetableHTML += `<tr><th><button class="toggle_set" ` +
                `onClick="toggleAvailable(1,${data.week_dates})">+` +
                `</button></th>`;

            for (let i =0; i < data.week_dates.length; i++) {
                // Create a Date object from the date string
                const date = new Date(data.week_dates[i]);

                // Get the day name from the Date object
                const dayName = date.toLocaleString('en-US', { weekday: 'long' });
                timetableHTML += `<td><button class="toggle_set"` +
                ` onClick="toggleAvailable(1, '${data.week_dates[i]}')">${dayName}` +
                `</button></td>`;
            }
            timetableHTML += `</tr>`;


            // Insert the HTML into the timetable container
            timetableContainer.innerHTML = timetableHTML;
        })
        .catch(error => console.error("Error fetching week data:", error));
    }

    document.getElementById("prev-week").addEventListener("click", () => {
        focusDate.setDate(focusDate.getDate() - 7);
        sessionStorage.setItem("focusDate", focusDate.toISOString());
        updateWeekInfo();
    });

    document.getElementById("next-week").addEventListener("click", () => {
        focusDate.setDate(focusDate.getDate() + 7);
        sessionStorage.setItem("focusDate", focusDate.toISOString());
        updateWeekInfo();
    });

    // Trigger the AJAX request when the page loads
    updateWeekInfo();
});

function formatDateWithOrdinal(dateString) {
    const date = new Date(dateString);
    const day = date.getDate();
    const month = date.toLocaleString("en-US", { month: "long" });

    // Function to get ordinal suffix (st, nd, rd, th)
    function getOrdinal(n) {
        if (n > 3 && n < 21) return "th"; // Covers 11th, 12th, 13th
        switch (n % 10) {
            case 1: return "st";
            case 2: return "nd";
            case 3: return "rd";
            default: return "th";
        }
    }

    return `${day}${getOrdinal(day)} of ${month}`;
}

function openModel(modelId) {
    document.getElementById(modelId).style.display = "flex";
}

function closeModel(modelId) {
    document.getElementById(modelId).style.display = "none";
}

function toggleAvailable(togType, target) {
    if (togType === 1)
    {
        if (true === true)// target is toggled unavailable
        {
            document.getElementById(target).style.color = "white";
        } else
        {
            document.getElementById(target).style.color = "red";
        }

    } else if (togType === 2)
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