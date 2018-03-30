# Syntaxnet Parsey McParseface Python Wrapper for DependencyParsing
**Note:** This syntaxnet built contains [The Great Models Move](https://github.com/tensorflow/models/pull/2430) change. 

### Introduction - Troubles of the world's best parser SyntaxNet

When Google made [The World’s Most Accurate Parser i.e., SyntaxNet open-source](https://research.googleblog.com/2016/05/announcing-syntaxnet-worlds-most.html), it grabbed widespread attention from machine-learning developers and researchers who were interested in core applications of NLU like automatic extraction of information, translation etc 

#### Pain Part - Syntaxnet is a RESEARCH MODEL:
<hr/>


- After The Great Models Move, Tensorflow categorized SyntaxNet as RESEARCH MODEL.
- As mentioned [here](https://github.com/tensorflow/models/pull/2430), Tensorflow team will no more provide  guaranteed support to SyntaxNet and they encouraged **Individual researchers to support** research models.
- The worser pain part of this restructure is that, it came with broken links within the repository which added to the woes of its installation. 

#### Salt on the wound:
<hr/>


Apart from having `high struggles in installation and huge learning curve, No official support and lack of clear documentation` led forums talking about myraid of issues on SyntaxNet without proper solutions. Some of them were as basic as:
- A lot of trouble understanding documentation around both syntaxnet and related tools
- How to use Parsey McParseface model in python application
- Confusing I/O handling in SyntaxNet because of default .conll format
- How to use/export the output (ascii tree or conll ) in a format that is easy to parse

## 1. What does this project do
This endevour addresses to make the life of SyntaxNet enthusiasts easier. It primarily saves all those hours to get `Google's SyntaxNet Parsey McParseface` up and running in a way it should be. For this, am providing two things as part of this project:
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
##### Here comes the most interesting (a.k.a challenging) part i.e., How to use syntaxnet in a python application. It should no more be of any trouble after this point :)

`my_parser_eval.py` is the file that contains the python-wrapper which I implemented to wrap SyntaxNet. The list of API's exposed in this wrapper are listed below:
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

## 3. How to run the parser:
```markdown
1. git clone https://github.com/spoddutur/syntaxnet.git
2. cd <syntaxnet-git-clone-directory>
3. python main.py 
4. That's it!!  It prints syntaxnet dependency parser output for given input english sentence
```

#### 3.1 Sample output for “Bob brought the pizza to Alice” input
<img src="https://user-images.githubusercontent.com/22542670/38134694-d492419e-3431-11e8-87a3-dcd6d0d36ebb.png" width="300"/>

Following gif shows how syntaxnet internally builds the dependency tree:

<img src="https://github.com/tensorflow/models/blob/master/research/syntaxnet/g3doc/images/looping-parser.gif" width="500" height="300"/>

## 4. Project Structure:
- **/models:** Originally cloned from syntaxnet git repository https://github.com/tensorflow/models . But this folder will additionally contain the bazel build “bazel-bin" folder with the needed runfiles.
- **custom_context.pbtxt:** Custom context file used in setting context for parser.
- **my_parser_eval.py:** python wrapper for “brain-tagger” POS tagger and “brain-parser” dependency parser. This file is heavily inspired from the [original parser_eval.py that syntaxnet provides](https://github.com/tensorflow/models/blob/master/syntaxnet/syntaxnet/parser_eval.py) with quiet some modifications aand enhancements.
- **main.py:** Demo sample usage
- **/data:** folder where parser’s intermediate input’s and output’s are dumped.
- **.whl:** osx package distribution of the final successful syntaxnet built using which you can setup `syntaxnet 0.2 version` in barely 5 minutes 
