(function () {
    const tabs = ["rooms", "reviews", "services", "policies", "location"];
    document.querySelectorAll(".tab-btn").forEach((btn) => {
    btn.addEventListener("click", () => {
        const t = btn.dataset.tab;
        // header styling
        document.querySelectorAll(".tab-btn").forEach((b) => {
        b.classList.remove("border-b-2", "border-blue-600", "text-blue-600");
        b.classList.add("text-slate-600");
        });
        btn.classList.add("border-b-2", "border-blue-600", "text-blue-600");
        // content switching
        tabs.forEach((id) =>
        document.getElementById(`tab-${id}`)?.classList.add("hidden")
        );
        document.getElementById(`tab-${t}`)?.classList.remove("hidden");
        });
    });
})();

// Guest Reviews Modal
(function () {
    const modal = document.getElementById("reviewsModal");
    const openBtn = document.getElementById("openReviewsModal");
    const closeBtn = document.getElementById("closeReviewsModal");
    const overlay = modal?.querySelector("[data-close]");

    function open() {
    modal.classList.remove("hidden");
    modal.classList.add("flex"); // to center
    document.body.style.overflow = "hidden";
    }
    function close() {
        modal.classList.add("hidden");
        modal.classList.remove("flex");
        document.body.style.overflow = "";
    }

    openBtn?.addEventListener("click", (e) => {
    e.preventDefault();
    open();
    });
    closeBtn?.addEventListener("click", close);
    overlay?.addEventListener("click", close);
    window.addEventListener("keydown", (e) => {
    if (e.key === "Escape" && !modal.classList.contains("hidden")) close();
    });
})();
