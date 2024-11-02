

        // Smooth scroll to top function
        function scrollToTop() {
            window.scrollTo({
                top: 0,
                behavior: 'smooth'
            });
        }

        document.addEventListener('DOMContentLoaded', function() {
        // Handle poster image errors
        const posters = document.querySelectorAll('.movie-poster');
    
        posters.forEach(poster => {
            poster.addEventListener('error', function() {
                console.log('Poster failed to load:', this.src);
                this.src = 'static/placeholder.jpg';
                this.classList.add('poster-error');
            });
        });

        // Optional: Add hover effects for movie posters
        const moviePosters = document.querySelectorAll('.movie-poster');
        moviePosters.forEach(poster => {
            poster.addEventListener('mouseenter', function() {
                this.style.transform = 'scale(1.05)';
            });
            
            poster.addEventListener('mouseleave', function() {
                this.style.transform = 'scale(1)';
            });
        });

        // Optional: Add slider functionality
        const sliderButtons = document.querySelectorAll('.slider-button');
        sliderButtons.forEach(button => {
            button.addEventListener('click', function() {
                const direction = this.dataset.direction;
                const container = this.closest('.movie-section').querySelector('.movie-container');
                const scrollAmount = direction === 'left' ? -220 : 220;
                container.scrollBy({
                    left: scrollAmount,
                    behavior: 'smooth'
                });
            });
        });
      });

        //-----------------CHATBOT CODING-----------------------
    
        let movies = [];
        let chatbotContext = 'initial';
        let currentRecommendations = [];
        
        document.addEventListener('DOMContentLoaded', async function() {
            await fetchMovies();
            
            const needHelpBtn = document.getElementById('needHelpBtn');
            const chatbotWidget = document.getElementById('chatbotWidget');
            const closeChatbot = document.getElementById('closeChatbot');
            const chatbotMessages = document.getElementById('chatbotMessages');
            const userInput = document.getElementById('userInput');
            const sendMessage = document.getElementById('sendMessage');
        
            needHelpBtn.addEventListener('click', function() {
                chatbotWidget.classList.remove('hidden');
                if (chatbotMessages.children.length === 0) {
                    addBotMessage("Hello! I'm here to help you find movies. What kind of movie are you looking for? You can search by genre, year, or rating.");
                }
            });
        
            closeChatbot.addEventListener('click', function() {
                chatbotWidget.classList.add('hidden');
                resetChatbot();
            });
        
            sendMessage.addEventListener('click', handleUserInput);
            userInput.addEventListener('keypress', function(e) {
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
        
            function processUserInput(input) {
                switch(chatbotContext) {
                    case 'initial':
                        if (input.toLowerCase().includes('genre')) {
                            chatbotContext = 'genre';
                            addBotMessage("Great! What genre are you interested in? (e.g., Action, Comedy, Drama)");
                        } else if (input.toLowerCase().includes('year')) {
                            chatbotContext = 'year';
                            addBotMessage("Sure! What year or range of years are you looking for? (e.g., 2020 or 2010-2020)");
                        } else if (input.toLowerCase().includes('rating')) {
                            chatbotContext = 'rating';
                            addBotMessage("Okay! What rating range are you looking for? (e.g., 7-10 for highly rated movies)");
                        } else {
                            addBotMessage("I can help you find movies by genre, year, or rating. Which would you like to search by?");
                        }
                        break;
                    case 'genre':
                        filterMoviesByGenre(input);
                        break;
                    case 'year':
                        filterMoviesByYear(input);
                        break;
                    case 'rating':
                        filterMoviesByRating(input);
                        break;
                    case 'more_movies':
                        if (input.toLowerCase().includes('yes') || input.toLowerCase().includes('sure')) {
                            displayMoreMovies();
                        } else {
                            addBotMessage("Alright! Is there anything else you'd like to know about movies?");
                            chatbotContext = 'initial';
                        }
                        break;
                    case 'movie_details':
                        const movieDetails = getMovieDetails(input);
                        if (movieDetails) {
                            addBotMessage(movieDetails);
                        } else {
                            addBotMessage("I'm sorry, I couldn't find details for that movie. Would you like to see more movie recommendations or start a new search?");
                        }
                        chatbotContext = 'initial';
                        break;
                }
            }
        
            function filterMoviesByGenre(genre) {
                currentRecommendations = movies.filter(movie => 
                    movie.genre.toLowerCase().includes(genre.toLowerCase())
                );
                displayResults(currentRecommendations);
            }
            
            function filterMoviesByYear(yearInput) {
                if (yearInput.includes('-')) {
                    const [startYear, endYear] = yearInput.split('-').map(Number);
                    currentRecommendations = movies.filter(movie => {
                        const movieYear = parseInt(movie.year);
                        return movieYear >= startYear && movieYear <= endYear;
                    });
                } else {
                    const year = parseInt(yearInput);
                    currentRecommendations = movies.filter(movie => parseInt(movie.year) === year);
                }
                displayResults(currentRecommendations);
            }
            
            function filterMoviesByRating(ratingInput) {
                const [minRating, maxRating] = ratingInput.split('-').map(Number);
                currentRecommendations = movies.filter(movie => {
                    const movieRating = parseFloat(movie.rating);
                    return movieRating >= minRating && movieRating <= maxRating;
                });
                displayResults(currentRecommendations);
            }
            
            function getMovieDetails(movieTitle) {
                const movie = movies.find(m => m.title.toLowerCase() === movieTitle.toLowerCase());
                if (movie) {
                    return `
                        Title: ${movie.title}
                        Year: ${movie.year}
                        Director: ${movie.director}
                        Stars: ${movie.stars}
                        Rating: ${movie.rating}
                        Description: ${movie.description || 'No description available'}
                    `;
                }
                return null;
            }
        
            function resetChatbot() {
                chatbotContext = 'initial';
                currentRecommendations = [];
                chatbotMessages.innerHTML = '';
                addBotMessage("Hello! I'm here to help you find movies. What kind of movie are you looking for? You can search by genre, year, or rating.");
            }
        });

        function displayResults(filteredMovies) {
            if (filteredMovies.length > 0) {
                const movieTitles = filteredMovies.slice(0, 5).map(movie => movie.title).join(', ');
                addBotMessage(`Here are some movies that match your criteria: ${movieTitles}`);
                addBotMessage("Would you like to see more details about any of these movies or see more recommendations?");
                chatbotContext = 'more_movies';
            } else {
                addBotMessage("I couldn't find any movies matching those criteria. Would you like to try a different search?");
                chatbotContext = 'initial';
            }
        }
    
        async function fetchMovies() {
            try {
                console.log('Attempting to fetch CSV file...');
                const response = await fetch('/imdb-movies-dataset.csv'); // Try with ./ first
                
                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }
                
                console.log('CSV file found and loaded');
                const csvText = await response.text();
                console.log('CSV content preview:', csvText.substring(0, 200)); // Show first 200 characters
                
                movies = parseCSV(csvText);
                console.log('Movies loaded successfully:', movies.length, 'movies');
                console.log('Sample movie:', movies[0]); // Show first movie object
                
            } catch (error) {
                console.error('Error loading movies:', error);
                console.log('Attempted path:', '/imdb-movies-dataset.csv');
                console.log('Current location:', window.location.pathname);
                
                // Initialize with sample data as fallback
                movies = [/* your sample movies */];
                console.log('Using sample movie data instead');
            }
        }
        
        function parseCSV(csvText) {
            const lines = csvText.split('\n');
            const headers = lines[0].split(',');
            const movies = [];
        
            for (let i = 1; i < lines.length; i++) {
                const values = lines[i].split(',');
                if (values.length === headers.length) {
                    const movie = {};
                    headers.forEach((header, index) => {
                        movie[header.trim()] = values[index].trim();
                    });
                    movies.push(movie);
                }
            }
        
            return movies;
        }
