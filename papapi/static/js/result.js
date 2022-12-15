if (!sessionStorage.getItem("id") || sessionStorage.getItem("step") < 4) {
    sessionStorage.clear()
    window.location.href = "/"
}

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

function restart() {
    sessionStorage.clear()
    close();
}