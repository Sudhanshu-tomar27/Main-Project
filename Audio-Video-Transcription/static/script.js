let processing = false;

document.addEventListener("DOMContentLoaded", function () {
    const forms = document.querySelectorAll("form");

    forms.forEach(form => {
        let clickedButtonValue = null;

        // Track which button was clicked
        form.querySelectorAll("button[type='submit']").forEach(button => {
            button.addEventListener("click", function () {
                clickedButtonValue = this.value;
            });
        });

        form.addEventListener("submit", function (e) {
            if (processing) return;
            processing = true;

            const action = clickedButtonValue || "transcript";

            let title = "Processing...";
            let text = "Please wait while AI is working...";

            if (action === "transcript") {
                title = "Generating Transcript";
                text = "Converting audio/video into verbatim text...";
            } else if (action === "summary") {
                title = "Creating AI Summary";
                text = "AI is analyzing content and generating key takeaways...";
            } else if (action === "notes") {
                title = "Preparing Audio / Video Notes";
                text = "Generating structured lecture notes and MOM...";
            } else if (action === "qa") {
                title = "Generating Interview Q&A";
                text = "Creating interview questions and comprehensive answers...";
            }

            showProcessing(title, text);
        });
    });
});

function showProcessing(title, text) {
    let box = document.getElementById("processing");

    if (box) {
        box.style.display = "flex";
        const titleEl = document.getElementById("process-title");
        const textEl = document.getElementById("process-text");
        if (titleEl) titleEl.innerHTML = title;
        if (textEl) textEl.innerHTML = text;
    }

    document.title = "⏳ Processing AI Documentation...";
}
