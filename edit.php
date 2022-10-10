<?php
	//doc: https://www.php.net/file_upload

	$image = $_POST["pic"];
	//Stores the filename as it was on the client computer.
	$imagename = $_FILES["pic"]["name"];
	//Stores the filetype e.g image/jpeg
	$imagetype = $_FILES["pic"]["type"];
	//Stores any error codes from the upload.
	$imageerror = $_FILES["pic"]["error"];
	//Stores the tempname as it is given by the host when uploaded.
	$imagetemp = $_FILES["pic"]["tmp_name"];

	//The path you wish to upload the image to
	$imagePath = "images/";

	if(is_uploaded_file($imagetemp)) {
		if(move_uploaded_file($imagetemp, $imagePath . $imagename)) {
			echo "Successfully uploaded the image.";
		}
		else {
			echo "Failed to move the image.";
		}
	}
	else {
		echo "Failed to upload the image.";
	}
?>