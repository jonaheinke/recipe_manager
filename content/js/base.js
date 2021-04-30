var body = null;
//var earths_shadow = null;
var cookie = document.cookie;
var darkmode = cookie[cookie.indexOf("=") + 1] != "0";

function set_cookie() {
	document.cookie = "darkmode=" + +darkmode + "; SameSite=Strict; path=/";
}

if(cookie.indexOf("darkmode=") == -1) {
	darkmode = window.matchMedia && window.matchMedia("(prefers-color-scheme: dark)").matches;
	set_cookie();
	if(darkmode) window.location.reload();
}

function toggle_theme() {
	if(body != null) {
		body.classList.toggle("dark");
		darkmode = !darkmode;
		set_cookie();
	}
}

document.addEventListener("DOMContentLoaded", function(event) {
	//earths_shadow = document.querySelector(".slider::after");
	body = document.querySelector("body");
});