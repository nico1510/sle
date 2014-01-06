build:
	make clean
	java -cp .:antlr-3.1.jar org.antlr.Tool Fsml.g


run:
	python -B FsmlModule.py
	dot -Tpdf sample_graph.dot -o sample_graph.pdf

test:
	cd tests; python -B FsmTest.py; cd ..

use:
	python -B User.py

clean:
	@rm -rf Fsml.tokens
	@rm -rf FsmlLexer.py
	@rm -rf FsmlLexer.pyc
	@rm -rf FsmlParser.py
	@rm -rf FsmlParser.pyc
	@rm -rf CodeGenerator.pyc
	@rm -rf Drawer.pyc
	@rm -rf OkFSM.pyc
	@rm -rf SimulateFSM.pyc
	@rm -rf TurnstileHandler_generated.py
	@rm -rf TurnstileHandler_generated.pyc
	@rm -rf TurnstileStepper_generated.pyc
	@rm -rf TurnstileStepper_generated.py
	@rm -rf FsmlModule.pyc
	@rm -rf sample_fsml.json
	@rm -rf sample_output.json
	@rm -rf sample_graph.dot
	@rm -rf sample_graph.pdf
	@rm -rf FsmExceptions.pyc
	@rm -rf ./tests/FsmTest.pyc

