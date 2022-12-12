var db;
var dbVersion = 1;
var columnsFromCsv = Object.keys(JSON.parse(sessionStorage.getItem("csv"))[0]);
var dataToBackend = { "fields": {} };
var current = 0;

const delay = ms => new Promise(res => setTimeout(res, ms));

document.addEventListener('DOMContentLoaded', () => {
    document.querySelector('#font').addEventListener('change', sendFont);
    dataToBackend["csv"] = JSON.parse(sessionStorage.getItem("csv"));
    for (const column of columnsFromCsv) {
        dataToBackend["fields"][column] = { "font": "Arimo-Regular.ttf", "size": 16, "color": (0, 0, 0, 255) }
    }
    document.getElementById("columnName").innerHTML = columnsFromCsv[current]
    initDb(loadImage);
    $("body").css("opacity", "1");
});

function sendFont(e) {
    var file = e.target.files[0];
    var filename = file.name;
    var reader = new FileReader();
    reader.readAsBinaryString(file);
    reader.onload = function (e) {
        var bits = btoa(e.target.result);
        var xmlHttp = new XMLHttpRequest();
        xmlHttp.onreadystatechange = () => {
            if (xmlHttp.readyState == 4 && xmlHttp.status == 200) {
                var select = document.getElementById("a")
                var opt = document.createElement("option")
                opt.value = filename;
                opt.innerHTML = filename;
                select.add(opt)
                select.value = filename;
            }
        }
        xmlHttp.open("POST", "/font", true)
        xmlHttp.setRequestHeader("Content-type", "application/json")
        xmlHttp.send(JSON.stringify({"font": bits, "filename": filename}))
    }

}

function close() {
    sessionStorage.setItem("step", 4);
    db.close()
    $("body").css("opacity", "0");
    setTimeout(function () {
        window.location.href = "/result";
    }, 500);
}

function initDb(callback) {
    var request = indexedDB.open('diplomas', dbVersion);
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
    var image = document.querySelector('#iimage');
    var trans = db.transaction(['image'], 'readonly');
    var objectStore = trans.objectStore('image');
    var openCursorRequest = objectStore.openCursor(null, 'prev');

    openCursorRequest.onsuccess = function (event) {
        if (event.target.result) {
            var maxTimeStamp = event.target.result.value;
            var req = objectStore.get(maxTimeStamp['timestamp']);
            req.onsuccess = function (e) {
                var record = e.target.result;
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
        dataToBackend["fields"][columnsFromCsv[current]]["font"] = document.getElementById("a").value
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
    xmlHttp.open("POST", "/preview", true);
    xmlHttp.setRequestHeader("Content-type", "application/json")
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
    dataToBackend["fields"][columnsFromCsv[current]]["size"] = document.getElementById("b").value
    dataToBackend["fields"][columnsFromCsv[current]]["font"] = document.getElementById("a").value
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

function loading() {
    gsap.timeline({ repeat: -1 })
        .to('.b1', { duration: 0.4, y: -25, ease: 'power3', transformOrigin: '50% 50%' }, 0)
        .to('.b1', { duration: 0.55, y: 55, ease: 'power2.inOut' }, 0.35)
        .to('.b1', { duration: 0.9, x: 120, ease: 'expo.inOut' }, 0.4)
        .to('.b1', { duration: 0.6, scale: 0.82, ease: 'power3.in', yoyo: true, repeat: 1 }, 0.25)
        .to('.b1', { duration: 0.4, y: 0, ease: 'back.out(6)' }, 0.95)
        .to('.b1', { duration: 0.4, rotation: -270, ease: 'power1.in' }, 0.9)

        .to('.b', { duration: 0.9, x: -30, ease: 'expo.inOut', stagger: 0.04 }, 0.3)
        .to('.b', { duration: 0.45, rotation: 5, stagger: 0.04, ease: 'power3.in', transformOrigin: '60% 95%' }, 0.3)
        .to('.b', { duration: 0.4, rotation: 0, stagger: 0.04, ease: 'back.out(10)' }, 0.85)
}

function sweapDisplay() {
    get = document.querySelector.bind(document)

    first = get("#main")
    second = get("#loading")

    first.style.opacity = 0;

    setTimeout(function () {
        first.style.display = "none";
        second.style.display = "block";
    }, 500)

    loading();

    second.style.opacity = 1;
}

async function getId(callback) {
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.onreadystatechange = () => {
        if (xmlHttp.readyState == 4 && xmlHttp.status == 200) {
            var js = JSON.parse(xmlHttp.responseText)
            callback(js["id"])
        }
    }
    xmlHttp.open("POST", "/format", true)
    xmlHttp.setRequestHeader("Content-type", "application/json")
    xmlHttp.send(JSON.stringify(dataToBackend));
}

async function checkIfReady(id) {
    console.log(id)
    var xmlHttp = new XMLHttpRequest();
    var done = false;
    xmlHttp.onreadystatechange = () => {
        if (xmlHttp.readyState == 4 && xmlHttp.status == 200) {
            var js = JSON.parse(xmlHttp.responseText)
            done = js['done']
        }
    };
    while (true) {
        await delay(2000);
        xmlHttp.open("GET", "/status?id=" + id, true);
        xmlHttp.send(null);
        if (done) break;
    };
    sessionStorage.setItem("id", id)
    close();
}

async function nextPage() {

    sweapDisplay();
    getId(checkIfReady);

    // close();
}

document.addEventListener("click", printMousePos);