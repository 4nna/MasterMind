
# cheating version, that knows the solution...

# RL version that can access the board directly
possible_actions = self.possibles = [[i, j, k, l]
                                for i in range(1, colors + 1)
                                  for j in range(1, colors + 1)
                                    for k in range(1, colors + 1)
                                      for l in range(1, colors + 1)]

#history:
pin_grid
button_grid


def act():
    #choose possible action
    #get reward (dependent on pins only.  (or pins and number of steps? - no..)
    # what reward makes sense? possibly not additive but multiplicative?


#train:
    #N_STATES = 4
    N_EPISODES = 20

    MAX_EPISODE_STEPS = 100

    MIN_ALPHA = 0.02

    alphas = np.linspace(1.0, MIN_ALPHA, N_EPISODES)
    gamma = 1.0
    eps = 0.2

q_table = dict()

def q(state, action=None):
    if state not in q_table:
        q_table[state] = np.zeros(len(ACTIONS))

    if action is None:
        return q_table[state]

    return q_table[state][action]

def choose_action(state):
    if random.uniform(0, 1) < eps:
        return random.choice(ACTIONS)
    else:
        return np.argmax(q(state))

start_state = #?
for e in range(N_EPISODES):

    state = start_state
    total_reward = 0
    alpha = alphas[e]

    for _ in range(MAX_EPISODE_STEPS):
        action = choose_action(state)
        next_state, reward, done = act(state, action)
        total_reward += reward

        q(state)[action] = q(state, action) + \
                           alpha * (reward + gamma * np.max(q(next_state)) - q(state, action))
        state = next_state
        if done:
            break
    print(f"Episode {e + 1}: total reward -> {total_reward}")
r = q(start_state)

new_state, reward, done = act(start_state, UP)
r = q(new_state)

# full RL version that uses mouse pointer itself..