#%%
# make a list of x, y, z - velocities:
arm_vel = [2, 3, 2.5]

# print the last entry in vel:
# TODO: debug the following line (you may need to fix multiple issues here)
print(arm_vel([3]))

#%%
# Now imagine that this is the velocity of the tip of a robot arm based on how its joints are rotating.
# If we want to add the velocity of a mobile base that it is attached to the arm to get the total velocity
# of the robot, we can add the base velocity to the arm velocity.
base_vel = [1, 0, 0]

# add the base velocity to the arm velocity:
total_robot_vel = arm_vel + base_vel

# we want to print a message saying "total velocity is: <actual values>"
# TODO: debug the following line (you may need to fix multiple issues here)
print(total velocity is:, total_robot_vel)

# TODO: answer the following questions as a comment below:
# After getting it to print, look at the output.
# Is the result the sum of the two velocities (a single vector with 3 numbers)?
# Answer:

# If not, what did the + operation do? and what ideas do you have to compute the sum?
# Answer:

#%%
# Now let's introduce the numpy library to make linear algebra operations much easier.
import numpy as np

# we can make arrays from the previous lists
arm_vel_np = np.array(arm_vel)
base_vel_np = np.array(base_vel)

# add the base velocity to the arm velocity:
total_robot_vel_np = arm_vel_np + base_vel_np

print('total velocity is:', total_robot_vel_np)

# TODO: answer this question as a comment below:
# Did this compute the sum of the two velocities as expected?
# Answer:


#%%
# Now we want to calculate the magnitude of the total velocity of the tip of the robot arm.
# We can do this by calculating the norm of the total velocity vector as follows:
total_robot_vel_magnitude = np.sqrt(total_robot_vel_np*total_robot_vel_np)

# TODO: answer this question as a comment below:
# Did this successfully calculate the magnitude? If not, why not?
# Answer:

# TODO: If it did not calculate the magnitude, fix the above line to correctly compute the magnitude.
# total_robot_vel_magnitude = <your solution here>

print('magnitude:', total_robot_vel_magnitude)

# The key here is just using intermediate steps and debugging to know what you are doing.

# ideas that might help:
# - you could index into the array to access individual elements
# - you could look for numpy functions that might help
# - you could try to utilize python's built-in exponentiation operator **
# - you could try to utilize python's built-in matrix multiplication operator @

