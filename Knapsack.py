# %% [markdown]
# # Knapsack Problem Using Genetic Algorithm
# 

# %%
import random

# %% [markdown]
# Random Initial Population
# 

# %%
def initialize_population(population_size , num_of_items):
    population = []
    for _ in range(population_size):
        individual = "".join(str(random.randint(0, 1)) for _ in range(num_of_items))
        population.append(individual)
    return population


# %% [markdown]
# Fitness Function

# %%
def fitness_function(chromosome , items , max_weight):
    total_value = 0
    total_weight = 0
    for i in range(len(chromosome)):
        if chromosome[i] == '1':
            total_value += items["N"+str(i+1)][0]
            total_weight += items["N"+str(i+1)][1]
    
    if total_weight <= max_weight:
        return total_value
    else:
        return 0
    


# %% [markdown]
# Evaluation Function
# 

# %%
def evaluation_function(population , items , max_weight):
    fitness_values = {chromosome : fitness_function(chromosome , items , max_weight) for chromosome in population}
    return fitness_values

# %% [markdown]
# Selection Function (Tournament Selection)

# %%
def tournament_selection(population , fitness_values , k=3):
    selected_chromosomes = random.sample(population , k)
    selected_chromosomes.sort(key = lambda chrom:fitness_values[chrom] , reverse=True)
    return selected_chromosomes[0]


# %% [markdown]
# One-Point Crossover
# 

# %%
def crossover_function(chromA , chromB):
    cut_point = random.randint(1, len(chromA) - 2)
    child1 = chromA[:cut_point] + chromB[cut_point:]
    child2 = chromB[:cut_point] + chromA[cut_point:]
    return child1, child2
    

# %% [markdown]
# Mutation Function

# %%
def mutation_function(chromosome , mutation_rate = 0.2):
    mutated_chromosome = ""
    
    for bit in chromosome:
        if random.random() < mutation_rate:
            mutated_chromosome += "0" if bit == "1" else "1"
        else:
            mutated_chromosome += bit

    return mutated_chromosome

# %% [markdown]
# Full Generation Cycle
# 

# %%
def evolve_generation(generations, generation_num, population_size, items, max_weight, mutation_rate=0.2, tournament_k=3):
    population = generations[str(generation_num)]
    fitness_values = evaluation_function(population,items,max_weight)

    new_population = []

    while len(new_population) < population_size:
        parent1 = tournament_selection(population , fitness_values , tournament_k)
        parent2 = tournament_selection(population , fitness_values , tournament_k)

        child1,child2 = crossover_function(parent1 , parent2)

        child1 = mutation_function(child1,mutation_rate)
        child2 = mutation_function(child2,mutation_rate)

        if len(new_population) < population_size:
            new_population.append(child2)
    
    generations[str(generation_num+1)] = new_population
    return generations


# %% [markdown]
# Driver Code

# %%
def run_knapsack_problem(generations,max_generations,population_size,items,max_weight,mutation_rate=0.1,tournament_k=3):
    best_solution = None
    best_fitness = 0

    for gen in range(max_generations):
        generations = evolve_generation(
            generations, 
            gen,
            population_size,
            items, 
            max_weight, 
            mutation_rate, 
            tournament_k
        )
    
        current_pop = generations[str(gen+1)]
        fitness_values = evaluation_function(current_pop , items , max_weight)
        best_in_gen = max(fitness_values , key=fitness_values.get)
        best_fitness_in_gen = fitness_values[best_in_gen]
        
        if best_fitness_in_gen > best_fitness:
            best_solution = best_in_gen
            best_fitness = best_fitness_in_gen
        
        print(f"Gen {gen+1}: Best Solution = {best_in_gen}, Best Fitness = {best_fitness_in_gen}")



    return generations,best_solution,best_fitness


# %% [markdown]
# Run Genetic Algorithm
# 

# %%
def decode_best_solution(sol , items):
    selected_items = []
    total_weight = 0
    total_value = 0
    for i, bit in enumerate(sol):
        if bit == "1":
            item_name = "N" + str(i+1)
            value, weight = items[item_name]
            selected_items.append((item_name , value,weight))
            total_weight += weight
            total_value += value
    return selected_items, total_weight, total_value

# %%
population_size = 10
max_generations = 6
max_weight = 10
mutation_rate = 0.1
tournament_k = 3

items = {
    "N1" : (14,1),
    "N2" : (23,3),
    "N3" : (8,7),
    "N4" : (9,4),
    "N5" : (17,5),
    "N6" : (15,6)
}
num_of_items = len(items)

generations = {
    "0" : initialize_population(population_size , num_of_items)
}

generations,best_solution,best_values = run_knapsack_problem(generations,max_generations,population_size,items,max_weight,mutation_rate,tournament_k)


print("--------------------------------")
for gen,pop in generations.items():
    print(f"Gen {gen} : {pop}")
    
print(f"Best solution : {best_solution}")
print(f"Best values : {best_values}")
print("--------------------------------")

selected_items , total_weight , total_value = decode_best_solution(best_solution,items)
print("--Selected Items in Best Solution:--")
for item,weight,value in selected_items:
    print(f"{item} : {weight} - {value}")

print(f"Total Weight : {total_weight}")
print(f"Total Value : {total_value}")




