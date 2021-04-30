function change_query() {
	var request = new XMLHttpRequest();
	request.onreadystatechange = function() {
		if(this.readyState == 4 && this.status == 200) {
			//nice
		}
	};
	request.open("POST", "/livesearch", true);
	request.send(document.getElementById("search").value);
}