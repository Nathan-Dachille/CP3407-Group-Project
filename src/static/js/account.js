// Account Javascript File
let userRole = "";
// General Account scripts
document.addEventListener("DOMContentLoaded", function () {
    // Retrieve the last focused date from sessionStorage or default to today
    let storedDate = sessionStorage.getItem("focusDate");
    let focusDate = storedDate ? new Date(storedDate) : new Date(); // Start with the user's current date

    userRole = document.getElementById("page_layout").getAttribute("data-user-role")

    console.log(userRole)
    // If the user is a Cleaner, do the cleaner-specific functionality
    if (userRole === 'CLEANER') {
        console.log(userRole)
        document.getElementById("prev-week").addEventListener("click", () => {
            let focusDate = new Date(sessionStorage.getItem("focusDate"));
            focusDate.setDate(focusDate.getDate() - 7);
            sessionStorage.setItem("focusDate", focusDate.toISOString());
            updateWeekInfo(focusDate);
        });

        document.getElementById("next-week").addEventListener("click", () => {
            let focusDate = new Date(sessionStorage.getItem("focusDate"));
            focusDate.setDate(focusDate.getDate() + 7);
            sessionStorage.setItem("focusDate", focusDate.toISOString());
            updateWeekInfo(focusDate);
        });

        // Trigger the AJAX request when the page loads
        updateWeekInfo(focusDate);
    }
    // If the user is a Customer, do the customer-specific functionality
    else if (userRole === 'CUSTOMER') {
        document.getElementById("sort-toggle").addEventListener("click", () => {
            const btn = document.getElementById("sort-toggle");
            const currentOrder = btn.getAttribute("data-order");
            const newOrder = currentOrder === "asc" ? "desc" : "asc";
            btn.setAttribute("data-order", newOrder);
            btn.textContent = newOrder === "asc" ? "↓" : "↑";
            applyFilters();
        });
        fetchBookings();
    }
});

function convertToTimeString(hour) {
    // Handle hour 0 as 12am, and 12 as 12pm
    if (hour === 0) {
        return "12am";
    } else if (hour === 12) {
        return "12pm";
    }

    // Convert hour to 12-hour format
    const hour12 = hour > 12 ? hour - 12 : hour;

    // Determine AM or PM
    const period = hour >= 12 ? "pm" : "am";

    // Return the formatted time string
    return `${hour12}${period}`;
}

