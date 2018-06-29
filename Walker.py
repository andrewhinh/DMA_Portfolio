#load the framework
import gym
import gym.spaces

#loads the environment
env = gym.make('FrozenLake-v0')

#4X4 grid info
print(env.observation_space)


#4 direction 0-3(left, down, right, up) respectively
print(env.action_space)

#declare score
score = 0
#episodes
for _ in range(100000):
    env.reset()  # resets the environment to the starting state
    #takes 10 steps
    for t in range(100):
        #action = env.action_space.sample() #defines action as random
        observation, reward, done, info = env.step(1) #take the action
        observation, reward, done, info = env.step(2)  # take the action

        env.render() #displays environment
        if done:
            score += reward
            break
print(score)