import random

class BirdAgent:
    def __init__(self,weights=None):
        self.num_inputs=4
        if weights is None:
            self.weights=[random.uniform(-1,1) for _ in range(self.num_inputs)]
        else:
            self.weights=weights

        self.fitness=0
        self.score=0
        self.alive=True

    def decide(self,inputs):
        weighted_sum=sum(w * i for w,i in zip(self.weights,inputs))
        return weighted_sum>0
    
    def mutate(self,mutation_rate=0.1):
        for i in range(len(self.weights)):
            self.weights[i]+=random.uniform(-0.5,0.5)

    def crossover(parent1,parent2):
        child_weights=[]
        for w1,w2 in zip(parent1.weights,parent2.weights):
            child_weights.append(random.choice([w1,w2]))
        return BirdAgent(weights=child_weights)
    