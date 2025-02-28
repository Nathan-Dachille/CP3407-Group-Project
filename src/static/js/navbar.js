const nav = document.querySelector(".primary-navigation");
const toggle = document.querySelector(".menu-toggle");
const header = document.querySelector(".primary-header");
var last_scroll_pos = window.pageYOffset;

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

function hide_topbar() {
	var new_scroll_pos = window.pageYOffset;

	if (last_scroll_pos < new_scroll_pos) {
		header.setAttribute("data-hide", "true");
		nav.setAttribute("data-visible", "false");
		toggle.setAttribute("data-open", "false");
	} else {
		header.setAttribute("data-hide", "false");
	}
	last_scroll_pos = new_scroll_pos;
}

document.addEventListener('scroll', hide_topbar);
toggle.addEventListener('click', toggle_navbar);


