document.addEventListener("DOMContentLoaded", function() {
    if (document.querySelector("body").dataset.successAlert === "true") {
        Swal.fire({
            title: 'Success!',
            text: 'You have successfully logged in.',
            icon: 'success',
            confirmButtonText: 'OK'
        });
    }
    if (document.querySelector("body").dataset.errorAlert === "true") {
        Swal.fire({
            title: 'Error!',
            text: 'There was an error logging in. Please try again.',
            icon: 'error',
            confirmButtonText: 'OK'
        });
    }
    if (document.querySelector("body").dataset.warningAlert === "true") {
        Swal.fire({
            title: 'Warning!',
            text: 'Warning',
            icon: 'warning',
            confirmButtonText: 'OK'
        });
    }
});