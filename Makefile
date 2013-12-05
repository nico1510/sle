build:
	make clean
	java -cp .:antlr-3.1.jar org.antlr.Tool Fsml.g


run:
	python FsmlModule.py


clean:
	@rm -rf Fsml.tokens
	@rm -rf FsmlLexer.py
	@rm -rf FsmlLexer.pyc
	@rm -rf FsmlParser.py
	@rm -rf FsmlParser.pyc
	@rm -rf sample_fsml.json
	@rm -rf sample_output.json
