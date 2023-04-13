
import grid2op
from grid2op.Agent import RandomAgent
# I create an environment
env = grid2op.make("G:\Document\powerbird\Grid2Op\grid2op\data\educ_case14_storage")

# define an agent here, this is an example
agent = RandomAgent(env.action_space)

# environment need to be "reset" before usage:
obs = env.reset()
reward = env.reward_range[0]
done = False

# now run through each steps like this
while not done:
    action = agent.act(obs, reward, done)
    obs, reward, done, info = env.step(action)
