import random
import math
from environment import Agent, Environment
from planner import RoutePlanner
from simulator import Simulator
import numpy as np

class LearningAgent(Agent):
    """ An agent that learns to drive in the Smartcab world.
        This is the object you will be modifying. """ 

    def __init__(self, env, learning=False, epsilon=1.0, alpha=0.5, epsilon_scalar=0.01):
        super(LearningAgent, self).__init__(env)     # Set the agent in the evironment 
        self.planner = RoutePlanner(self.env, self)  # Create a route planner
        self.valid_actions = self.env.valid_actions  # The set of valid actions

        # Set parameters of the learning agent
        self.learning = learning # Whether the agent is expected to learn
        self.Q = dict()          # Create a Q-table which will be a dictionary of tuples

        """
        Q has this structure:
        
        { 'state-1': { 
            'action-1' : Qvalue-1,
            'action-2' : Qvalue-2,
             ...
           },
          'state-2': {
            'action-1' : Qvalue-1,
             ...
           },
           ...
        }
        
        as the agent encounters states, it will take various actions and record their q values here.
        the q value is the rewards received at this state, for taking this action.
        
        
        
        """

        self.epsilon = epsilon   # Random exploration factor
        """
        
        this factor should decay to 0 between trials, as the number of trials grows. This is because the agent is expected to learn,
        and do less exploring as it matures.
        
        """

        self.alpha = alpha       # Learning factor

        ###########
        ## TO DO ##
        ###########
        # Set any additional class parameters as needed

        self.nb_trials = 1.0
        self.epsilon_scalar = epsilon_scalar

        print(self)


    def reset(self, destination=None, testing=False):
        """ The reset function is called at the beginning of each trial.
            'testing' is set to True if testing trials are being used
            once training trials have completed. """

        # Select the destination as the new location to route to
        self.planner.route_to(destination)
        
        ########### 
        ## TO DO ##
        ###########



        # Update epsilon using a decay function of your choice
        #self.epsilon = self.epsilon - 0.01  # reduce epsilon by 0.05 after each trial

        # math.pow(self.nb_trials, 2) # decays too fast
        #self.epsilon = math.pow(self.alpha, self.nb_trials) # get to 30%
        #self.epsilon -= 0.05 # get to 10% but bad rating, doesnt get there on time
        #self.epsilon = math.exp(-self.alpha*self.nb_trials) # goes to below 10%, smoother decay
        #self.epsilon = math.cos(self.alpha*self.nb_trials) # goes to 25%
        #self.epsilon = math.exp(-self.epsilon_scalar*self.nb_trials) # make epsilon independent of alpha
        # negative of gompertz function decay
        g_a = -1.0  # flips to negative, converges to 0
        g_b = 40.0  # controls x direction displacement, higher goes left
        g_c = 4.0  # controls slops of transition between 1 and 0, higher is steeper
        g_val = self.nb_trials / 700
        self.epsilon = (g_a * math.exp(-g_b * math.exp(-g_c * g_val))) + 1

        # like this you exponentially slower decay, so you have enough time to learn from q after exploring
        # but alpha decrease should only affect how much q is updated with new info, not how much epsilon decays

        if self.nb_trials % 300 == 0:
            #self.alpha -= (self.alpha * 0.50)
            pass
            # problem is, makeing alpha smaller increases epsilon again, so it will wobble


        # Update additional class parameters as needed
        self.nb_trials +=1.0



        # If 'testing' is True, set epsilon and alpha to 0
        if testing:
            self.epsilon = 0.0
            self.alpha = 0.0

        return None



    # figure out what state i am currently in
    def build_state(self):
        """ The build_state function is called when the agent requests data from the 
            environment. The next waypoint, the intersection inputs, and the deadline 
            are all features available to the agent. """

        # Collect data about the environment
        waypoint = self.planner.next_waypoint() # The next waypoint, or direction the smartcab should drive to get to the destination at some point
        # this is relative to the current heading of the smartcab

        inputs = self.env.sense(self)           # Visual input - intersection light and traffic

        """
        inputs has:
            light
            left: where vehicle to left of smartcab wants to go
            right: where vehicle to left of smartcab wants to go
            oncoming: where vehicle to left of smartcab wants to go
            
            these values are None if there are no vehicle in those positions of the intersection
        
        """

        deadline = self.env.get_deadline(self)  # Remaining deadline in units of remaining number of actions until out of time

        ########### 
        ## TO DO ##
        ###########
        # Set 'state' as a tuple of relevant data for the agent        

        # i think we need light and oncoming for safety, and we need deadline, waypoint for efficiency.

        #state = (waypoint, inputs["light"], inputs["oncoming"], deadline, inputs["left"], inputs["right"])
        # forward from left could make problems if you run over a red light specifically then. What about crashes when they go left?

        # a priori knowledge approach: not reinforcement learning. Left=forward because in U.S you can turn right on red if no traffic.
        state = (waypoint, inputs["light"], inputs["oncoming"], inputs["left"]=="forward")

        # reinforcement learning: use everything and let it figure out whats useful. Deadline can lead to recklessness.
        #state = (waypoint, inputs["light"], inputs["oncoming"], inputs["left"], inputs["right"], deadline)

        return state


    def get_maxQ(self, state):
        """ The get_max_Q function is called when the agent is asked to find the
            maximum Q-value of all actions based on the 'state' the smartcab is in. """

        ########### 
        ## TO DO ##
        ###########
        # Calculate the maximum Q-value of all actions for a given state

        # break ties between max q if they are the same values. Else you might always prefer a certain action, and will keep picking it, although a different one is better
        # say the first action reward is net 0, but the second action would start accumulating positive Q thereafter. If you never pick it, you have a problem.
        # implement this in choose_action
        maxQ = max(self.Q[state].values())

        return maxQ


    def createQ(self, state):
        """ The createQ function is called when a state is generated by the agent. """

        ########### 
        ## TO DO ##
        ###########
        # When learning, check if the 'state' is not in the Q-table
        if self.learning: # need to remember Qs when learning...
            if state not in self.Q:
                self.Q[state] = {}
                for action in self.valid_actions:
                    self.Q[state][action] = 0.0

        # If it is not, create a new dictionary for that state
        #   Then, for each action available, set the initial Q-value to 0.0

        return


    def choose_action(self, state):
        """ The choose_action function is called when the agent is asked to choose
            which action to take, based on the 'state' the smartcab is in. """

        # Set the agent state and default action
        self.state = state
        self.next_waypoint = self.planner.next_waypoint() # ask planner for next waypoint
        action = None

        ########### 
        ## TO DO ##
        ###########
        # When not learning, choose a random action
        if not self.learning:
            action = random.choice(self.valid_actions)

        # When learning, choose a random action with 'epsilon' probability
        #   Otherwise, choose an action with the highest Q-value for the current state
        else:

            # there is also a random.random() function that generates uniformly random numbers between 0 and 1. Much easier than below ;)

            outcomes =['random', 'highest']
            positive_epsilon = abs(self.epsilon)  # if epsilon is 0 its -0.0000
            prob = [positive_epsilon, 1-positive_epsilon]

            if np.random.choice(outcomes, p= prob) == "random":

                action = random.choice(self.valid_actions)
            else:

                # pick best action as dictated by Q, if its a tie pick a random action
                maxQ = max(self.Q[state].values())
                maxQs = [key for key, m in self.Q[state].items() if m == maxQ]
                action_with_highest_q_value_in_current_state = random.choice(maxQs)
                action = action_with_highest_q_value_in_current_state
                print(action)

                # you will check this action against reality next, and get a reward for it.
                # later this reward will influence your Q learning for this round.


        return action


    def learn(self, state, action, reward):
        """ The learn function is called after the agent completes an action and
            receives an award. This function does not consider future rewards 
            when conducting learning. """

        """
            we are given the type <s, a, r, s'>. At this point, the agent has already chosen an action, and received a reward for it
            
            the content of state will be the state the agent was in before chosing this action (old state).
            
            we do not have access to the new state.
            
            Q for this state has not been updated yet with the reward of the current action.
            
        """

        ###########
        ## TO DO ##
        ###########
        # When learning, implement the value iteration update rule
        #   Use only the learning rate 'alpha' (do not use the discount factor 'gamma')
        """
         the q function is :
         Q(s, a) = R(state) + gamma * sum_s_prime[ T(s,a,s') * max_a_prime Q(s',a')                      ]
         gamma is the discount factor of future rewards, T the transition probability for each state,action,next state tuple.
         max a prime means chose best action after getting to s' to maximise Q in state s prime.
         notice that we are leaving state s via the specific action a.

         q needs to be updated by the current learning rate alpha
        
            alpha decreases to 0 over time, so that the learned value converges to the expected (average) value
            also, things you learn earlier matter more than those you learn later
            
        the idea is to move to the expected q value over time, but problem is q is also changing over time.
        but it still works (proven somewhere)
        
        
        """

        current_q = self.Q[state][action]

        reward_for_current_action = reward # reward we got at this state for chosing action

        gamma = 0  # complete discounting here, we dont use the max q at this state, only the current reward

        """
        this is the best Q (future rewards) you can get based on current knowledge of Q, if you are in the current state
        there is an associated action to this max Q, which is the action you took in this step (so its already done).
        
        """
        max_q_at_this_state = self.get_maxQ(state) # should this be the max q of the next state s prime?
        """
         what i do now is just pick the best action at the current state and add its q to current q. I am also adding it again through reward, but this is the real world reward, wheras Q is the learned reward.
         so i keep updating Q with information from real reward, as well as historical rewards that accumulate in the Q dictionary for this state,action pair
         
         we give a weight of 1-alpha to current_q, so that we are not yet completely certain, but as alpha is small it gets a fairly large weight.
         
         """

        updated_q = ((1.0 - self.alpha) * current_q) + (self.alpha * (reward_for_current_action + gamma * max_q_at_this_state))

        """
        so somehow the max_q_at this state tells me what action is best to do next based on future rewards
        but as we dont use it, the current reward is what i learn
        the action chosen was done using max Q, so max Q is also current q, so dont have to add it again in function.
        maybe max Q could somehow help with the future?
        
        """

        # now we update the q value for this state,action pair with the Q from the best action
        self.Q[state][action] = updated_q

        return


    def update(self):
        """ The update function is called when a time step is completed in the 
            environment for a given trial. This function will build the agent
            state, choose an action, receive a reward, and learn if enabled. """

        state = self.build_state()          # Get current state
        self.createQ(state)                 # Create 'state' in Q-table
        action = self.choose_action(state)  # Choose an action
        reward = self.env.act(self, action) # Receive a reward

        if self.learning:
            self.learn(state, action, reward)   # Q-learn

        return
        