function formatDateWithOrdinal(dateString) {
    const date = new Date(dateString);
    const day = date.getDate();
    const month = date.toLocaleString("en-US", { month: "short" });

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

// Utility function to get CSRF token from cookies
function getCSRFToken() {
    const cookies = document.cookie.split("; ");
    for (let cookie of cookies) {
        const [name, value] = cookie.split("=");
        if (name === "csrftoken") {
            return value;
        }
    }
    return "";
}

// Cleaner Account Scripts

function fetchWeekData(focusDate = null) {
    if (!focusDate) {
        let storedDate = sessionStorage.getItem("focusDate");
        focusDate = storedDate ? new Date(storedDate) : new Date();
    }

    // Ensure the date is stored properly in sessionStorage
    sessionStorage.setItem("focusDate", focusDate.toISOString().split('T')[0]);

    // Get today's date (you can change this to any date logic you prefer)
    const formatDate = focusDate.toISOString().split('T')[0]; // Formats date as YYYY-MM-DD

    // Send the new date via AJAX to the server
    return fetch(`/profile/?user_date=${formatDate}`, {
        method: 'GET',
        headers: {
            'X-Requested-With': 'XMLHttpRequest'
        }
    })
    .then(response => response.json())
    .then(data => {
        if (!data || !data.current_date || !data.week_dates
            || !data.week_number || !data.ava_data) {
            console.error("Invalid data received:", data);
            return null;
        }
        return data; // Return the valid data
    })
    .catch(error => {
        console.error("Error fetching week data:", error);
        return null;
    });
}

function updateWeekInfo(focusDate = null) {
    fetchWeekData(focusDate).then(data => {
        if (!data) return;
        console.log("Current Date:", data.current_date);
        console.log("Week Number:", data.week_number);
        console.log("Week Dates:", data.week_dates);
        console.log("Availability Data:", data.ava_data);

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

        const request_data = {
            dates: data.week_dates,
            availability: data.ava_data,
        }
        console.log("Request body:", JSON.stringify(request_data))

        return fetch(`/get_bookings/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-Requested-With': 'XMLHttpRequest',
                "X-CSRFToken": getCSRFToken() // Needed for Django security
            },
            body: JSON.stringify(request_data)
        })
        .then(response => {
            if (!response.ok) throw new Error(`HTTP error: ${response.status}`);
            return response.json();
        })
        .then(b_data => {
            if (!b_data) {
                console.error("Invalid data received:", b_data);
                return null;
            }
            console.log(b_data)
            // Table Section:
            const timetableContainer = document.getElementById("timetable")
            let timetableHTML = '<table class="timetable">';

            // Add table headers
            timetableHTML += `<tr><th><button class="toggle_set" ` +
                `onClick="toggleAvailable({togType:1, target_days:'${data.week_dates}'.split(','), target_hours:[]})">+` +
                `</button></th>`;

            data.week_dates.forEach((date) => {
                // Create a Date object from the date string
                const date_d = new Date(date);

                // Get the day name from the Date object
                const dayName = date_d.toLocaleString('en-US', { weekday: 'short' });
                timetableHTML += `<th><button class="toggle_set"` +
                ` onClick="toggleAvailable({togType:1, target_days:'${date}'.split(','), target_hours:[]})">${dayName}`
                    +`</button></th>`;
            });

            timetableHTML += `</tr>`;

            // Add table content

            for (let i = 0, weekDates = data.week_dates, avail = data.ava_data; i < 24; i++) {
                let t_string = convertToTimeString(i)

                timetableHTML += `<tr><th><button class="toggle_set" ` +
                `onClick="toggleAvailable({togType:1,target_days:'${weekDates}'.split(','),target_hours:[${[i]}]})">
                ${t_string}</button></th>`;

                for (let j = 0; j < weekDates.length; j++) {
                    let currentDate = weekDates[j]; // Get the current date from the week
                    // Find availability for this date and time
                    let dayAvailability = avail.find(entry => entry.ava_date === currentDate);
                    let isAvailable = dayAvailability && dayAvailability.available_hours.includes(i);

                    let bookedBookings = []; // To store all booked booking IDs for this time
                    let isBooked = false;
                    if (b_data.bookings_a) {
                        // Find the booking for this specific date
                        let booking = b_data.bookings_a.find(booking => booking.date === currentDate);

                        if (booking && booking.booking_hours && booking.booking_hours.includes(i)) {
                            timetableHTML += `<th><button class="toggle_set fields a_book"` +
                            ` onClick="openBooking({IDs:[${booking.id}]})">‎</button></th>`;
                            isBooked = true;
                        }
                    }
                    if (!isBooked && b_data.bookings_u) {
                        let bookings = b_data.bookings_u.filter(booking => booking.date === currentDate
                            && booking.booking_hours.includes(i));

                        if (bookings.length > 0) {
                            bookings.forEach(booking => {
                                console.log(booking.id)
                                bookedBookings.push(booking.id); // Add booking ID to the array
                            });
                            console.log(bookedBookings)
                            console.log(JSON.stringify(bookedBookings))
                            timetableHTML += `<th><button class="toggle_set fields u_book"` +
                                ` onClick="openBooking({ IDs: ${JSON.stringify(bookedBookings) }})">‎</button></th>`;
                            isBooked = true;
                        }
                    }
                    if (!isBooked) {
                        let buttonClass = isAvailable ? "ava" : "n_ava";

                        timetableHTML += `<th><button class="toggle_set fields ${buttonClass}"` +
                        ` onClick="toggleAvailable({togType:2, target_days:'${weekDates[j]}'.split(','),
                        target_hours:[${i}]})">‎</button></th>`;
                    }
                }

                timetableHTML += `</tr>`;
            }

            // Insert the HTML into the timetable container
            timetableContainer.innerHTML = timetableHTML;
        })
        .catch(error => {
            console.error("Error fetching week data:", error);
            return null;
        });
    })
    .catch(error => console.error("Error fetching data:", error));
}

