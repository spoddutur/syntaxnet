## Syntaxnet setup for OSx

I’ve setup tensorflow-syntaxnet in a virtual env named ‘tf’ in OsX. Please find the below steps that helped me in getting the build successful in OsX:

1. Setup virtual environment named ‘tf’.
  ```markdown
  virtualenv -p /usr/local/bin/python tf
	source tf/bin/activate
  ```
2. Install **six** - tensor flow dependency: `sudo easy_install --upgrade six`
3. Install tensor flow 0.8: `sudo pip install --upgrade https://storage.googleapis.com/tensorflow/mac/tensorflow-0.8.0-py2-none-any.whl`
Test tensor flow installation with helloworld in python terminal:
![image](https://user-images.githubusercontent.com/22542670/38160623-82471074-34de-11e8-89b8-c6d89da40fb4.png)
4. Install SyntaxNet Dependencies:
 ```markdown
 brew install swig
 pip freeze | grep protobuf
 sudo pip install -U protobuf==3.2.0
 pip install asciitree
 pip install numpy
 pip install autograd==1.1.13
 Install bazel 0.5.4
 Download bazel-0.5.4-without-jdk-installer-darwin-x86_64.sh from  https://github.com/bazelbuild/bazel/releases 
 chmod +x ~/Downloads/bazel-0.5.4-without-jdk-installer-darwin-x86_64.sh
 sh ~/Downloads/bazel-0.5.4-without-jdk-installer-darwin-x86_64.sh
 pip install mock
 brew install graphviz
 pip install pygraphviz
 ```
5. Download syntaxnet:
```markdown
cd <LOCATION_TO_WHERE_SYNTAXNET_REPO_WILL_BE_COPIED>
git clone --recursive https://github.com/tensorflow/models.git
```
6. Configure:
```markdown
cd <LOCATION_TO_WHERE_SYNTAXNET_REPO_IS_COPIED>/models/research/syntaxnet/tensorflow
./configure
```
7. Build Syntaxnet: 
 ```markdown
 cd <LOCATION_TO_WHERE_SYNTAXNET_REPO_IS_COPIED>
 run “bazel test --linkopt=-headerpad_max_install_names dragnn/... syntaxnet/... util/utf8/…”
 ```
8. Test Syntaxnet: 
```markdown
cd <LOCATION_TO_WHERE_SYNTAXNET_REPO_IS_COPIED>/models/research/syntaxnet
echo 'Bob brought the pizza to Alice.' | syntaxnet/demo.sh
```
9. Output:
![image](https://user-images.githubusercontent.com/22542670/38160624-86233bd2-34de-11e8-9401-3d05c995ca50.png)

 
