const reg_email = $("#reg_email");
const reg_pass_one = $("#reg_pass_one");
const reg_pass_two = $("#reg_pass_two");

const reg_email_note = $("#reg_email_note");
const reg_pass_two_note = $("#reg_pass_two_note");
const all_reg_note = $("#all_reg_note");

const validateEmail = (email) => {
  return String(email)
    .toLowerCase()
    .match(
      /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/
    );
};

function register(e) {
	e.preventDefault();
	console.log("enter")
	all_reg_note.text("");
	reg_email_note.text("");
	reg_pass_two_note.text("");

	if (reg_email.val() == null || reg_email.val() == "" ||
		reg_pass_one.val() == null || reg_pass_one.val() == "" ||
		reg_pass_two.val() == null || reg_pass_two.val() == ""
	) {	
		all_reg_note.text("Empty fields");

	} else if (!validateEmail(reg_email.val()) || reg_email.val() == "") {
		reg_email_note.text("Invalid Email");

	} else if ((reg_pass_one.val()).length < 3 ) {
		reg_pass_two_note.text("Password very short");

	} else if (reg_pass_one.val() !== reg_pass_two.val()) {
		reg_pass_two_note.text("Password not identical");

	} else {
		const data = {
			reg_email: reg_email.val(),
			reg_pass: reg_pass_one.val(),
		};
		console.log(data)
		$.post("http://127.0.0.1:5000/register", data, function(result){
			all_reg_note.text(result.msg);
			if (result.status) {
				all_reg_note.css("color", "green");
			} else {
				all_reg_note.css("color", "red");
			}
		});
	}
}

$("#reg_btn").click(register);
