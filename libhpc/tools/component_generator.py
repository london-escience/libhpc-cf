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
     
import os
from os.path import expanduser
import optparse
import logging
import xml.etree.ElementTree as ET

from python_code_generator import CodeGeneratorBackend

# Set up logging config
LOG = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                    datefmt='%m-%d %H:%M')

logging.getLogger(__name__).setLevel(logging.DEBUG)

class LibhpcComponentGenerator():
    
    component_group = ''
    component_file = ''
    component_list = []
    namespace = ''
    
    def __init__(self, input_file):
        self.component_file = input_file
    
    def generate_component_code(self):
        if len(self.component_list) < 1:
            LOG.debug('No component information available to generate code from. Call parse_component_xml() function on your XML first')
            return ''
        
        c = CodeGeneratorBackend()
        c.begin(tab='    ')
        c.write('# Generated libhpc component code. Auto-generated by libhpc component generator.\n#\n\n')
        c.write('from libhpc.cf.params import Parameter\n')
        c.write('from libhpc.cf.funcs import Component\n\n')
        c.write('# Component parameter definitions\n\n')
        component_params = {}
        for component in self.component_list:
            comp_name = component.component_id
            comp_params = component.parameters
            
            component_params[comp_name] = {}
            component_params[comp_name]['input'] = []
            component_params[comp_name]['output'] = []

            for param_id in range(len(comp_params)):
                param = comp_params[param_id]
                param_type = param.param_type
                comp_var = comp_name.replace('.','_') + '_' + param_type + '_' + str(param_id+1)
                component_params[comp_name][param_type].append(comp_var)
                c.write(comp_var + ' = Parameter(\'' + comp_var + '\', \'' + param.param_datatype + '\', \'' + param.param_direction + '\', ' + str(param.param_ignore) + ')\n')
        
        c.write('\n# Component definitions\n\n')

        #bwa_aln = Component('bwa.align', 'BWA Initial Alignment', 'libhpc.wrapper.bio.bwa.align', [bwa_aln_ref_genome, bwa_aln_short_read, bwa_aln_output_file], [bwa_aln_result])
        for component in self.component_list:
            comp_name = component.component_id
            
            c.write(comp_name.replace('.','_') + ' = Component(\'' + comp_name + '\', \'' + component.description + '\', \'' + component.wrapper_function + '\', [')
            for i in range(len(component_params[comp_name]['input'])):
                c.write(component_params[comp_name]['input'][i])
                if i+1 < len(component_params[comp_name]['input']):
                    c.write(', ')
            c.write('], [')
            for i in range(len(component_params[comp_name]['output'])):
                c.write(component_params[comp_name]['output'][i])
                if i+1 < len(component_params[comp_name]['output']):
                    c.write(', ')
            c.write('])\n')        
        LOG.debug('\n' + c.end())
        return '\n' + c.end()
        
    def generate_component_wrappers(self):
        if len(self.component_list) < 1:
            LOG.debug('No component information available to generate component wrappers. Call parse_component_xml() on your XML first')
            return ''
        
        wrapper_list = []
        for component in self.component_list:
            component_id_underscored = component.component_id.replace('.','_')
            executable_var = component_id_underscored + '_exec'
            wrapper_package = component.wrapper_function.split('.')
            LOG.debug('Wrapper package split: ' + str(wrapper_package))
            
            c = CodeGeneratorBackend()
            c.begin(tab='    ')
            c.write('# Generated libhpc component wrapper code. Auto-generated by libhpc component generator.\n#\n\n')
            c.write('from subprocess import call\n\n')
            c.write('# Executable, as specified in wrapper definition XML\n')
            c.write(executable_var + ' = ' + component.wrapper.executable + '\n\n')
            c.write('def set_' + executable_var + '(' + component_id_underscored  +'_location):\n')
            c.indent()
            c.write('global ' + executable_var + '\n')
            c.write(executable_var + ' = ' + component_id_underscored + '_location\n\n')
            c.dedent()
            c.write('def get_' + executable_var + '():\n')
            c.indent()
            c.write('global ' + executable_var + '\n')
            c.write('return ' + executable_var + '\n\n')
            c.dedent()
            
            #cparams = component.wrapper.executable_params
            
            c.write('def ' + wrapper_package[-1] + '(')
            param_separator = ''
            #reached_optional_params = False
            for param in component.parameters:
                # If this is an input parameter then we add it to the list of function params
                if param.param_type == 'input':
                    c.write(param_separator + param.param_id)
                    # If we have an optional parameter, add a default value
                    # However, we can't have an optional parameter before all 
                    # required params have been listed.
                    if param.param_optional:
                        pass
                    param_separator = ', '
            c.write('):\n')
            c.indent()
            c.write('print "Running ' + component.description + '\\n"\n')
            
            #status = call([bwa_exec, 'sampe', '-f', sam_output_file, ref_genome_file, short_read_alignment_indexes[0], short_read_alignment_indexes[1], short_read_files[0], short_read_files[1]])
            #print '\tBWA sampe...DONE...Status code: ' + str(status) + '\n\n'
            #return (status, sam_output_file)
            output_params = []
            call_code = ''
            for param in component.parameters:
                # Looking for the names of all output parameters, we put
                # them into a list so that if there's more than one we can
                # write them out as a tuple
                if param.param_type == 'output':
                    output_params.append(param.param_id)
            LOG.debug('output_params: ' + str(output_params))
            return_val = ''
            if len(output_params) == 1:
                return_val += output_params[0]
            elif len(output_params) > 1:
                return_val += '( '
                for i in range(len(output_params)):
                    return_val += output_params[i]
                    if i+1 < len(output_params):
                        return_val += ', '
                return_val += ' )'
                
            # Now write out the call command that runs the required tool
            call_code = return_val + ' = call([' + executable_var
            
            first_param = True
            for param in component.wrapper.executable_params:
                if len(param) >= 2:
                    if not first_param:
                        call_code += ', '
                    else:
                        first_param = False
                    if param[0] != None:
                        call_code += "'" + param[0] + "'"
                    if param[1] != None:
                        # If we wrote out a parameter for the previous
                        # element of the tuple then we need to add a comma-space
                        # at the end of the string 
                        if call_code [-2] != ',':
                            call_code += ', '
                        
                        if param[1].find('::') == -1:
                            call_code += "'" + param[1] + "'"
                        else:
                            if param[1].find('::') == param[1].rfind('::'):
                                call_code += param[1][param[1].find('::') +2:]
                            else:
                                call_code += param[1][param[1].find('::') +2 : param[1].rfind('::')] + '[' + param[1][param[1].rfind('::')+2:] + ']'
            
            c.write(call_code + '])\n')
            c.write('return ' + return_val + '\n\n')
            c.dedent()
            wrapper_list.append((component.component_id, component.wrapper_function, '\n' + c.end()))
            LOG.debug('\n' + c.end())            
        
        return wrapper_list
            
    def parse_component_xml(self):
        tree = ET.parse(self.component_file)
        root = tree.getroot()
        if 'componentGroup' in root.attrib:
            self.component_group = root.attrib['componentGroup']
        else:
            self.component_group = ''
        
        self.namespace = root.tag[root.tag.find('{'):root.tag.rfind('}')+1]
        LOG.debug("Root tag: " + root.tag + '\t\tNamespace: ' + self.namespace)
        
        comp_list = root.findall(self.namespace + 'component')
        
        for component in comp_list:
            component_id = component.find(self.namespace + 'id').text
            component_description = component.find(self.namespace + 'description').text
            component_wrapper_func = component.find(self.namespace + 'wrapperFunction').text
            params = component.find(self.namespace + 'parameters')
            curry_params_pos = params.find(self.namespace + 'curryParamsPosition').text
            component_param_list = []
            new_param_objects = self.parse_params_by_type(params, 'inputParam')
            LOG.debug('Received details of %d params of type inputParam...' % len(new_param_objects))
            component_param_list += new_param_objects
            
            new_param_objects = self.parse_params_by_type(params, 'outputParam')
            LOG.debug('Received details of %d params of type outputParam...' % len(new_param_objects))
            component_param_list += new_param_objects
            
            LOG.debug('We now have a total of %d parameters parsed...' % len(component_param_list))
            
            # Now we create the component object and add it to the component list
            c = _LibhpcComponent(component_id, component_description, component_wrapper_func, curry_params_pos, component_param_list) 
            
            # Now that the component has been created, add any wrapper info
            # to the component if wrapper config is provided
            wrapper = None
            wrapper_config = component.find(self.namespace + 'wrapper')
            if wrapper_config != None:
                wrapper_gen = wrapper_config.find(self.namespace + 'generateSimpleWrapper')
                if wrapper_gen != None:
                    # If we get to this point then some configuration has been
                    # provided to support generation of a wrapper function
                    wrapper_exec = wrapper_gen.find(self.namespace + 'executable').text
                    wrapper_exec_param_list = []
                    wrapper_exec_params = wrapper_gen.findall(self.namespace + 'executableParam')
                    for wparam in wrapper_exec_params:
                        wparam_tuple = (wparam.find(self.namespace + 'paramSwitch').text,wparam.find(self.namespace + 'paramValue').text) 
                        wrapper_exec_param_list.append(wparam_tuple)
                    wrapper = _LibhpcComponent._LibhpcComponentWrapper(wrapper_exec, wrapper_exec_param_list)
                                
            c.set_wrapper(wrapper)
            self.component_list.append(c)
    
    def parse_params_by_type(self, params_obj, param_type):
        param_list = []
        for param in params_obj.findall(self.namespace + param_type):
            p_type = 'input' if param_type == 'inputParam' else 'output'
            p_id = param.find(self.namespace + 'paramId').text
            p_datatype = param.find(self.namespace + 'paramType').text
            p_dir = param.find(self.namespace + 'paramDirection').text
            p_optional_search =  param.find(self.namespace + 'paramOptional')
            if p_optional_search == None:
                p_optional = False
            else:
                p_optional = True
            p_ignore_search =  param.find(self.namespace + 'ignoreParam') 
            if p_ignore_search == None:
                p_ignore = False
            else:
                p_ignore = True 
            param_obj = _LibhpcComponent._LibhpcComponentParameter(p_type, p_id, p_datatype, p_dir, p_optional, p_ignore)
            param_list.append(param_obj)
        return param_list
    
    def get_component_group(self):
        return self.component_group

