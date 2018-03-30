# Syntaxnet Parsey McParseface Python Wrapper
**Note:** This syntaxnet built contains [The Great Models Move](https://github.com/tensorflow/models/pull/2430) change. 

## This project does two things:
- **One line (~5mins) SyntaxNet 0.2 installation**: 

```sudo pip install syntaxnet-0.2-cp27-cp27m-macosx_10_6_intel.whl```

#### Specs:
<img src="https://user-images.githubusercontent.com/22542670/38134683-ca75dcac-3431-11e8-850e-b6379c07957b.png" height="100"/>

- **Syntaxnet Parsey McParseface wrapper**: This project lets you use Google's SyntaxNet Parsey McParseface (en Model) from python code saving you all the hours of dealing with installation setup and training models. In particular, I’ve demoed Dependency Parsing using syntaxnet.

## Demo
- I wrote a sample python code to use this wrapper and run syntaxnet's dependency parser. 
- **Input:** English sentence text
- **Output:** Dependency graph tree

Following gif shows how syntaxnet internally builds the dependency tree:


<img src="https://github.com/tensorflow/models/blob/master/research/syntaxnet/g3doc/images/looping-parser.gif" width="500" height="300"/>

## How to run the parser:
```markdown
1. git clone https://github.com/spoddutur/syntaxnet.git
2. cd <syntaxnet-git-clone-directory>
3. python main.py 
4. That's it!!  It prints syntaxnet dependency parser output for given input english sentence
```

## Sample output for “Bob brought the pizza to Alice” input
<img src="https://user-images.githubusercontent.com/22542670/38134694-d492419e-3431-11e8-87a3-dcd6d0d36ebb.png" width="300"/>

## Project Structure:
- **/models:** Originally cloned from syntaxnet git repository https://github.com/tensorflow/models . But this folder will additionally contain the bazel build “bazel-bin" folder with the needed runfiles.
- **custom_context.pbtxt:** Custom context file used in setting task context. Heavily inspired from here. https://github.com/plowman/python-mcparseface/blob/master/custom_context.pbtxt 
- **my_parser_eval.py:** python wrapper for “brain-tagger” POS tagger and “brain-parser” dependency parser. This file is tweak of the original parser_eval.py that synthxnet provides.  https://github.com/tensorflow/models/blob/master/syntaxnet/syntaxnet/parser_eval.py. with quiet some modifications like ability to call wrapper several times without needing to load model eveytime etc.
- **main.py:** Demo sample usage
- **/data:** folder where parser’s intermediate input’s and output’s are dumped.
- **.whl:** osx package distribution of the final successful syntaxnet built using which you can setup `syntaxnet 0.2 version` in barely 5 minutes 
