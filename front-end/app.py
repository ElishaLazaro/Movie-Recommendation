from flask import Flask, render_template
import requests  # for making API calls if you're using a movie API

app = Flask(__name__)

# This is your main route that handles the homepage
@app.route('/')
def home():
    # Example of hardcoded movie data
    popular_movies = [
        {
            'Title': 'The Dark Knight',
            'Poster': 'https://example.com/dark-knight-poster.jpg',
            'Rating': '9.0',
            'Year': '2008'
        },
        {
            'Title': 'Inception',
            'Poster': 'https://example.com/inception-poster.jpg',
            'Rating': '8.8',
            'Year': '2010'
        },
        # Add more movies as needed
    ]
    
    # If you're using an API (like TMDB), you might do something like this:
    '''
    api_key = 'your_api_key'
    response = requests.get(f'https://api.themoviedb.org/3/movie/popular?api_key={api_key}')
    popular_movies = response.json()['results']
    '''
    
    # Render the template and pass the movie data to it
    return render_template('index.html', popular_movies=popular_movies)

# Add more routes as needed
@app.route('/action')
def action():
    # Handle action movies page
    return render_template('action.html')

@app.route('/comedy')
def comedy():
    # Handle comedy movies page
    return render_template('comedy.html')

if __name__ == '__main__':
    app.run(debug=True)