document.addEventListener('DOMContentLoaded', () => {
    $("body").css("opacity", "1");
});

function close() {
    $("body").css("opacity", "0");
    setTimeout(function() {
        window.location.href = "/";
    }, 500);
}

function downloadResult() {
    window.location.href = "/download?id=" + sessionStorage.getItem("id")
}

function restart(c) {
    sessionStorage.clear()
    close();
}