import gym
import tflearn as tf
import numpy as np


env = gym.make('CartPole-v0')
#print(env.observation_space)
#print(env.action_space)

#What are these observations?
env.reset()
#obs, rew, done, info = env.step(env.action_space.sample())
#print(obs)
#ideally we don't need to know, the machine should be able to figure out a model regardless
#but for our curiouse young minds, they are:
# [position of cart, velocity of cart, angle of pole, rotation rate of pole]

#we want to generate some training data
#We'll do this by playing games randomly, and saving good episodes
#First we will need a good threshold for a good win
score_requirement = 50

#the goal is 200 steps, but just in case let's play our games to a max of 500
goal_steps = 500

#and lets play 10000 games, seemed to work well last time
initial_games = 10000

#a learning rate, use this later
LR = 1e-3

#ok, now let's generate
def initial_population():
    #so we're gonna play a lot of games, and the good ones we want to save
    #we'll need all the moves from good games.
    #Let's store these as observation, move pairs, but it starts as an empty list
    training_data = []
    #also curious the scores of the good games, so lets make a place for those
    accepted_scores = []
    print("Playing Random Games....")
    for _ in range(initial_games):
        env.reset()

        #set up a place to record THIS game
        #later, if it's good, we'll add it to training_data[]
        game_memory = []

        # the tricky thing about this is that we want to store the move taken
        # after an observation, so we need to store the previous observation each time
        #let's make a place for that
        prev_observation = []

        #finally, we need to keep track of the score for this game:
        score = 0

        #now let's play a game
        for x in range(goal_steps):
            #do a step! we need to store the action first though:
            action = env.action_space.sample()
            observation, reward, done, info = env.step(action)

            #update score
            score += reward

            #now the tricky part, we want to store the previous obs and the action we took
            #we'll have to skip the first move, but that's ok
            if(x > 0):  #at least one move so far
                game_memory.append([prev_observation, int(action)])
            prev_observation = observation
            if done:
                break

        #ok the games over, let's see if it was good
        if score > score_requirement:
            #save that score
            accepted_scores.append(score)

            #now we want to append all our good moves to the master list of good moves
            for data in game_memory:
                # convert to one-hot (this is the output layer for our neural network)
                if data[1] == 1:
                    output = [0,1]
                elif data[1] == 0:
                    output = [1,0]

                # saving our training data
                training_data.append([data[0], output])

            #harrison converts the actions to 'one-hot' type
            #https://machinelearningmastery.com/why-one-hot-encode-data-in-machine-learning/
            #this is good for environment where more than one thing can be done
            #this is also how the neural nets like to be traininedself.
            #you can think of it like: each step of the process,
            # the net narrows down a move left or right as a probability
            #so we need a value for both, thus a 1x2 array
        #if you'd like to see an example observation:
        #if _ == 9999: print(prev_observation)
    #let's see what scores were good
    print(accepted_scores)
    return training_data


#now that we've created data, let's create our neural net
#this will take an parameter of input_size,
#so it could be useful for other envs, but it will end up being 4
def neural_net_model(input_size):

    #to avoid awkward imports, we're going to just use the tf prefix for all
    #there's a little bit more going on here than in our titanic example, so let's take it slow

    #the first layer is our input layer
    #we have to tell it the shape of our data,
    #that's always [None, the number of inputs, other input layers, more layer, etc]
    #here we have a shape of 4 input (the observation) by 1 (one observation each time)
    #in this case, input_size, will be 4, but by using a variable, we could do other shapes
    network = tf.input_data(shape=[None, input_size], name='input')

    #a hidden layer with 128 nodes, using regular linear regression (this is default)
    network = tf.fully_connected(network, 128, activation='relu')
    #so dropout is a bit weird. basically, to prevent overfitting (over analyzing the problem),
    #we'll randomly drop part of the network. We do this to attempt to get a more organic,
    #less strict network that won't create rules that are too harsh.
    #more info: https://www.cs.toronto.edu/~hinton/absps/JMLRdropout.pdf
    #we could experiment with this, I think
    network = tf.dropout(network, 0.8)

    #alright lets make a bunch more layers, keeping it symmetrical
    network = tf.fully_connected(network, 256, activation='relu', name="hlayer1")
    network = tf.dropout(network, 0.8)

    network = tf.fully_connected(network, 512, activation='relu' , name="hlayer2")
    network = tf.dropout(network, 0.8)

    network = tf.fully_connected(network, 256, activation='relu', name="hlayer3")
    network = tf.dropout(network, 0.8)

    network = tf.fully_connected(network, 128, activation='relu', name="hlayer4")
    network = tf.dropout(network, 0.8)

    #this is our output layer.
    #it contains an array like [l, r], probabilities for each lef or right
    #if you're curious about activations:
    #https://github.com/Kulbear/deep-learning-nano-foundation/wiki/ReLU-and-Softmax-Activation-Functions
    #essentially the softmax activation will squash our outputs into a probability distrubution
    network = tf.fully_connected(network, 2, activation='softmax', name="out")

    #right now, I don't get what this does.
    network = tf.regression(network, learning_rate=LR)

    #make a Deep Neaural Net wtih with network
    model = tf.DNN(network, tensorboard_dir='log')

    return model

#now that we have functions to collect data, set up a neural net,
#we need to train the network
def train_model(training_data):
    #this is the awkard part, we need to organize that data a bit better,
    #in order to actually feed it to the net

    X = [i[0] for i in training_data]#.reshape(-1,len(training_data[0][0]),1)
    y = []
    for i in training_data:
        y.append(i[1])

    model = neural_net_model(input_size = len(X[0]))
    model.fit(X, y, n_epoch=5, show_metric=True,  run_id='openai_learning')
    return model


def play_with_model(model):
    scores = []
    choices = []
    print("Playing wtih Trained Model.....")
    for each_game in range(10):
        score = 0
        game_memory = []
        prev_obs = []
        env.reset()
        for _ in range(goal_steps):
            env.render()

            if len(prev_obs)==0:
                action = env.action_space.sample()
            else:
                #this clever call finds the index of the max argument
                #since predict will return something like [][0.23.., 0.76..]]
                #it will return 0 if the first is bigger, 1 if the second
                # which is the same as 'left' or 'right' in the action space
                action = np.argmax(model.predict([prev_obs])[0])

            choices.append(action)

            new_observation, reward, done, info = env.step(action)
            prev_obs = new_observation
            game_memory.append([new_observation, action])
            score+=reward
            if done: break

        scores.append(score)

    print(scores)



model = train_model(initial_population())
#it's good to see how the model predicts things
#print(model.predict([[ 0.14332623,  0.24608396, -0.2131985,  -0.85725035]]))
play_with_model(model)














#next
