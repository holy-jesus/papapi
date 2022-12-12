var db;
var dbVersion = 1;

document.addEventListener('DOMContentLoaded', () => {
    initDb();
    document.querySelector('#picture').addEventListener('change', saveImage);
    $("body").css("opacity", "1");
});

function close() {
    sessionStorage.setItem("step", 2);
    db.close()
    $("body").css("opacity", "0");
    setTimeout(function () {
        window.location.href = "/second_step";
    }, 500);
};

function initDb() {
    var request = indexedDB.open('diplomas', dbVersion);
    request.onerror = function (e) {
        console.error('Unable to open database.');
    };
    request.onsuccess = function (e) {
        db = e.target.result;
        console.log('db opened');
    };
    request.onupgradeneeded = function (e) {
        db = e.target.result;
        db.createObjectStore('image', { keyPath: "timestamp" });
    };
};

function saveImage(e) {
    var file = e.target.files[0];
    var reader = new FileReader();
    reader.readAsBinaryString(file);
    reader.onload = function (e) {
        var bits = e.target.result;
        var ob = {
            timestamp: Date.now(),
            data: bits
        };
        var trans = db.transaction(['image'], 'readwrite');
        var objectStore = trans.objectStore('image');
        var countRequest = objectStore.count();
        countRequest.onsuccess = () => {
            var amount = countRequest.result;
            var openCursorRequest = objectStore.openCursor(null);
            openCursorRequest.onsuccess = function (event) {
                var cursor = event.target.result;
                if (cursor && amount >= 5) {
                    objectStore.delete(cursor.key);
                    amount = amount - 1;
                    cursor.continue();
                }
            }
            var addReq = objectStore.add(ob);
            addReq.onerror = (e) => {
                console.log('Error storing data');
                console.error(e);
            };
            addReq.onsuccess = function (e) {
                console.log("Added image to IndexedDB")
                close();
            };
        };
    };
};