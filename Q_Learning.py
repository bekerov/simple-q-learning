from Grid_World_With_Moving_Goal import Environment
from Q_Table import Q_Table
from Agent_Animation import run_animation

# define parameters
gamma = 0.9
num_training_episodes = 1000


def run_episode(state, q_table, env):
    episode_data = []
    done = False
    while not done:
        # get best available action according to q_table
        action = q_table.get_best_action(state)
        # take chosen action
        (next_state, reward, done) = env.step(state, action)
        # record step data
        episode_data.append((state, action, reward, next_state))
        state = next_state
    return episode_data


def train_on_episode(episode_data, q_table):
    # loop backwards through episode_data, since that is the order in which
    # we want to do updates
    for i in range(len(episode_data)-1, -1, -1):
        step_data = episode_data[i]
        q_table.update(step_data, gamma)


# training_log is a list of training episodes
# return a tuple whose first value is the average number of time steps required
# to reach the goal on the first runs, and whose second value is the average
# number needed on the last runs
def get_comparative_average_time_to_goal(training_log, interval_length):
    num_episodes = len(training_log)
    lengths_of_episodes = [len(episode_data) for episode_data in training_log]
    interval_1 = lengths_of_episodes[0:interval_length]
    interval_2 = lengths_of_episodes[num_episodes-interval_length:num_episodes]
    return (sum(interval_1)/float(len(interval_1)),
            sum(interval_2)/float(len(interval_2)))

# used to assess the average, average time to goal over many trials
def get_average_of_tuple_list(ls):
    x_total = 0
    y_total = 0
    for (x,y) in ls:
        x_total += x
        y_total += y
    return (x_total/len(ls), y_total/len(ls))


def main():
    # initializations
    training_log = []
    env = Environment()
    q_table = Q_Table(env)

    # training loop
    for _ in range(num_training_episodes):
        # reset the state to a random position in the environment
        initial_state = env.reset()
        # run through an episode to completion, returning the sequence of state,
        # action and reward values
        episode_data = run_episode(initial_state, q_table, env)
        #print episode_data[0]
        training_log.append(episode_data)
        # update the q_table on the data from the most recent episode
        train_on_episode(episode_data, q_table)

    # assess training results by comparing the average lengths of the
    # first training episodes against the average lenghts of the last ones
    print get_comparative_average_time_to_goal(training_log, 50)

    # run comparative animations, before and after training
    #run_animation(env.x_limit, env.y_limit, training_log[0])
    #run_animation(env.x_limit, env.y_limit, training_log[-1])

# assess whether meaningful learning is taking place by doing many trials from
# scratch and determining average, average comparative performance of an agent at
# the start of learning and at the end of learning
def does_learning_really_take_place():
    for trial in range(0,1000):
        average_times_to_goal = []

        # initializations
        training_log = []
        env = Environment()
        q_table = Q_Table(env)

        # training loop
        for _ in range(num_training_episodes):
            # reset the state to a random position in the environment
            initial_state = env.reset()
            # run through an episode to completion, returning the sequence of state,
            # action and reward values
            episode_data = run_episode(initial_state, q_table, env)
            #print episode_data[0]
            training_log.append(episode_data)
            # update the q_table on the data from the most recent episode
            train_on_episode(episode_data, q_table)

        # assess training results by comparing the average lengths of the
        # first 10 training episodes against the average lenghts of the last 10
        average_times_to_goal.append(
        get_comparative_average_time_to_goal(training_log, 50))
    print get_average_of_tuple_list(average_times_to_goal)

does_learning_really_take_place()
