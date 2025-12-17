import { ref } from 'vue'
import { useHomeService } from '@/services/home.service'
import { useMovieService } from '@/services/movie.service'

export function useCombinedMoviesService() {
  const homeService = useHomeService()
  const movieService = useMovieService()
  
  const moviesCache = ref(new Map())

  const enrichMovies = async (basicMovies) => {
    if (!basicMovies?.length) return []
    
    const moviesWithDetails = await Promise.all(
      basicMovies.map(async (basicMovie) => {
        const movieId = basicMovie.id || basicMovie.film_id
        
        if (moviesCache.value.has(movieId)) {
          return moviesCache.value.get(movieId)
        }

        try {
          const [details, avgRating] = await Promise.all([
            movieService.getFilmDetails(movieId),
            movieService.getAverageRating(movieId)
          ])

          const enrichedMovie = {
            ...basicMovie,
            poster_url: movieService.formatPosterUrl(details.poster_url || details.poster),
            avg_rating: avgRating?.rating || avgRating?.avg_rating || null,
            rating: basicMovie.rating || null
          }

          moviesCache.value.set(movieId, enrichedMovie)
          return enrichedMovie
        } catch (error) {
          console.error(`Error loading details for movie ${movieId}:`, error)
          return basicMovie
        }
      })
    )
    
    return moviesWithDetails
  }

  return {
    async getMoviesWithDetails(category = 'top_films') {
      try {
        const homeData = await homeService.getHomeData()
        const basicMovies = homeData[category]?.items || []
        return await enrichMovies(basicMovies)
      } catch (error) {
        console.error('Error loading movies with details:', error)
        return []
      }
    },

    async enrichActorFilmography(films) {
      return await enrichMovies(films)
    },

    async getAllHomeMoviesWithDetails() {
      const categories = ['top_films', 'newest_films', 'recommended', 'trending']
      
      const results = await Promise.all(
        categories.map(category => this.getMoviesWithDetails(category))
      )

      return {
        top_films: { items: results[0] },
        newest_films: { items: results[1] },
        recommended: { items: results[2] },
        trending: { items: results[3] }
      }
    },
      async getMoviesByIds(filmIds) {
        if (!filmIds?.length) return []
        
        const uniqueIds = [...new Set(filmIds)]
        
        const movies = await Promise.all(
        uniqueIds.map(async (filmId) => {
            if (moviesCache.value.has(filmId)) {
            return moviesCache.value.get(filmId)
            }

            try {
            const [details, avgRating] = await Promise.all([
                movieService.getFilmDetails(filmId),
                movieService.getAverageRating(filmId)
            ])

            const enrichedMovie = {
                id: filmId,
                film_id: filmId,
                title: details.title || `Фильм ${filmId}`,
                poster_url: movieService.formatPosterUrl(details.poster_url || details.poster),
                avg_rating: avgRating?.rating || avgRating?.avg_rating || null,
                rating: null
            }

            moviesCache.value.set(filmId, enrichedMovie)
            return enrichedMovie
            } catch (error) {
            console.error(`Error loading details for movie ${filmId}:`, error)
            return {
                id: filmId,
                film_id: filmId,
                title: `Фильм ${filmId}`,
                poster_url: null,
                avg_rating: null,
                rating: null
            }
            }
        })
        )
        
        return movies
    },

    clearCache() {
      moviesCache.value.clear()
    }
  }
}