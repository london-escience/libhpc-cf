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
import threading

import types
from collections import Iterable
from funcs import Function
import Queue

PAR_TASK_IDENTIFIER_INT = '<<PAR_TASK_ID, int>>'
PAR_TASK_IDENTIFIER_STRING = '<<PAR_TASK_ID, string>>'

# A library of coordination forms that provide high-level
# constructs for defining application flow

# The PIPE form takes a list of functions where each requires the 
# output of the following function as its input. Each function
# accepts a parameter list where each item is a parameter object
# that contains metadata describing the parameter.
# PIPE returns a function that will enact the requested PIPE operation
# when called. The elements of the function_list parameter may be 
# instances of cffuncs.Function or may be functions representing other
# coordination forms.
#
# PIPE is passed a list of functions and the initial parameter list.
# If the initial parameter list is empty, it is expected to be passed in
# to the partially prepared PIPE function that is returned.
def PIPE(function_list, initial_param_list = None):
    print "PIPE cf called...preparing PIPE function...\n"
    print 'Received a list of ' + str(len(function_list)) + ' functions\n'
    
    if initial_param_list == None:
        print "No initial param list provided, the generated function will expect this as its first parameter...\n"
    
    
    def PIPE_implementation(initial_param_list = initial_param_list, par_task_id = None):
        # Work through the function list in reverse
        # Elements may be instances of cffuncs.Function or may be
        # functions resulting from the pre-evaluation of nested
        # coordination forms.
        count = 0
        output = None
        
        for func_element in reversed(function_list):
            # An element of the PIPE may be an instance of cffuncs.Function
            # or a tuple containing an instance of cffuncs.Function as the
            # first element followed by parameters as the subsequent elements.
            
            func = None
            new_params = None
            
            # If we have a tuple, extract the function and the other params
            if type(func_element) == type(tuple()):
                func = func_element[0]
                new_params = func_element[1:]
                
                # At this point, we run through the new params
                # and look to see if any of them contain the PAR_TASK_ID
                # tag. If so, we replace this tag with the PAR task id number.
                # We set par task id to -1 if one is not specified and this
                # PIPE is therefore not running as part of a PAR task
                if par_task_id == None:
                    print 'PIPE: No parallel task identifier provided, assume we\'re not running in a PAR and setting task_id to 0.'
                    par_task_id = 0
                else:
                    print 'PIPE: We\'re running in a PAR environment. Checking additional inputs for task id replacement...'
                new_params = process_param_tags(new_params, par_task_id)
            else:
                func = func_element
            
            # Prepare parameters - if we're at element 0 then read input from initial_param_list
            # If for some reason there are params provided in new_params then we prepend the
            # initial_param_list to these params.
            print 'PIPE: Initial output value for function ' + str(count) + ' before adding new_params: <' + str(output) + '>\n'
            print 'PIPE: New params for function ' + str(count) + ' <' + str(new_params) + '>'
            
            # If we're on the first iteration, add the initial params to new_params
            if count == 0:
                if initial_param_list == None:
                    print 'initial_param_list is empty, assume first element of PIPE' \
                        ' is another cf that will produce initial parameter list.\n'
                elif new_params != None:
                    # Need to check whether 'new_params' (those added into pipe in tuple with function name)
                    # are placed before or after the output params from the previous function
                    # Get metadata from function to determine whether to add additional
                    # params before or after existing params
                    if func.static_params_pre():
                        output = list(new_params) + list(initial_param_list) 
                    else:
                        output = list(initial_param_list) + list(new_params)
                else:
                    output = list(initial_param_list)
            else:
                # Need to check whether 'new_params' (those added into pipe in tuple with function name)
                # are placed before or after the output params from the previous function
                # Get metadata from function to determine whether to add additional
                # params before or after existing params
                if new_params != None:
                    # If previous output value was not wrapped in list, wrap it now
                    if type(list()) != type(output):
                        output = [output]
                    if func.static_params_pre():
                        output = list(new_params) + output
                    else:
                        output = output + list(new_params)
            
            print 'PIPE: Complete input to function ' + str(count) + ' <' + str(output) + '>\n'
            
            # Check if func is an instance of cffuncs.Function or a function
            # resulting from the pre-evaluation of another coordination forms expression
            if isinstance(func, Function):
                # if we reach this code, the current element of the PIPE is a
                # standard function that will be called via its metadata object.
                # If we're at element 0, the input may be coming from some
                # other coordination form that has not yet been evaluated.
                print 'Function ' + func.get_code() + ' requires ' + str(len(func.parameters)) + ' params. '
                print 'Function input contains: ' + str(len(output)) + ' params\n'
                
                # Count up the expected number of input parameters
                expected_input_count = 0
                for p in func.parameters:
                    if p.get_dir() == 'input':
                        expected_input_count = expected_input_count + 1
                print 'Expecting at least <' + str(expected_input_count) + '> input params for function <' \
                    + func.get_name() + '> which takes total of ' + str(len(func.parameters)) + ' params\n'
                if len(output) < expected_input_count:
                    raise ValueError('Function ' + func.get_code + ' has ' + str(len(func.parameters)) + \
                        ' parameters and expects ' + str(expected_input_count) + ' input parameters but only ' \
                        + str(len(output)) + ' are available.')
                
                print 'About to run function <' + func.get_code() + '>...\n'
                output = func.run(output)
            elif isinstance(func, types.FunctionType):
                # If we reach this code, we assume that this element of the
                # PIPE is a pre-evaluated, nested, coordination forms expression
                # If we're at element 0, the input may be coming from some
                # other coordination form that has not yet been evaluated.
                print 'About to run pre-evaluated function <' + func.__name__ + '>...\n'
                if type(output) != type(list()):
                    # Need to check why output must be wrapped as list
                    # This causes an issue for nested split elements
                    # Replacing wrapping of tuple with list with conversion to a list
                    if output != None:
                        #output = [output]
                        if type(output) == type(""):
                            output = [output]
                        else:
                            output = list(output)
                output = func(output)
            else:
                print('One of the functions in the function_list is of an unknown type. Unable to evaluate this PIPE expression...')
                raise ValueError('One of the functions in the function_list is of an unknown type. Unable to evaluate this PIPE expression...')

            print 'Processing function ' + str((count+1)) + ' of ' + str(len(function_list)) + '\n'
            count += 1
            
        return output
    
    # Return the PIPE implementation function
    return PIPE_implementation
    
