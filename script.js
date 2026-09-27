

let y = 0
let game = document.getElementById("game")
let flags = []

for (let i = 0; i < 10; i++) {

    const element = document.createElement("img");
    element.src = "4x3/0 (" + Math.floor(Math.random() * 271 + 1) + ").svg"
    flags.push(element)
    game.appendChild(element)
    function fall() {

        let time = Math.floor(Math.random() * 50000 + 5000)
        element.style.transitionDuration = time + "ms"

        setTimeout(function () {
            element.style.top = window.innerHeight + "px"
            // y+=4
            element.style.transform = "rotate(2160deg)"
        }, 1000)

        setTimeout(function zzz() {

            console.log(Math.random() * 50000)
            element.style.transitionDuration = " 0ms"
            element.style.top = 0
            element.style.transform = "rotate(0deg)"
            element.style.left = Math.floor(Math.random() * game.offsetWidth) + "px"
            setTimeout(function () {
                fall()


            }, 500)

        }, time)
    }
    fall()
}


// _______________________________________________

let reset = document.getElementById("reset")
let timer = document.getElementById("timer")
let modalButton = document.getElementById("modalButton")
let startModal = document.getElementById("startModal")
modalButton.addEventListener('click', startTimer)


reset.addEventListener('click', ()=>   console.log(89898) )



console.log(reset);

function startTimer() {
   
    console.log(77777);
    startModal.style.opacity = 0
    startModal.style.pointerEvents = "none"

    // let timerSeconds = 18
    // let minutes = 0
    // let seconds = 0
    // const gameinterval = setInterval(() => {
    //     console.log(666);
    //     timerSeconds -= 1
    //     minutes = Math.floor(timerSeconds / 60)
    //     seconds = timerSeconds % 60
    //     let formattedSeconds = seconds < 10 ? "0" + seconds : seconds


    //     timer.innerHTML = minutes + "." + formattedSeconds
    //     if (timerSeconds == 0) {
    //         clearInterval(gameinterval)
    //     }


    // }, 1000);




}