function toggleAvailable({togType=0, target_days=[""], target_hours=[]}) {
    const request_data = {
            type: togType,
            days: Array.isArray(target_days) ? target_days : [target_days],
            hours: Array.isArray(target_hours) ? target_hours : [target_hours],
    }
    console.log("Request body:", JSON.stringify(request_data))
    fetch("/toggle_availability/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": getCSRFToken() // Needed for Django security
        },
        body: JSON.stringify(request_data)
    })
    .then(response => response.json())
    .then(data => {
        console.log("Response", data);
        if (data.success) {
            updateWeekInfo();
        } else {
            console.error("Error:", data.error);
        }
    })
    .catch(error => console.error("Error:", error));
}

function dupAvailability() {
    let selectedDate = document.getElementById("DateInput").value;
    console.log(selectedDate)

    if (!selectedDate) {
        alert("Please select a date.");
        return;
    }

    fetchWeekData().then(data => {
        if (!data) return;
        console.log("Current Date:", data.current_date);
        console.log("Week Number:", data.week_number);
        console.log("Week Dates:", data.week_dates);
        console.log("Availability Data:", data.ava_data);


        const request_data = {
            t_date: selectedDate,
            s_week: data.week_dates,
        }
        console.log("Request body:", JSON.stringify(request_data))

        fetch("/duplicate_availability/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": getCSRFToken()  // Ensure CSRF token is included
            },
            body: JSON.stringify(request_data)
        })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    updateWeekInfo();
                    alert("Availability duplicated successfully!");
                } else {
                    console.error("Error:", data.error);
                }
            })
            .catch(error => console.error("Error:", error));
    });
}

function moveTo() {
    let focusDate = new Date(document.getElementById("DateInput").value);
    console.log(focusDate)
    sessionStorage.setItem("focusDate", focusDate.toISOString());
    updateWeekInfo(focusDate);
}

// Assuming the fetch function is fetching booking data from your server
function fetchBookingDetails(bookingId) {
    console.log(bookingId)
    return fetch(`/find_booking/?booking_id=${bookingId}`, {
        method: 'GET',
        headers: {
            'X-Requested-With': 'XMLHttpRequest'
        }
    })
    .then(response => response.json())
    .then(data => {
        if (!data) {
            console.error("Invalid data received:", data);
            return null;
        }
        console.log(data)
        return data; // Return the valid data
    })
    .catch(error => {
        console.error("Error fetching booking data:", error);
        return null;
    });
}