# The PAR form takes a list of functions that can be run in parallel.
# It identifies the most suitable way to run these functions.
# This may be sequentially, as multiple concurrent threads or on 
# separate machines.
# PAR returns a new function that will carry out this computation when 
# its run method is called.
# Ultimately there will be multiple implementations of this PAR function
# but for now, there will be a single, hard-coded multi-threaded implementation
def PAR(function_list, param_list=None):
    print "PAR cf called...preparing parameters\n"

    # If param_list is none, we expect to find the parameters
    # in a tuple with the function name. If its not None,
    # the function name is likely to be on its own and params
    # are pulled from the list.
    
    # If the parameter list is not none, it should be the same
    # length as the function list
    
    # TODO: Is this correct? Don't we need to check if each element of function_list
    # is the length of the corresponding element of param_list?
    if param_list == None:
        print 'We have missing parameters, these will be passed with function call\n'
    else:
        print 'Parameter list provided, checking the correct number of params have been provided\n'
        if not len(function_list) == len(param_list):
            raise ValueError('A parameter list has been provided. ' \
                    'This must be the same length as the function list <' \
                    + str(len(function_list)) + '> but is of length <' + str(len(param_list)) + '>')
    
#        # We need to ensure that all elements of the param_list are tuples so that
#        # they can be correctly processed.
#        element_count = 0
#        for element in param_list:
#            if type(element) != type(tuple()):
#                param_list[element_count] = tuple([element])
#            element_count = element_count + 1
    
    print "PAR cf...generating PAR implementation\n"
    def PAR_implementation(base_params=None, function_list = function_list):
    
        output = [None] * len(function_list)
        thread_list = []
        
