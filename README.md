# Syntaxnet Parsey McParseface Python Wrapper
**Note:** This syntaxnet built contains [The Great Models Move](https://github.com/tensorflow/models/pull/2430) change. 

## 1. What does this project do?
This project primarily saves you all the hours of dealing with installation and setup needed to use `Google's SyntaxNet Parsey McParseface` from inside your python code. It achieves this by providing two things:
1. **One line (~5mins) SyntaxNet 0.2 installation**
2. **Syntaxnet Parsey McParseface wrapper**

<br/>

## 1.1 One line (~5mins) SyntaxNet 0.2 installation
Iam sharing the osx package distribution `i.e., .whl file` that I've got successfully built using `bazel` build tool with all tests passing after pulling the latest code from [syntaxnet git repository](https://github.com/tensorflow/models). This will setup `syntaxnet 0.2 version` in barely 5 minutes as shown below:
```markdown
sudo pip install syntaxnet-0.2-cp27-cp27m-macosx_10_6_intel.whl
```
##### Tech Stack:
<img src="https://user-images.githubusercontent.com/22542670/38137700-d6bb2276-3443-11e8-8aa2-6f883d978fed.png" width="600" height="100"/>

## 1.2 Syntaxnet Parsey McParseface wrapper 
`my_parser_eval.py` is the file that contains python-wrapper which I implemented. It wraps following two parsers for demo: 
1. **brain-tagger** POS tagger and 
2. **brain-parser** dependency parser. 

It can be easily made generic and extended further to add more parsers like **brain-morpher** etc as needed. The list of API's exposed in this wrapper are listed below:
```markdown
1. Api to initialise parser: 
`tagger = my_parser_eval.SyntaxNetProcess("brain_tagger")`

2. Api to input data to parser: 
`my_parser_eval._write_input("<YOUR_ENGLISH_SENTENCE_INPUT>")`

3. Api to invoke parser: 
`tagger.eval()`

3. Api to read parser's output in conll format:
`my_parser_eval._read_output()`

4. Api to pretty print parser's output as tree: 
`my_parser_eval.pretty_print()`
```
## 2. Demo
- I wrote `main.py` (a sample python code) to demo this wrapper. It performs `syntaxnet's dependency parsing`. 
- **Input to main.py:** English sentence text
- **Output from main.py:** Dependency graph tree


Following gif shows how syntaxnet internally builds the dependency tree:

<img src="https://github.com/tensorflow/models/blob/master/research/syntaxnet/g3doc/images/looping-parser.gif" width="500" height="300"/>

## 3. How to run the parser:
```markdown
1. git clone https://github.com/spoddutur/syntaxnet.git
2. cd <syntaxnet-git-clone-directory>
3. python main.py 
4. That's it!!  It prints syntaxnet dependency parser output for given input english sentence
```

#### 3.1 Sample output for “Bob brought the pizza to Alice” input
<img src="https://user-images.githubusercontent.com/22542670/38134694-d492419e-3431-11e8-87a3-dcd6d0d36ebb.png" width="300"/>

## 4. Project Structure:
- **/models:** Originally cloned from syntaxnet git repository https://github.com/tensorflow/models . But this folder will additionally contain the bazel build “bazel-bin" folder with the needed runfiles.
- **custom_context.pbtxt:** Custom context file used in setting task context. Heavily inspired from here. https://github.com/plowman/python-mcparseface/blob/master/custom_context.pbtxt 
- **my_parser_eval.py:** python wrapper for “brain-tagger” POS tagger and “brain-parser” dependency parser. This file is tweak of the original parser_eval.py that synthxnet provides.  https://github.com/tensorflow/models/blob/master/syntaxnet/syntaxnet/parser_eval.py. with quiet some modifications like ability to call wrapper several times without needing to load model eveytime etc.
- **main.py:** Demo sample usage
- **/data:** folder where parser’s intermediate input’s and output’s are dumped.
- **.whl:** osx package distribution of the final successful syntaxnet built using which you can setup `syntaxnet 0.2 version` in barely 5 minutes 
