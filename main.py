import numpy as np

class GridworldEnv:
    def __init__(self, rows=5, cols=5, gamma=0.9):
        self.rows = rows
        self.cols = cols
        self.gamma = gamma
        self.state = (0, 0)
        
        # Special transitions state
        self.special_states = {

            (0, 1): ((4, 1), 10), 
            (0, 3): ((2, 3), 5)    
        }
        
        self.actions = ['NORTH', 'SOUTH', 'WEST', 'EAST']
        self.action_map = {

            'NORTH': (-1, 0),
            'SOUTH': (1, 0),
            'WEST': (0, -1),
            'EAST': (0, 1)
        }
    
    def reset(self, state=(0, 0)):
        self.state = state
        return self.state

    def step(self, action):

        if self.state in self.special_states:
            next_state, reward = self.special_states[self.state]
        else:
            move = self.action_map[action]
            new_r = self.state[0] + move[0]
            new_c = self.state[1] + move[1]


            if 0 <= new_r < self.rows and 0 <= new_c < self.cols:
                next_state = (new_r, new_c)
                reward = 0
            else:
                next_state = self.state
                reward = -1 

        self.state = next_state
        return next_state, reward

    def get_available_actions(self, state):
        
        return self.actions.copy()

    def render(self):

        grid = np.full((self.rows, self.cols), '*', dtype=str)
        r, c = self.state
        grid[r][c] = 'A'
        print("\n".join(" ".join(row) for row in grid))
        print()


if __name__ == "__main__":
    env = GridworldEnv()
    env.reset((0, 0))

    print("Initial State:")
    env.render()


    #Number of random actions
    num_random_actions = 7  


    for i in range(num_random_actions):

        action = np.random.choice(env.get_available_actions(env.state))
        
        print(f"Performing action: {action}")
        

        new_state, reward = env.step(action)
        print(f"Action: {action}, New State: {new_state}, Reward: {reward}")
        env.render()