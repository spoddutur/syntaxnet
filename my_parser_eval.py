import os
import sys
import time
import asciitree
import collections
import random
import string
import time
import contextlib
import re

PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))

runfiles_path = os.path.join(PROJECT_ROOT, 'models', 'research', 'syntaxnet', 'bazel-bin', 'syntaxnet', 'parser_eval.runfiles')
tensorflow_path = os.path.join(PROJECT_ROOT, 'models', 'research', 'syntaxnet', 'bazel-bin', 'syntaxnet', 'parser_eval.runfiles',
                               'external', 'tf')

sys.path.append(runfiles_path)
sys.path.append(tensorflow_path)

import tensorflow as tf
from tensorflow.python.platform import tf_logging as logging
from syntaxnet import sentence_pb2, structured_graph_builder
from syntaxnet.ops import gen_parser_ops
import syntaxnet.load_parser_ops
# from syntaxnet.conll2tree import to_dict

input_file_path = os.path.join(PROJECT_ROOT, "data", "input-file.txt")
output_file_path = os.path.join(PROJECT_ROOT, "data", "output-file.txt")
parser_path = os.path.join(PROJECT_ROOT, 'models', 'research', 'syntaxnet', 'bazel-bin', 'syntaxnet', 'parser_eval')
mcparseface_path = os.path.join(PROJECT_ROOT, 'models', 'research', 'syntaxnet', 'syntaxnet', 'models', 'parsey_mcparseface')
tagger_params_path = os.path.join(mcparseface_path, 'tagger-params')
parser_params_path = os.path.join(mcparseface_path, 'parser-params')
task_context_path = os.path.join(PROJECT_ROOT, "custom_context.pbtxt")

def _read_output():
	# print "############## READING OUTPUT ###############"
	output_file = open(output_file_path, mode="r")
	result = output_file.read()
	output_file.close()
	# print "############## OUTPUT READ: ###############", result
	return result

def _write_input(sentence):
	# print "############## WRITING INPUT ###############"
	# print input_file_path
	input_file = open(input_file_path, mode="w")
  	input_file.write(sentence)
  	input_file.flush()
	input_file.close()

def to_dict(sentence):
  	token_str = list()
	# children = [[] for token in sentence.token]
	children = [[] for i in range(0, len(sentence.token)+1)]
	roots = []
	root = -1
	for i in range(0, len(sentence.token)):
		token = sentence.token[i]
		token_str.append('%s %s %s @%d' %
		(token.word, token.tag, token.label, (i+1)))
		if token.head == -1:
			roots.append(i)
			root = i
		else:
			print "appending child:", i , token.word, " - to parent - ", token.head
			children[token.head].append(i)

	assert roots, "Couldnt find roots!!"

	if len(roots) > 1:
		# multiple roots so we make a fake one to be their parent
		# root = Token(0, 'ROOT', 'ROOT-LEMMA', 'ROOT-CPOS', 'ROOT-POS',
		# 	None, None, 'ROOT-DEPREL', None, None, None)
		print ("========== FOUND > 1 ROOT ==========", roots)
		new_root = '%s %s %s @%d' %("","","",len(token_str))
		token_str.append(new_root)
		index_of_new_root = len(token_str) - 1
		children[index_of_new_root] = roots #ROOT-POS
		root = index_of_new_root

	visited = []
	for i in range(len(children)):
		visited.append(0) 
		
	def _get_dict(i):
		d = collections.OrderedDict()
		for c in children[i]:
			# print "CHILDREN:", c, token_str[c]
			#if (visited[c] == 0):
			#	visited[c] = 1
			#	d[token_str[c]] = _get_dict(c)

	  		d[token_str[c]] = _get_dict(c)
		return d

	tree = collections.OrderedDict()
	tree[token_str[root]] = _get_dict(root)
	return tree

def pretty_print():
	_write_input(_read_output().strip())
	logging.set_verbosity(logging.INFO)
	with tf.Session() as sess:
		src = gen_parser_ops.document_source(batch_size=32,
					corpus_name='input-from-file-conll',
					task_context=task_context_path)
		sentence = sentence_pb2.Sentence()
		while True:
			documents, finished = sess.run(src)
			logging.info('Read %d documents', len(documents))
			# for d in documents:
			# 	sentence.ParseFromString(d)
			# 	as_asciitree(sentence)
			for d in documents:
				sentence.ParseFromString(d)
				tr = asciitree.LeftAligned()
				d = to_dict(sentence)
				print('Input: %s' % sentence.text)
				print('Parse:')
				tr_str = tr(d)
				pat = re.compile(r'\s*@\d+$')
				for tr_ln in tr_str.splitlines():
					print(pat.sub('', tr_ln))
			if finished:
				break

