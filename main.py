from random import randint

# a list of all people that are participating
names = (
    'Lori',
    'Jeff',
    'Mark',
    'Dominique',
    'Melinda',
    'John',
    'Matt',
    'Marie',
    'Daniel',
    'Harold',
    'Shannon'
)

# who got for who last year. used to make sure we don't assign them the same this year
previous_allocation_names = {
    'Lori': 'Jeff',
    'Jeff': 'Mark',
    'Mark': 'Dominique',
    'Dominique': 'Melinda',
    'Melinda': 'John',
    'John': 'Matt',
    'Matt': 'Marie',
    'Marie': 'Daniel',
    'Daniel': 'Harold',
    'Harold': 'Lori',
    'Shannon': None,
}

# it's easier to work with indexes. might be over-complicating it, but it makes sense to me
previous_allocation_indexes = {}
for giver in previous_allocation_names:
    if previous_allocation_names[giver]:
        previous_allocation_indexes[names.index(giver)] = names.index(previous_allocation_names[giver])
    else:
        previous_allocation_indexes[names.index(giver)] = None

        
# people that are already assigned a gift giver
assigned_gifts = set()

# override allocations for some people for what-ever reason; perhaps they are absent and someone lives near them
allocation_override = {
#    'Marie': 'Shannon',
}

allocation_override_indexes = {}
for giver in allocation_override:
    allocation_override_indexes[names.index(giver)] = names.index(allocation_override[giver])
    assigned_gifts.add(names.index(allocation_override[giver]))

# it's better if we restrict households from giving to each other. the recipricol relationship will be enforced as well (A: B --> B: A).
immediate_family = {
    'Lori': {'Mark'},
    'Jeff': {'Melinda'},
    'Dominique': {'John', 'Marie', 'Harold'},
    'Matt': {'Daniel', 'Shannon'},
}
       
immediate_family_indexes = {}
for person in immediate_family:
    immediate_family_indexes[names.index(person)] = set()
    for member in immediate_family[person]:
        immediate_family_indexes[names.index(person)].add(names.index(member))
    # create recipricol relationship
    for member in immediate_family[person]:
        immediate_family_indexes[names.index(member)] = (immediate_family_indexes[names.index(person)] - set((names.index(member),))) | set( (names.index(person),))
        
# index -> set of possibilities
possibility_matrix = dict()

while True:
    possibility_lengths_list = list()
    for giver_index in range(0, len(names)):
        if giver_index in possibility_matrix and len(possibility_matrix[giver_index]) == 1:
            pass # these people are already assigned to give a gift to someone
        elif giver_index in allocation_override_indexes:
            possibility_matrix[giver_index] = (allocation_override_indexes[giver_index],)
        else:
            # gift givers can't give to themselves, the person they gave to last year, their immediate family, or someone who is already getting a gift
            possibility_matrix[giver_index] = set(range(0, len(names))) - {giver_index, previous_allocation_indexes[giver_index]} - assigned_gifts - immediate_family_indexes[giver_index]
            
            # it's better if the person giving them a gift isn't also given a gift by the same person
            # TODO can avoid this iteration with another data structure
            if giver_index in assigned_gifts:
                for index in possibility_matrix:
                    if len(possibility_matrix[index]) == 1 and giver_index in possibility_matrix[index]:
                        possibility_matrix[giver_index] -= set((index,))
            
            # we'll get the only item left by index zero later, which doesn't work if its a set
            if len(possibility_matrix[giver_index]) == 1:
                possibility_matrix[giver_index] = list(possibility_matrix[giver_index])
            
        possibility_lengths_list.append(len(possibility_matrix[giver_index]))

    # we're going to assign the next giver based on who has the smallest set of choices (finalized choices don't count)
    choice_set = set(possibility_lengths_list) - set((1,))
    if not choice_set:
        break
    minimum = min(choice_set)
    
    next_giver = possibility_lengths_list.index(minimum)    
    choice = list(possibility_matrix[next_giver])[randint(0, minimum - 1)]
    
    possibility_matrix[next_giver] = (choice,)
    assigned_gifts.add(choice)  

new_allocation = dict()
for giver_index in possibility_matrix:
    new_allocation[names[giver_index]] = names[possibility_matrix[giver_index][0]]
    
print(new_allocation)
