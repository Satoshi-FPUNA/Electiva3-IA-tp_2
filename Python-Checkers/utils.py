
# Función para contar estados expandidos
states_expanded = 0

def count_expansion():
    global states_expanded
    states_expanded += 1

def reset_expansion_count():
    global states_expanded
    states_expanded = 0

def get_expansion_count():
    return states_expanded