class SyntaxNetProcess:

	def __init__(self, action=None):
		self._sess = tf.Session()
		self._variable_scope = action.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(6))
		arg_prefix = action
		task_context = task_context_path
		print("_init: 0")
		if action == "brain_tagger":
			hidden_layer_sizes = [64]
			model_path = tagger_params_path
			output = 'output-to-file'
			input = 'input-from-file'
		elif action == "brain_parser":
			hidden_layer_sizes = [512, 512]
			model_path = parser_params_path
			output = 'output-to-file-conll'
			input = 'input-from-file-conll'
		else:
			raise Exception("Do not recognize action %s" % action)

		print("_init: 1")
		with tf.variable_scope(self._variable_scope):
			feature_sizes, domain_sizes, embedding_dims, num_actions = self._sess.run(
				gen_parser_ops.feature_size(task_context=task_context,
				arg_prefix=arg_prefix))
			print("_init: 2")
			beam_size = 8
			max_steps = 1000
			batch_size = 1024
			slim_model = True

			self._parser = structured_graph_builder.StructuredGraphBuilder(
				num_actions,
				feature_sizes,
				domain_sizes,
				embedding_dims,
				hidden_layer_sizes,
				gate_gradients=True,
				arg_prefix=arg_prefix,
				beam_size=beam_size,
				max_steps=max_steps)

			print("_init: 3")
			self._parser.AddEvaluation(task_context,
				batch_size,
				corpus_name=input,
				evaluation_max_steps=max_steps)
			print("_init: 4")
			# with tf.Session() as sess:
			self._sess.run(self._parser.inits.values())
			self._parser.AddSaver(slim_model)
			self._parser.saver.restore(self._sess, model_path)

			self._task_context = task_context
			self._output = 'stdout-conll' #output
		print("_init: Done")

	def eval(self, sentence=None):
		with stdout_redirected(output_file_path):
			if (sentence):
				_write_input(sentence)

			self._eval()

			result = _read_output()
			return result

	def _eval(self):
		
		with tf.variable_scope(self._variable_scope):
			sink_documents = tf.placeholder(tf.string)
			sink = gen_parser_ops.document_sink(sink_documents,
					task_context=self._task_context, 
					corpus_name=self._output)

			t = time.time()
			num_epochs = None
			num_tokens = 0
			num_correct = 0
			num_documents = 0
			while True:
				tf_eval_epochs, tf_eval_metrics, tf_documents = self._sess.run([
						self._parser.evaluation['epochs'],
						self._parser.evaluation['eval_metrics'],
						self._parser.evaluation['documents'],
						])

				if len(tf_documents):
					logging.info('Processed %d documents', len(tf_documents))
					num_documents += len(tf_documents)
					self._sess.run(sink, feed_dict={sink_documents: tf_documents})

				num_tokens += tf_eval_metrics[0]
				num_correct += tf_eval_metrics[1]
				if num_epochs is None:
					num_epochs = tf_eval_epochs
				elif num_epochs < tf_eval_epochs:
					break

			logging.info('Total processed documents: %d', num_documents)
			if num_tokens > 0:
				eval_metric = 100.0 * num_correct / num_tokens
				logging.info('num correct tokens: %d', num_correct)
				logging.info('total tokens: %d', num_tokens)
				logging.info('Seconds elapsed in evaluation: %.2f, '
						'eval metric: %.2f%%', time.time() - t, eval_metric)

@contextlib.contextmanager
def stdout_redirected(dest_filename):
    oldstdchannel = os.dup(sys.stdout.fileno())
    strm = open(dest_filename, 'w')  # bypassing linux 64 kb pipe limit
    os.dup2(strm.fileno(), sys.stdout.fileno())

    yield

    os.dup2(oldstdchannel, sys.stdout.fileno())
    os.close(oldstdchannel)
    strm.close()
