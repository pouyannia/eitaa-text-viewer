
const messagesContainer = document.getElementById("messages");
const statusElement = document.getElementById("status");
const refreshButton = document.getElementById("refreshBtn");

// تبدیل تاریخ ISO به تاریخ و ساعت شمسی
function formatDate(dateString) {
    if (!dateString) return "تاریخ نامشخص";

    const date = new Date(dateString);

    if (isNaN(date.getTime())) {
        return dateString;
    }

    return new Intl.DateTimeFormat("fa-IR", {
        dateStyle: "medium",
        timeStyle: "short",
        timeZone: "Asia/Tehran"
    }).format(date);
}

// نمایش پیام‌ها
function displayMessages(messages) {

    messagesContainer.innerHTML = "";

    if (!messages || messages.length === 0) {
        messagesContainer.innerHTML =
            '<p class="empty">پیامی برای نمایش وجود ندارد.</p>';

        statusElement.textContent = "پیامی دریافت نشد";
        return;
    }

    messages.forEach(message => {

        const article = document.createElement("article");
        article.className = "message";

        const content = document.createElement("div");
        content.className = "content";
        content.textContent = message.text;

        const date = document.createElement("span");
        date.className = "date";
        date.textContent = formatDate(message.published_at);

        article.appendChild(content);
        article.appendChild(date);

        messagesContainer.appendChild(article);
    });

    statusElement.textContent =
        `${messages.length} پیام نمایش داده شد`;
}

// دریافت اطلاعات از فایل JSON
async function refreshMessages() {

    refreshButton.disabled = true;
    statusElement.textContent = "در حال دریافت پیام‌ها...";

    try {

        const response = await fetch(
            `messages.json?t=${Date.now()}`,
            { cache: "no-store" }
        );

        if (!response.ok) {
            throw new Error("HTTP Error: " + response.status);
        }

        const data = await response.json();

        displayMessages(data.messages);

    } catch (error) {

        console.error(error);

        statusElement.textContent =
            "خطا در دریافت اطلاعات";

        messagesContainer.innerHTML =
            '<p class="empty">دریافت پیام‌ها ناموفق بود. دوباره تلاش کنید.</p>';

    } finally {

        refreshButton.disabled = false;
    }
}

// اتصال دکمه به‌روزرسانی
refreshButton.addEventListener("click", refreshMessages);

// دریافت اولیه
refreshMessages();
