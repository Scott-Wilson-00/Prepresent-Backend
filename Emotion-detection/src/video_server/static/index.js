

begin_presenting = () => fetch("http://127.0.0.1:8080/present", {method: "GET", mode: 'no-cors'})
.then(function (response) {
    location.reload()
}).then (function (text) {
    console.log(text)
})

stop_presenting = () => fetch("http://127.0.0.1:8080/stop-presenting", {method: "GET", mode: 'no-cors'})
.then(function (response) {
    location.reload()
}).then (function (text) {
    console.log(text)
})