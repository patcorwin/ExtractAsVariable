import re
import sublime
import sublime_plugin


class ExtractAsVariableCommand(sublime_plugin.TextCommand):
    '''
    Takes the selected text and inserts it on a new line above preceded by an
    equals sign, placing the cursor at that line and where the text was.
    
    Ex:
        # selection    ]___________________________________[
        thing.setSize( thing.getWith() + buffer * 3 + offset )
        
        # Turns into ( ][ are the cursors):
        ][ = thing.getWith() + buffer * 3 + offset
        thing.setSize( ][ )
    '''
 
    def run(self, edit):
 
        sels = iter(self.view.sel())
        
        for sel in sels:
            if not sel.empty():
                
                # Extract the first valid selection
                self.introduce_variable(edit, sel)
                
                # Simply remove the following selection and replace with cursor.
                for sel in sels:
                    if not sel.empty():
                        self.view.replace(edit, sel, '')
               
    def introduce_variable(self, edit, sel):
        sel_text = self.view.substr(sel)
        top_line = self.view.lines(sel)[0]
        top_line_text = self.view.substr(top_line)
        indentation = ''
 
        match = re.search(r'\W*', top_line_text, re.UNICODE)
 
        if match:
            indentation = match.group(0)
 
        var_declaration = indentation + ' = ' + sel_text + '\n'
 
        self.view.replace(edit, sel, '')
        
        self.view.insert(edit, top_line.a, var_declaration)

        startOfLine = top_line.a + len(indentation)
        self.view.sel().add( sublime.Region(startOfLine, startOfLine) )
        