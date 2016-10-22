from random import randint

class hashabledict(dict):
    def __hash__(self):
        return hash(tuple(sorted(self.items())))

class Environment:

    def __init__(self):
        # define the boundary of the Environment
        self.x_limit = 5
        self.y_limit = 3
        # define the action space
        self.action_space = ["up", "left", "down", "right"]
        # define a mapping from state to reward
        # use it to generate a mapping from (state, action) to reward
        # in this case we use the convention that
        self.goal_reward = 100

        # note that unlike Grid_World_With_Single_Stationary_Goal, this
        # Environment doesn't have a reward_map; instead the notion of reward
        # comes out of coinciding location of agents and goals

    def initialize_q_table(self):
        q_table = {}
        for agent_x in range(1, self.x_limit+1):
            for agent_y in range(1, self.y_limit+1):
                for action in self.action_space:
                    for goal_x in range(1, self.x_limit+1):
                        for goal_y in range(1, self.y_limit+1):
                            q_table[
                            (
                                hashabledict(
                                    {
                                        'agent': (agent_x, agent_y),
                                        'goal': (goal_x, goal_y)
                                    }
                                ),
                                action
                            )] = 0
        return q_table

    def reset(self):
        return hashabledict({'agent': (1,1), 'goal': (5,3)})

    def step(self, state, action):
        next_state = self.state_transition(state, action)
        # note that it is in fact much simpler to define the reward function
        # in terms of state, than to implement it in terms of (state, action)
        reward = self.reward(next_state)
        if reward == self.goal_reward:
            done = True
        else:
            done = False
        return (next_state, reward, done)

    def state_transition(self, state, action):
        # account for the agent's movement
        (agent_x, agent_y) = state['agent']
        if action == "up":
            next_agent_state = (agent_x, agent_y-1)
        elif action == "down":
            next_agent_state = (agent_x, agent_y+1)
        elif action == "left":
            next_agent_state = (agent_x-1, agent_y)
        elif action == "right":
            next_agent_state = (agent_x+1, agent_y)
        # correct for the possibility of agent state going out of bounds
        if next_agent_state[0] > self.x_limit:
            next_agent_state = (self.x_limit, next_agent_state[1])
        elif next_agent_state[1] > self.y_limit:
            next_agent_state = (next_agent_state[0], self.y_limit)
        elif next_agent_state[0] < 1:
            next_agent_state = (1, next_agent_state[1])
        elif next_agent_state[1] < 1:
            next_agent_state = (next_agent_state[0], 1)

        # acount for the goal's movement
        (goal_x, goal_y) = state['goal']
        goal_action = self.action_space[randint(0, len(self.action_space)-1)]
        if goal_action == "up":
            next_goal_state = (goal_x, goal_y-1)
        elif goal_action == "down":
            next_goal_state = (goal_x, goal_y+1)
        elif goal_action == "left":
            next_goal_state = (goal_x-1, goal_y)
        elif goal_action == "right":
            next_goal_state = (goal_x+1, goal_y)
        # correct for the possibility of agent state going out of bounds
        if next_goal_state[0] > self.x_limit:
            next_goal_state = (self.x_limit, next_goal_state[1])
        elif next_goal_state[1] > self.y_limit:
            next_goal_state = (next_goal_state[0], self.y_limit)
        elif next_goal_state[0] < 1:
            next_goal_state = (1, next_goal_state[1])
        elif next_goal_state[1] < 1:
            next_goal_state = (next_goal_state[0], 1)

        return hashabledict({'agent': next_agent_state,
                                   'goal': next_goal_state})



    def reward(self, state):
        if state['agent'] == state['goal']:
            return self.goal_reward
        else:
            return 0
