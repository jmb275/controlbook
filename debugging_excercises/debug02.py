# %%
import numpy as np


# %%
# We will be adding vectors a lot in this course and are trying to highlight
# some of the common pitfalls that you might encounter when doing so.
a = np.array([1, 2, 3])
b = np.array([[1], [2]])
result = a + b

# TODO: answer the following questions as comments below (you may have to lookup
# how to find the shape of a numpy array - this will be a very useful debugging
# tool throughout the course):

# What is the shape of a?
# Answer:

# What is the shape of b?
# Answer:

# What is the shape of result?
# Answer:

# Why did this happen? and what occurred?
# Answer:


# %%
# You may multiply vectors in this course, so we are trying to highlight what
# happens when you do so.
a = np.array([1, 2, 3])
b = np.array([4])
result = a * b

# TODO: answer the following questions as comments below:
# Is the output what you would expect to come from the * operator?
# Answer:

# Can you explain how it happened?
# For example, were all 3 elements of a multiplied by the constant b, only some,
# or did something other than multipliation occur?
# Answer:


# %%
# You may accidentally try to add arrays of different shapes and we are trying to
# highlight what happens in this case and the error message you will see.
a = np.ones((2, 3))
b = np.ones((3, 2))
result = a + b

# TODO: answer the following questions as comments below:
# Why doesn't this work?
# Answer:

# TODO: fix the code so that you can successfully add them without changing the
# original shapes (use numpy or matrix/vector operations rather than chaging the
# numbers inside of the ones() function that define the shape).
# The result should have 6 numbers, but it doesn't matter if the result is 2x3 or 3x2.


# %%
# This situation is highly likely to happen to you at some point in this course,
# so we are tyring to help you recognize it early.
a = np.array([1, 2, 3])
b = np.array([[1], [2], [3]])
result = a + b

# TODO: answer the following questions as comments below:
# Is the result the sum of two vectors (3 numbers)?
# Answer:

# What is the shape of a and the shape of b?
# Answer:

# Why is the result 3x3? and what does the addition do in this case?
# Answer:


# %%
# We will be doing matrix-vector multiplications a lot in this course, so we are
# trying to highlight some of the common pitfalls that you might encounter when doing so.
# In this case 'b' is a 3x3 identity matrix, and 'a' is a vector with 3 elements
# as a 1D numpy array. A 1D numpy array meaning the shape is (3,) rather than (3,1),
# or a list rather than a list of lists.
a = np.array([1, 2, 3])
b = np.eye(3)
result1 = b * a
result2 = b @ a

# Which of these provides the intended result of matrix-vector multiplication?
# TODO: put your answer here as a comment and justify it.
# Answer:


# %%
# This is the same as before, but we will reshape a to be a vector as a 2D numpy array.
a_column = a.reshape((3, 1))
result1 = b * a_column
result2 = b @ a_column

# TODO: answer the following questions as comments below:
# Which of these provides the intended result of matrix-vector multiplication?
# Answer:

# (T/F) The * operator does scalar or element-wise multiplication.
# Answer:

# (T/F) The @ operator does matrix-vector multiplication.
# Answer:


# %%
# From linear algebra, we know that (ba)^T = a^T b^T. Since b is an identity matrix,
# we know that b^T = b. So we should have (ba)^T = a^T b...the transpose of the
# result from the previous 2 examples.
result1 = a @ b
result2 = a.T @ b
result3 = a_column @ b
result4 = a_column.T @ b

# TODO: answer the following questions as comments below:
# Which of the 4 results failed to multiply? Why? (comment it out after answering)
# Answer:

# Was there a difference between result1 and result2? Why or why not?
# Hint: does transposing a vector as a 1D array (i.e., a.T) do anything?
# Answer:


# The previous 3 examples were to show that vectors can be represented
# as either 1D or 2D numpy arrays (lists or lists of lists). When doing matrix-vector
# multiplication, the resulting vector will have the same shape as the input vector.
# Either way is valid and yields the same result, just represented slighly differently.
# We highly recomend that you pay attention to the shape of your arrays when performing
# linear algebra operations using numpy.

# TODO: leave a comment below stating that you read the previous paragraph.
# Answer:


