from streamlit_searchbox import st_searchbox

suggestions_list = [
    "esercizio",
    "esercizi",
    "esercizio permutazioni",
    "esercizio disposizioni",
    "esercizio combinazioni",
    "esercizio distribuzione Bernoulli",
    "esercizio ditribuzione Binomiale",
    "esercizio distribuzione Poisson",
    "esercizio distribuzione Geometrica",
    "esercizio distribuzione Ipergeometrica",
    "esercizio distribuzione Pascal",
    "esercizio distribuzione Gauss",
    "esercizio distribuzione Uniforme",
    "esercizio distribuzione Esponenziale",
    ]

def search(searchterm):
    
    suggestions_list_result = []
    for suggestion in suggestions_list:
        if searchterm.lower() in suggestion.lower():
            suggestions_list_result.append(suggestion)
        
    if searchterm not in suggestions_list_result:
        suggestions_list_result.append(searchterm)

    return suggestions_list_result
