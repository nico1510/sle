grammar Fsml;

options {
	language=Python;
}

@init {
   self.fsmObject = dict()
   self.stateObject = dict()
   self.transitions = dict()
   self.currentState = ""
}

@members {
    def addState(self, initialText, idText):
        self.stateObject = dict()
        self.stateObject['transitions'] = dict()
        self.stateObject['initial'] = (initialText=='initial')
        self.fsmObject[idText] = self.fsmObject.get(idText, []) + [self.stateObject]
        self.currentState = idText

    def addTransition(self, inputText, outputText, targetStateText):
        self.stateObject['transitions'][inputText] = self.stateObject['transitions'].get(inputText, []) + [("" if str(outputText) == "None" else outputText, self.currentState if str(targetStateText) == "None" else targetStateText)]
}

fsm 	    : ( state )* ;
state	    : initial 'state' id {self.addState($initial.text,$id.text)} '{' ( transition )* '}' ;
initial     : 'initial'
	        |
	        ;
transition  : input_ ('/' action )? ( '->' id )? ';' {self.addTransition($input_.text, $action.text, $id.text)} ;
id	        : NAME ;
input_	    : NAME ;
action	    : NAME ;
NAME	    : ('a'..'z'|'A'..'Z')+ ;
WS          : ( '\t' | ' ' | '\r' | '\n'| '\u000C' )+    { $channel = HIDDEN; } ;