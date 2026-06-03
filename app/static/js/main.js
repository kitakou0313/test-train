document.addEventListener("DOMContentLoaded", function () {
    // ダッシュボードの期限切れタスク件数をAPIから取得して更新する
    const overdueEl = document.getElementById("overdue-count");
    if (overdueEl) {
        fetch("/api/tasks/overdue")
            .then((res) => res.json())
            .then((data) => {
                overdueEl.textContent = data.count;
            })
            .catch(() => {});
    }
});
