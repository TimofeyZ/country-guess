import { countries } from "./countries.js";
let y = 0
let game = document.getElementById("game")
let flags = []
for (let i = 0; i < 10; i++) {
    const element = document.createElement("img");
    element.src = "4x3/0 (" + Math.floor(Math.random() * 271 + 1) + ").svg"
    flags.push(element)
    game.appendChild(element)
    function fall() {
        element.style.left = Math.floor(Math.random() * game.offsetWidth) + "px"
        let time = Math.floor(Math.random() * 50000 + 5000)
        element.style.transitionDuration = time + "ms"
        setTimeout(function () {
            element.style.top = window.innerHeight + 110 + "px"
            // y+=4
            element.style.transform = "rotate(2160deg)"
        }, 1000)
        setTimeout(function zzz() {
            console.log(Math.random() * 50000)
            element.style.transitionDuration = " 0ms"
            element.style.top = -50 + "px"
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
let gameinterval
let favicon = document.querySelector("link[rel='shortcut icon']")
let buttons = document.getElementById("buttons")
let reset = document.getElementById("reset")
let image = document.getElementById("img")
let timer = document.getElementById("timer")
let modalButton = document.getElementById("modalButton")
let startModal = document.getElementById("startModal")
let mainImg = document.querySelector("#img")
modalButton.addEventListener('click', startTimer)
let randomCountry = Math.floor(Math.random() * countries.length)
let randomImage = Math.floor(Math.random() * countries[randomCountry].amount + 1)
let trueAnswerAmount = 0
reset.addEventListener('click', () => startTimer())
let score = document.querySelector("#score")
console.log(reset);
let slideCountry = 0
let slideImage = 1
let slideshow
function changeSlide() {
    slideCountry = Math.floor(Math.random() * countries.length)

    slideImage = Math.floor(
        Math.random() * countries[slideCountry].amount + 1
    )

    startModal.style.backgroundImage =
        `url("countries/${countries[slideCountry].name}/0 (${slideImage}).jpg")`
}
let flagCounter = 1
slideshow = setInterval(changeSlide, 10000)
setInterval(

    function () {
        if (flagCounter > 271) {
            flagCounter = 1
        }
        favicon.href = "4x3/0 (" + flagCounter % 271 + ").svg"
        flagCounter++

    }

    , 500)
function startTimer() {
    clearInterval(gameinterval)
    clearInterval(slideshow)
    console.log(77777);
    startModal.style.opacity = 0
    startModal.style.pointerEvents = "none"
    getcountry()
    let timerSeconds = 180
    let minutes = 0
    let seconds = 0
    gameinterval = setInterval(() => {
        console.log(666);
        timerSeconds -= 1
        minutes = Math.floor(timerSeconds / 60)
        seconds = timerSeconds % 60
        let formattedSeconds = seconds < 10 ? "0" + seconds : seconds


        timer.innerHTML = minutes + "." + formattedSeconds
        if (timerSeconds == 0) {
            clearInterval(gameinterval)
            score.innerHTML = "your score: " + trueAnswerAmount
            startModal.style.opacity = 1
            startModal.style.pointerEvents = "auto"
            trueAnswerAmount = 0
            slideshow = setInterval(changeSlide, 3000)
        }


    }, 1000);
}
let trueAnswer
function getcountry() {
    buttons.innerHTML = ""
    buttons.style.pointerEvents = "auto";
    image.src = "countries/" + countries[randomCountry].name + "/0 (" + randomImage + ").jpg"
    trueAnswer = countries[randomCountry].name
    let variants = []
    let randInt = Math.floor(Math.random() * 6 + 2)
    let fakeCountries = [...countries]
    for (let i = 0; i < randInt; i++) {
        variants.push(fakeCountries[randomCountry].name)
        fakeCountries = fakeCountries.filter((c) => c.name != fakeCountries[randomCountry].name)
        randomCountry = Math.floor(Math.random() * fakeCountries.length)
    }
    variants.sort(() => Math.random() - 0.5)
    console.log(variants, trueAnswer);

    for (let i = 0; i < randInt; i++) {
        let button = document.createElement("button")
        buttons.appendChild(button)
        button.innerHTML = variants[i]
        button.id = variants[i]
        button.addEventListener('click', isAnswer)


    }
}
function isAnswer(event) {
    let correctButton = document.getElementById(trueAnswer)
    let selectedAnswer = event.target.id;
    buttons.style.pointerEvents = "none";
    correctButton.style.backgroundColor = "green";
    if (selectedAnswer !== trueAnswer) {
        event.target.style.backgroundColor = "red";
        setTimeout(function () {
            getcountry()


        }, 1000)
    }
    else {
        trueAnswerAmount++
        setTimeout(function () {
            getcountry()


        }, 300)
    }
}