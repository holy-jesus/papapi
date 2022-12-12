document.addEventListener('DOMContentLoaded', () => {
    document.querySelector('#csv').addEventListener('change', saveCSV);
    $("body").css("opacity", "1");
});

function close() {
    sessionStorage.setItem("step", 3);
    $("body").css("opacity", "0");
    setTimeout(function() {
        window.location.href = "/third_step";
    }, 500);
}

function saveCSV(e) {
    let file = e.target.files[0];
    Papa.parse(file, {
        header: true,
        complete: function(result) {
            console.log(result.data)
            sessionStorage.setItem("csv", JSON.stringify(result.data))
            sessionStorage.setItem("step", 3)
            close();
        }
    });
}