/* =====================================
   FILE UPLOAD DISPLAY
===================================== */

const fileInput = document.querySelector('input[type="file"]');

if (fileInput) {

    fileInput.addEventListener("change", function () {

        if (this.files.length > 0) {

            let fileName = this.files[0].name;

            this.style.color = "#ff2400";

            alert("Selected File: " + fileName);
        }

    });

}


/* =====================================
   AI PROCESSING EFFECT
===================================== */

const forms = document.querySelectorAll("form");

forms.forEach(function (form) {

    form.addEventListener("submit", function (e) {

        const clickedButton =
            document.activeElement;

        let heading = "Processing...";
        let message = "Please wait...";

        if (clickedButton) {

            switch (clickedButton.value) {

                case "transcript":
                    heading = "Generating Transcript...";
                    message = "Converting audio/video into text.";
                    break;

                case "summary":
                    heading = "Generating AI Summary...";
                    message = "Creating professional summary.";
                    break;

                case "notes":
                    heading = "Generating Notes...";
                    message = "Preparing notes with headings.";
                    break;

                case "qa":
                    heading = "Generating Interview Q&A...";
                    message = "Creating interview questions and answers.";
                    break;

                default:
                    heading = "Processing...";
                    message = "Please wait...";
            }

        }

        showLoader(heading, message);

    });

});


function showLoader(title, text) {

    let loader = document.createElement("div");

    loader.className = "processing-box";

    loader.innerHTML = `

        <div class="loader-circle"></div>

        <h3>${title}</h3>

        <p>${text}</p>

    `;

    document.body.appendChild(loader);

}


/* =====================================
   BUTTON CLICK ANIMATION
===================================== */

const buttons = document.querySelectorAll(".buttons button");

buttons.forEach(button => {

    button.addEventListener("click", function () {

        this.disabled = true;

        this.innerHTML = "Processing...";

    });

});


/* =====================================
   PREVENT DOUBLE CLICK
===================================== */

let clicked = false;

document.querySelectorAll("button").forEach(btn => {

    btn.addEventListener("click", function (e) {

        if (clicked) {

            e.preventDefault();

            return;
        }

        clicked = true;

        setTimeout(() => {

            clicked = false;

        }, 3000);

    });

});