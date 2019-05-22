from dragonfly import Function, Key, Text, Mouse, Pause, Dictation, Choice, Grammar , ContextAction


from castervoice.lib import control, settings, text_manipulation_functions

from castervoice.lib.context import AppContext
from castervoice.lib.dfplus.additions import IntegerRefST
from castervoice.lib.dfplus.merge import gfilter
from castervoice.lib.dfplus.merge.mergerule import MergeRule
from castervoice.lib.dfplus.merge.ccrmerger import CCRMerger
from castervoice.lib.dfplus.state.short import R

# Advertisement
print("""Check out the new experimental text manipulation commands in castervoice\lib\ccr\core\text_manipulation.py 
    You may want to reduce the pause time in the functions in castervoice\lib\text_manipulation_functions.py
    """)

class TextManipulation(MergeRule):
    pronunciation = "text manipulation"


    mapping = {

        
        # requires the latest version of dragonfly because of her recent modification of the Function action
            # I think dragonfly2-0.13.0
        # The PAUSE TIMES in these functions should be reduced (possibly depending on the application ).
        # I have them cranked up very high right now just to make sure everything works.
        # the keypress waittime should probably be made shorter for these commands.
        # When these commands are not working in a particular application sometimes the problem is that 
        # there is not enough time from when control-c is pressed until the contents of the clipboard are passed into the function
        # The solution is to add a longer pause after pressing control see in the supporting functions in text_manipulation_functions.py
        # For some applications this pause ( and other pauses in the functions for that matter ) is not necessary
        # and may be removed by the user if they wish to speed up the execution of these commands
        # These functions copy text into the clipboard and then return whatever you had there before backing onto the clipboardself.
        # If you are using the multi clipboard, this might be annoying because you will have some
        # extra junk put on the second slot on your multi clipboard. To combat this problem you
        # could use castervoice.lib.context.read_selected_without_altering_clipboard() instead of pyperclip


# Todo: Find way to to better consolidate these context actions.
        
        # # PROBLEM: sometimes Dragon thinks the variables are part of dictation.           
        "(replace|change) <lease_ross> [<number_of_lines_to_search>] [<occurrence_number>] <dictation> (with|to) <dictation2>":
            R(ContextAction(default=Function(text_manipulation_functions.copypaste_replace_phrase_with_phrase,
                       dict(dictation="replaced_phrase", dictation2="replacement_phrase", lease_ross="left_right"), 
                       cursor_behavior="standard"), actions=[
                        # Use different cursor method for texstudio
                        (AppContext(executable="texstudio"), Function(text_manipulation_functions.copypaste_replace_phrase_with_phrase,
                       dict(dictation="replaced_phrase", dictation2="replacement_phrase", lease_ross="left_right"), 
                       cursor_behavior="texstudio"))]),
              rdescript="Text Manipulation: replace text to the left or right of the cursor"),
        
        "remove <lease_ross> [<number_of_lines_to_search>] [<occurrence_number>] <dictation>":
            R(ContextAction(default=Function(text_manipulation_functions.copypaste_remove_phrase_from_text,
                       dict(dictation="phrase", lease_ross="left_right"), cursor_behavior="standard"),
                       actions=[(AppContext(executable="texstudio"), Function(text_manipulation_functions.copypaste_remove_phrase_from_text,
                       dict(dictation="phrase", lease_ross="left_right"), cursor_behavior="texstudio"))]),
              rdescript="Text Manipulation: remove chosen phrase to the left or right of the cursor"),
        "remove lease [<number_of_lines_to_search>] [<occurrence_number>] <left_character>":
            R(ContextAction(default=Function(text_manipulation_functions.copypaste_remove_phrase_from_text,
                       dict(left_character="phrase"),
                       left_right="left", cursor_behavior="standard"), actions=[(AppContext(executable="texstudio"), 
                       Function(text_manipulation_functions.copypaste_remove_phrase_from_text,
                       dict(left_character="phrase"),
                       left_right="left", cursor_behavior="texstudio"))]),
              rdescript="Text Manipulation: remove chosen character to the left of the cursor"),
        "remove ross [<number_of_lines_to_search>] [<occurrence_number>] <right_character>":
            R(ContextAction(default=Function(text_manipulation_functions.copypaste_remove_phrase_from_text,
                       dict(right_character="phrase"),
                       left_right="right", cursor_behavior="standard"),
                       actions=[(AppContext("texstudio"), 
                       Function(text_manipulation_functions.copypaste_remove_phrase_from_text,
                       dict(right_character="phrase"),
                       left_right="right", cursor_behavior="texstudio"))]),
              rdescript="Text Manipulation: remove chosen character to the right of the cursor"),

        
        "go <lease_ross> [<number_of_lines_to_search>] [<before_after>] [<occurrence_number>] <dictation>":
            R(ContextAction(default = Function(text_manipulation_functions.move_until_phrase,
                       dict(dictation="phrase", lease_ross="left_right"), cursor_behavior="standard"), 
                       # Use different method for texstudio
                       actions=[             
                (AppContext(executable="texstudio"), Function(text_manipulation_functions.move_until_phrase,
                       dict(dictation="phrase", lease_ross="left_right"), cursor_behavior="texstudio")),
                ]), rdescript="Text Manipulation: move to chosen phrase to the left or right of the cursor"),
        "go lease [<before_after>] [<number_of_lines_to_search>] [<occurrence_number>] <left_character>":
            R(ContextAction(default=Function(text_manipulation_functions.move_until_phrase,
                       dict(left_character="phrase"),
                       left_right="left", cursor_behavior="standard"), actions=[(AppContext("texstudio"),
                       Function(text_manipulation_functions.move_until_phrase,
                       dict(left_character="phrase"),
                       left_right="left", cursor_behavior="texstudio"))]),
              rdescript="Text Manipulation: move to chosen character to the left of the cursor"),
        "go ross [<before_after>] [<number_of_lines_to_search>] [<occurrence_number>] <right_character>":
            R(ContextAction(default=Function(text_manipulation_functions.move_until_phrase,
                       dict(right_character="phrase"),
                       left_right="right", cursor_behavior="standard"), actions=[(AppContext("texstudio"),
                       Function(text_manipulation_functions.move_until_phrase,
                       dict(right_character="phrase"),
                       left_right="right", cursor_behavior="texstudio"))]),
              rdescript="Text Manipulation: move to chosen character to the right of the cursor"),
        "grab <lease_ross> [<number_of_lines_to_search>] [<occurrence_number>] <dictation>":
            R(ContextAction(default=Function(text_manipulation_functions.select_phrase, 
            dict(dictation="phrase", lease_ross="left_right"), 
            cursor_behavior="standard"), actions=[(AppContext("texstudio"),
            Function(text_manipulation_functions.select_phrase,
                       dict(dictation="phrase", lease_ross="left_right"),
                       cursor_behavior="texstudio"))]),
                 rdescript="Text Manipulation: select chosen phrase"),
        "grab lease [<number_of_lines_to_search>] [<occurrence_number>] <left_character>":
            R(ContextAction(default=Function(text_manipulation_functions.select_phrase,
            dict(left_character="phrase"), left_right="left",
            cursor_behavior="standard"), actions=[(AppContext("texstudio"),
            Function(text_manipulation_functions.select_phrase, dict(left_character="phrase"), left_right="left",
            cursor_behavior="texstudio"))]),
            rdescript="Text Manipulation: select chosen character to the left"),
        "grab ross [<number_of_lines_to_search>] [<occurrence_number>] <right_character>":
            R(ContextAction(default=Function(text_manipulation_functions.select_phrase, dict(right_character="phrase"), 
            left_right="right", cursor_behavior="standard"), actions=[(AppContext("texstudio"),
            Function(text_manipulation_functions.select_phrase, dict(right_character="phrase"), left_right="right",
            cursor_behavior="texstudio"))]),
            rdescript="Text Manipulation: select chosen character to the right"),
        
        "grab <lease_ross> [<number_of_lines_to_search>] until [<before_after>] [<occurrence_number>] <dictation> ":
            R(ContextAction(default=Function(text_manipulation_functions.select_until_phrase, 
            dict(dictation="phrase", lease_ross="left_right"), 
            cursor_behavior="standard"), actions=[(AppContext("texstudio"),
            Function(text_manipulation_functions.select_until_phrase, dict(dictation="phrase", lease_ross="left_right"), 
            cursor_behavior="texstudio"))]),
                 rdescript="Text Manipulation: select until chosen phrase"),
        "grab lease [<number_of_lines_to_search>] until [<before_after>] [<occurrence_number>] <left_character>":
            R(ContextAction(default=Function(text_manipulation_functions.select_until_phrase, dict(left_character="phrase"), 
            left_right="left", cursor_behavior="standard"), actions=[(AppContext("texstudio"),
            Function(text_manipulation_functions.select_until_phrase, dict(left_character="phrase"), 
            left_right="left", cursor_behavior="texstudio"))]),
            rdescript="Text Manipulation: select left until chosen character"),
        "grab ross [<number_of_lines_to_search>] until [<before_after>] [<occurrence_number>] <right_character>":
            R(ContextAction(default=Function(text_manipulation_functions.select_until_phrase, dict(right_character="phrase"), 
            left_right="right", cursor_behavior="standard"),
            actions=[(AppContext("texstudio"), Function(text_manipulation_functions.select_until_phrase,
            dict(right_character="phrase"), left_right="right", cursor_behavior="texstudio"))]),
            rdescript="Text Manipulation: select right until chosen character"),
        "wipe <lease_ross> [<number_of_lines_to_search>] [until] [<before_after>] [<occurrence_number>] <dictation>":
            R(ContextAction(default=Function(text_manipulation_functions.copypaste_delete_until_phrase,
                       dict(dictation="phrase", lease_ross="left_right"), cursor_behavior="standard"),
                       actions=[(AppContext("texstudio"), Function(text_manipulation_functions.copypaste_delete_until_phrase,
                       dict(dictation="phrase", lease_ross="left_right"), cursor_behavior="texstudio"))]),
              rdescript="Text Manipulation: delete left until chosen phrase"),
        "wipe lease [<number_of_lines_to_search>] [until] [<before_after>] [<occurrence_number>] <left_character>":
            R(ContextAction(default=Function(text_manipulation_functions.copypaste_delete_until_phrase,
                       dict(left_character="phrase"),
                       left_right="left", cursor_behavior="standard"),
                       actions=[(AppContext("texstudio"), Function(text_manipulation_functions.copypaste_delete_until_phrase,
                       dict(left_character="phrase"),
                       left_right="left", cursor_behavior="texstudio"))]),
              rdescript="Text Manipulation: delete left until chosen character"),
        "wipe ross [<number_of_lines_to_search>] [until] [<before_after>] [<occurrence_number>] <right_character>":
            R(ContextAction(default=Function(text_manipulation_functions.copypaste_delete_until_phrase,
                       dict(right_character="phrase"), 
                       left_right="right", cursor_behavior="standard"), 
                       actions=[(AppContext("texstudio"), Function(text_manipulation_functions.copypaste_delete_until_phrase,
                       dict(right_character="phrase"), 
                       left_right="right", cursor_behavior="texstudio"))]),
              rdescript="Text Manipulation: delete left until chosen character"),
        


        
    }
    extras = [
        Dictation("dict"),
        Dictation("dictation"),
        Dictation("dictation2"),
        Dictation("text"),
        IntegerRefST("n", 1, 100),
        IntegerRefST("m", 1, 100),
        IntegerRefST("wait_time", 1, 1000),
        IntegerRefST("number_of_lines_to_search", 1, 50),
        Choice("character_sequence", {
            "comma": ",",
        }),
     Choice(
            "left_character", {
                "[left] prekris": "(",
                "right prekris": ")",
                "[left] brax": "[",
                "right brax": "]",
                "[left] angle": "<",
                "right angle": ">",
                "[left] curly": "{",
                "right curly": "}",
                "quotes": '"',
                "(single quote | thin quote)": "'",
                "comma": ",",
                "(dot | period)": ".",
                "questo": "?",
                "deckle": ":",
                "semper": ";",
                "backtick": "`",
                "equals": "=",
                "dolly": "$",
                "slash": "/",
                "backslash": "\\",
                "minus": "-",
                "plus": "+",
                "starling": "*",
                "x-ray": "x",

            }),
        Choice(
            "right_character", {
                "[right] prekris": ")",
                "left prekris": "(",
                "[right] brax": "]",
                "left brax": "[",
                "[right] angle": ">",
                "left angle": "<",
                "[right] curly": "}",
                "left curly": "{",
                "quotes": '"',
                "(single quote | thin quote)": "'",
                "comma": ",",
                "(dot | period)": ".",
                "questo": "?",
                "deckle": ":",
                "semper": ";",
                "backtick": "`",
                "equals": "=",
                "dolly": "$",
                "slash": "/",
                "backslash": "\\",
                "minus": "-",
                "plus": "+",
                "starling": "*",
                "x-ray": "x",
                
            }),
        Choice("lease_ross", {
            "lease": "left",
            "ross": "right",
        }),
        Choice("before_after", {
            "before": "before",
            "after": "after",
        }),
        Choice("occurrence_number", {
            "first": 1,
            "second": 2,
            "third": 3,
            "fourth": 4,
            "fifth": 5,
            "sixth": 6,
            "seventh": 7,
            "eighth": 8,
            "ninth": 9,
            "tenth": 10,
        }),
        
        
    ]
    defaults = {"n": 1, "m": 1, "spec": "", "dict": "", "text": "", "mouse_button": "", 
        "horizontal_distance": 0, "vertical_distance": 0, 
        "lease_ross": "left",
        "before_after": None,
        "number_of_lines_to_search": 0,
        "occurrence_number": 1,}

control.nexus().merger.add_global_rule(TextManipulation())



