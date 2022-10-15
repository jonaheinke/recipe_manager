const frames = {
	home: 0,
	view: 1,
	edit: 2
};

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

function image_animation(event) {
	event.preventDefault();
	event = event || window.event;
    var card = event.target || e.srcElement;
	console.log(card);

	//var image = card.querySelector("img");
	var image = card;
	console.log(image);
	//TODO: change this to image
	var coords = card.getBoundingClientRect();
	var target_x = 100;
	var target_y = 100;
	var target_width = 400;
	var target_height = 400;

	//card.style.zIndex = 1;
	console.log("translate(" + (target_x - coords.left) + "px, " + (target_y - coords.top) + "px) scale(" + (target_width / coords.width) + ", " + (target_height / coords.height) + ")")
	image.style.transform = "translate(" + (target_x - coords.left) + "px, " + (target_y - coords.top) + "px) scale(" + (target_width / coords.width) + ", " + (target_height / coords.height) + ")";
}

document.addEventListener("DOMContentLoaded", function(event) {
	//earths_shadow = document.querySelector(".slider::after");
	body = document.querySelector("body");

	var cards = document.querySelectorAll(".card");
	var card_images = document.querySelectorAll(".card > img");
	console.log("DOMContentLoaded finished");
});

document.addEventListener("keydown", e => {
	if(e.ctrlKey && e.key === "s") {
		e.preventDefault();
		console.log("CTRL + S");
	}
});

document.addEventListener("alpine:init", () => {
	Alpine.data("search", () => ({
		init() {
			this.results = [{'id': 2, 'src': 'https://d2gg9evh47fn9z.cloudfront.net/800px_COLOURBOX17706474.jpg', 'title': 'Test Recommended Result'},
							{'id': 3, 'src': 'https://images.immediate.co.uk/production/volatile/sites/30/2020/08/chorizo-mozarella-gnocchi-bake-cropped-9ab73a3.jpg', 'title': 'Second Recipe'},
							{'id': 4, 'src': 'https://www.blueosa.com/wp-content/uploads/2020/01/the-best-top-10-indian-dishes.jpg', 'title': 'Third Recipe'},
							{'id': 5, 'src': 'https://www.expatica.com/app/uploads/sites/6/2014/05/german-food.jpg', 'title': 'Fourth Recipe'},
							{'id': 6, 'src': 'https://www.eatthis.com/wp-content/uploads/sites/4/2019/06/deep-dish-pizza-chicago.jpg', 'title': 'Fifth Recipe'},
							{'id': 7, 'src': 'https://assets.vogue.in/photos/5fe1b6ff921d2894cf08210d/2:3/w_1280,c_limit/food%20and%20faith.jpg', 'title': 'Sixth Recipe'}];
		},

		searchquery: "",
		results: [],
		layout: "mosaic",

		load_search_results() {
			if(this.searchquery == "") {
				this.init();
				return;
			}
			var request = new XMLHttpRequest();
			var that = this;
			request.onreadystatechange = function() {
				if(this.readyState == 4 && this.status == 200 && request.responseText != "") {
					console.log(request.responseText);
					that.results = JSON.parse(request.responseText);
				}
			};
			request.open("POST", "/livesearch", true);
			request.send(this.searchquery);
		}
	}));
});