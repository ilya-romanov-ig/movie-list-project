import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from collections import defaultdict

class MovieRecommender:
    def __init__(self, data_paths):
        self.data_paths = data_paths
        self._load_data()
        self._preprocess_dates()
        self.recommendations_cache = {}
        self.time_decay_days = 90
        self.last_update = datetime.now()
        
    def _load_data(self):
        self.ratings = pd.read_csv(self.data_paths['ratings'], parse_dates=['rated_at'])
        self.fav_films = pd.read_csv(self.data_paths['fav_films'], parse_dates=['added_at'])
        self.fav_actors = pd.read_csv(self.data_paths['fav_actors'], parse_dates=['added_at'])
        self.film_actor = pd.read_csv(self.data_paths['film_actor'])
    
    # ДОБАВЛЯЕМ НОВЫЙ МЕТОД:
    def update_data(self):
        """Обновление данных модели"""
        self._load_data()
        self._preprocess_dates()
        self.recommendations_cache.clear()
        self.last_update = datetime.now()
    
    def _preprocess_dates(self):
        """Предобработка временных данных"""
        current_time = datetime.now()
        
        if not self.ratings.empty and 'rated_at' in self.ratings.columns:
            self.ratings['time_weight'] = self.ratings['rated_at'].apply(
                lambda x: self._calculate_time_weight(x, current_time)
            )
            
            self.ratings['weighted_rating'] = self.ratings['rating'] * self.ratings['time_weight']
        
        if not self.fav_films.empty and 'added_at' in self.fav_films.columns:
            self.fav_films['time_weight'] = self.fav_films['added_at'].apply(
                lambda x: self._calculate_time_weight(x, current_time)
            )
        
        if not self.fav_actors.empty and 'added_at' in self.fav_actors.columns:
            self.fav_actors['time_weight'] = self.fav_actors['added_at'].apply(
                lambda x: self._calculate_time_weight(x, current_time)
            )
    
    def _calculate_time_weight(self, event_time, current_time):
        """
        Рассчитывает временной вес по формуле экспоненциального затухания
        Более свежие события имеют больший вес
        """
        days_diff = (current_time - event_time).days
        if days_diff <= 0:
            return 1.0
        return np.exp(-np.log(2) * days_diff / 30)
    
    def _get_user_engagement_level(self, user_id):
        """
        Определяет уровень вовлеченности пользователя
        Возвращает: 'new' (холодный старт), 'light', 'active', 'power'
        """
        has_ratings = user_id in self.ratings['user_id'].values if not self.ratings.empty else False
        has_fav_films = user_id in self.fav_films['user_id'].values if not self.fav_films.empty else False
        has_fav_actors = user_id in self.fav_actors['user_id'].values if not self.fav_actors.empty else False
        
        if not (has_ratings or has_fav_films or has_fav_actors):
            return 'new'  
        
        rating_count = len(self.ratings[self.ratings['user_id'] == user_id]) if has_ratings else 0
        fav_film_count = len(self.fav_films[self.fav_films['user_id'] == user_id]) if has_fav_films else 0
        fav_actor_count = len(self.fav_actors[self.fav_actors['user_id'] == user_id]) if has_fav_actors else 0
        
        total_activity = rating_count + fav_film_count + fav_actor_count
        
        if total_activity == 0:
            return 'new'
        elif total_activity < 5:
            return 'light'
        elif total_activity < 20:
            return 'active'
        else:
            return 'power'
    
    def _get_popular_films(self, n=20, min_ratings=3):
        """
        Возвращает популярные фильмы (для холодного старта)
        Учитывает средний рейтинг и количество оценок
        """
        if self.ratings.empty:
            return []
        
        film_stats = self.ratings.groupby('film_id').agg({
            'weighted_rating': ['mean', 'count'],
            'rating': 'mean'  
        })
        
        film_stats.columns = ['weighted_avg', 'rating_count', 'simple_avg']
        
        film_stats = film_stats[film_stats['rating_count'] >= min_ratings]
        
        if len(film_stats) == 0:
            popular = self.ratings['film_id'].value_counts().head(n).index.tolist()
            return popular
        
        C = film_stats['simple_avg'].mean()
        m = film_stats['rating_count'].quantile(0.7)
        
        def weighted_score(row):
            v = row['rating_count']
            R = row['simple_avg']
            return (v / (v + m) * R) + (m / (v + m) * C)
        
        film_stats['popularity_score'] = film_stats.apply(weighted_score, axis=1)
        
        popular_films = film_stats.sort_values('popularity_score', ascending=False).head(n)
        
        return popular_films.index.tolist()
    
    def _get_trending_films(self, n=15, days=30):
        """
        Возвращает трендовые (недавно популярные) фильмы
        """
        if self.ratings.empty:
            return []
            
        current_time = datetime.now()
        time_threshold = current_time - timedelta(days=days)
        
        recent_ratings = self.ratings[self.ratings['rated_at'] > time_threshold]
        
        if len(recent_ratings) == 0:
            return []
        
        trending = recent_ratings.groupby('film_id').agg({
            'rating': ['mean', 'count']
        })
        
        trending.columns = ['avg_rating', 'rating_count']
        trending = trending[trending['rating_count'] >= 2]
        
        if len(trending) == 0:
            return []
        
        trending['trend_score'] = trending['avg_rating'] * np.log1p(trending['rating_count'])
        
        trending_films = trending.sort_values('trend_score', ascending=False).head(n)
        
        return trending_films.index.tolist()
    
    def _collaborative_recommendations(self, user_id, n=20):
        """
        Улучшенная коллаборативная фильтрация с временными весами
        """
        if self.ratings.empty:
            return []
            
        user_ratings = self.ratings[self.ratings['user_id'] == user_id]
        
        if len(user_ratings) < 3: 
            return []
        
        all_users = self.ratings['user_id'].unique()
        
        user_vector = dict(zip(user_ratings['film_id'], user_ratings['weighted_rating']))
        
        similar_users = []
        
        for other_user in all_users:
            if other_user == user_id:
                continue
                
            other_ratings = self.ratings[self.ratings['user_id'] == other_user]
            other_vector = dict(zip(other_ratings['film_id'], other_ratings['weighted_rating']))
            
            common_films = set(user_vector.keys()) & set(other_vector.keys())
            
            if len(common_films) >= 2: 
                user_scores = [user_vector[f] for f in common_films]
                other_scores = [other_vector[f] for f in common_films]
                
                similarity = np.corrcoef(user_scores, other_scores)[0, 1]
                
                if similarity > 0.3: 
                    similar_users.append((other_user, similarity))
        
        # Сортируем по сходству
        similar_users.sort(key=lambda x: x[1], reverse=True)
        similar_users = similar_users[:10]  
        
        recommendations = defaultdict(float)
        
        for other_user, similarity in similar_users:
            other_ratings = self.ratings[
                (self.ratings['user_id'] == other_user) & 
                (self.ratings['rating'] >= 4.0)  
            ]
            
            for _, row in other_ratings.iterrows():
                film_id = row['film_id']
                if film_id not in user_vector: 
                    score = row['weighted_rating'] * similarity * row['time_weight']
                    recommendations[film_id] += score
        
        sorted_recs = sorted(recommendations.items(), key=lambda x: x[1], reverse=True)
        
        return [film_id for film_id, _ in sorted_recs[:n]]
    
    def _content_based_recommendations(self, user_id, n=20):
        """
        Контентные рекомендации на основе избранных актеров и фильмов
        с учетом временных весов
        """
        if self.fav_actors.empty and self.fav_films.empty:
            return []
            
        user_fav_actors = self.fav_actors[self.fav_actors['user_id'] == user_id]
        
        user_fav_films = self.fav_films[self.fav_films['user_id'] == user_id]
        
        if len(user_fav_actors) == 0 and len(user_fav_films) == 0:
            return []
        
        actor_weights = defaultdict(float)
        for _, row in user_fav_actors.iterrows():
            actor_weights[row['actor_id']] += row['time_weight']
        
        if len(user_fav_films) > 0:
            fav_film_ids = user_fav_films['film_id'].tolist()
            actors_from_films = self.film_actor[self.film_actor['film_id'].isin(fav_film_ids)]
            
            for _, row in actors_from_films.iterrows():
                actor_weight = 1.0 / (row['order_in_cast'] if pd.notna(row['order_in_cast']) else 5)
                film_weight = user_fav_films[
                    user_fav_films['film_id'] == row['film_id']
                ]['time_weight'].mean()
                
                actor_weights[row['actor_id']] += actor_weight * film_weight
        
        all_films_with_actors = self.film_actor[self.film_actor['actor_id'].isin(actor_weights.keys())]
        
        watched_films = set(user_fav_films['film_id'].tolist())
        if user_id in self.ratings['user_id'].values:
            user_rated = set(self.ratings[self.ratings['user_id'] == user_id]['film_id'])
            watched_films.update(user_rated)
        
        film_scores = defaultdict(float)
        
        for _, row in all_films_with_actors.iterrows():
            film_id = row['film_id']
            
            if film_id in watched_films:
                continue
                
            actor_id = row['actor_id']
            role_weight = 1.0 / (row['order_in_cast'] if pd.notna(row['order_in_cast']) else 5)
            
            film_scores[film_id] += actor_weights[actor_id] * role_weight
        
        sorted_films = sorted(film_scores.items(), key=lambda x: x[1], reverse=True)
        
        return [film_id for film_id, _ in sorted_films[:n]]
    
    def get_recommendations(self, user_id, n=10, use_cache=True):
        """
        Основная функция получения рекомендаций
        """
        cache_key = f"{user_id}_{n}"
        if use_cache and cache_key in self.recommendations_cache:
            return self.recommendations_cache[cache_key]
        
        engagement = self._get_user_engagement_level(user_id)
        
        if engagement == 'new':
            popular = self._get_popular_films(n // 2)
            trending = self._get_trending_films(n // 2)
            
            recommendations = list(dict.fromkeys(popular + trending))[:n]
            
            if len(recommendations) < n:
                all_films = list(set(self.ratings['film_id'].unique()) | 
                                set(self.film_actor['film_id'].unique()))
                available = [f for f in all_films if f not in recommendations]
                additional = list(np.random.choice(available, 
                                                 min(n - len(recommendations), len(available)), 
                                                 replace=False))
                recommendations.extend(additional)
                
        elif engagement == 'light':
            cb_recs = self._content_based_recommendations(user_id, int(n * 0.7))
            popular = self._get_popular_films(n - len(cb_recs))
            recommendations = list(dict.fromkeys(cb_recs + popular))[:n]
            
        else:
            cf_recs = self._collaborative_recommendations(user_id, n // 2)
            cb_recs = self._content_based_recommendations(user_id, n // 2)
            
            all_recs = []

            intersection = list(set(cf_recs) & set(cb_recs))
            all_recs.extend(intersection)
            
            cb_only = [f for f in cb_recs if f not in all_recs]
            all_recs.extend(cb_only)
            
            cf_only = [f for f in cf_recs if f not in all_recs]
            all_recs.extend(cf_only)
            
            if len(all_recs) < n:
                popular = self._get_popular_films(n - len(all_recs))
                popular_filtered = [f for f in popular if f not in all_recs]
                all_recs.extend(popular_filtered)
            
            recommendations = all_recs[:n]
        
        if use_cache:
            self.recommendations_cache[cache_key] = recommendations
            
        return recommendations
    
    # ДОБАВЛЯЕМ МЕТОДЫ ИЗ ИСХОДНОГО КОДА:
    def update_user_preferences(self, user_id, action_type, item_id, rating=None):
        """
        Обновление предпочтений пользователя в реальном времени
        """
        current_time = datetime.now()
        
        if action_type == 'rate':
            new_rating = pd.DataFrame([{
                'user_id': user_id,
                'film_id': item_id,
                'rating': rating,
                'rated_at': current_time,
                'time_weight': 1.0, 
                'weighted_rating': rating
            }])
            self.ratings = pd.concat([self.ratings, new_rating], ignore_index=True)
            
        elif action_type == 'fav_film':
            new_fav = pd.DataFrame([{
                'user_id': user_id,
                'film_id': item_id,
                'added_at': current_time,
                'time_weight': 1.0
            }])
            self.fav_films = pd.concat([self.fav_films, new_fav], ignore_index=True)
            
        elif action_type == 'fav_actor':
            new_fav = pd.DataFrame([{
                'user_id': user_id,
                'actor_id': item_id,
                'added_at': current_time,
                'time_weight': 1.0
            }])
            self.fav_actors = pd.concat([self.fav_actors, new_fav], ignore_index=True)
        
        self._clear_user_cache(user_id)
    
    def _clear_user_cache(self, user_id):
        """Очистка кеша для пользователя"""
        keys_to_delete = [k for k in self.recommendations_cache.keys() if k.startswith(f"{user_id}_")]
        for key in keys_to_delete:
            del self.recommendations_cache[key]