import matplotlib.pyplot as plt
import matplotlib
import io
import urllib, base64
from django.shortcuts import render
from django.http import HttpResponse

from .models import Movie

def home(request):
    #return HttpResponse('<h1>Welcome to Home Page</h1>')
    # return render(request,'home.html', {'name':'<span style="color: green;">Santiago Palacio</span>'})
    searchTerm = request.GET.get('searchMovie')
    if searchTerm:
        movies = Movie.objects.filter(title__icontains=searchTerm)
    else:
        movies = Movie.objects.all()
    return render(request,'home.html',{'searchTerm':searchTerm ,'movies':movies})

def about(request):
    # return HttpResponse('<h1>Welcome to About Page</h1>')
    return render(request,'about.html')

def singup(request):
    email = request.GET.get('email')
    return render(request,'singup.html',{'email':email})


def statistics_view(request):
    matplotlib.use('Agg')
    all_movies = Movie.objects.all()
    
    # Diccionarios para almacenar la cantidad de películas por año y por género
    movie_counts_by_year = {}
    movie_counts_by_genre = {}
    
    for movie in all_movies:
        # Contar películas por año
        year = movie.year if movie.year else "None"
        movie_counts_by_year[year] = movie_counts_by_year.get(year, 0) + 1
        
        # Contar películas por género (considerando solo el primer género)
        if movie.genre:
            first_genre = movie.genre.split(',')[0].strip()  # Suponiendo que los géneros están separados por comas
            movie_counts_by_genre[first_genre] = movie_counts_by_genre.get(first_genre, 0) + 1
    
    def generate_graph(data, title, xlabel, ylabel):
        bar_width = 0.5
        bar_positions = range(len(data))
        
        plt.figure(figsize=(10, 5))
        plt.bar(bar_positions, data.values(), width=bar_width, align='center')
        plt.title(title)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.xticks(bar_positions, data.keys(), rotation=90)
        plt.subplots_adjust(bottom=0.3)
        
        buffer = io.BytesIO()
        plt.savefig(buffer, format='png')
        buffer.seek(0)
        plt.close()
        
        image_png = buffer.getvalue()
        buffer.close()
        
        return base64.b64encode(image_png).decode('utf-8')
    
    graphic_years = generate_graph(movie_counts_by_year, 'Movies per Year', 'Year', 'Number of Movies')
    graphic_genres = generate_graph(movie_counts_by_genre, 'Movies per Genre', 'Genre', 'Number of Movies')
    
    return render(request, 'statistics.html', {'graphic_years': graphic_years, 'graphic_genres': graphic_genres})