#        if base_params != None:
#            # We need to ensure that all elements of the base_params list are
#            # tuples so that they can be correctly processed.
#            element_count = 0
#            for element in base_params:
#                if type(element) != type(tuple()):
#                    base_params[element_count] = tuple([element])
#                element_count = element_count + 1
    
        # For each function in the function list prepare a new thread
        # that will run the function. Results will be assigned in the order
        # of function_list to the output array.
        count = 0
        for func_element in function_list:
            print 'Handling func_element ' + str(count) + ': ' + str(func_element) 
            # If we have a tuple, extract the function and the other params
            func = None
            params = []
            
            
            # TODO: If we have missing parameters, check that the right number are provided.
            
            # parameters = []
            # See if we've been given a tuple containing a function and params,
            # or whether we've just been given the function
            if type(func_element) == type(tuple()):
                func = func_element[0]
                static_params = list(func_element[1:])
                # If we've got base params to which the static params are added, 
                # make sure the static params are placed correctly before or after
                # base params depending on the function metadata
                if static_params != None:
                    if func.static_params_pre():
                        print 'Place static params <' + str(static_params) + '> for partial func_list BEFORE existing params <' + str(base_params[count]) + '>\n'
                        params = static_params + [base_params[count]]
                    else:
                        print 'Place static params <' + str(static_params) + '> for partial func_list AFTER existing params <' + str(base_params[count]) + '>\n'
                        params = [base_params[count]] + static_params
            else:
                func = func_element
                if (param_list == None) and (base_params == None):
                    raise ValueError('Function was called without parameters, expecting to find parameters in param_list but this is also empty.')
                if param_list != None:
                    if hasattr(param_list[count], '__iter__'):
                        params = list(param_list[count])
                    else:
                        params = list([param_list[count]])
                if base_params != None:
                    if hasattr(base_params[count], '__iter__'):
                        params = params + list(base_params[count])
                    else:
                        params = params + list([base_params[count]])
            
            # At this point we've processed the parameters and combined any
            # params provided in the original parameter list with any additional
            # parameters added through a function tuple. We can now pre-process any
            # task identifier tags.
            params = process_param_tags(params, count)
            
            # We've now split the function and parameters into separate groups            
            print 'Parameters for passing to thread: ' + str(params)
            print 'Tuple of params to call thread function with: ' + str(tuple(params))
            
            
            # func may be an instance of the Function class or another (nested)
            # co-ordination form.
            if isinstance(func, Function):
                print 'About to run function <' + func.get_code() + '>, additional params provided <' + str(params) + '>...\n'
                # Create a thread for this function
                thread_list.append(threading.Thread(target=func.run, args=[tuple(params), (output, count)]))
            elif isinstance(func, types.FunctionType):
                print 'About to run nested non-function object <' + str(func) + '>, additional params provided <' + str(params) + '>...\n'
                #thread_list.append(threading.Thread(target=func, args=[tuple(params), (output, count)]))
                # Based on the info here: http://stackoverflow.com/questions/6893968/how-to-get-the-return-value-from-a-thread-in-python
                # we're using a wrapper function to get the result from the nested function object
                # that is called by the thread
                def func_wrapper(parameter_list, result_store=None, func=func):
                    return_value = func(parameter_list)
                    if result_store != None:
                        print 'PAR_NESTED_FORM: Storing result <' + str(return_value) + '> to result store index ' + str(result_store[1])
                        print 'PAR_NESTED_FORM: Result array: ' + str(result_store[0])
                        print 'PAR_NESTED_FORM: Storing return value to result store for function <' + str(func) + '>.'
                        result_store[0][result_store[1]] = return_value
                
                #result_queue = Queue.Queue()
                
                # Create a thread for this function
                new_thread = threading.Thread(target=func_wrapper, args=[tuple(params), (output, count)])
                #new_thread.result_queue = result_queue
                thread_list.append(new_thread)
                
            else:
                print('PAR: One of the functions in the function_list is of an unknown type. Unable to evaluate this PAR expression...')
                raise ValueError('PAR: One of the functions in the function_list is of an unknown type. Unable to evaluate this PAR expression...')
            
            count = count+1
            
        # Run the threads
        print 'We now have a list of <' + str(len(thread_list)) + '> functions to run in parallel...'
        for thread_to_run in thread_list:
            thread_to_run.start()
    
        # Set a join to wait until all jobs are completed
        print 'Waiting for all parallel jobs to complete...'
        for thread_to_run in thread_list:
            thread_to_run.join()
        print 'All parallel jobs have completed...'
        
        print 'Final output: ' + str(output)
        return output

    return PAR_implementation
    
