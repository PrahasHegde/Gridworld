import numpy as np
import matplotlib.pyplot as plt


#Gridworld Environment
class GridworldEnv:
    def __init__(self, rows=5, cols=5):
        self.rows = rows
        self.cols = cols
        self.state = (0, 0)

        #Special states 
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

        self.total_reward = 0
        self.reward_history = []

    def reset(self, state=(0, 0)):
        self.state = state
        self.total_reward = 0
        self.reward_history = []
        return self.state

    def step(self, action):
        if self.state in self.special_states:
            next_state, reward = self.special_states[self.state]
        else:
            move = self.action_map.get(action.upper())
            if move is None:
                return self.state, -1  # Invalid action

            new_r = self.state[0] + move[0]
            new_c = self.state[1] + move[1]

            if 0 <= new_r < self.rows and 0 <= new_c < self.cols:
                next_state = (new_r, new_c)
                reward = 0
            else:
                next_state = self.state
                reward = -1

        self.state = next_state
        self.total_reward += reward
        self.reward_history.append(self.total_reward)
        return next_state, reward

    def get_available_actions(self):
        return self.actions

    def render(self):
        grid = np.full((self.rows, self.cols), '*', dtype=str)
        r, c = self.state
        grid[r][c] = 'A'
        print("\nCurrent Grid:")
        print("\n".join(" ".join(row) for row in grid))
        print(f"Total Reward: {self.total_reward}\n")

    def plot_rewards(self):
        if self.reward_history:
            plt.plot(range(1, len(self.reward_history)+1), self.reward_history, marker='o')
            plt.title("Total Accumulated Reward Over Time")
            plt.xlabel("Steps")
            plt.ylabel("Reward")
            plt.grid(True)
            plt.show()
        else:
            print("No steps taken")


# Input Loop
if __name__ == "__main__":
    env = GridworldEnv()
    env.reset((0, 0))
    env.render()

    print("Enter Action: 'NORTH', 'SOUTH', 'WEST', 'EAST'. Type 'EXIT' to quit.\n")

    while True:
        action = input("Your action: ").strip().upper()
        if action == "EXIT":
            print("Thanks for Playing...")
            env.plot_rewards()
            break
        if action not in env.get_available_actions():
            print("Invalid")
            continue

        new_state, reward = env.step(action)
        print(f"Moved {action} , New State: {new_state}, Reward: {reward}")
        env.render()
