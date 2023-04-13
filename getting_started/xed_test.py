import os
import sys
import grid2op
from grid2op.Agent import DoNothingAgent, BaseAgent
from tqdm.notebook import tqdm  # for easy progress bar
display_tqdm = False  # this is set to False for ease with the unitt test, feel free to set it to True
import numpy as np
max_iter = 100  # to make computation much faster we will only consider 100 time steps
import pdb
import matplotlib.pyplot as plt



try:
    from lightsim2grid import LightSimBackend
    bk_cls = LightSimBackend
except ImportError as exc:
    print(f"Error: {exc} when importing faster LightSimBackend")
    from grid2op.Backend import PandaPowerBackend
    bk_cls = PandaPowerBackend

env_name = "G:\Document\powerbird\Grid2Op\grid2op\data\educ_case14_storage"
env = grid2op.make(env_name, test=True, backend=bk_cls())

print("Is this environment suitable for redispatching: {}".format(env.redispatching_unit_commitment_availble))


observed = []
# perform a valid redispatching action
env.set_id(0)  # make sure to use the same environment input data.
obs_init = env.reset()  # reset the environment
act = env.action_space()
act.is_ambiguous()
#
# act = env.action_space({"redispatch":[(0, -1),(1, -1),(5,-1)]})
storage_act1 = env.action_space({"redispatch":[(0, -3),(1, -3),(5,-3)],"set_storage": [(0, -2.7), (1, 3.14)]})
#[(0, -5),(1, 2)]
#[(0, -5),(1, 2),(2, -3)]
#[(0, -5),(1, 2),(5, 3)]
# obs, reward, done, info = env.step(act)
#
# print(info)
# print("actual dispatch at time step 0: {}".format(obs.actual_dispatch))
obs,reward,done,info = env.step(storage_act1)
print(info)
print("actual dispatch at time step 0: {}".format(obs.actual_dispatch))
observed.append(obs)