function openBooking({ IDs }) {
    const bookingIds = Array.isArray(IDs) ? IDs : JSON.parse(IDs);
    console.log(bookingIds)
    if (Array.isArray(bookingIds)) {
        console.log("Booking IDs:", bookingIds);
    } else {
        console.error("Received an invalid value for bookingIds:", bookingIds);
    }
    const now = new Date(); // current local time of the user

    // Get the container where booking details will be displayed
    let bookingDetailsContainer = document.getElementById("booking-details-container");

    // Start with header
    bookingDetailsContainer.innerHTML = '<div class="content_box background-grey round booking_layout"><h1>Bookings:</h1></div>';

    // Loop through each ID and append as they arrive
    bookingIds.forEach(bookingId => {
        fetchBookingDetails(bookingId)
            .then(booking => {
                if (booking && booking.bookingInfo) {
                    const b = booking.bookingInfo;
                    const lockoutTime = new Date(new Date(`${b.date}T${b.start_time}`) - (1 * 3600000));

                    let bookingHTML = `<div class="content_box background-grey round booking_layout">
                        <div class="booking_element">
                        <h3>Booking Details for ${b.user_name}</h3>
                        <h3>Booking ID: ${b.id}</h3>
                        <p><strong>Date:</strong> ${b.date}</p>
                        <p><strong>Time Period:</strong> ${b.start_time}${b.end_time ? ` - ${b.end_time}` : ''}</p>
                        <p><strong>Service:</strong> ${b.service}</p>`;

                    // Render stars for rating
                    const rating = b.rating || 0;
                    let stars = "";
                    for (let i = 1; i <= 5; i++) {
                        stars += i <= rating ? "★" : "☆";
                    }
                    bookingHTML += `<p><strong>Rating:</strong> ${stars}</p>`;

                    bookingHTML += `<p><strong>Email:</strong> ${b.email || "N/A"}</p>`;

                    if (b.assigned_id) {
                        bookingHTML += `<p><strong>Phone:</strong> ${b.phone || "N/A"}</p>
                                        <p><strong>Address:</strong> ${b.address_str || "N/A"}</p>`;

                        if (lockoutTime > now) {
                            bookingHTML += `<p><button class="booking_button"
                                            onClick="toggleAccept({ ID: ${b.id} })">
                                            Cancel Booking
                                            </button></p>`;
                        } else {
                            bookingHTML += `<p>
                                            <input type="number" class="booking_rating" id="rating-${b.id}" name="rating" min="1" max="5" required>
                                            <button class="booking_button"
                                                onClick="addRating({ Source: 2, ID: ${b.id}, rating: 'rating-${b.id}' })">
                                                Set Rating
                                            </button>
                                            </p>`;
                        }

                        bookingHTML += `</div>
                                        <div class="booking_element">
                                        <h3>Notes:</h3>
                                        <div class="note_block">
                                            <p>${b.notes || 'None'}</p>
                                        </div>
                                        </div>`;
                    } else {
                        bookingHTML += `<p><button class="booking_button"
                                            onClick="toggleAccept({ ID: ${b.id} })">
                                            Accept Booking
                                            </button></p></div>`;
                    }

                    bookingHTML += `</div>`;

                    bookingDetailsContainer.innerHTML += bookingHTML;
                } else {
                    bookingDetailsContainer.innerHTML += `<p>Booking not found for ID ${bookingId}</p>`;
                }
            })
            .catch(error => {
                console.error("Error fetching booking:", error);
                bookingDetailsContainer.innerHTML += `<p>Error loading booking ID ${bookingId}</p>`;
            });
    });
}

function toggleAccept({ ID }) {
    const request_data = {
            target: ID,
    }
    console.log("Request body:", JSON.stringify(request_data))
    fetch("/toggle_accept/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": getCSRFToken() // Needed for Django security
        },
        body: JSON.stringify(request_data)
    })
    .then(response => response.json())
    .then(data => {
        console.log("Response", data);
        if (data.success) {
            if (userRole === 'CLEANER') {
                updateWeekInfo();
            } else {
                fetchBookings();
            }
        } else {
            console.error("Error:", data.error);
        }
    })
    .catch(error => console.error("Error:", error));
}

// Customer Account Scripts
let allBookings = [];

function fetchBookings() {
    fetch('/api/customer_bookings/', {
        headers: { 'X-Requested-With': 'XMLHttpRequest' }
    })
    .then(res => res.json())
    .then(data => {
        allBookings = data.bookings;
        renderBookings(allBookings);
    })
    .catch(err => console.error("Error fetching bookings:", err));
}

