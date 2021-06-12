var request = null;
var dom_results = null;

document.addEventListener("DOMContentLoaded", function(event) {
	dom_results = document.getElementById("searchresults");
});

function change_query(event) {
	//if(request != null) request.abort();
	if(!("content" in document.createElement("template"))) {
		console.log("Your browser doesn't support HTML templates.")
		return;
	}
	request = new XMLHttpRequest();
	request.onreadystatechange = function() {
		if(this.readyState == 4 && this.status == 200 && request.responseText != "") {
			console.log(request.responseText);
			var html = "";
			for(result of JSON.parse(request.responseText)) {
				/*
				var clone = document.getElementsByTagName("template")[0].content.cloneNode(true);
				var a = clone.children[0];
				var img = a.children[0];
				var header = a.children[1];
				a.href = "view?id=" + result["id"];
				img.src = "";
				header.textContent = result["title"];
				dom_results.appendChild(clone); //document.importNode(template.content, true)*/
				html += "<a href=" + result["id"] + "><img src=''><h2>" + result["title"] + "</h2></a>";
			}
			dom_results.innerHTML = html;
			/*
			//Remove all search results
			while(dom_results.firstChild) dom_results.removeChild(dom_results.firstChild);
			const results = JSON.parse(request.responseText);
			for(result of results) {
				let a = document.createElement("a");
				a.textContent = result["title"];
				a.href = "view?id=" + result["id"];
				dom_results.appendChild(a);
			}*/
		}
	};
	request.open("POST", "/livesearch", true);
	request.send(event.target.value);
}