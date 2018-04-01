# Syntaxnet Parsey McParseface Python Wrapper for DependencyParsing
**Note:** This syntaxnet build contains [The Great Models Move](https://github.com/tensorflow/models/pull/2430) change. 

## 1. Introduction

When Google declared that [The World’s Most Accurate Parser i.e., SyntaxNet goes open-source](https://research.googleblog.com/2016/05/announcing-syntaxnet-worlds-most.html), it grabbed widespread attention from machine-learning developers and researchers who were interested in core applications of NLU like automatic extraction of information, translation etc. Following gif shows how syntaxnet internally builds the dependency tree:

<img src="https://github.com/tensorflow/models/blob/master/research/syntaxnet/g3doc/images/looping-parser.gif" width="500" height="300"/>

## 2. Troubles of the world's best parser SyntaxNet
Predominantly one will find two approaches to use SyntaxNet:
1. Using [demo.sh](https://github.com/tensorflow/models/blob/master/research/syntaxnet/syntaxnet/demo.sh) script provided by syntaxnet
2. Invoke the same from python as a subprocess as shown below. This approach is obviously inefficient, non-scalable and over-kill as it internally calls two other python scripts (parser_eval and conll2tree).
```markdown
import subprocess
import os
os.chdir(r"../models/syntaxnet")
subprocess.call([    
"echo 'Bob brought the pizza to Alice.' | syntaxnet/demo.sh"
], shell = True)
```
```diff
+ I wanted a proper scalable python application where one can do `import syntaxnet` and use it as shown below:
+ import syntaxnet
+ from syntaxnet import gen_parser_ops...
+ I could manage to get this done and hence sharing my project here. Please find below as to how I got this!!
```

#### 2.1 Pain Part - Syntaxnet is a RESEARCH MODEL:
<hr/>

- After [The Great Models Move](https://github.com/tensorflow/models/pull/2430), Tensorflow categorized SyntaxNet as RESEARCH MODEL.
- As mentioned [here](https://github.com/tensorflow/models/pull/2430), Tensorflow team will no more provide  guaranteed support to SyntaxNet and they encouraged **Individual researchers to support** research models.

#### 2.2 Salt on the wound:
<hr/>

Apart from having `high struggles in installation and huge learning curve, no official support and lack of clear documentation` led forums talking about myraid of issues on SyntaxNet without proper solutions. Some of them were as basic as:
- A lot of trouble understanding documentation around both syntaxnet and related tools
- How to use Parsey McParseface model in python application
- Confusing I/O handling in SyntaxNet because of the uncommon .conll file format it uses for input and output.
- How to use/export the output (ascii tree or conll ) in a format that is easy to parse

## 3. What this project does?
This endevour addresses to make the life of SyntaxNet enthusiasts easier. It primarily saves all those hours to get `Google's SyntaxNet Parsey McParseface` up and running in a way it should be. For this, am providing two things as part of this project:
1. **One line (~5mins) SyntaxNet 0.2 installation**
2. **Syntaxnet Parsey McParseface wrapper for POS tagging and dependency parsing**

<br/>

## 3.1 One line (~5mins) SyntaxNet 0.2 installation
Iam sharing the osx syntaxnet package distribution `i.e., syntaxnet-0.2-cp27-cp27m-macosx_10_6_intel.whl file` in this git repo that I've got successfully built using `bazel` build tool with all tests passing after pulling the latest code from [syntaxnet git repository](https://github.com/tensorflow/models). This will setup `syntaxnet 0.2 version` with a simple command in barely 5 minutes as shown below:
```markdown
git clone https://github.com/spoddutur/syntaxnet.git
cd <CLONED_SYNTAXNET_PROJ_DIR>
sudo pip install syntaxnet-0.2-cp27-cp27m-macosx_10_6_intel.whl
```
Isn't 
##### Tech Stack:
<img src="https://user-images.githubusercontent.com/22542670/38137700-d6bb2276-3443-11e8-8aa2-6f883d978fed.png" width="600" height="100"/>

## 3.2 Syntaxnet Parsey McParseface wrapper for POS tagging and Dependency parsing 
##### Here comes the most interesting (a.k.a challenging) part i.e., How to use syntaxnet in a python application. It should no more be of any trouble after this point :)

`my_parser_eval.py` is the file that contains the python-wrapper which I implemented to wrap SyntaxNet. The list of API's exposed in this wrapper are listed below:
```markdown
1. Api to initialise parser: 
`tagger = my_parser_eval.SyntaxNetProcess("brain_tagger")`
("brain_tagger" will initialise pos tagger. change it to "brain_parser" for dependency parsing)

2. Api to input data to parser: 
`my_parser_eval._write_input("<YOUR_ENGLISH_SENTENCE_INPUT>")`

3. Api to invoke parser: 
`tagger.eval()`

3. Api to read parser's output in conll format:
`my_parser_eval._read_output()`

4. Api to pretty print parser's output as tree: 
`my_parser_eval.pretty_print()`
```
## 4. Demo
- I wrote `main.py` (a sample python code) to demo this wrapper. It performs `syntaxnet's dependency parsing`. 
- **Input to main.py:** English sentence text
- **Output from main.py:** Dependency graph tree

## 5. How to run the parser:
```markdown
1. git clone https://github.com/spoddutur/syntaxnet.git
2. cd <syntaxnet-git-clone-directory>
3. python main.py 
4. That's it!!  It prints syntaxnet dependency parser output for given input english sentence
```

#### 5.1 Sample output for “Bob brought the pizza to Alice” input
<img src="https://user-images.githubusercontent.com/22542670/38134694-d492419e-3431-11e8-87a3-dcd6d0d36ebb.png" width="300"/>

## 6. Project Structure:
- **/models:** Originally cloned from syntaxnet git repository https://github.com/tensorflow/models . But this folder will additionally contain the bazel build “bazel-bin" folder with the needed runfiles.
- **custom_context.pbtxt:** Custom context file used in setting context for parser.
- **my_parser_eval.py:** python wrapper for “brain-tagger” POS tagger and “brain-parser” dependency parser. This file is heavily inspired from the [original parser_eval.py that syntaxnet provides](https://github.com/tensorflow/models/blob/master/syntaxnet/syntaxnet/parser_eval.py) with quiet some modifications aand enhancements.
- **main.py:** Demo sample usage
- **/data:** folder where parser’s intermediate input’s and output’s are dumped.
- **.whl:** osx package distribution of the final successful syntaxnet built using which you can setup `syntaxnet 0.2 version` in barely 5 minutes 
