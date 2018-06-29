import gym
env = gym.make('MountainCar-v0')
observation = env.reset()
env.render()
print(observation)

for i_episode in range(1):
    observation = env.reset()
    for t in range(100):
        env.render()
        print(observation)
        action = env.action_space.sample()
        observation, reward, done, info = env.step(action)
        if done:
            print("Episode {} timesteps".format((t+1)))
            break
