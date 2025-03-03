# %% [markdown]
# ### Maximize f(x) = x^2 using genetic algorithm, where x ranges from 0-31

# %% [markdown]
# Step 1 : Initialize Random Population
# 

# %%
import random
population_size = 10


generations = {
    "0" : [bin(random.randint(0,31))[2:].zfill(5) for _ in range(population_size)]
}


# %% [markdown]
# Step 2: Fitness function

# %%
def binary_to_decimal(binary):
    return int(binary, 2)

def fitness_function(x):
    return x**2

# %% [markdown]
# Step 3: Evaluation Function
# 

# %%
def evaluation_function(population):
    fitness_values = {chromosome : fitness_function(binary_to_decimal(chromosome)) for chromosome in population}
    return fitness_values

# %% [markdown]
# Step 4: Selection Function
# 

# %%
def roulette_selection(population , fitness_values , num_parents):
    total_fitness = sum(fitness_values.values())
    selection_probabilities = {chromosome:fitness/total_fitness for chromosome,fitness in fitness_values.items()}
    
    selected_parents = random.choices(
        list(selection_probabilities.keys()),
        weights=list(selection_probabilities.values()),
        k=num_parents
        )
    
    return selected_parents

# %% [markdown]
# Step 5: Crossover Function
# 

# %%
def crossover_function(chromA , chromB):
    cut_point = random.randint(1, len(chromA) - 2)
    child1 = chromA[:cut_point] + chromB[cut_point:]
    child2 = chromB[:cut_point] + chromA[cut_point:]
    return child1, child2

parent1 = "11010"
parent2 = "00101"

child1, child2 = crossover_function(parent1, parent2)
print("Parent 1:", parent1)
print("Parent 2:", parent2)
print("Child 1:", child1)
print("Child 2:", child2)


# %% [markdown]
# Step 6: Mutation Function
# 

# %%
def mutation_function(chromosome , mutation_rate = 0.2):
    mutated_chromosome = ""
    
    for bit in chromosome:
        if random.random() < mutation_rate:
            mutated_chromosome += "0" if bit == "1" else "1"
        else:
            mutated_chromosome += bit

    return mutated_chromosome


chromosome = "10101010001"
mutated_chromosome = mutation_function(chromosome, mutation_rate=0.2)

print("Original:", chromosome)
print("Mutated :", mutated_chromosome)

# %% [markdown]
# Step 7: Full Generation Cycle

# %%
def evolve_generation(generations, generation_num, num_parents, mutation_rate=0.2, num_of_elites=2, all_elites=[]):
    population = generations[str(generation_num)]
    fitness_values = {chrom: fitness_function(binary_to_decimal(chrom)) for chrom in population}

    if num_parents % 2 == 1 and num_parents + 1 <= len(population):
        num_parents += 1

    #Select Elites
    sorted_chromosomes = sorted(fitness_values, key=fitness_values.get, reverse=True)
    elites = sorted_chromosomes[:num_of_elites]
    for elite in elites:
        if elite not in all_elites:
            all_elites.append(elite)

    #Select Parents
    parents = roulette_selection(population, fitness_values, num_parents)

    #Crossover + Child Mutation
    offsprings = []
    for i in range(0, len(parents) - 1, 2):
        child1, child2 = crossover_function(parents[i], parents[i+1])
        offsprings.append(mutation_function(child1,mutation_rate))
        offsprings.append(mutation_function(child2,mutation_rate))


    #Select Remaining Chromosomes (excluding elites & children) and Mutate
    remaining_pool = [chrom for chrom in population if chrom not in elites and chrom not in offsprings]
    mutated_chromosomes = [mutation_function(chrom, mutation_rate) for chrom in remaining_pool]

    #Create Next Generation
    next_gen = elites + offsprings + mutated_chromosomes

    #Ensure Population Size is Maintained
    while len(next_gen) < len(population):
        next_gen.append(random.choice(population))
    next_gen = next_gen[:len(population)]

    generations[str(generation_num + 1)] = next_gen
    return generations, all_elites


# %% [markdown]
# Step 8: Run Genetic Algorithm
# 

# %%
def run_genetic_algorithm(generations , num_of_gens , num_parents=4 , mutation_rate = 0.2 , num_elites = 2):

    all_elites = []
    for gen in range(num_of_gens):
        generations , all_elites = evolve_generation(
            generations,
            gen,
            num_parents,
            mutation_rate,
            num_elites,
            all_elites
        )
    
    best_solution = max(all_elites , key= lambda chrom: fitness_function(binary_to_decimal(chrom)))
    best_value = binary_to_decimal(best_solution)
    best_fitness = fitness_function(best_value)

    print("\n===== Genetic Algorithm Results =====")
    print(f"Total Generations Run: {num_of_gens}")
    print(f"Best Overall Solution: {best_solution} (Decimal: {best_value}) with Fitness: {best_fitness}")

    return best_solution,best_value,best_fitness,generations



    

# %%

import random
population_size = 10


generations = {
    "0" : [bin(random.randint(0,31))[2:].zfill(5) for _ in range(population_size)]
}
best_chromosome, best_x, best_fitness,generations = run_genetic_algorithm(generations, num_of_gens=3)
#num of max generations = 3
#num of parents = 4
#num of elites = 2
#mutation rate = 0.2

# %%
for gen_num , population in generations.items():
    print(f"Gen {gen_num} : {population}")

# %%



