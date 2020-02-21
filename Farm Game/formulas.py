from random import uniform

def evento_ocurre(prob_arbol, prob_oro):
    if uniform(0, prob_oro) > uniform(0, prob_arbol):
        return "oro"
    else:
        return "arbol"
