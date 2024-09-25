const guessInput = document.querySelector('#guess');
const submitButton = document.querySelector('#submit-guess');
const feedback = document.querySelector('#feedback')
const displayedScore = document.querySelector('#score-count')

const wordsFound= [];

getScore();

async function getScore() {
    res = await axios.get('/score');
    displayedScore.innerHTML = `Score: ${res.data.score}`;
}

async function handleSubmit(evt){
    evt.preventDefault();
    word = guessInput.value;
    
    // make sure input is not blank
    if (guessInput.value === ''){
        return }
    
    // don't allow same word twice
    if (wordsFound.indexOf(word) !== -1){
        showResponse('Already found!');
        guessInput.value = '';
        return
    }

    // get response from server
    const res = await axios.get(`/check?guess=${word}`);
    
    if (res.data.result === "not-word"){
        showResponse('Not a word!');
        guessInput.value = '';
    }
    
    if (res.data.result === "not-on-board"){
        showResponse('Not on board!');
        guessInput.value = '';
    }
    if (res.data.result === "ok"){
        showResponse(`&check;`)
        displayedScore.innerHTML = `Score: ${res.data.score}`;
        guessInput.value = '';
        wordsFound.push(word)
    }

}

function showResponse(msg){
    feedback.innerHTML = `${msg}`;
    setTimeout(function(){
        feedback.innerHTML = '';
    }, 2000)
}

submitButton.addEventListener('click', handleSubmit)
