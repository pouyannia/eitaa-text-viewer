
// Eitaa Text Viewer

const messagesContainer = document.getElementById("messages");
const statusElement = document.getElementById("status");
const refreshButton = document.getElementById("refreshBtn");

// Sample messages for testing

const sampleMessages = [
    {
        text: "به گزارش خبرگزاری فارس، آخرین اخبار و رویدادهای کشور را در این کانال دنبال کنید.",
        date: "2026-11-01 14:00"
    },
    {
        text: "این یک پیام آزمایشی برای بررسی نحوه نمایش مطالب در صفحه است.",
        date: "2026-11-01 13:30"
    }
];

// Display messages

function displayMessages(messages) {

    messagesContainer.innerHTML = "";

    messages.forEach(message => {

        const article = document.createElement("article");
        article.className = "message";

        const content = document.createElement("div");
        content.textContent = message.text;

        const date = document.createElement("span");
        date.className = "date";
        date.textContent = message.date;

        article.appendChild(content);
        article.appendChild(date);

        messagesContainer.appendChild(article);

    });

    statusElement.textContent =
        `${messages.length} پیام نمایش داده شد`;

}

// Refresh

function refreshMessages() {

    statusElement.textContent = "در حال به‌روزرسانی...";

    displayMessages(sampleMessages);

}

// Button event

refreshButton.addEventListener("click", refreshMessages);

// Initial display

refreshMessages();
