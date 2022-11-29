let db;
let dbVersion = 1;
var columnsFromCsv = Object.keys(JSON.parse(sessionStorage.getItem("csv"))[0]);
var dataToBackend = {"fields": {}};
var current = 0;


document.addEventListener('DOMContentLoaded', () => {
    dataToBackend["csv"] = JSON.parse(sessionStorage.getItem("csv"));
    for (const column of columnsFromCsv) {
        dataToBackend["fields"][column] = {"font": "Ubuntu-L.ttf", "size": 16, "color": (0, 0, 0, 255)}
    }
    document.getElementById("columnName").innerHTML = columnsFromCsv[current]
    initDb(loadImage);
});


function initDb(callback) {
    let request = indexedDB.open('diplomas', dbVersion);
    request.onerror = function (e) {
        console.error('Unable to open database.');
    }
    request.onsuccess = function (e) {
        db = e.target.result;
        console.log('db opened');
        callback();
    }
    request.onupgradeneeded = function (e) {
        db = e.target.result;
        db.createObjectStore('image', { keyPath: "timestamp" });
        callback();
    }
}

function loadImage() {
    let image = document.querySelector('#iimage');
    let trans = db.transaction(['image'], 'readonly');
    let objectStore = trans.objectStore('image');
    var openCursorRequest = objectStore.openCursor(null, 'prev');

    openCursorRequest.onsuccess = function (event) {
        if (event.target.result) {
            let maxTimeStamp = event.target.result.value;
            let req = objectStore.get(maxTimeStamp['timestamp']);
            req.onsuccess = function (e) {
                let record = e.target.result;
                dataToBackend["template"] = btoa(record.data);
                image.src = 'data:image/png;base64,' + btoa(record.data);
            }
        }

    };
}

// font
function update1(c) {
    dataToBackend["fields"][columnsFromCsv[current]]["font"] = c;
}

// font size
function update2(c) {
    dataToBackend["fields"][columnsFromCsv[current]]["size"] = c;
}

function printMousePos(event) {
    var elemRect = event.target.getBoundingClientRect();
    console.log(elemRect)
    console.log((event.clientX - elemRect.left) + "|" + (event.clientY - elemRect.top))
    if (event.target.tagName == "IMG") {
        if ((current + 2) > columnsFromCsv.length) {
            document.getElementById("showpreview").removeAttribute("hidden")
            document.getElementById("buttonnext").removeAttribute("hidden")
        }
        else if ((current + 2) <= columnsFromCsv.length) {
            document.getElementById("nextcolumn").removeAttribute("hidden")
            document.getElementById("showpreview").removeAttribute("hidden")
        }

        dataToBackend["fields"][columnsFromCsv[current]]['percentage'] = [((event.clientX - elemRect.left) / elemRect.width), ((event.clientY - elemRect.top) / elemRect.height)]
        dataToBackend["fields"][columnsFromCsv[current]]["size"] = document.getElementById("b").value
    }
}

function download_preview() {
    font = document.getElementById("a")
    font_size = document.getElementById("b")
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.onreadystatechange = function () {
        if (xmlHttp.readyState == 4 && xmlHttp.status == 200) {
            js = JSON.parse(xmlHttp.response)
            document.querySelector('#iimage').src = 'data:image/png;base64,' + js['image']
        }
    }
    xmlHttp.open("POST", "/preview", true); // true for asynchronous 
    xmlHttp.setRequestHeader("Content-type", "application/json")
    console.log(dataToBackend)
    xmlHttp.send(JSON.stringify(dataToBackend));

}

function next() {
    current = current + 1
    if ((current + 1) > columnsFromCsv.length) {
        document.getElementById("nextcolumn").setAttribute("hidden", true)
    }
    else if ((current + 1) <= columnsFromCsv.length) {
        document.getElementById("nextcolumn").setAttribute("hidden", true)
        document.getElementById("showpreview").setAttribute("hidden", true)
    }
    document.getElementById("columnName").innerHTML = columnsFromCsv[current]
}

function prev() {
    if ((current + 2) > columnsFromCsv.length) {
        document.getElementById("nextcolumn").setAttribute("hidden", true)
    }
    else if ((current + 2) <= columnsFromCsv.length) {
        document.getElementById("nextcolumn").setAttribute("hidden", true)
        document.getElementById("showpreview").setAttribute("hidden", true)
    }
    document.getElementById("columnName").innerHTML = columnsFromCsv[current + 1]
    current = current + 1
}

function nextPage() {
    sessionStorage.setItem("dataToBackend", JSON.stringify(dataToBackend))
    window.location.href = "/result"
}

document.addEventListener("click", printMousePos);