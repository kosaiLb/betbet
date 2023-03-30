const log_email = $("#log_email");
const log_pass = $("#log_pass");

const all_log_note = $("#all_log_note");

const validateEmail = (email) => {
  return String(email)
    .toLowerCase()
    .match(
      /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/
    );
};

function login(e) {
	e.preventDefault();
	all_log_note.text("");

	if (log_email.val() == null || log_email.val() == "" ||
		log_pass.val() == null || log_pass.val() == ""
	) {
		all_log_note.text("Empty fields");

	} else if (!validateEmail(log_email.val()) || log_email.val() == "") {
		all_log_note.text("Invalid Email");

	} else if ((log_pass.val()).length < 3 ) {
		all_log_note.text("Password very short");

	} else {
		const data = {
			log_email: log_email.val(),
			log_pass: log_pass.val(),
		};
		$.post("http://127.0.0.1:5000/login", data, function(result){

			if (result.status) {
				sessionStorage.setItem("log_hash", result.session);
				sessionStorage.setItem("log_user_id", result.log_user_id);
				window.location.replace("http://localhost:5000/dash");
			}
			all_log_note.text(result.msg);
		});
	}

}

$("#log_btn").click(login);
