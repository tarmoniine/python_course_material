
# coding: utf-8

# In[1]:

from Bio import pairwise2


# ### Task:
# 
# You have two sequences:
# seq1 = 'ACGTCCTTCATT'
# seq2 = 'GTCTCATG'
# 
# You have a scoring scheme where
# * a match gives you +1
# * a mismatch gives you 0
# * gap opening costs −10
# 
# Find the best alignment of the two sequences.
# 
# You have a scoring scheme where:
# * a match gives you +1
# * a mismatch gives you −1
# * gap opening costs you −1
# 
# Find the best alignment of the two sequences.
# 
# HINT: look at the following documentation page 
# for Biopython:
# http://biopython.org/DIST/docs/api/Bio.pairwise2-module.html

# In[2]:

seq1 = 'ACGTCCTTCATT'
seq2 =  'GTCTCATG'
pairwise2.align.localms(seq1, seq2, 1, 0, -10, -10000000)


# In[3]:

pairwise2.align.localms(seq1, seq2, 1, -1, -1, -10000000)


# ### The format_alignment function
# 
# pairwise2 has a format_alignment function to better visualize the alignment output. 

# In[4]:

out_tuplesA = pairwise2.align.localms(seq1, seq2, 1, 0, -10, -10000000)
out_tuplesB = pairwise2.align.localms(seq1, seq2, 1, -1, -1, -10000000)

print('1, 0, -10, -inf:')
for ot in out_tuplesA:
    print(pairwise2.format_alignment(*ot))
    
print('\n1, -1, -1, -inf:')
for ot in out_tuplesB:
    print(pairwise2.format_alignment(*ot))


# ### Using the Entrez databases via Biopython
# 
# You can access all of the information in the Entrez databases 
# via Biopython, although a new Python package, Bioservices, is 
# probably easier and provides access to MANY different online 
# databases. https://pythonhosted.org/bioservices/

# In[5]:

from Bio import Entrez
Entrez.email = 'tniine@gmail.com'


# In[6]:

handle = Entrez.einfo()
record = Entrez.read(handle)
record['DbList']


# In[7]:

handle = Entrez.einfo(db='pubmed')
record = Entrez.read(handle)
record['DbInfo']['Description']


# In[8]:

handle = Entrez.esearch(db='pubmed', term='persister')
record = Entrez.read(handle)
record['IdList']


# In[9]:

handle = Entrez.efetch(db='pubmed', id='25267859')
print(handle.read())


# ### Curve fitting
# 
# One common task for biologists is to fit experimental data 
# to a function. For example, one may want to fit a 4 parameter 
# logistic equation to enzyme-linked immunosorbent assay (ELISA) 
# data. The usual formula for this model is:
# 
# $f(x) = \frac{A - D}{1 + \left(\frac{x}{C}\right)^B} + D$,
# 
# where $x$ is the concentration, $A$ is the minimum asymptote, $B$ is the steepness, $C$ is the inflection point and $D$ is the maximum asymptote.

# In[11]:

#get_ipython().magic('matplotlib inline')
import numpy as np
#import numpy.random
import matplotlib.pyplot as plt
from scipy.optimize import leastsq

def logistic4(x, A, B, C, D):
    '''Four parameter logistic equation.
    
    $f(x) = \frac{A - D}{1 + \left(\frac{x}{C}\right)^B} + D$
    '''
    return ((A-D)/(1.0+((x/C)**B))) + D

def residuals(parameters, y, x):
    '''Deviations of data from logistic4'''
    A, B, C, D = parameters
    #we need to know the error
    err = y - logistic4(x, A, B, C, D)
    return err

# Make up some data for fitting and add noise
# In practice, y_meas would be read in from a file
#x_mesured - tells how many data points there are.
x_measured = np.linspace(0, 20, 12)
#100 points along x telg
x_true = np.linspace(0, 20, 100)

# True parameter values
#here we are giving answer in advance.
A, B, C, D = true_parameters = 0.5, 2.5, 8, 7.3
y_true = logistic4(x_true, *true_parameters)#A, B, C, D)

# Simulated measurements of data.
#samples from the normal distripution, we also add the errors here to the "perfect" data
y_measured = logistic4(x_measured, *true_parameters) + 0.2 * np.random.randn(len(x_measured))

# Initial guess for parameters
# usually it doesnot mather which values we put in here.
initial_parameters = [0, 1, 1, 1]

# Fit equation using least squares optimization
# 
leastsq_output = leastsq(residuals, initial_parameters, args=(y_measured, x_measured))

# Plot results
# r-- red line, bo - blue dots, loc= position of the legend
plt.plot(x_true, logistic4(x_true, *leastsq_output[0]), 'r--')
plt.plot(x_measured, y_measured, 'bo')
plt.plot(x_true, y_true, 'g-')
plt.title('Least squares fit to logistic equation with noisy data')
plt.legend(['Fit', 'Data', 'True'], loc='upper left')


plt.text(10, 2.5, 'Parameter   True   Estimated')
for index, estimated_value in enumerate(leastsq_output[0]):
    param_key = 'ABCD'[index]
    true_value = true_parameters[index]
    plot_text = '{:>10} {:>12.2f} {:>10.2f}'.format(param_key, true_value, estimated_value)
    plt.text(10, 2-index*0.5, plot_text)

#plt.show()
plt.savefig('test.pdf')

# In[ ]:


