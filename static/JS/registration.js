document.addEventListener("DOMContentLoaded", function () {
    const registrationForm = document.querySelector("#registrationForm");

    registrationForm.addEventListener("submit", function (event) {
        event.preventDefault();

        const prn = document.querySelector("#exampleDatepicker1").value;
        const name = document.querySelector("#form3Example1q").value;
        const year = document.querySelector("#domain").value;
        const email = document.querySelector("#form3Example1w").value;

        const formData = new FormData();
        formData.append("prn", prn);
        formData.append("name", name);
        formData.append("year", year);
        formData.append("email", email);

        fetch("/register", {
            method: "POST",
            body: formData,
        })
            .then((response) => response.json())
            .then((data) => {
                if (data.success) {
                    // Registration was successful, you can redirect the user or show a success message
                    alert("Registration successful!");
                    // You can redirect the user to another page if needed
                    // window.location.href = "/success";
                } else {
                    // Registration failed, show an error message
                    alert("Registration failed. Please try again.");
                }
            })
            .catch((error) => {
                console.error("Error:", error);
                alert("An error occurred. Please try again later.");
            });
    });
});
