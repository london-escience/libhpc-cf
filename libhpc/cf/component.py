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
import sys
import importlib
import threading

import params
from collections import Iterable

class Component():
    '''
    A function and its associated metadata to be run with some
    coordination forms parameters.
    '''
    
    # A unique string identifier and human-readable name for this function
    # While the ID content can be anything, a package style structure is recommended
    component_id = ''
    component_name = ''
    component_code = ''
    
    # Metadata for parameters and return types - list of instances of cfparams.Parameter
    parameters = []
    # Metadata for function return types - list of cfparams.Parameter (function may return list or tuple) 
    return_data = []
    #dependencies = []
    # Additional parameters - whether these should be added to the parameter list before or
    # after existing params. In some case this matters.
    additional_params = 'pre'

    def __init__(self, id, name, function_entry_point, input_params, return_params, static_pos = 'post'):
        '''
        Constructor
        '''
        print 'Creating a new coordination forms component...'
        self.component_id = id
        self.component_name = name
        self.component_code = function_entry_point
        self.parameters = input_params
        self.return_data = return_params
        self.static_params_pos = static_pos
        #self.dependencies = dependencies
        print 'Creating a new coordination forms component...\n\tID: '  + self.component_id + '\tType: ' + self.component_name + '\n'
        
    def get_id(self):
        return self.component_id
    
    def get_name(self):
        return self.component_name
    
    def get_params(self):
        return self.parameters
    
    def get_return_data(self):
        return self.return_data
    
    def get_code(self):
        return self.component_code
    
    def get_dependencies(self):
        return self.dependencies
    
    def static_params_pre(self):
        if self.static_params_pos == 'pre':
            return True
        else:
            return False

    def run(self, parameter_list, result_store=None):
        print 'Parameter list provided: <' + str(parameter_list) + '>\n\n'
        if not hasattr(parameter_list, '__iter__'):
                parameter_list = [parameter_list]
                
        print 'Component to run: ' + self.component_name + ' - ' + str(len(parameter_list)) + ' parameters.\n'
        
        # Handle lookup of function code that we're going to run.
        # Lookup uses the string providing the package and name of the function 
        function_parts = self.component_code.rsplit('.',1)
        func = None
        if len(function_parts) == 2:
            #mod = __import__(function_parts[0])
            mod = importlib.import_module(function_parts[0])
            sys.stdout.write('Got module ' + str(mod) + '\n')
        else:
            sys.stdout.write('ValueError: The provided component_name <' + str(function_parts) + '> is invalid, a fully qualified name must be specified.\n')
            raise ValueError('The provided component_name <' + str(function_parts) + '> is invalid, a fully qualified name must be specified.')
        func = getattr(mod, function_parts[1], None)
        sys.stdout.write('Checking if function ' + str(func) + ' is callable...function parts: ' + str(function_parts) + '\n')
        if callable(func):
            sys.stdout.write('Function is callable\n\n')
            # Do any pre/post processing of function data here.
            sys.stdout.write(threading.current_thread().getName() + ': About to run function...\n\n')
            # TODO: Handle None inputs to parameter list? Received an earlier error about marshalling
            # values to unicode and thought this was because I was passing a None as a parameter. Check this.
            # Problem occurred when calling fastqplitter with None as a parameter. 
            result = func(*parameter_list)
            
            # Turn off returning result as a tuple for now.
            #if type(result) != type(tuple()):
            #    result = (result,)
            
            result_length = 1
            if hasattr(result,'__iter__'):
                result_length = len(result)
            print 'Function <' + self.get_name() + '> has completed and returned <' + str(result_length) + '> values.\n'
            
            # We now prepare a tuple to return. This contains all the parameters
            # That are marked as outputs and not marked as being ignored.
            # A list will be built and converted to a tuple
            return_list = []
            
            # First check the function return value. This may be a single value or
            # an iterable list. If its length is 1 we assume its just a single return value.
            # If its greater than 1 we assume its wrapped in a list or tuple. We build a corresponding
            # list that will end up as the first element of return_list
            count = 0
            if len(self.return_data) == 0:
                # No value is returned so ignore return value
                pass
            elif len(self.return_data) == 1: 
                if not self.return_data[0].ignore():
                    # We're returning a single value, it may be wrapped in
                    # a tuple or list or may be an unwrapped value
                    if hasattr(result,'__iter__'):
                        #return_list.append(result[0])
                        return_list.append(result)
                    else:
                        return_list.append(result)
                count = count + 1
            else:
                return_result_list = []
                for value in self.return_data:
                    if not value.ignore():
                        # TODO: Do we want to package up the main return value as a list
                        # leading to the following line appending result[0][count]?
                        return_result_list.append(result[count])
                    count = count + 1
                return_list.append(return_result_list)
            
            # Now we go through the other parameters in turn, adding them to the 
            # return list if they're marked as output and not marked to be ignored.
            print 'Count is: ' + str(count) + ', we\'re expecting the remaining return values in the result tuple.'
            for value in self.parameters:
                if (value.get_dir() == 'output') or (value.get_dir() == 'inout'):
                    if not value.ignore():
                        return_list.append(result[count])
                    count = count + 1
            
            # If we've been provided with a result store and an
            # associated index, we store the result here, otherwise
            # we return the result. result_store[0] is the list for results to
            # be stored to, result_store[1] is the index at which to store the result  
            if result_store != None:
                print 'Storing result <' + str(return_list) + '> to result store index ' + str(result_store[1])
                print 'Result array: ' + str(result_store[0])
                if len(return_list) == 1:
                    print 'Storing single value to result store for function <' + self.get_name() + '>.'
                    result_store[0][result_store[1]] = return_list[0]
                elif len(return_list) > 1:
                    print 'Storing <' + str(len(return_list)) + '> values from function <' + self.get_name() + '> to result store.'
                    result_store[0][result_store[1]] = tuple(return_list)
                #else:
                #   result_store[0][result_store[1]] = result
        
            if len(return_list) == 1:
                print 'Returning a single value from function <' + self.get_name() + '>.'
                return return_list[0]
            elif len(return_list) > 1:
                print 'Returning <' + str(len(return_list)) + '> values from function <' + self.get_name() + '>.'
                return tuple(return_list)
            else:
                print 'Nothing to return from function <' + self.get_name() + '>.'
        
class ComponentList():
    '''
    A list of parameter objects to be passed to a coordination 
    forms operator
    '''

    component_list = []

    def __init__(self, *component_list):
        '''
        Constructor
        '''
        print 'Creating a new coordination forms component list with ' + len(component_list) + ' components...'
        
        for comp in component_list:
            self.component_list.append(comp)
    
    # Return the length of the parameter list
    def __len__(self):
        return len(self.component_list)
    
    def get_function(self, num):
        # TODO: Error checking
        return self.component_list[num]
    