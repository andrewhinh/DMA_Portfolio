# Load the framework
import gym

#Load the environment
env = gym.make('FrozenLake-v0')

#Each environment has a 'observation_space' and a 'action_space'
#The former is information the environment can know. In this case, it's a 4x4 grid of 16 numbers
print(env.observation_space)
#The above will show you Discrete(16), meaning it returns an integer with 16 possible values, so 0-15
#these represent the 16 spots the 'player' can be in.

#The action_space is the actions you can do.
print(env.action_space)
#'Discrete(4)' refers to the 4 directions you can move in, 0-3. These are the values you can pass to the 'step' call.

score = 0
#for a bunch of  episodes
for _ in range(10000):
    #refresh and render the initial state
    env.reset()
    for t in range(100):   #take 100 steps
        #through trial, we know that
        # 0 = LEFT
        # 1 = DOWN
        # 2 = RIGHT
        # 3 = UP
        # and [env.action_space.sample()] = random move
        obs, rew, done, info = env.step(env.action_space.sample()) # take an action
        #print(obs) #The observation, which is where the player is
        if done:  #The player either hit a hole or the goal
            #print("Episode over after {} steps".format(t+1)) #how long did that take
            score += rew  # you get +1 for reaching the goal, 0 otherwise. This will tell us how many successful attempts we had
            #env.render()  # Take a look at the final state
            break
print(score)  # Take a look at how many successes
