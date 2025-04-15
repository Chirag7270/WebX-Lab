function checkUsername(username) {
	const xhr = new XMLHttpRequest();
	xhr.open("POST", "check-username.php", true);
	xhr.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
	xhr.onreadystatechange = function () {
	  if (xhr.readyState === 4 && xhr.status === 200) {
		document.getElementById("usernameStatus").innerText = xhr.responseText;
	  }
	};
	xhr.send("username=" + encodeURIComponent(username));
  }
  
  function autoSuggestCollege(input) {
	const xhr = new XMLHttpRequest();
	xhr.open("GET", "colleges.json", true);
	xhr.onreadystatechange = function () {
	  if (xhr.readyState === 4 && xhr.status === 200) {
		const colleges = JSON.parse(xhr.responseText);
		let matches = colleges.filter(c => c.toLowerCase().startsWith(input.toLowerCase()));
		let suggestions = matches.map(c => `<div onclick="selectCollege('${c}')">${c}</div>`).join('');
		document.getElementById("suggestions").innerHTML = suggestions;
	  }
	};
	xhr.send();
  }
  
  function selectCollege(college) {
	document.getElementById("college").value = college;
	document.getElementById("suggestions").innerHTML = '';
  }
  
  function submitForm() {
	const name = document.getElementById("name").value;
	const college = document.getElementById("college").value;
	const username = document.getElementById("username").value;
	const password = document.getElementById("password").value;
	const repassword = document.getElementById("repassword").value;
  
	if (name === "") {
	  alert("Name cannot be empty!");
	  return;
	}
	if (password !== repassword) {
	  alert("Passwords do not match!");
	  return;
	}
  
	const xhr = new XMLHttpRequest();
	xhr.open("POST", "register.php", true);
	xhr.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
  
	xhr.onreadystatechange = function () {
	  if (xhr.readyState === 4 && xhr.status === 200) {
		document.getElementById("responseMessage").innerText = xhr.responseText;
	  }
	};
  
	const data = `name=${encodeURIComponent(name)}&college=${encodeURIComponent(college)}&username=${encodeURIComponent(username)}&password=${encodeURIComponent(password)}`;
	xhr.send(data);
  }
  