def GET_CF_RUNNER(cf_string):
    pass

# The BYPASS form is applied to a function that is to be run
# but have its output bypassed. The provided function is run with
# the specified input and the input is then directed to the output.
def BYPASS(func, params=None, par_task_id = None):
    print "BYPASS cf called...preparing parameters\n"

    # If param_list is none, we expect to find the parameters
    # in a tuple with the function name. If its not None,
    # the function name is likely to be on its own and params
    # are pulled from the list.
    
    # If the parameter list is not none, it should be a single item
    # or a tuple of multiple parameters
    
    if params == None:
        print 'BYPASS: Parameters not provided, we expect to receive these with function call\n'
    else:
        print 'BYPASS: Parameter list provided\n'
        
    
    print "BYPASS cf...generating BYPASS implementation\n"
    def BYPASS_implementation(param_list = params, func = func, par_task_id = None):
    
        print 'Handling function ' + str(func)
       
        # The function passed to BYPASS may be an instance of cffuncs.Function
        # or a tuple containing an instance of cffuncs.Function as the
        # first element followed by parameters as the subsequent elements.
        
        new_params = None
        output = None
        
        # If we have a tuple, extract the function and the other params
        # Otherwise, func is already the function so leave it as is
        if type(func) == type(tuple()):
            new_params = func[1:]
            func = func[0]
            
            # At this point, we run through the new params
            # and look to see if any of them contain the PAR_TASK_ID
            # tag. If so, we replace this tag with the PAR task id number.
            # We set par task id to -1 if one is not specified and this
            # PIPE is therefore not running as part of a PAR task
            if par_task_id == None:
                print 'BYPASS: No parallel task identifier provided, assume we\'re not running in a PAR and setting task ID to 0.'
                par_task_id = 0
            else:
                print 'BYPASS: We\'re running in a PAR environment. Pre-processing parameters for tags.'
            new_params = process_param_tags(new_params, par_task_id)
                    
        # If for some reason there are params provided in new_params then we prepend the
        # initial_param_list to these params.
        print 'BYPASS: Initial params for function <' + str(params) + '>'
        print 'BYPASS: New params for function <' + str(new_params) + '>'
        
        if param_list == None:
            print 'param_list is empty so assuming we\'ll receive params on function call'
        elif new_params != None:
            # Need to check whether 'new_params' (those added into pipe in tuple with function name)
            # are placed before or after the output params from the previous function
            # Get metadata from function to determine whether to add additional
            # params before or after existing params
            if func.static_params_pre():
                output = list(new_params) + list(param_list) 
            else:
                output = list(param_list) + list(new_params)
        else:
            output = list(param_list)
        
        print 'BYPASS: Complete input to function <' + str(output) + '>\n'
        
        # Check if func is an instance of cffuncs.Function or a function
        # resulting from the pre-evaluation of another coordination forms expression
        if isinstance(func, Function):
            # if we reach this code, the cfunction provided to BYPASS is a
            # standard function that will be called via its metadata object.
            # The input may be coming from some
            # other coordination form that has not yet been evaluated.
            print 'Function ' + func.get_code() + ' requires ' + str(len(func.parameters)) + ' params. '
            print 'Function input contains: ' + str(len(output)) + ' params\n'
            
            # Count up the expected number of input parameters
            expected_input_count = 0
            for p in func.parameters:
                if p.get_dir() == 'input':
                    expected_input_count = expected_input_count + 1
            print 'Expecting at least <' + str(expected_input_count) + '> input params for function <' \
                + func.get_name() + '> which takes total of ' + str(len(func.parameters)) + ' params\n'
            if len(output) < expected_input_count:
                raise ValueError('Function ' + func.get_code + ' has ' + str(len(func.parameters)) + \
                    ' parameters and expects ' + str(expected_input_count) + ' input parameters but only ' \
                    + str(len(output)) + ' are available.')
            
            print 'About to run function <' + func.get_code() + '>...\n'
            output = func.run(output)
        elif isinstance(func, types.FunctionType):
            # If we reach this code, we assume that this BYPASS contains
            # a pre-evaluated, nested, coordination forms expression
            # The input may be coming from some
            # other coordination form that has not yet been evaluated.
            print 'About to run pre-evaluated function <' + func.__name__ + '>...\n'
            if type(output) != type(list()):
                if output != None:
                    output = [output]
            output = func(output)
        else:
            print('BYPASS: The function provided is of an unknown type. Unable to evaluate this BYPASS expression...')
            raise ValueError('BYPASS: The function provided is of an unknown type. Unable to evaluate this BYPASS expression...')

        print 'BYPASS: Handled function ' + str(func.get_code()) + '\n'
            
        return param_list

    return BYPASS_implementation

