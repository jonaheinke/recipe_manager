var body = null;
var earths_shadow = null;
var darkmode = {{darkmode['int']}};

function toggle_theme() {
	if(body != null) body.classList.toggle("dark");
	darkmode = !darkmode;
	document.cookie = "darkmode=" + (darkmode ? 1 : 0) + "; path=/";
}

document.addEventListener("DOMContentLoaded", function(event) {
	earths_shadow = document.querySelector(".slider::after");
	body = document.querySelector("body");
});