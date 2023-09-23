from ga.algorithm import Algorithm
from sqlalchemy.orm import Session
from fastapi import Depends
import numpy as np
import math 

from db.database import get_db
from db.repositories import UserRepository, MovieRepository, RatingsRepository

class MyGeneticAlgorithm(Algorithm):

    def __init__(self, query_search, individual_size, population_size, p_crossover, p_mutation, all_ids, max_generations=100, size_hall_of_fame=1, fitness_weights=(1.0, ), seed=42, db=None) -> None:


        super().__init__(
            individual_size, 
            population_size, 
            p_crossover, 
            p_mutation, 
            all_ids, 
            max_generations, 
            size_hall_of_fame, 
            fitness_weights, 
            seed)
        
        self.db = db
        self.all_ids = all_ids
        self.query_search = query_search
        
    # # DO PROFESSOR
    # def evaluate(self, individual):

    #     if len(individual) != len(set(individual)):
    #         return (0.0, )
        
    #     if len(list(set(individual) - set(self.all_ids))) > 0:
    #         return (0.0, )
        
    #     ratings_movies = RatingsRepository.find_by_movieid_list(self.db, individual)

    #     if len(ratings_movies) > 0:
    #         mean_ = np.mean([obj_.rating for obj_ in ratings_movies])
    #     else:
    #         mean_ = 0.0

    #     return (mean_, )

    # #Código DO CLAUDIO
    # def evaluate(self, individual):
    #     # Verifique se o indivíduo possui IDs únicos e pertence à lista de IDs válidos
    #     if len(individual) != len(set(individual)) or any(id not in self.all_ids for id in individual):
    #         return (0.0,)

    #     # Encontre as classificações dos filmes representados pelo indivíduo no banco de dados
    #     ratings_movies = RatingsRepository.find_by_movieid_list(
    #         self.db, individual)

    #     if len(ratings_movies) > 0:
    #         # Calcule a média das classificações
    #         mean_rating = np.mean([obj.rating for obj in ratings_movies])

    #         # Calcule a variância das classificações
    #         variance = np.var([obj.rating for obj in ratings_movies])

    #         # Calcule a métrica de aptidão ponderada (por exemplo, média - 0.2 * variância)
    #         fitness = mean_rating - 0.2 * variance

    #         # Retorne a métrica de aptidão em uma tupla
    #         return (fitness,)
    #     else:
    #         # Se nenhum filme for encontrado, retorne aptidão zero
    #         return (0.0,)

    # # TESTE 01 -  TENTANDO UTILIZAR O USUÁRIO, O QUAL VAI ANALISAR
    # def evaluate(self, individual):
    #     if len(individual) != len(set(individual)):
    #         return (0.0, )

    #     if len(list(set(individual) - set(self.all_ids))) > 0:
    #         return (0.0, )

    #     # Obtenha as avaliações do usuário identificado por self.query_search
    #     user_ratings = RatingsRepository.find_by_userid(self.db, self.query_search)

    #     # Extraia os IDs dos filmes avaliados pelo usuário
    #     user_movie_ids = [rating.movieId for rating in user_ratings]

    #     # Verifique se os filmes recomendados estão na lista de filmes avaliados pelo usuário
    #     recommended_movie_ids = set(individual)
    #     intersection = set(user_movie_ids).intersection(recommended_movie_ids)

    #     # Calcule a média das avaliações dos filmes recomendados pelo usuário
    #     if len(intersection) > 0:
    #         ratings_movies = RatingsRepository.find_by_movieid_list(self.db, list(intersection))
    #         mean_rating = np.mean([rating.rating for rating in ratings_movies])
    #     else:
    #         mean_rating = 0.0

    #     return (mean_rating, )

    # TESTE 02(O que vai se utilizado) - TENTANDO UTILIZAR O USUÁRIO, O QUAL VAI ANALISAR
    def evaluate(self, individual):
        # Verifique se o indivíduo possui IDs únicos e pertence à lista de IDs válidos
        if len(individual) != len(set(individual)) or any(id not in self.all_ids for id in individual):
            return (0.0,)

        # Obtenha as avaliações do usuário identificado por self.query_search
        user_ratings = RatingsRepository.find_by_userid(self.db, self.query_search)

        if len(user_ratings) == 0:
            return (0.0,)

        # Encontre as classificações dos filmes representados pelo indivíduo no banco de dados
        ratings_movies = RatingsRepository.find_by_movieid_list(self.db, individual)

        if len(ratings_movies) > 0:
            # Calcule a média das classificações dos filmes representados pelo indivíduo
            mean_rating = np.mean([obj.rating for obj in ratings_movies])

            # Calcule a variância das classificações dos filmes representados pelo indivíduo
            variance = np.var([obj.rating for obj in ratings_movies])

            # Calcule a métrica de aptidão ponderada (por exemplo, média - 0.2 * variância)
            fitness = mean_rating - 0.2 * variance

            # Retorne a métrica de aptidão em uma tupla
            return (fitness,)
        else:
            # Se nenhum filme for encontrado, retorne aptidão zero
            return (0.0,)