# The SPLIT form takes a single list of inputs and splits this list into
# two equal parts.
def SPLIT(param=None):
    print "SPLIT cf called...preparing parameters\n"

    # If param is none, we expect the input parameter to be
    # passed in when the implementation is called.
    if param == None:
        print 'SPLIT: No input provided, this will be passed with the function call...\n'
    else:
        print 'SPLIT: Input parameter provided, checking that this is a list or tuple\n'
        if not (type(param) == type([])) or (type(param) == type(tuple())):
            raise ValueError('SPLIT: The parameter provided is not a list or a tuple: ' \
                    + str(param))
        
    print "SPLIT cf...generating SPLIT implementation\n"
    def SPLIT_implementation(new_param = None, base_params=param):

        print "Running SPLIT implementation with base_params: " + str(base_params) + " and new parameters: " + str(new_param)
        # Prepare a two item list to contain the split input params    
        output = [None] * 2
        if base_params == None:
            if type(new_param) == type(tuple()):
                base_params = tuple()
            else:
                base_params = []
        
        # If we've been given new params, concatenate them with the original list
        if new_param != None:
            if type(new_param) != type(base_params):
                new_param = list(new_param)
                base_params = list(base_params)
            
            # Concatenate parameters
            base_params += new_param
        
        if(len(base_params) % 2 == 0):
            output[0] = base_params[:len(base_params)/2]
            output[1] = base_params[len(base_params)/2:]
        else:
            output[0] = base_params[:len(base_params)/2+1]
            output[1] = base_params[len(base_params)/2+1:]
        
        return output

    return SPLIT_implementation

