function uploadAndProcess(action) {
    let fileInput = document.getElementById(`${action}-file`);
    let file = fileInput.files[0];

    if (!file) {
        alert("Please select a file first!");
        return;
    }

    let formData = new FormData();
    formData.append("file", file);

    if (action === "encrypt" || action === "decrypt") {
        let passwordInput = document.querySelector(`#${action}-password`);
        let password = passwordInput.value.trim();
        if (!password) {
            alert("Please enter a password!");
            return;
        }
        formData.append("password", password);
    }

    fetch(`http://127.0.0.1:5000/${action}`, {
        method: "POST",
        body: formData,
    })
        .then(response => {
            if (!response.ok) {
                return response.json().then(err => {
                    alert("You entered the wrong password!");
                    throw new Error(err.error);
                });
            }
            return response.blob();
        })
        .then(blob => {
            let link = document.createElement("a");
            link.href = URL.createObjectURL(blob);
            link.download = file.name +
                (action === "compress" ? ".huff" :
                    action === "encrypt" ? ".enc" :
                        action === "decrypt" ? "" : ".txt");

            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
        })
        .catch(error => {
            console.error("Error:", error);
        });
}