def run():
    """ Driving function for running the simulation. 
        Press ESC to close the simulation, or [SPACE] to pause the simulation. """

    ##############
    # Create the environment
    # Flags:
    #   verbose     - set to True to display additional output from the simulation
    #   num_dummies - discrete number of dummy agents in the environment, default is 100
    #   grid_size   - discrete number of intersections (columns, rows), default is (8, 6)
    #   reward_late - gradient of late punishment, not needed if deadline not part of state variables
    env = Environment(verbose=False)
    
    ##############
    # Create the driving agent
    # Flags:
    #   learning   - set to True to force the driving agent to use Q-learning
    #    * epsilon - continuous value for the exploration factor, default is 1
    #    * alpha   - continuous value for the learning rate, default is 0.5
    #    * epsilon_scalar - multiplier in epsilon decay function, controls speed of decay
    agent = env.create_agent(LearningAgent, learning=True, epsilon=1, alpha=0.01, epsilon_scalar=0.001)
    # nb of trials before testing is controled by epsilon decay rate
    """"
        epsilon_scalar = 0.0005 gives 10k trials, with A+ rating for safety and reliability
        0.001 gives about 5000 trials
        
        it seems with epsilon scalar 0.05, and only 100 trials, but removing deadline from state, you get A rating!
        this is because the feature space is much smaller, so all states can be visited fairly quickly
        
        
    """
    
    ##############
    # Follow the driving agent
    # Flags:
    #   enforce_deadline - set to True to enforce a deadline metric
    env.set_primary_agent(agent, enforce_deadline=True)

    ##############
    # Create the simulation
    # Flags:
    #   update_delay - continuous time (in seconds) between actions, default is 2.0 seconds, smallest 1 millisecond
    #   display      - set to False to disable the GUI if PyGame is enabled
    #   log_metrics  - set to True to log trial and simulation results to /logs
    #   optimized    - set to True to change the default log file name
    sim = Simulator(env, update_delay=0.001, log_metrics=True, optimized=True, display=False)
    
    ##############
    # Run the simulator
    # Flags:
    #   tolerance  - epsilon tolerance before beginning testing, default is 0.05 
    #   n_test     - discrete number of testing trials to perform, default is 0
    sim.run(n_test=10, tolerance=0.01)

    # reliability gets worse as epsilon goes below alpha
    # key is to increase nb of trials, this improves reliability a lot. But need to find optimal stopping point


if __name__ == '__main__':
    run()

    # you need to run this from a command prompt inside the smartcab folder. From there call:
    # python smartcab/agent.py
    # just set up the working directory to parent in config for pycharm, then it works

    import sys, os
    #sys.path.append("D:/Python Projects/machine_learning/udacity_ml_projects/machine-learning/projects/smartcab/")
    root_dir = os.path.dirname(os.path.dirname(__file__))
    sys.path.append(root_dir)

    import visuals as vs
    #vs.plot_trials("sim_improved-learning.csv")
    vs.plot_trials("sim_improved-learning.csv")

