# Copyright (c) 2015, Imperial College London
# All rights reserved.
# 
# Redistribution and use in source and binary forms, with or without 
# modification, are permitted provided that the following conditions are met:
# 
# 1. Redistributions of source code must retain the above copyright notice, 
# this list of conditions and the following disclaimer.
# 
# 2. Redistributions in binary form must reproduce the above copyright notice, 
# this list of conditions and the following disclaimer in the documentation 
# and/or other materials provided with the distribution.
# 
# 3. Neither the names of the copyright holders nor the names of their 
# contributors may be used to endorse or promote products derived from this 
# software without specific prior written permission.
# 
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" 
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE 
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE 
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE 
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR 
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF 
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS 
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN 
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) 
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE 
# POSSIBILITY OF SUCH DAMAGE.
# -----------------------------------------------------------------------------
#
# This file is part of the libhpc-cf Coordination Forms library that has been 
# developed as part of the libhpc projects 
# (http://www.imperial.ac.uk/lesc/projects/libhpc).
#
# We gratefully acknowledge the Engineering and Physical Sciences Research
# Council (EPSRC) for their support of the projects:
#   - libhpc: Intelligent Component-based Development of HPC Applications
#     (EP/I030239/1).
#   - libhpc Stage II: A Long-term Solution for the Usability, Maintainability
#     and Sustainability of HPC Software (EP/K038788/1).
'''
File created on Aug 7, 2012

@author: jhc02
'''

class Parameter():
    '''
    A parameter (component port) and its associated metadata to be passed to a
    coordination forms operator.
    '''
    
    # A unique string identifier for this parameter
    # While the content can be anything, a package style structure is recommended
    param_id = ''
    
    # The type of parameter: string, int, float
    param_types = ['string','int','float','list']
    param_dir = ['input','output','inout']
    type = 'string'
    dir = 'input'
    ignore_param = False
    index = None
    
    # The value of this parameter
    # value
    

    def __init__(self, id, type, dir='input', ignore=None, index=None, value=None):
        '''
        Constructor
        '''
        print 'Creating a new coordination forms parameter...'
        self.param_id = id
        if type not in self.param_types:
            raise ValueError(type + ' is not an accepted parameter data type value')
        self.type = type
        if dir not in self.param_dir:
            raise ValueError(dir + ' is not an accepted parameter direction value')
        self.dir = dir
        if (ignore != None) and ((ignore == True) or (ignore == False)):
            self.ignore_param = ignore
        if (index != None) and (index >= 0):
            self.index = index
        self.value = value
        print 'Creating a new coordination forms parameter...\n\tID: ' + self.param_id + '\tType: ' \
            + self.type + '\tValue: ' + str(self.value) + '\n\tDirection: ' + self.dir + '\tIgnore: ' \
            + str(self.ignore_param) + '\tIndex: ' + str(self.index) + '\n'
        
    def get_id(self):
        return self.param_id
    
    def get_type(self):
        return self.type

    def get_dir(self):
        return self.dir
    
    def get_value(self):
        return self.value
    
    def ignore(self):
        return self.ignore_param

class ParameterList():
    '''
    A list of parameter objects to be passed to a coordination 
    forms operator
    '''

    parameter_list = []

    def __init__(self, *param_list):
        '''
        Constructor
        '''
        print 'Creating a new coordination forms parameter list with ' + len(param_list) + ' arguments...'
        
        for param in param_list:
            self.parameter_list.append(param)
    
    # Return the length of the parameter list
    def __len__(self):
        return len(self.parameter_list)
    
    def get_param(self, num):
        # TODO: Error checking
        return self.parameter_list[num]
    