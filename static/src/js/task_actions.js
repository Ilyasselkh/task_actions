/** @odoo-module **/

const STATUS_WORDS = {
    overdue: ["en retard", "overdue"],
    today: ["aujourd'hui", "today"],
    done: ["realisee", "realise", "terminee", "termine", "done"],
};

function hasAnyWord(text, words) {
    return words.some((word) => text.includes(word));
}

function getText(element) {
    return (element.textContent || "")
        .trim()
        .toLowerCase()
        .normalize("NFD")
        .replace(/[\u0300-\u036f]/g, "");
}

function enrichActionCards(root = document) {
    root.querySelectorAll(".ta_kanban_card, .ta_form_sheet").forEach((element, index) => {
        if (!element.classList.contains("ta_dynamic_ready")) {
            element.style.animationDelay = `${Math.min(index * 35, 180)}ms`;
            element.classList.add("ta_dynamic_ready");
        }

        const text = getText(element);
        const isOverdue = hasAnyWord(text, STATUS_WORDS.overdue);
        const isToday = hasAnyWord(text, STATUS_WORDS.today);
        const isDone = hasAnyWord(text, STATUS_WORDS.done);

        element.classList.toggle("ta_is_overdue", isOverdue);
        element.classList.toggle("ta_is_today", isToday);
        element.classList.toggle("ta_is_done", isDone);
        element.classList.toggle("ta_attention", isOverdue && !isDone);
    });
}

function startActionObserver() {
    enrichActionCards();

    const observer = new MutationObserver((mutations) => {
        for (const mutation of mutations) {
            if (mutation.type === "childList" || mutation.type === "characterData") {
                enrichActionCards();
                break;
            }
        }
    });

    observer.observe(document.body, {
        childList: true,
        characterData: true,
        subtree: true,
    });
}

if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", startActionObserver, { once: true });
} else {
    startActionObserver();
}