class _LibhpcComponent():
    component_id = ''
    description = ''
    wrapper_function = ''
    parameters = []
    curry_params_position = ''
    wrapper = None
    
    class _LibhpcComponentParameter():
        param_type = ''
        param_id = ''
        param_datatype = ''
        param_direction = ''
        param_optional = False
        param_ignore = False
        
        def __init__(self, p_type, p_id, p_datatype, p_dir, p_optional=False, p_ignore=False):
            LOG.debug('Creating new component parameters: %s, %s, %s, %s, %s, %s' % (p_type, p_id, p_datatype, p_dir, p_optional, p_ignore))
            self.param_type = p_type
            self.param_id = p_id
            self.param_datatype = p_datatype
            self.param_direction = p_dir
            self.param_ignore = p_ignore
    
    class _LibhpcComponentWrapper():
        executable = ''
        executable_params = []
        
        def __init__(self, executable, executable_params):
            LOG.debug('Creating new component wrapper config: %s, %s' % (executable, executable_params))
            self.executable = executable
            self.executable_params = executable_params
    
    def __init__(self, comp_id, description, wrapper_function, curry_pos, parameters=None):
        self.component_id = comp_id
        self.description = description
        self.wrapper_function = wrapper_function
        self.curry_params_position = curry_pos
        if parameters is not None:
            self.parameters = parameters
    
    def add_param(self, parameter):
        self.parameters.append(parameter)
        
    def set_wrapper(self, wrapper):
        self.wrapper = wrapper
    
    def print_info(self):
        print '\nComponent: ' + self.component_id
        print '\tDescription: ' + self.description
        print '\tWrapper Function: ' + self.wrapper_function
        for parameter in self.parameters:
            print '\tParameter: ' + parameter.param_id
            print '\t\tParameter type: ' + parameter.param_type
            print '\t\tParameter data type: ' + parameter.param_datatype
            print '\t\tParameter direction: ' + parameter.param_direction
            print '\t\tIgnore parameter?: ' + str(parameter.param_ignore)
        

