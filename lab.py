#!/usr/bin/env python3

import pickle
# NO ADDITIONAL IMPORTS ALLOWED!

# Note that part of your checkoff grade for this lab will be based on the
# style/clarity of your code.  As you are working through the lab, be on the
# lookout for things that would be made clearer by comments/docstrings, and for
# opportunities to rearrange aspects of your code to avoid repetition (for
# example, by introducing helper functions).

def transform_data(raw_data):
    """
    Takes in raw_data, which is in the form of 3-element tuples (actor_id_1, actor_id_2, film_id)
    
    Returns the data restructured in the following way:
        dictionary -> id: dictionary of actors they acted with set of films they were in together
            4724: { 
                1640: { film ids }
                2786: { film ids }
                1540: { film ids }
            }
            1640: { 4724, 2786 }
            1540: { 4724 }
            2786: { 4724, 1640 }
            films: {
                film_id: set of actor ids that were in this film
            }
    """
    refactored_data = { 'films': {} }
    for tuple_data in raw_data:
        actor_id_1 = tuple_data[0]
        actor_id_2 = tuple_data[1]
        film_id = tuple_data[2]

        if not film_id in refactored_data['films']:
            refactored_data['films'][film_id] = set()
        refactored_data['films'][film_id] |= { actor_id_1, actor_id_2 }

        if actor_id_1 == actor_id_2:
            continue

        if actor_id_1 in refactored_data:
            if actor_id_2 in refactored_data[actor_id_1]:
                refactored_data[actor_id_1][actor_id_2].add(film_id)
            else:
                refactored_data[actor_id_1][actor_id_2] = { film_id }
        else:
            refactored_data[actor_id_1] = {
                actor_id_2: { film_id }
            }

        if actor_id_2 in refactored_data:
            if actor_id_1 in refactored_data[actor_id_2]:
                refactored_data[actor_id_2][actor_id_1].add(film_id)
            else:
                refactored_data[actor_id_2][actor_id_1] = { film_id }
        else:
            refactored_data[actor_id_2] = {
                actor_id_1: { film_id }
            }
    return refactored_data

def acted_together(data, actor_id_1, actor_id_2):
    """
    Returns T or F for whether the two inputed actors acted together (considers every actor 
    to have acted with themselves)
    """
    if actor_id_1 == actor_id_2:
        return True
    return actor_id_2 in data[actor_id_1]

def actors_with_bacon_number(data, n):
    """
    Returns a Python set containing the ID numbers of all the actors with Bacon number n
    """
    if n == 0: # only kevin bacon has a bacon number of 0
        return { 4724 }
    if n == 1: # bacon number 1 is anyone who acted with kevin bacon
        return {actor_id for actor_id in data[4724]}
    
    # initializes the seen set to have all actors with bacon numbers 0 or 1
    seen = { 4724 }
    seen |= { actor_id for actor_id in data[4724] }
    # initializes the last pool set to have all actors with bacon number 1
    last_pool = { actor_id for actor_id in data[4724] }
    current_pool = set()
    cur_bacon_number = 2
    while cur_bacon_number <= n:
        # loops over last pool of actors and adds people they acted with to the current pool if said actor hasn't already been seen
        while last_pool:
            actor_id = last_pool.pop()
            for co_actor_id in data[actor_id]:
                if not co_actor_id in seen:
                    current_pool.add(co_actor_id)
                    seen.add(co_actor_id)
        # if it reached the desired bacon number or the current pool is empty (i.e. no more actors to search through)
        # then it returns the pool of actors with bacon number n
        if cur_bacon_number == n or len(current_pool) == 0:
            return current_pool
        cur_bacon_number += 1
        # updates last pool to be the current pool and resets current pool to be an empty set
        last_pool = current_pool
        current_pool = set()

def breadth_first_search(start, is_goal, successors):
    """
    Breadth first search helper function takes in goal function and successors function and searches for a value
    that satisfies the goal function and returns the path to that value
    """
    # initialize visted set and agenda w/ start
    seen = { start }
    agenda = [[start]]
    # used index in agenda to keep track of what paths have been tried, since agenda.pop(0) on a long list is also slow
    index = 0
    while index < len(agenda):
        # grabs an actor to look at
        cur_actor_id = agenda[index][-1]
        # loops over their co-actors
        for co_actor_id in successors(cur_actor_id):
            # if this co-actor hasn't been seen
            if not co_actor_id in seen:
                # and they meet the goal, then it returns the path
                if is_goal(co_actor_id):
                    return agenda[index] + [co_actor_id]
                # otherwise, they're added to the agenda and seen
                agenda.append(agenda[index] + [co_actor_id])
                seen.add(co_actor_id)
        index += 1
    return None

def bacon_path(data, actor_id):
    """
    Return a list of actor IDs (any shortest list if there are several) detailing a "Bacon path" from 
    Kevin Bacon to the actor. If no path exists, return None.
    """
    # BFS since it is guaranteed to return the shortest path
    def goal_function(aid):
        return aid == actor_id
    def get_co_actors(aid):
        return data[aid]
    return breadth_first_search(4724, goal_function, get_co_actors)

def actor_to_actor_path(data, actor_id_1, actor_id_2):
    """
    Returns a list of actor IDs (any shortest list) detailing a path from the first actor to the second
    """
    # BFS since it is guaranteed to return the shortest path
    if actor_id_1 == actor_id_2:
        return [actor_id_1]
    def goal_function(aid):
        return aid == actor_id_2
    def get_co_actors(aid):
        return data[aid]
    return breadth_first_search(actor_id_1, goal_function, get_co_actors)