function renderBookings(bookings) {
    const container = document.getElementById("customer-bookings-container");
    container.innerHTML = '';

    if (bookings.length === 0) {
        container.innerHTML = '<p>No bookings found.</p>';
        return;
    }

    bookings.forEach(b => {
        const card = document.createElement('div');
        card.className = 'booking-card';
        card.innerHTML = `
            <h4>${b.service} on ${b.date} from ${b.start_time} to ${b.end_time}</h4>
            <p><strong>Status:</strong> ${b.status}</p>
        `;
        if (b.user_name) {
            card.innerHTML += `
                <p><strong>Assignment:</strong> ${b.user_name}</p>
                <p><strong>Email:</strong> ${b.email || "N/A"}</p>
                <p><strong>Phone:</strong> ${b.phone || "N/A"}</p>
            `;
            // Render stars for rating
            const rating = b.rating || 0;
            let stars = "";
            for (let i = 1; i <= 5; i++) {
                stars += i <= rating ? "★" : "☆";
            }
            card.innerHTML += `<p><strong>Rating:</strong> ${stars}</p>`;
            if (b.status === "Upcoming") {
                card.innerHTML += `<p><button class="booking_button"
                                onClick="toggleAccept({ ID: ${b.id} })">
                                Reject Cleaner
                                </button></p>`;
            }
        } else {
            card.innerHTML += `
                <p><strong>Assignment:</strong> Unassigned</p>
            `;
        }
        card.innerHTML += `
            <h5><strong>Notes:</strong></h5>
            <p>${b.notes || 'None'}</p>
            `;
        if (b.status === "Upcoming") {
            card.innerHTML += `<p><button class="booking_button"
                                onClick="deleteBooking({ ID: ${b.id} })">
                                Cancel Booking
                                </button></p>
                            `;
        } else {
            card.innerHTML += `<p>
                            <input type="number" class="booking_rating" id="rating-${b.id}" name="rating" min="1" max="5" required>
                            <button class="booking_button"
                                onClick="addRating({ Source: 1, ID: ${b.id}, rating: 'rating-${b.id}' })">
                                Set Rating
                            </button>
                            </p>`;
        }
        container.appendChild(card);
    });
}

function applyFilters() {
    const assignmentFilter = document.getElementById("assignment-filter").value;
    const statusFilter = document.getElementById("status-filter").value;
    const serviceFilter = document.getElementById("service-filter").value.toLowerCase();
    const sortOrder = document.getElementById("sort-toggle").getAttribute("data-order");

    let filtered = allBookings.filter(b => {
        // Assignment filter
        if (assignmentFilter === "assigned" && !b.user_name) return false;
        if (assignmentFilter === "unassigned" && b.user_name) return false;

        // Status filter (date comparison)
        const bookingDate = new Date(`${b.date}T${b.start_time}`);
        const now = new Date();
        if (statusFilter === "upcoming" && bookingDate < now) return false;
        if (statusFilter === "past" && bookingDate >= now) return false;

        // Service filter (basic text match)
        if (serviceFilter && !b.service.toLowerCase().includes(serviceFilter)) return false;

        return true;
    });

    // Sorting
    filtered.sort((a, b) => {
        const dateA = new Date(`${a.date}T${a.start_time}`);
        const dateB = new Date(`${b.date}T${b.start_time}`);
        return sortOrder === "asc" ? dateA - dateB : dateB - dateA;
    });

    renderBookings(filtered);
}

function deleteBooking({ ID }) {
    const request_data = {
            target: ID,
    }
    console.log("Request body:", JSON.stringify(request_data))
    fetch("/delete_booking/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": getCSRFToken() // Needed for Django security
        },
        body: JSON.stringify(request_data)
    })
    .then(response => response.json())
    .then(data => {
        console.log("Response", data);
        if (data.success) {
            if (userRole === 'CLEANER') {
                updateWeekInfo();
            } else {
                fetchBookings();
            }
        } else {
            console.error("Error:", data.error);
        }
    })
    .catch(error => console.error("Error:", error));
}