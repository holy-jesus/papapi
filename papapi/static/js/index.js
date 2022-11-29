let db;
let dbVersion = 1;

document.addEventListener('DOMContentLoaded', () => {
    initDb();
    document.querySelector('#picture').addEventListener('change', saveImage );
    $("body").css("opacity", "1");
});

function close() {
    $("body").css("opacity", "0");
    setTimeout(function() {
        window.location.href = "/second_step";
    }, 500);
}

function initDb() {
    let request = indexedDB.open('diplomas', dbVersion);
    request.onerror = function(e) {
        console.error('Unable to open database.');
    }
    request.onsuccess = function(e) {
        db = e.target.result;
        console.log('db opened');
    }
    request.onupgradeneeded = function(e) {
        db = e.target.result;
        db.createObjectStore('image', {keyPath:"timestamp"});
    }
}

function saveImage(e) {
    let file = e.target.files[0];
    var reader = new FileReader();
    reader.readAsBinaryString(file);
    reader.onload = function(e) {
        let bits = e.target.result;
        let ob = {
            timestamp:Date.now(),
            data:bits
        };
        let trans = db.transaction(['image'], 'readwrite');
        let addReq = trans.objectStore('image').add(ob);
        addReq.onerror = function(e) {
            console.log('error storing data');
            console.error(e);
        }

        trans.oncomplete = function(e) {
            sessionStorage.setItem("step", 2);
            close();
            
        }
    }
}