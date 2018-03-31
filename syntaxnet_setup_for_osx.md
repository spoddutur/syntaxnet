## Syntaxnet setup for OSx

I’ve setup tensorflow-syntaxnet in a virtual env named ‘tf’ in OsX. Please find the below steps that helped me in getting the build successful in OsX:

1. Setup virtual environment named ‘tf’.
  ```markdown
  virtualenv -p /usr/local/bin/python tf
  source tf/bin/activate
  ```
2. Install **six** - tensor flow dependency: 
```markdown
sudo easy_install --upgrade six
```
3. Install tensor flow:
```markdown
sudo pip install --upgrade tensorflow
```
4. Test tensor flow installation with helloworld in python terminal:
```markdown
python
import tensorflow as tf
hello = tf.constant('HelloWorld, Tensorflow!!')
sess = tf.session()
print(sess.run(hello))
```
5. Install SyntaxNet Dependencies:
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
6. Download syntaxnet:
```markdown
cd <LOCATION_TO_WHERE_SYNTAXNET_REPO_WILL_BE_COPIED>
git clone --recursive https://github.com/tensorflow/models.git
```
7. Configure:
```markdown
cd <LOCATION_TO_WHERE_SYNTAXNET_REPO_IS_COPIED>/models/research/syntaxnet/tensorflow
./configure
```
8. Build Syntaxnet: 
 ```markdown
 cd <LOCATION_TO_WHERE_SYNTAXNET_REPO_IS_COPIED>
 run “bazel test --linkopt=-headerpad_max_install_names dragnn/... syntaxnet/... util/utf8/…”
 ```
9. Test Syntaxnet: 
```markdown
cd <LOCATION_TO_WHERE_SYNTAXNET_REPO_IS_COPIED>/models/research/syntaxnet
echo 'Bob brought the pizza to Alice.' | syntaxnet/demo.sh
```
10. Output:
[!image](https://user-images.githubusercontent.com/22542670/38160793-93ae9d1c-34e0-11e8-813d-56298256858d.png)