def actor_path(data, actor_id_1, goal_test_function):
    """
    Returns a list of actor ids representing the shortest path from the actor id to any actor that
    satisfies the goal test function
    
    If no actors satisfy the goal condition, it returns None
    """
    # BFS since it is guaranteed to return the shortest path
    if goal_test_function(actor_id_1):
        return [actor_id_1]
    def get_co_actors(aid):
        return data[aid]
    return breadth_first_search(actor_id_1, goal_test_function, get_co_actors)

def movie_path(data, actor_id_1, actor_id_2):
    """
    Returns a list of movie names that connects them, if such a list exists, otherwise it returns None
    """
    # gets the actor to actor path from the helper function
    actor_id_path = actor_to_actor_path(data, actor_id_1, actor_id_2)
    # loops over the path grabbing actors in pairs and seeing what film they were in together
    if actor_id_path:
        movie_path = []
        index = 0
        while index < len(actor_id_path) - 1:
            actor1 = actor_id_path[index]
            actor2 = actor_id_path[index+1]
            for movie in data[actor1][actor2]:
                movie_path.append(movie)
                break
            index += 1
        return movie_path
    return None

def actors_connecting_films(data, film1, film2):
    """
    Returns the shortest possible list of actor ids (in order) that connect the two films (beginning with
    the id of an actor who was in the first film and ending with id of an actor who was in the second film)

    If no such path exists, then it returns None
    """
    # defines the goal function to be if the inputed actor was in film2
    def goal_function(actor_id):
        return actor_id in data['films'][film2]
    # best path keeps track of the shortest actpr path found from film1 to film2
    best_path = None
    for actor_id_1 in data['films'][film1]:
        # uses actor path helper function to search for path that ends with an actor that was in film2
        path = actor_path(data, actor_id_1, goal_function)
        if path and (best_path == None or len(path) < len(best_path)):
            best_path = path
    return best_path

def get_actor_name(actor_id):
    """
    Takes in actor's id and returns their name
    """
    with open('resources/names.pickle', 'rb') as g:
        namesdb = pickle.load(g)
        for actor in namesdb:
            if namesdb[actor] == actor_id:
                return actor

def get_actor_id(name):
    """
    Takes in actor's name and returns their id
    """
    with open('resources/names.pickle', 'rb') as g:
        namesdb = pickle.load(g)
        return namesdb[name]


def get_movie_name(movie_id):
    """
    Takes in movie's id and returns the movie's name
    """
    with open('resources/movies.pickle', 'rb') as g:
        moviesdb = pickle.load(g)
        for movie in moviesdb:
            if moviesdb[movie] == movie_id:
                return movie

if __name__ == '__main__':
    # with open('resources/small.pickle', 'rb') as f:
    #     smalldb = pickle.load(f)
    #     print(transform_data(smalldb))

    # Section 2 - 
        # names.pickle: dictionary with actor's names as the keys and values as the actor's id
    # print(get_actor_id('Bryn Dowling'))
    # print(get_actor_name(1175130))

    # Section 4 - 
    # with open('resources/small.pickle', 'rb') as f:
    #     smalldb = pickle.load(f)
    #     print(acted_together(transform_data(smalldb), get_actor_id('Jonathan Sanders'), get_actor_id('Stellan Skarsgard')))
    #     print(acted_together(transform_data(smalldb), get_actor_id('Toi Svane Stepp'), get_actor_id('Cory Pendergast')))
        
    # Section 5 -
        # Kevin Bacon: 4724     bacon_score = 0
    # with open('resources/tiny.pickle', 'rb') as f:
    #     tinydb = pickle.load(f)
    #     print(tinydb)
    #     print(transform_data(tinydb))
    #     print(bacon_path(transform_data(tinydb), 1640))

    # with open('resources/large.pickle', 'rb') as f:
    #     largedb = pickle.load(f)

        # Section 5 - Bacon Number
        # actor_ids_6 = actors_with_bacon_number(transform_data(largedb), 6)
        # actors_with_bacon_number_6 = set()
        # for actor_id in actor_ids_6:
        #     actors_with_bacon_number_6.add(get_actor_name(actor_id))
        # print(actors_with_bacon_number_6)

        # Section 6.1.1 - Speed
        # bacon_path_6 = bacon_path(transform_data(largedb), get_actor_id('Alban Guyon'))
        # alban_guyon_bacon_path = []
        # for actor_id in bacon_path_6:
        #     alban_guyon_bacon_path.append(get_actor_name(actor_id))
        # print(alban_guyon_bacon_path)

        # Section 6.2 - Arbitrary Paths
        # actor_id_path = actor_to_actor_path(transform_data(largedb), get_actor_id('Ann Milhench'), get_actor_id('Theresa Russell'))
        # actor_name_path = []
        # for actor_id in actor_id_path:
        #     actor_name_path.append(get_actor_name(actor_id))
        # print(actor_name_path)

        # Section 7 - Movie Paths
        # movie_id_path = movie_path(transform_data(largedb), get_actor_id('Ed Harris'), get_actor_id('Sven Batinic'))
        # movie_name_path = []
        # for movie_id in movie_id_path:
        #     movie_name_path.append(get_movie_name(movie_id))
        # print(movie_name_path)



    # additional code here will be run only when lab.py is invoked directly
    # (not when imported from test.py), so this is a good place to put code
    # used, for example, to generate the results for the online questions.
    pass