def check_append_to_file():
    return False

if __name__ == '__main__':
    # Setup the accepted command line options and parse 
    # the incoming parameter list
    clparser = optparse.OptionParser(usage='usage: %prog [options] <XML component definition file>')
    clparser.add_option("-o", "--output-directory", action="store", type="string", default="~/.libhpc", dest="output_dir", 
                        help="The directory to place the generated python files into")
    clparser.add_option("-s", "--output-stdout", action="store_true", dest="std_out", 
                        help="Dump generated python code to stdout rather than saving to a file")

    # Get the params from the command line parser
    (options, args) = clparser.parse_args()
    
    output_dir = options.output_dir
    
    # args should contain the name of the XML file we want to use as input
    if len(args) != 1:
        clparser.print_help()
        exit()
    else:
        input_file = args[0]
    
    if not os.path.exists(input_file):
        LOG.debug("Couldn't find the specified input file <%s>" % input_file)
        print 'The specified input file [' + input_file + '] could not be found...'
        exit()
    
    # We've now parsed the input options and checked for existence of the input file
    # Now check if the ~/.libhpc directory exists, if not, create it and
    # the components subdirectory
    if output_dir == '~/.libhpc':
        user_home = expanduser('~')
        libhpc_dir = os.path.join(user_home, '.libhpc')
    elif output_dir.startswith('~'):
        user_home = expanduser(output_dir[0:output_dir.find(os.sep)])
        libhpc_dir = os.path.join(user_home, output_dir[output_dir.find(os.sep)+1:])
    else:
        libhpc_dir = output_dir
    libhpc_component_dir = os.path.join(libhpc_dir, 'component')
    libhpc_wrapper_dir = os.path.join(libhpc_dir, 'wrapper')
    if not os.path.exists(libhpc_dir):
        LOG.debug('.libhpc directory does not exist in your home directory. Creating .libhpc...')
        os.mkdir(libhpc_dir)
    
    if not os.path.exists(libhpc_component_dir):
        LOG.debug('Creating .libhpc/components...')
        os.mkdir(libhpc_component_dir)
    
    # We can now create an instance of the component generator
    gen = LibhpcComponentGenerator(input_file)
    gen.parse_component_xml()
    LOG.debug("Component info:\n\n")
    for comp in gen.component_list:
        comp.print_info()
        
    component_group = gen.get_component_group()
    LOG.debug("Component group: " + component_group)
           
    component_code = gen.generate_component_code()
    component_group_path = component_group.replace('.', os.sep)
    component_group_dir = os.path.join(libhpc_component_dir, component_group_path)
    if not os.path.exists(component_group_dir):
        os.makedirs(component_group_dir)
        # Now we create an __init__.py file in each created directory to
        # mark out these directories as Python packages
        component_group_list = component_group.split('.')
        for i in range(len(component_group_list)):
            init_file = os.path.join(libhpc_component_dir, os.sep.join(component_group_list[0:i+1]), '__init__.py')
            LOG.debug('Checking for init.py in: ' + init_file)            
            if not os.path.exists(init_file):
                open(init_file, 'a').close()
        
    write_mode = 'w'
    if os.path.exists(os.path.join(component_group_dir, component_group + '.py')):
        if not check_append_to_file():
            LOG.debug('Not overwriting existing file...')
            write_mode = ''
        else:
            write_mode = 'a+'
    if write_mode != '':
        with open(os.path.join(component_group_dir, component_group + '.py'), write_mode) as f:
            f.write(component_code)
        
    wrapper_list = gen.generate_component_wrappers()
    for wrapper in wrapper_list:
        wrapper_function = wrapper[1]
        wrapper_function_elements = wrapper_function.split('.')
        if len(wrapper_function_elements) == 1:
            wrapper_file = wrapper_function_elements[0] + '.py'
        else:
            wrapper_file = wrapper_function_elements[-2] + '.py'
        wrapper_dir = ''
        if len(wrapper_function_elements) > 2:
            wrapper_dir = os.sep.join(wrapper_function_elements[:-2])    
        write_mode = 'w'
        if not os.path.exists(os.path.join(libhpc_wrapper_dir, wrapper_dir)):
            os.makedirs(os.path.join(libhpc_wrapper_dir, wrapper_dir))
            
            # Now we create an __init__.py file in each created directory to
            # mark out these directories as Python packages
            wrapper_dir_list = wrapper_dir.split(os.sep)
            for i in range(len(wrapper_dir_list)):
                init_file = os.path.join(libhpc_wrapper_dir, os.sep.join(wrapper_dir_list[0:i+1]), '__init__.py')
                LOG.debug('Checking for init.py in: ' + init_file)            
                if not os.path.exists(init_file):
                    open(init_file, 'a').close()
            
        if os.path.exists(os.path.join(os.path.join(libhpc_wrapper_dir, wrapper_dir, wrapper_file))):
            write_mode = 'a+'
        if write_mode != '':
            with open(os.path.join(libhpc_wrapper_dir, wrapper_dir, wrapper_file), write_mode) as f:
                f.write(wrapper[2])
    LOG.debug('WRAPPER LIST:\n\n' + str(wrapper_list))
    