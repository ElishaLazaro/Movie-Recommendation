// Smooth scroll to top function
function scrollToTop() {
    window.scrollTo({
        top: 0,
        behavior: 'smooth'
    });
}

document.addEventListener('DOMContentLoaded', function () {
    // Handle poster image errors
    const posters = document.querySelectorAll('.movie-poster');

    posters.forEach(poster => {
        poster.addEventListener('error', function () {
            console.log('Poster failed to load:', this.src);
            this.src = 'static/placeholder.jpg';
            this.classList.add('poster-error');
        });
    });




});


//-----------------CHATBOT CODING-----------------------

let movies = [];
let chatbotContext = 'initial';
let currentRecommendations = [];

document.addEventListener('DOMContentLoaded', async function () {

    const needHelpBtn = document.getElementById('needHelpBtn');
    const chatbotWidget = document.getElementById('chatbotWidget');
    const closeChatbot = document.getElementById('closeChatbot');
    const chatbotMessages = document.getElementById('chatbotMessages');
    const userInput = document.getElementById('userInput');
    const sendMessage = document.getElementById('sendMessage');

    needHelpBtn.addEventListener('click', function () {
        chatbotWidget.classList.remove('hidden');
        if (chatbotMessages.children.length === 0) {
            addBotMessage("Hello! I'm here to help you find movies. What kind of movie are you looking for? You can search by genre, year, or rating.");
        }
    });

    closeChatbot.addEventListener('click', function () {
        chatbotWidget.classList.add('hidden');
        resetChatbot();
    });

    sendMessage.addEventListener('click', handleUserInput);
    userInput.addEventListener('keypress', function (e) {
        if (e.key === 'Enter') {
            handleUserInput();
        }
    });

    function handleUserInput() {
        const message = userInput.value.trim();
        if (message) {
            addUserMessage(message);
            processUserInput(message);
            userInput.value = '';
        }
    }

    function addUserMessage(message) {
        const messageElement = document.createElement('div');
        messageElement.className = 'mb-2 text-right';
        messageElement.innerHTML = `<span class="bg-blue-500 text-white rounded-lg py-2 px-3 inline-block">${message}</span>`;
        chatbotMessages.appendChild(messageElement);
        chatbotMessages.scrollTop = chatbotMessages.scrollHeight;
    }

    function addBotMessage(message) {
        const messageElement = document.createElement('div');
        messageElement.className = 'mb-2';
        messageElement.innerHTML = `<span class="bg-gray-200 rounded-lg py-2 px-3 inline-block">${message}</span>`;
        chatbotMessages.appendChild(messageElement);
        chatbotMessages.scrollTop = chatbotMessages.scrollHeight;
    }

    function resetChatbot() {
        chatbotContext = 'initial';
        currentRecommendations = [];
        chatbotMessages.innerHTML = '';
        addBotMessage("Hello! I'm here to help you find movies. What kind of movie are you looking for? You can search by genre, year, or rating.");
    }


    function processUserInput(input) {
        switch (chatbotContext) {
            case 'initial':
                if (input.toLowerCase().includes('genre')) {
                    chatbotContext = 'genre';
                    addBotMessage("Great! What genre are you interested in? (e.g., Action, Comedy, Drama)");
                    userInput.placeholder = "ex: Drama, Romance, Action"
                } else if (input.toLowerCase().includes('year')) {
                    chatbotContext = 'year';
                    addBotMessage("Sure! What year or range of years are you looking for? (e.g., 2020 or 2010-2020)");
                    userInput.placeholder = "ex: 1993 - 2010"
                } else if (input.toLowerCase().includes('rating')) {
                    chatbotContext = 'rating';
                    addBotMessage("Okay! What rating range are you looking for? (e.g., 7-10 for highly rated movies)");
                    userInput.placeholder = "ex: 6.7 - 7.8"
                } else {
                    addBotMessage("I can help you find movies by genre, year, or rating. Which would you like to search by?");
                }
                break;
            case 'genre':
                fetchMoviesByGenre(input);
                break;
            case 'year':
                fetchMoviesByYearRange(input);
                break;
            case 'rating':
                fetchMoviesByRatingRange(input);
                break;
            case _:
                chatbotContext = initial

            // case 'more_movies':
            //     if (input.toLowerCase().includes('yes') || input.toLowerCase().includes('sure')) {
            //         displayMoreMovies();
            //     } else {
            //         addBotMessage("Alright! Is there anything else you'd like to know about movies?");
            //         chatbotContext = 'initial';
            //     }
            //     break;
            // case 'movie_details':
            //     const movieDetails = getMovieDetails(input);
            //     if (movieDetails) {
            //         addBotMessage(movieDetails);
            //     } else {
            //         addBotMessage("I'm sorry, I couldn't find details for that movie. Would you like to see more movie recommendations or start a new search?");
            //     }
            //     chatbotContext = 'initial';
            //     break;
        }
    }

    function fetchMoviesByRatingRange(ratingRange) {
        addBotMessage("Redirecting to recommend page. Please wait...");
        setTimeout(() => {
            let r = ratingRange.trim()
            r = r.split("-")

            window.location.href = `recommend.html?by=rating&min=${r[0]}&max=${r[1]}`
        }, 1000 * 2)
    }
    function fetchMoviesByYearRange(yearRange) {
        addBotMessage("Redirecting to recommend page. Please wait...");
        setTimeout(() => {
            let y = yearRange.trim()
            y = y.split("-")

            window.location.href = `recommend.html?by=year&min=${y[0]}&max=${y[1]}`
        }, 1000 * 2)
    }
    function fetchMoviesByGenre(genre) {
        addBotMessage("Redirecting to recommend page. Please wait...");
        setTimeout(() => {
            let g = genre.trim()
            g = g.split(",")
            const genres = g.map((ge) => ge[0].toUpperCase() + ge.slice(1).toLowerCase())
            g = encodeURIComponent(btoa(JSON.stringify(genres)))

            window.location.href = `recommend.html?by=genre&g=${g}`
        }, 1000 * 2)
    }


});
