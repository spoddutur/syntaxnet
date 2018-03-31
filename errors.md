## Errors encountered during setup:	
	
## 1. Build Errors
Build is done with `bazel test --linkopt=-headerpad_max_install_names dragnn/... syntaxnet/... util/utf8/...` command.
I ran into a myriad of issues before getting the build successful with all tests passing.
Iam listing some of the issues I faced here and how i got them fixed and hoping to help some SyntaxNet enthusiast out there facing similar issues :)]

1.1. Bazel version
##### Issue:
Current Bazel version is 0.10.0, expected at least 0.4.5
```diff
- ERROR: Error evaluating WORKSPACE file
- ERROR: error loading package 'external': Package 'external' contains errors
INFO: Elapsed time: 0.127s
- FAILED: Build did NOT complete successfully (0 packages loaded)
```
##### Cause: Initially, I had latest bazel version installed using `pip install bazel` (0.11.1).
##### Fix: Downgraded it to 0.5.1 as mentioned in the error.

2. Bazel 0.5.1 install failed: brew install bazel@0.5.1
Issue:
Last 15 lines from /Users/surthi/Library/Logs/Homebrew/bazel@0.5.1/01.compile.sh:
at com.google.devtools.build.buildjar.BazelJavaBuilder.processRequest(BazelJavaBuilder.java:89)
at com.google.devtools.build.buildjar.BazelJavaBuilder.runPersistentWorker(BazelJavaBuilder.java:66)
at com.google.devtools.build.buildjar.BazelJavaBuilder.main(BazelJavaBuilder.java:44) Caused by: java.util.MissingResourceException: Can't find bundle for base name com.google.errorprone.errors, locale en_IN
at java.util.ResourceBundle.throwMissingResourceException(ResourceBundle.java:1573)
at java.util.ResourceBundle.getBundleImpl(ResourceBundle.java:1396)
at java.util.ResourceBundle.getBundle(ResourceBundle.java:854)
at com.sun.tools.javac.util.JavacMessages.lambda$add$0(JavacMessages.java:106)
Cause: bazel compile via brew failed.
Fix: Downloaded installer from bazel release version as mention in step 5.7 above and installed.

Trying to mutate frozen object:
Issue:
“~/Envs/models/research/syntaxnet/syntaxnet/syntaxnet.bzl”, line 53, in tf_proto_library_py py_proto_library(name = name, srcs = srcs, srcs_versi...", <5 more arguments>) File "/private/var/tmp/_bazel_XXX/f74e5a21c3ad09aeb110d9de15110035/external/protobuf_archive/protobuf.bzl", line 374, in py_proto_library py_libs += [default_runtime] trying to mutate a frozen object ERROR: package contains errors: dragnn/protos
Cause: Bug in 0.4.5 version bazel
Fix: Install 0.5.4 version of bazel

autograd setup
Issue #1:
Bazel build of syntax net showed ~20 failing tests. Upon introspection, main error source is dependency on autograd python package
cat /root/.cache/bazel/_bazel_root/3b4c7ccb85580bc382ce4a52e9580003/execroot/__main__/bazel-out/local-opt/testlogs/syntaxnet/util/resources_test/test.log
from autograd import core as ag_core ImportError: No module named autograd
Fix #1: pip install autograd

Issue #2: cannot import name container_types
Cause: Upon fixing with pip install autograd succesfully installs the package and throws a name import error
cat /root/.cache/bazel/_bazel_root/3b4c7ccb85580bc382ce4a52e9580003/execroot/__main__/bazel-out/local-opt/testlogs/syntaxnet/util/resources_test/test.log
from autograd import container_types ImportError: cannot import name container_types
Fix #2: We need to install a compatible version of autograd (1.1.13) pip install autograd==1.1.13.
Also, again, make sure you have Bazel 0.5.4

4. bazel build failed with a bunch of tests on graph visualization’s and some more due to protobuf version incompatibility

Issue:
/private/var/tmp/_bazel_surthi/81559a7957a70ca9917043de0cb80034/execroot/__main__/bazel-out/local-opt/testlogs/dragnn/python/graph_builder_test/test.log
//dragnn/python:render_parse_tree_graphviz_test                          FAILED in 7.2s
/private/var/tmp/_bazel_surthi/81559a7957a70ca9917043de0cb80034/execroot/__main__/bazel-out/local-opt/testlogs/dragnn/python/render_parse_tree_graphviz_test/test.log
//dragnn/python:render_spec_with_graphviz_test                           FAILED in 7.3s
/private/var/tmp/_bazel_surthi/81559a7957a70ca9917043de0cb80034/execroot/__main__/bazel-out/local-opt/testlogs/dragnn/python/render_spec_with_graphviz_test/test.log
//dragnn/python:visualization_test                                       FAILED in 2.1s
/private/var/tmp/_bazel_surthi/81559a7957a70ca9917043de0cb80034/execroot/__main__/bazel-out/local-opt/testlogs/dragnn/python/visualization_test/test.log
//examples/dragnn:test_run_all_tutorials                                 FAILED in 7.9s
Cause: Two things. One, I had 3.0.0 protobuf installed and second missed installing pygraphviz.
Fix:
pip install -U protobuf==3.2.0
pip install pygraphviz

while running https://github.com/tensorflow/models/blob/master/research/syntaxnet/examples/dragnn/interactive_text_analyzer.ipynb ran into following problem:  https://stackoverflow.com/questions/47068709/your-cpu-supports-instructions-that-this-tensorflow-binary-was-not-compiled-to-u
References:
https://github.com/tensorflow/models.git
https://github.com/plowman/python-mcparseface/blob/master/models/syntaxnet/tensorflow/tensorflow/g3doc/get_started/os_setup.md
https://github.com/SaintNazaire/syntaxnet_bazel0.5.4/blob/master/Dockerfile
https://github.com/tensorflow/models/tree/master/research/syntaxnet

Couple of other links that helped me in resolving the issues I ran into:
https://stackoverflow.com/questions/47688252/tensorflow-trying-to-mutate-a-frozen-object-bazel
https://github.com/tensorflow/models/issues/1271
https://stackoverflow.com/questions/45991520/tensorflow-image-retraining-tutorial-bazel-error
https://github.com/tensorflow/models/issues/2355
https://github.com/tensorflow/models/issues/1271
https://github.com/bazelbuild/bazel/issues/4483
https://github.com/tensorflow/tensorflow/issues/16662
https://github.com/bazelbuild/bazel/issues/3018
https://www.tensorflow.org/install/install_mac
