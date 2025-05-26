import numpy as np

# Gridworld Environment with Two Agents
class GridworldEnv:
    def __init__(self, rows=5, cols=5):
        self.rows = rows
        self.cols = cols
        self.agent_states = [(0, 0), (4, 4)]  # Starting positions for Agent 1 and Agent 2

        self.special_states = {
            (0, 1): ((4, 1), 10),
            (0, 3): ((2, 3), 5)
        }

        self.actions = ['UP', 'DOWN', 'LEFT', 'RIGHT']
        self.action_map = {
            'UP': (-1, 0),
            'DOWN': (1, 0),
            'LEFT': (0, -1),
            'RIGHT': (0, 1)
        }

        self.total_rewards = [0, 0]
        self.reward_histories = [[], []]

    def reset(self, states=[(0, 0), (4, 4)]):
        self.agent_states = states
        self.total_rewards = [0, 0]
        self.reward_histories = [[], []]
        return self.agent_states

    def step(self, agent_id, action):
        state = self.agent_states[agent_id]

        if state in self.special_states:
            next_state, reward = self.special_states[state]
        else:
            move = self.action_map.get(action.upper())
            if move is None:
                return state, -1  # Invalid action

            new_r = state[0] + move[0]
            new_c = state[1] + move[1]

            if 0 <= new_r < self.rows and 0 <= new_c < self.cols:
                next_state = (new_r, new_c)
                reward = 0
            else:
                next_state = state
                reward = -1

        self.agent_states[agent_id] = next_state
        self.total_rewards[agent_id] += reward
        self.reward_histories[agent_id].append(self.total_rewards[agent_id])
        return next_state, reward

    def get_available_actions(self):
        return self.actions

    def render(self):
        grid = np.full((self.rows, self.cols), '.', dtype=str)
        r1, c1 = self.agent_states[0]
        r2, c2 = self.agent_states[1]

        if self.agent_states[0] == self.agent_states[1]:
            grid[r1][c1] = 'X'  # both agents in the same cell
        else:
            grid[r1][c1] = 'A'  # Agent 1
            grid[r2][c2] = 'B'  # Agent 2

        print("\nCurrent Grid:")
        print("\n".join(" ".join(row) for row in grid))
        print(f"Agent A Reward: {self.total_rewards[0]} | Agent B Reward: {self.total_rewards[1]}\n")


# Input Loop
if __name__ == "__main__":
    env = GridworldEnv()
    env.reset()
    env.render()

    print("Enter Action in format 'agent_id ACTION' (e.g., '0 UP' or '1 LEFT'). Type 'EXIT' to quit.\n")

    while True:
        action_input = input("Your action: ").strip().upper()
        if action_input == "EXIT":
            print("Exiting the gridworld...")
            break

        try:
            agent_id_str, action = action_input.split()
            agent_id = int(agent_id_str)
            if agent_id not in [0, 1] or action not in env.get_available_actions():
                raise ValueError
        except ValueError:
            print("Invalid input. Use format like '0 UP' or '1 RIGHT'")
            continue

        new_state, reward = env.step(agent_id, action)
        print(f"Agent {agent_id} moved {action} → New State: {new_state}, Reward: {reward}")
        env.render()