# %%
# The following are some additional examples that we want you to look at to
# understand how numpy multiplication, broadcasting, and shapes work.

result1 = a_column * a
result2 = a * a_column
result3 = a_column.T * a
result4 = a * a_column.T

# TODO: answer these questions as comments below:
# Is result1 the same as result2? What about result3 and result4? What does this
# tell you about the order of multiplication when using the * operator?
# Answer:


# %%
# Broadcasting example
M = np.ones((3, 3))
result1 = M * a_column.T
result2 = M * a_column
result3 = M * a

# TODO: answer these questions as comments below:
# Is result3 the same as result1 or result2?
# Answer:

# (T/F) Because a_column.T is a row vector, it did element-wise multiplication
# broadcasted across each row of M.
# Answer:

# (T/F) Because a_column is a column vector, it did element-wise multiplication
# broadcasted across each column of M.
# Answer:

# (T/F) Because a is a 1D array, numpy automatically treated it as a row vector
# and did element-wise multiplication broadcasted across each row of M.
# Answer:


# %%
result1 = a * a
result2 = a @ a
result3 = a_column * a_column
result4 = a_column @ a_column
result5 = a_column.T @ a_column

# TODO: answer these questions as comments below:
# Why does a @ a work? but a_column @ a_column doesn't? (comment out result4)
# Answer:

# Which of these computes the sum of the squares (dot product of a vector with itself)?
# Answer:

# Which of these does element-wise multiplication?
# Answer:


# %%
result1 = a_column @ a_column.T
result2 = a @ a.T
result3 = np.outer(a, a)

# TODO: answer these questions as comments below:
# What does transposing a vector as a 1D array do (a.T)?
# Answer:

# Is result1 the same as result2 or result3?
# Answer:

# (T/F) I can compute an outer product using 1D arrays and transposes.
# Answer:


# %%
## Read the following when you are done with the above TODOs:

# Note: * does scalar or element-wise multiplication, while @ does matrix multiplication.

# Note: when doing matrix-vector multiplication where the vector is a 1D array,
# numpy will automatically treat the vector as a row or column vector based on
# the operation being performed. This is different from MATLAB where a vector
# is always treated as a column vector unless transposed.
# For example: vec @ matrix will treat vec as a row vector, while matrix @ vec
# will treat vec as a column vector.

# Note: when doing vector-vector multiplication with 1D arrays, numpy will always
# do a dot product. You can not do a @ a.T to achieve an outer product, instead
# you can use np.outer(a, a) to perform an outer product. Another possible
# vector-vector operation is a cross product, which can be done with np.cross(a, b).

# Note: when using vectors as 2D arrays, they are essentially matrices and @ operations
# should behave as you would expect from linear algebra if you pay attention the
# their shapes.

# TODO: leave a comment below stating that you read the previous 4 notes.
# Answer:


# if you still have questions about broadcasting, and array dimensions, please see the following:
# https://numpy.org/doc/stable/user/basics.broadcasting.html
# https://www.youtube.com/watch?v=oG1t3qlzq14

# %%
# A quick introduction to memory management in numpy
a = np.ones(3)
b = a
b += 1

# TODO: answer these questions as comments below:
# Before looking at the output, what do you think a and b will be?
# Answer:

# After looking at the output, were you correct? Why or why not?
# Answer:


# %%
a = np.ones(3)
b = a.copy()
b += 1

# TODO: answer these questions as comments below:
# Did changing b also change a this time? Why or why not?
# Answer:


# %%
# One last memory management example - we will do essentially the same thing
# in all of the simulations throughout the course.
x_hist = []
x = np.zeros(3)
for i in range(3):
    x += 1
    x_hist.append(x)
x_hist = np.array(x_hist)


# TODO: answer these questions as comments below:
# We want the history of x at each step, so we want x_hist to be an array of
# [[1,1,1], [2,2,2], [3,3,3]].
# Did we achieve this? If not, what is x_hist?
# Answer:

# TODO: fix the code so that x_hist contains what we want (only modify lines
# inside of the for loop).

# hints:
#  - you could use .copy() somewhere
#  - you could avoid using +=, which modifies the array in place (no copy)

# %%

