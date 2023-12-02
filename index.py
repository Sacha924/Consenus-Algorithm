import random


class Node:
    def __init__(self, identifier, initial_state):
        self.identifier = identifier
        self.state = initial_state
        self.neighbors = []

    def query(self, querying_color=None):
        if self.state == '⊥' and querying_color:
            self.state = querying_color
        return self.state

    def update_state(self, new_state):
        self.state = new_state

    def sample_neighbors(self, k):
        return random.sample(self.neighbors, min(k, len(self.neighbors)))

class SlushAlgorithm:
    def __init__(self, k, alpha, initial_states):
        self.nodes = [Node(i, state) for i, state in enumerate(initial_states)]
        self.k = k
        self.alpha = alpha
        for node in self.nodes:
            node.neighbors = self.nodes

    def on_query(self, node, col):
        return node.query(col)

    def run_slush_round(self):
        for node in self.nodes:
            if node.state == '⊥':
                continue

            sampled_neighbors = node.sample_neighbors(self.k)
            neighbor_states = [self.on_query(neighbor, node.state) for neighbor in sampled_neighbors]
            state_count = {state: neighbor_states.count(state) for state in set(neighbor_states)}

            for state, count in state_count.items():
                if count >= self.alpha * self.k and state != node.state:
                    node.update_state(state)
                    break

    def run(self):
        rounds_taken = 0
        while True:
            rounds_taken+=1
            states_before = [node.state for node in self.nodes]
            self.run_slush_round()
            states_after = [node.state for node in self.nodes]
            if states_before == states_after:
                break
        return rounds_taken, states_after[0]


def generate_initial_states(num_R, num_B, num_neutral):
    initial_states = ['R'] * num_R + ['B'] * num_B + ['⊥'] * num_neutral
    random.shuffle(initial_states)
    return initial_states

k = 10
alpha = 0.8

count_R = 0
count_B = 0
count_Rounds = 0

for i in range(2000):
    initial_states = generate_initial_states(2200,2200,400)
    slush = SlushAlgorithm(k, alpha, initial_states)
    rounds_taken, final_state = slush.run()

    if final_state == "R":
        count_R += 1
    else:
        count_B += 1
    count_Rounds += rounds_taken
    # print("all nodes become ",final_state, " after ", rounds_taken, " rounds")

print("R probability of winning : ", (count_R/2000)*100, "%")
print("B probability of winning : ", (count_B/2000)*100, "%")
print("Average number of rounds : ", (count_Rounds/2000))