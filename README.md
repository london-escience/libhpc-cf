# PyCompForms: The Libhpc Coordination Forms Library

This project provides a Python library for creating software components and coordination forms for use either standalone or alongside tools and services from the libhpc framework.

Coordination Forms are functional-style operators that can be used to orchestrate software components. They provide an abstract approach to specifying pipelines of components and can be used to specify advanced component orchestration that can be difficult and messy to define in standard workflow environments. Coordination Forms were originally defined in a 1995 paper by Darlington et al. ([http://dl.acm.org/citation.cfm?id=699075](http://dl.acm.org/citation.cfm?id=699075)).

This library provides the ability to define software components, along with Python wrappers for a component's implementation. A component may be abstract - that is, it does not directly contain any implementation. Multiple underlying implementations may be provided and the libhpc framework, or third-party code making use of this library, may select the required implementation for a component at runtime. Coordination forms may also have multiple implementations, as explained below, and by combining this library with an automated mapper, it is possible for developers or users to write abstract task specifications for which a suitable implementation can be selected based on the hardware available and user requirements at runtime. 



### Software Components

Software components defined using this library consist of a set of metadata defining a component's inputs and outputs and, potentially, one or more component implementations. A component *can* be defined without any implementation but this relies on other developers to provide an implementation before the component can be used.

A component is based on a `libhpc.cf.component.Component` object. If the component implementation is written in another language and must be called via the command line or some other external tooling, a Python wrapper must also be provided to support the component's implementation. This library includes support for auto-generation of Python wrappers for command-line tools.

### Coordination Forms

Coordination forms are functional-style operators that are applied to components to define orchestration of control and data flow between them. Coordination forms may be general or domain-specific and while a small set of general forms are provided with this library, it is intended that developers will add new forms suited to their specific domains where required. 

As with components, coordination forms are abstract and may have multiple implementations. For example, consider a form that is designed to undertake a set of independent tasks. We call this form `PAR`. `PAR` is provided with a list of *n* components and list of inputs of length *n*, one per component. Consider a simple example:

```
result = PAR( [add, add, sub], 
              [ (10, 5), (234, 221), (64, 31) ])
```

We would expect this to provide the result `[ 15, 455, 33 ]`. However, while we know from its functional nature what the `PAR` form is intended to do and the result that we expect, `PAR` provides an abstract representation of this process and we have no information about how the process is actually undertaken. Consider three possible implementations of the `PAR` coordination form:

* **Sequential:** The components are executed sequentially.
* **Multi-threaded:** Each component is executed in a separate thread.
* **IaaS cloud:** Each component is executed on a separate Infrastructure-as-a-Service cloud node.

In the current release of this library, base implementations of each coordination form are provided. The ability to plug in different implementations of forms is undergoing testing and will be made available soon.

## Library Functionality and API

The library provides the following key features:

* Define abstract components and Python wrappers for native tools
* A set of coordination form implementations that can be applied to components to build application definitions or pipelines
* A tool for building Python component definitions from an XML description
* A set of sample Bioinformatics components and associated wrappers

We first provide an overview of the API.

### Packages and Modules

The following Python packages are provided in this library:

* `	libhpc.cf` - coordination form and component API
* `libhpc.component` - abstract component definitions
* `libhpc.tools` - the component generator tool for converting XML component definitions into code
* `libhpc.wrapper` - Python wrappers for command-line-based component implementations

Within these packages, the key modules are:

* `	libhpc.cf.component` - contains the `Component` class for defining abstract components
* `	libhpc.cf.params` - contains the `Parameter` class for defining component input/output parameters (component ports)
* `	libhpc.cf.forms` - contains coordination form implementations
* `	libhpc.component.bio` - contains definitions for a set of Bioinformatics components
* `	libhpc.wrapper.*` - a set of modules providing Python wrapper implementations for the Bioinformatics components
* `libhpc.tools.component_generator` - contains a python tool that can be run from the command line to generate Python component definitions from an XML component specification

### Specifying a component

A component object may be defined programmatically or from an XML description using the component generator tool provided with this project. Here we look at the programmatic approach, the use of XML is described later in this documentation.

A component is specified by creating an instance of the `libhpc.cf.component.Component` class. Components include a set of input/output parameters. Each of these is defined using an instance of the `libhpc.cf.params.Parameter` class.

```
Component(id, name, function_entry_point, 
          input_params, return_params, 
          static_pos = 'post')
```
`id` - A unique string identifier for this component; a package style structure is recommended for this parameter.

`name` - A string naming this component, does not need to be unique.

`function_entry_point` - A string specifying a fully qualified Python function that is the entry point for the default implementation of this component. Empty string should be provided if no default implementation is available.

`input_params` - A list of zero or more `Parameter` objects defining the input parameters for this component.

`return_params` - A list of zero or more `Parameter` objects defining the output parameters for this component.

`static_pos` - A string, either `'pre'` or `'post'` defining whether "curried" or statically injected parameters should be placed at the start or end of the input parameter list. The default value for this parameter is `'post'`. The use of curried parameters is explained further in the coordination forms documentation below.

The `input_params` and `return_params` parameters take instances of the `libhpc.cf.params.Parameter` class:

```
Parameter(id, type, dir='input', 
          ignore=None, index=None, 
          value=None)
```

`id` - A unique string identifier for this parameter, a package-style structure is recommended.

`type` - A string defining the type of this parameter, one of `'string'`, `'int'`, `'float'`, `'list'`.

`dir` - A string defining the direction of this parameter, one of `'input'`, `'output'`, `'inout'`.

`ignore` - An optional Boolean value determining whether this parameter should be ignored. There are circumstances where the parameter may not be required in an output list and setting ignore to `True` ensures that it is not represented in the associated component's output.

`index` - An optional integer value which, if provided, gives a hint to the processing framework about where in the list of inputs/outputs this parameter should be placed.

`value` - An optional default value for this parameter.

#### Example

This example shows how we can define a Bioinformatics component to run the Burrows-Wheeler aligner command line tool for mapping gene sequences against a reference genome. This example will demonstrate the specification of a component for the *aln* sub-command of bwa. For now, we assume that there is a Python wrapper function named `align` available in the module `libhpc.wrapper.bio.bwa`.

Our component will take three input parameters: the reference genome file name, the short read input file name and the name of the output file. It will return the integer result code of running the command line bwa aln process. We begin by defining instances of the `Parameter` class to define these parameters and then we define the component.

```
bwa_aln_ref_genome = Parameter('bio.bwa.aln.ref_genome_param', 'string', 'input', False)
bwa_aln_short_read = Parameter('bio.bwa.aln.short_read_file', 'string', 'input', False)
bwa_aln_output_file = Parameter('bio.bwa.aln.output_file', 'string', 'inout', False)
bwa_aln_result = Parameter('bio.bwa.aln.bwa_aln_status', 'int', 'output', True)

bwa_aln = Component('bio.bwa.align', 'BWA Initial Alignment',
                    'libhpc.wrapper.bio.bwa.align', 
                    [bwa_aln_ref_genome, bwa_aln_short_read,
                     bwa_aln_output_file], 
                    [bwa_aln_result])

```

The above code gives us a component object `bwa_aln` with a default implementation that can be executed directly by calling its `run(parameter_list)` function or using within coordination forms expressions. Note that the `bwa_aln_output_file` parameter has a direction of `'inout'`. This is because this parameter may be generated internally within the component and populated when the component has completed if no value was provided as input but it may also be used as an input parameter with a specific output filename specified when the component is run.

### Available coordination forms 

A group of coordination forms, each with a default implementation, is provided in the `libhpc.cf.forms` module:

* `PAR` - Run a series of independent components.
* `PIPE` - Run a pipeline of components, the output from one is passed as input to the next component in the pipeline.
* `BYPASS` - Ignore the output of the target component or coordination forms expression, pass through the original input as the output.
* `SPLIT`- Takes a single list as input and splits this into two equal parts which are provided as the output.
* `FILTER` - Given an output list from a component or coordination forms expression and a list of integer indices, this form outputs only the elements in the original input list specified by the indicies in the integer list.
* `APPEND` - Takes a component or coordination forms expression and outputs the result of this input appended to the original input parameters.

### Coordination Forms API

The coordination forms functions described below can be found within the `libhpc.cf.forms` module. We use the simple demonstration components `add`, `sub`, `mult` and `div` to provide examples of using the coordination forms.

###### Note: Running coordination form expressions

Note that each of the coordination form functions shown here returns a function. To run the coordination form immediately we add `()` to the end of the definition. We'll demonstrate later in this documentation how the returning of a function from a coordination form function call is used in more complex coordination form expressions.

###### Note: Coordination forms and components are interchangable as inputs

Also note that components and coordination forms are interchangable as inputs so a component list may also contain more complex coordination form expressions in place of individual components. 

###### Currying values

Currying is used when the execution of a component returns a partially evaluated function that requires additional input to be executed. Consider a pipeline of two add components, each of which take two inputs. The first component will return a single value, the sum of its two inputs. In the case of a `PIPE`, it will attempt to pass this single value as input to the next function in the `PIPE`, however, this function requires two inputs. We curry the second input as a static value in the `component_list` that is provided as input to the `PIPE`. When currying values, the element in the `component_list` is specified as a tuple with the component as the first element in the tuple and one or more curried inputs specified as additional values in the tuple, e.g.

`PIPE( [add, (add, 23)], [(12, 45)])() = 80`

#### PAR

`PAR` runs a set of independent tasks (represented using components). Different implementations of `PAR` may be provided to use different approaches to execute the tasks depending on the available hardware capabilities. The result of `PAR` is that all the specified components will have been run and their results provided in a list ordered the same as the original input component list.

```python
par_function = PAR( component_list, input_list )
result_list = par_function()
```

`PAR` runs the list of components in `component_list` passing the item at position *p* in the `input_list` as input to the component at position *p* in the `component_list`. Both `component_list` and `input_list` *must* be the same length. The output provided in `result_list` is a list of results of the same length as `component_list` and `input_list`. Depending on the output of the corresponding component, an item in `result_list` may be a single value, a list or a tuple.

###### Example

```python
result_list = PAR( [add, sub, add, mult], 
                   [(23, 45), (12, 4), (365, 23, 221), (87, 23)])()
                   
result_list:  [68, 8, 121, 2001]
```

#### PIPE

`PIPE` runs a series of components in order, passing the initial input to the `PIPE` to the first component and then passing the output of each component to the next in the `PIPE` until the final component has run and its output is provided as the output of the `PIPE` expression.

```python
pipe_function = PIPE( component_list, initial_input )
result = pipe_function()
```

`component_list` is the list of components to be run, in order from left to right. The left-hand component in the list (at position 0) will be run first and passed the `initial_input` as its input. When the `PIPE` is run, the output of the component in position 0 of the `component_list` will be passed as input to the component in position 1 and so on until the output from the final component is returned as the output from the `PIPE`.

###### Example
```python
result = PIPE([add, (sub, 32), (add, 34, 22), (mult, 46)], 
              [122, 233])()

result: 17434
```

#### BYPASS

`BYPASS` runs the specified component or coordination form expression but ignores the results, passing the original input as its output. 

This is particularly useful for non-functional components that have external side-effects. Such situations can often not be avoided when using existing third-party tools. For example, consider a tool that generates an output file that is named based on a hardcoded convention and written directly to disk. This cannot be easily returned directly by the component being run because it may not be aware of the name of the output file but the file may be automatically picked up by a subsequent component running a compatible tool that is aware of the naming convention.

```python
bypass_function = BYPASS( component, input )
result = bypass_function()

input == result: True
```

###### Example
In this example, we consider a pipe of three components. The first generates some data to process, the second generates an index file for this data on disk while the third component reads the generated data as input and looks for its index file on disk. We apply `BYPASS` to the second component because the third component requires the generated data from the first component as its input but it cannot run until the index file is available on disk.

```python
result = PIPE( [ data_generator, BYPASS(indexer), data_processor ],
               ('/tmp/data_gen_spec.txt', )()
             )

```

#### SPLIT

`SPLIT` takes an input list or tuple and splits it into two equal parts. The output will be a list containing two lists if the original input was a list or two tuples if the original input was a tuple. This is useful if breaking up data to be passed to multiple components. If the input consists of an odd number of items, the first output list/tuple will contain one more item than the second.

###### Example
```python
result = SPLIT([ (12, 34), 23, 322, ('testa', 'testb'), 12 ])()

result: [ [(12, 34), 23, 322], [('testa', 'testb'), 12] ]

```

#### FILTER

`FILTER` takes a list of integers and list of input parameters. The output of `FILTER` consists only of the items at the indices specified in integer list. The item list is 0-indexed. In the case where integers in the first list are greater than the number of items in the input list, these erroneous values are ignored.

###### Example
```python
result = FILTER( [ 2, 3, 5 ], [23, 45, (12, 332), (34, 8), 98, 2] )()

result: [ (12, 332), (34, 8), 2 ]
```

#### APPEND

`APPEND` runs the target component(s) or coordination forms expression and appends the output from this to the original input.

###### Example
```python
result = PIPE( [ APPEND((add, 23)), add ], [ (12, 43) ])()

result: [ 55, 78 ]

```

## Specifying components in XML

Components can also be specified using XML from which the Python component definition can be generated. Where a Python wrapper is required to run a command line tool, this can also be defined in XML and auto-generated.

An example of specifying a component using XML is provided in `doc/xml/sample_component_spec.xml`.

Multiple components can be specified in a single XML file. All XML component specifications must start with the `<components>` root tag. This tag has a `componentGroup` attribute that is used to logically group components and their generated files in separate directories. A component definition file should begin as follows:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<components xmlns="http://www.imperial.ac.uk/lesc/projects/libhpc/component" 
            componentGroup="{ group_name }">
```
where `{ group_name }` should be replaced with your chosen group name.

The `components` tag can contain one or component `component` tags defining components. Each component follows this structure:

```xml
<component>
    <id>{ component unique ID }</id>
    <description>{ component description }</description>
    <wrapperFunction>{ fully qualified class/function name }</wrapperFunction>
    <parameters>
        <inputParam>
            ...
        </inputParam>
        ...
        <outputParam>
            ...
        </outputParam>
        <curryParamsPosition>{ pre | post }</curryParamsPosition>
    </parameters>
    <wrapper>
        ...
    </wrapper>
</component>
```

###### Input / Output Parameters

The parameters tag can contain 0 or more `<inputParam>` tags and 0 or 1 `<outputParam>` tags. These are defined as follows:

```xml
<inputParam>
    <!-- A unique ID for this parameter -->
    <paramId> </paramId>
    <!-- The type of this parameter - int, float, string, list -->
    <paramType> </paramType>
    <!-- The direction of this parameter - input, output, inout -->
    <paramDirection> </paramDirection>
    <!-- Identifies this as an optional parameter -->
    <paramOptional />
    <!-- Identifies this as a parameter that should be ignored -->
    <ignoreParam />
</inputParam>
```

The structure for `<outputParam>` is the same is `<inputParam>` except that the direction must be output.

The `<wrapper>` tag allows the specification of parameters that can be used to generate a Python wrapper around a command line tool. At present, only tools that are configured using command line switches/parameters are supported. We call this a SimpleWrapper and it is specified using the `<generateSimpleWrapper>` tag. This tag contains an `<executable>` tag defining the executable to be run, followed by 0 or more `<executableParam>` tags and finally an optional `<executableResult>` tag. `<executableParam>` tags contain a `<paramSwitch>` tag and a `<paramValue>` tag. Both are required but `<paramSwitch>` may be empty if a value is provided on the command line without an associated switch. An example of a simple component wrapper definition is shown below:

```xml
<wrapper>
    <generateSimpleWrapper>
        <executable>/usr/local/bwa/bin/bwa_exec</executable>
        <executableParam>
            <paramSwitch></paramSwitch>
            <paramValue>sampe</paramValue>
        </executableParam>
        <executableParam>
            <paramSwitch>-f</paramSwitch>
            <paramValue>output.sam</paramValue>
        </executableParam>
        ...
        <executableResult>
            <paramValue>0</paramValue>
        </executableResult>
    </generateSimpleWrapper>
</wrapper>
```

Since providing static values for the parameters is very limited and impractical in most cases, `<paramValue>` may reference input and output parameters in the main component parameters definition. Parameters are referenced by prefixing their ID in the main parameter definition with `inputParam::` for input parameters and `outputParam::` for output parameters. If a parameter is a list, individual list items can be referenced by appending `::<list_index>` onto the `paramValue` identifier. Consider the following component parameter definitions:

```xml
<component>
    <id>...</id>
    <description>...</description>
    <wrapperFunction>...</wrapperFunction>
    <parameters>
        <!-- Input params -->
        <inputParam>
            <paramId>ref_genome_param</paramId>
            <paramType>string</paramType>
            <paramDirection>input</paramDirection>
        </inputParam>
        <inputParam>
            <paramId>short_read_indexes_param</paramId>
            <paramType>list</paramType>
            <paramDirection>input</paramDirection>
        </inputParam>
        <!-- Output params -->
        <outputParam>
            <paramId>bwa_sampe_status</paramId>
            <paramType>int</paramType>
            <paramDirection>output</paramDirection>
            <ignoreParam/>
        </outputParam>
    </parameters>
    ...
</component>
```

The above parameters could be referenced in a wrapper's `executableParam` blocks as follows:

```xml
<executableParam>
    <paramSwitch></paramSwitch>
    <paramValue>inputParam::ref_genome_param</paramValue>
</executableParam>
<executableParam>
    <paramSwitch></paramSwitch>
    <paramValue>inputParam::short_read_indexes_param::0</paramValue>
</executableParam>
<executableResult>
    <paramValue>outputParam::bwa_sampe_status</paramValue>
</executableResult>
```
Note in the above example how item 0 of the `short_read_indexes_param` list is referenced.        

## Examples

Some examples of using coordination forms to specify and run bioinformatics pipelines will be added here.

## License & Information
This code is licensed under the BSD 3-clause license. See the `LICENSE` file for more information.

This library has been developed at Imperial College London by Jeremy Cohen as part of the Engineering and Physical Sciences Research Council (EPSRC)-funded libhpc (EP/I030239/1) and libhpc II (EP/K038788/1) projects. 