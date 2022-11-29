document.addEventListener('DOMContentLoaded', () => {
    
    document.querySelector('#csv').addEventListener('change', saveCSV);
});

function saveCSV(e) {
    let file = e.target.files[0];
    Papa.parse(file, {
        header: true,
        complete: function(result) {
            console.log(result.data)
            sessionStorage.setItem("csv", JSON.stringify(result.data))
            sessionStorage.setItem("step", 3)
            window.location.href = "/third_step"
        }
    });
}