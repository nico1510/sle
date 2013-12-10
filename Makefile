build:
	make clean
	java -cp .:antlr-3.1.jar org.antlr.Tool Fsml.g


run:
	python -B FsmlModule.py
	python -B CodeGenerator.py


clean:
	@rm -rf Fsml.tokens
	@rm -rf FsmlLexer.py
	@rm -rf FsmlParser.py
	@rm -rf sample_fsml.json
	@rm -rf sample_output.json
	@rm -rf TurnstileHandler_generated.py
	@rm -rf FsmlLexer.pyc
	@rm -rf FsmlParser.pyc
	@rm -rf TurnstileHandler_generated.pyc
	@rm -rf FsmlModule.pyc
	@rm -rf CodeGenerator.pyc
	@rm -rf TurnstileStepper_generated.pyc
	@rm -rf TurnstileStepper_generated.py
