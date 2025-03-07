# %% [markdown]
# # Word Guesser using Genetic Algorithm
# 

# %% [markdown]
# Fitness Function

# %%
def fitness_function(chromosome, actualword):
    fitness_score = 0
    for b,c in zip(chromosome,actualword):
        if b==c:
            fitness_score+=1
    
    return fitness_score


# %% [markdown]
# Evaluation Function

# %%
def evaluation_function(population ,actualword,word_length):
    fitness_values = {chrom:fitness_function(chrom,actualword) for chrom in population}
    return fitness_values


# %% [markdown]
# Selection Function

# %%
import random
def tournament_selection(population , fitness_values , k=3):
    selected_chroms = random.sample(population,k)
    selected_chroms.sort(key=lambda chrom:fitness_values[chrom],reverse=True)
    return selected_chroms[0]

# %% [markdown]
# Crossover Function

# %%
def crossover_function(chromA , chromB):
    cut_point = random.randint(1, len(chromA) - 2)
    child1 = chromA[:cut_point] + chromB[cut_point:]
    child2 = chromB[:cut_point] + chromA[cut_point:]
    return child1, child2
    

# %% [markdown]
# Mutation Function

# %%
import string

def mutation_function(chromosome, mutation_rate=0.1):
    mutated_chromosome = list(chromosome)

    for i in range(len(mutated_chromosome)):
        if random.random() < mutation_rate:
            new_char = random.choice(string.ascii_lowercase.replace(mutated_chromosome[i], ''))
            mutated_chromosome[i] = new_char

    return "".join(mutated_chromosome)

chromosome = "balaaj"
mutated_chromosome = mutation_function(chromosome, mutation_rate=0.3)
print(f"Original: {chromosome}")
print(f"Mutated:  {mutated_chromosome}")

# %% [markdown]
# Run Genetic Algorithm

# %%
def evolve_generation(generations , gen_num ,actualword,population_size,mutation_rate=0.1,tournament_k=3):
    word_length = len(actualword)
    population = generations[str(gen_num)]
    fitness_values = evaluation_function(population,actualword,word_length)

    new_population = []
    for _ in range(population_size // 2):
        parent1 = tournament_selection(population,fitness_values,tournament_k)
        parent2 = tournament_selection(population,fitness_values,tournament_k)
        child1,child2 = crossover_function(parent1,parent2)
        new_population.extend([child1,child2])
    
    new_population = [mutation_function(chrom,mutation_rate) for chrom in new_population]

    generations[str(gen_num+1)] = new_population
    return generations

# %% [markdown]
# Driver Function

# %%
def run_word_guesser(generations,max_generations,population_size,actualword,mutation_rate=0.1,tournament_k=3):
    solution = None

    for gen in range(max_generations):
        fitness_values = evaluation_function(generations[str(gen)] , actualword , len(actualword))

        best_chromosome = max(fitness_values,key=fitness_values.get)
        best_fitness = fitness_values[best_chromosome]

        print(f"Gen {gen}: Best = {best_chromosome} | Fitness = {best_fitness}")

        if best_fitness == len(actualword):
            solution = best_chromosome
            break
        
        generations = evolve_generation(generations, gen, actualword, population_size, mutation_rate, tournament_k)

    if solution:
        print(f"\n Solution found in Generation {gen}: {solution}")
    else:
        print("\nMax generations reached. Best guess:", best_chromosome)

    return solution ,generations


# %%
import random
import string
def initialize_population(population_size, word_length):
    population = []
    for _ in range(population_size):
        individual = "".join(random.choice(string.ascii_lowercase) for _ in range(word_length))
        population.append(individual)
    return population


# %%
actualword = input("Enter a word to guess : ")
actualword = "".join(c.lower() for c in actualword)

population_size = 50
max_gens = 50
mutation_rate = 0.1
tournament_k = 3


generations = {
    "0" : initialize_population(population_size,len(actualword))
}

guess, generations = run_word_guesser(generations,max_gens,population_size,actualword,mutation_rate,tournament_k)

# %%



