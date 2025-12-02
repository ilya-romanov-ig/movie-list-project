import pickle
import numpy as np
import pandas as pd
from typing import List, Dict, Any

class MovieRecommender:
    def __init__(self, model_path: str, data_path: str):
        self.model = self.load_model(model_path)
        self.movies_df = pd.read_csv(data_path)
        
    def load_model(self, path: str):
        with open(path, 'rb') as f:
            return pickle.load(f)
    
    def collaborative_filtering(self, user_id: int, n_recommendations: int = 10):
        predicted_ratings = self.model.predict(user_id)
        top_indices = np.argsort(predicted_ratings)[::-1][:n_recommendations]
        
        recommendations = []
        for idx in top_indices:
            movie = self.movies_df.iloc[idx]
            recommendations.append({
                'movie_id': int(movie['movieId']),
                'title': movie['title'],
                'predicted_rating': float(predicted_ratings[idx]),
                'genres': movie['genres'].split('|')
            })
        
        return recommendations
    
    def content_based(self, movie_ids: List[int], n_recommendations: int = 10):
        pass
    
    def hybrid_recommendation(self, user_id: int, n_recommendations: int = 10):
        pass