# The FILTER form takes a list of integers and a list or tuple  
# of function output data is its input. The integer list defines the indices
# of the function output data to be passed on to the next function.
# A new list or tuple is generated (dependent on the input type) and this
# contains only the specified indices from the input data.
def FILTER(selection_indices, params=None):
    print "FILTER cf called...preparing parameters\n"

    # If param_list is none, we expect to find the parameters
    # in a tuple with the function name or provided at a later time
    # when the function is called. If its not None,
    # the function name is likely to be on its own and params
    # are pulled from the list.
    
    # If the parameter list is not none, it should be a single item, a list
    # or a tuple of multiple parameters
    
    if params == None:
        print 'FILTER: Parameters not provided, we expect to receive these with function call\n'
    else:
        print 'FILTER: Parameter list provided\n'
        
    
    print "FILTER cf...generating FILTER implementation\n"
    def FILTER_implementation(param_list = params, selection_indices = selection_indices):

        print 'FILTER: Input data to filter: ' + str(param_list)
            
        # Check that a list of integers was provided for the selection indices
        if type(selection_indices) != type([]):
            print "FILTER: No selection indices specified, returning empty list"
            return []
        
        # Check that enough parameters are available to satisfy all indices in the list
        if max(selection_indices) > len(param_list)-1:
            print "FILTER: A selection index of " + str(max(selection_indices)) + \
                " (zero indexed) was specified but only " + str(len(param_list)) + \
                " input parameters have been provided. Returning empty list."
            return []
           
        # Otherwise we now know that we can satisfy the requirements of the input
        # so we build a new output list based on the positions and order specified
        # in the selection indices list.
        if (type(param_list) != type([])) and (type(param_list) != type(tuple())):
            return [param_list]
        
        output_list = []
        for index in selection_indices:
            output_list.append(param_list[index])
                
        if type(param_list) == type(tuple()):
            # Convert output to tuple so its in the same format as original input
            output_list = tuple(output_list)
        
        print "FILTER: Return data from filter: " + str(output_list)
        
        return output_list

    return FILTER_implementation

