import numpy as np

class GridworldEnv:
    def __init__(self, rows=5, cols=5):
        self.rows = rows
        self.cols = cols
        self.state = (0, 0)  # starting state

        # Special state transitions: (current_pos): (next_pos, reward)
        self.special_states = {
            (0, 1): ((4, 1), 10),  # A → A'
            (0, 3): ((2, 3), 5)    # B → B'
        }

        # Define actions and their effects on (row, col)
        self.actions = {
            'UP': (-1, 0),
            'DOWN': (1, 0),
            'LEFT': (0, -1),
            'RIGHT': (0, 1)
        }

    def reset(self, state=(0, 0)):
        self.state = state
        return self.state

    def step(self, action):
        action = action.upper()

        # Check if current state is a special one
        if self.state in self.special_states:
            next_state, reward = self.special_states[self.state]
        else:
            if action not in self.actions:
                return self.state, -1  # Invalid action

            dr, dc = self.actions[action]
            r, c = self.state
            new_r, new_c = r + dr, c + dc

            # Stay in place if move goes out of bounds
            if 0 <= new_r < self.rows and 0 <= new_c < self.cols:
                next_state = (new_r, new_c)
                reward = 0
            else:
                next_state = self.state
                reward = -1  # Penalty for hitting wall

        self.state = next_state
        return next_state, reward

    def render(self):
        grid = np.full((self.rows, self.cols), '.', dtype=str)
        r, c = self.state
        grid[r][c] = 'A'  # Mark agent position

        print("\nGrid State:")
        for row in grid:
            print(" ".join(row))
        print()

# Simple loop to play the Gridworld
if __name__ == "__main__":
    env = GridworldEnv()
    env.reset((0, 0))
    env.render()

    print("Use actions: UP, DOWN, LEFT, RIGHT. Type 'EXIT' to quit.\n")

    while True:
        action = input("Your action: ").strip().upper()

        if action == 'EXIT':
            print("Thanks for playing! Goodbye.")
            break

        next_state, reward = env.step(action)
        print(f"→ Moved {action}, New State: {next_state}, Reward: {reward}")
        env.render()
