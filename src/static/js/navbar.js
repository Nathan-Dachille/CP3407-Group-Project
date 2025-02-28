const nav = document.querySelector(".primary-navigation");
const toggle = document.querySelector(".menu-toggle");

function toggle_navbar() {
	const visible = nav.getAttribute("data-visible");
	const open = nav.getAttribute("data-open");

	if (visible === "false") {
		nav.setAttribute("data-visible", "true");
		toggle.setAttribute("data-open", "true");
	} else {
		nav.setAttribute("data-visible", "false");
		toggle.setAttribute("data-open", "false");
	}
}


toggle.addEventListener('click', toggle_navbar);