# The APPEND form takes a component or co-ordination form description
# and runs this entity, appending its output to the original input data  
def APPEND(func, params=None):
    print "APPEND cf called...preparing parameters\n"

    # If param_list is none, we expect to find the parameters
    # in a tuple with the function name. If its not None,
    # the function name is likely to be on its own and params
    # are pulled from the list.
    
    # If the parameter list is not none, it should be a single item
    # or a tuple of multiple parameters
    
    if params == None:
        print 'APPEND: Parameters not provided, we expect to receive these with function call\n'
    else:
        print 'APPEND: Parameter list provided\n'
        
    
    print "APPEND cf...generating APPEND implementation\n"
    def APPEND_implementation(param_list = params, func = func):
    
        print 'Handling function ' + str(func)
       
        # The function passed to BYPASS may be an instance of cffuncs.Function
        # or a tuple containing an instance of cffuncs.Function as the
        # first element followed by parameters as the subsequent elements.
        # Alternatively it may a nested coordination form - an instance of 
        # types.FunctionType
        
        new_params = None
        input = None
        output = None
        
        # If we have a tuple, extract the function and the other params
        # Otherwise, func is already the function so leave it as is
        if type(func) == type(tuple()):
            new_params = func[1:]
            func = func[0]
                                
        # If for some reason there are params provided in new_params then we prepend the
        # initial_param_list to these params.
        print 'APPEND: Initial params for function <' + str(params) + '>'
        print 'APPEND: New params for function <' + str(new_params) + '>'
        
        if param_list == None:
            print 'param_list is empty so assuming we\'ll receive params on function call'
        elif new_params != None:
            # Need to check whether 'new_params' (those added into pipe in tuple with function name)
            # are placed before or after the output params from the previous function
            # Get metadata from function to determine whether to add additional
            # params before or after existing params
            if func.static_params_pre():
                input = list(new_params) + list(param_list) 
            else:
                input = list(param_list) + list(new_params)
        else:
            input = list(param_list)
        
        print 'APPEND: Complete input to function <' + str(input) + '>\n'
        
        # Check if func is an instance of cffuncs.Function or a function
        # resulting from the pre-evaluation of another coordination forms expression
        if isinstance(func, Function):
            # if we reach this code, the cfunction provided to BYPASS is a
            # standard function that will be called via its metadata object.
            # The input may be coming from some
            # other coordination form that has not yet been evaluated.
            print 'APPEND: Function ' + func.get_code() + ' requires ' + str(len(func.parameters)) + ' params. '
            print 'APPEND: Function input contains: ' + str(len(input)) + ' params\n'
            
            # Count up the expected number of input parameters
            expected_input_count = 0
            for p in func.parameters:
                if p.get_dir() == 'input':
                    expected_input_count = expected_input_count + 1
            print 'Expecting at least <' + str(expected_input_count) + '> input params for function <' \
                + func.get_name() + '> which takes total of ' + str(len(func.parameters)) + ' params\n'
            if len(input) < expected_input_count:
                raise ValueError('Function ' + func.get_code + ' has ' + str(len(func.parameters)) + \
                    ' parameters and expects ' + str(expected_input_count) + ' input parameters but only ' \
                    + str(len(input)) + ' are available.')
            
            print 'About to run function <' + func.get_code() + '>...\n'
            output = func.run(input)
        elif isinstance(func, types.FunctionType):
            # If we reach this code, we assume that this APPEND contains
            # a pre-evaluated, nested, coordination forms expression
            # The input may be coming from some
            # other coordination form that has not yet been evaluated.
            print 'APPEND: About to run pre-evaluated function <' + func.__name__ + '>...\n'
            if type(output) != type(list()):
                if output != None:
                    output = [output]
            output = func(input)
        else:
            print('APPEND: The function provided is of an unknown type. Unable to evaluate this APPEND expression...')
            raise ValueError('APPEND: The function provided is of an unknown type. Unable to evaluate this APPEND expression...')

        
        if isinstance(func, Function):
            print 'APPEND: Handled function <' + str(func.get_code()) + '>. Combining input/output list.\n'
        elif isinstance(func, types.FunctionType):
            print 'APPEND: Handled function <' + func.__name__ + '>. Combining input/output list.\n'
        
        return_data = []
        
        if type(input) == type(output):
            if (type(input) == type([])) or (type(input) == type(tuple())):
                return_data = input + output
            else:
                return_data = [input] + [output]
        elif type(input) == type([]):
            if type(output) == type(tuple()):
                return_data = input + list(output)
            else:
                return_data = input + [output]
        elif type(input) == type(tuple()):
            if type(output) == type([]):
                return_data = input + tuple(output)
            else:
                return_data = input + (output, )
        else:
            return_data = [input] + [output]
        
        print 'Return data from APPEND: ' + str(return_data)
        
        return return_data

    return APPEND_implementation


# Process the provided list of parameters for replacement of tags.
def process_param_tags(param_list, task_id=-1):
    
    new_param_list = []
    for param in param_list:
        if type(param) == type(""):
            print 'PRE_PROCESS_PARAM_TAGS: Checking string param for task ID replacement.'
            if PAR_TASK_IDENTIFIER_STRING in param:
                print 'PRE_PROCESS_PARAM_TAGS: String PAR_ID replacement for: ' + str(param)
                param = param.replace(PAR_TASK_IDENTIFIER_STRING, str(task_id))
                print 'PRE_PROCESS_PARAM_TAGS: Param after replacement: ' + str(param)
            elif PAR_TASK_IDENTIFIER_INT in param:
                print 'PRE_PROCESS_PARAM_TAGS: Integer PAR_ID replacement for: ' + str(param)
                param = param.replace(PAR_TASK_IDENTIFIER_INT, str(task_id))
                param = int(param)
                print 'PRE_PROCESS_PARAM_TAGS: Param after replacement: ' + str(param)
        
        new_param_list.append(param)
    
    return new_param_list