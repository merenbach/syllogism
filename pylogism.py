#!/usr/bin/python
# -*- coding: utf-8 -*-

import os



# from the latest BASIC distribution:
#   Syllogism 1.0. November 8, 2002
#   I edited this program in 2002, for compatibility with freeware BASIC
#   interpreters for the Mac: Chipmunk BASIC 3.5.7 and Metal BASIC 1.7.3.
#   Peace. Ben Sharvy. luvnpeas99@yahoo.com
#
# This port is under active development by Andrew Merenbach

#xyz = list()
#xyz.append("some", "  is", "<null>", "some", "  is not", "*")
#xyz.append("all", "*  is", "<null>", "no", "*  is", "*")
#xyz.append("<null>", "+  is", "<null>", "<null>", "+  is not", "*")
#xyz.append("<null>", "+  = ", "+", "<null>", "+   = / = ", "*")

#rem l1 => length_of_symbol_table
#rem n1 => negative_premise_count
#rem b(63) => term_article(63)
#rem d(63) => term_dist_count(63)
#rem e(2) => recent_article_types(2)
#rem g(63) => term_type(63)
#rem k(63) => link_order(63) : rem this may be right
#rem n(63) => line_numbers(63)
#rem o(63) => term_occurrences(63)
#rem t(7) => recent_symbol_types(7) : rem this should be right--see (former) line 2020
#rem a$(3) => article_strings[3)
#rem g$(2) => term_type_name$(2) : rem hopefully this is right
#rem l$(63) => line_strings$(63)
#rem s$(6) => recent_symbol_strings[6] : rem hopefully this is right
#rem t$(65) => term_strings$(65)
#rem w$( 2 ) => recent_term_strings

prompt = '>'

articles = ("a ", "an ", "sm ")
term_type_names = ("undetermined type", "general term", "designator")

sample_lines = (
    "10 all mortals are fools",
    "20 all athenians are men",
    "30 all philosophers are geniuses",
    "40 all people with good taste are philosophers",
    "50 richter is a diamond broker",
    "60 richter is the most hedonistic person in florida",
    "70 all men are mortal",
    "80 no genius is a fool",
    "90 all diamond brokers are people with good taste",
    "100 the most hedonistic person in florida is a decision-theorist",
)

x_array = ('some', 'some', 'all', 'no', '', '', '', '')
y_array = ("  is", "  is not", "*  is", "*  is", "+  is", "+  is not", "+  = ", "+   = / = ")
z_array = ("", "*", "", "*", "", "*", "+", "*")

# prepopulated plurals that might otherwise confuse the program
plurals = dict(
    [
        ("socrates", "socrates"),
        ("parmenides", "parmenides"),
        ("epimenides", "epimenides"),
        ("mice", "mouse"),
        ("lice", "louse"),
        ("geese", "goose"),
        ("children", "child"),
        ("oxen", "ox"),
        ("people", "person"),
        ("teeth", "tooth"),
        ("wolves", "wolf"),
        ("wives", "wife"),
        ("selves", "self"),
        ("lives", "life"),
        ("leaves", "leaf"),
        ("shelves", "shelf"),
        ("elves", "elf"),
        ("dwarves", "dwarf"),
        ("knives", "knife"),
        ("thieves", "thief"),
        ("neckties", "necktie"),
        ("hippies", "hippie"),
        ("yippies", "yippie"),
        ("yuppies", "yuppie"),
        ("moonies", "moonie"),
        ("druggies", "druggie"),
        ("cookies", "cookie"),
        ("commies", "commie"),
        ("groupies", "groupie"),
        ("tomatoes", "tomato"),
        ("alcibiades", "alcibiades"),
        ("thales", "thales"),
        ("aries", "aries"),
        ("athens", "athens"),
        ("species", "species"),
        ("feces", "feces"),
        ("geniuses", "genius"),
        ("sorites", "sorites"),
        ("crises", "crisis"),
        ("emphases", "emphasis"),
        ("memoranda", "memorandum"),
        ("theses", "thesis"),
        ("automata", "automaton"),
        ("formulae", "formula"),
        ("stigmata", "stigma"),
        ("lemmata", "lemma"),
        ("vertices", "vertex"),
        ("vortices", "vortex"),
        ("indices", "index"),
        ("codices", "codex"),
        ("matrices", "matrix"),
        ("gasses", "gas"),
        ("gases", "gas"),
        ("buses", "bus"),
        ("aches", "ache"),
        ("headaches", "headache"),
        ("grits", "grits"),
        ("molasses", "molasses"),
        ("gas", "gas"),
        ("christmas", "christmas"),
        ("mathematics", "mathematics"),
        ("semantics", "semantics"),
        ("physics", "physics"),
        ("metaphysics", "metaphysics"),
        ("ethics", "ethics"),
        ("linguistics", "linguistics"),
        ("kiwis", "kiwi"),
        ("israelis", "israeli"),
        ("goyim", "goy"),
        ("seraphim", "seraph"),
        ("cherubim", "cherub"),
        ("semen", "semen"),
        ("amen", "amen"),
        ("ZZZZZ", "ZZZZZ")
    ]
)


class Premise(object):
    def __init__(self, line):
        self.raw = line.strip()
        tokens = line.strip().split()
        self.line_number = int(tokens[0])
        self.statement = u' '.join(tokens[1:])
    
    def empty(self):
        """ Check whether this premise actually contains a statement.

        Returns
        -------
        boolean : `True` if a statement exists for this premise, `False` otherwise.
        """
        return not self.statement or len(self.statement) == 0
    
    def __repr__(self):
        return self.raw

class Rubric(object):
    """ Hold a list of premises. """
    def __init__(self):
        self.premises = []

    def reset(self):
        """ Remove all premises. """
        self.premises = []

    def enter_line(self, line):
        """ Try to parse a string into a premise and add it to our lookup table.
        
        Parameters
        ----------
        line : string
               A string to parse into a premise.

        Returns
        -------
        boolean : `True` if a premise was added successfully, `False` otherwise.
                  If this method returns `False`, odds are that an error message was printed.
        """
        try:
            premise = Premise(line)
        except ValueError:
            # Invalid input
            print("*** Invalid entry.")
            return False
        return self.enter_premise(premise)
    
    def enter_premise(self, premise):
        """ Try to add a premise to our lookup table.
        
        Parameters
        ----------
        premise : Premise
                  A premise to add to our lookup table.

        Returns
        -------
        boolean : `True` if the premise was added successfully, `False` otherwise.
                  If this method returns `False`, odds are that an error message was printed.
        """
        if premise.empty():
            return self.remove_line(premise.line_number, silent=False)
        else:
            # Remove any lines with the same line number
            self.remove_line(premise.line_number, silent=True)
            self.premises.append(premise)
            # If a statement was included, replace the existing line
            # Otherwise, simply don't put the statement into place

            # Sort the new premises by line number
            # We only need to do this when adding lines                
            self.premises.sort(key=lambda p: p.line_number)
            return True

    def remove_line(self, line_number, silent=False):
        """ Remove a premise (identified by line number) from the lookup table.
        
        Parameters
        ----------
        line_number : integer
                      A premise line number for whose existence to check.
        silent      : boolean
                      `True` to complain if line does not exist or if no premises are entered,
                      `False` otherwise.

        Returns
        -------
        boolean : `True` if the line was removed, `False` otherwise.
        """
        if self.line_exists(line_number):
            self.premises = [p for p in self.premises if p.line_number != line_number]
            return True
        elif len(self.premises) == 0:
            # No premises have been entered
            if not silent:
                self.show_error_no_premises()
            return False
        else:
            # The premise to remove did not exist
            if not silent:
                print("Line {0} not found".format(line_number))
            return False

    def line_exists(self, line_number):
        """ Check if a premise with a given line number exists in the lookup table.
        
        Parameters
        ----------
        line_number : integer
                      A premise line number for whose existence to check.

        Returns
        -------
        boolean : `True` if a premise with the given line number exists already, `False` otherwise.
        """
        for p in self.premises:
            if p.line_number == line_number:
                return True
        return False

    def p(self, analyze=False):
        """ Printable format """
        lines = []
        last_premise = self.premises[-1:]
        if len(last_premise) > 0:
            max_padding_chars = len(str(last_premise[0].line_number))
            # Format lines with nice spacing
            premise_groups = ((p.line_number, p.statement) for p in self.premises)
            for p in premise_groups:
                if not analyze:
                    lines.append(u' {0} {1}'.format(str(p[0]).rjust(max_padding_chars), p[1]))
                else:
                    lines.append(u" [TODO] Distribution analysis listing")
        return u'\n'.join(lines)

    def __repr__(self):
        return self.p()

    def show_error_no_premises(self):
        """ Show an error if no premises have been entered. """
        print("No premises")

class Syllogism(object):
    pass

class SyllogismController(object):
    show_messages = True
    premise_list = []


    line_numbers_arranged = []      # l()
    line_strings = []       # l$()
    term_article = []       # b()
    term_strings = []       # t$()
    term_types = []         # g()
    conclusion_terms = []   # c()
    neg_premises = 0        # n1
    modern_valid = False    # v1
    symbol_count = 0        # l1
    lowest_line = 0         # l(0)

    #recent_term_strings = []   # w$()
    recent_term_1 = ''
    recent_term_2 = ''
    recent_term_type_1 = (-1)
    recent_term_type_2 = (-1)
    recent_symbol_types = []    # t()
    recent_symbol_strings = []  # s$()

    syllogism_form = (-1)       # d1

    a_array_0 = 0   # a(0)
    a_array = []    # a()

    q_array = []
    r_array = []

    # length_of_symbol_table = len(term_strings)
    #im a(63),c(63),term_dist_count(63),term_type(63),l(63),line_numbers(63),term_occurrences(63),p(63),q(63)
    #dim r(63),term_article(63),k(63),j(4),recent_symbol_types[7],recent_article_types(2),h(2)
    #dim article_strings[3),line_strings$(63),term_strings$(65)
    #dim g$(2),recent_symbol_strings[6],recent_term_strings[MY_TWO],x$(7),y$(7),z(7)

    def __init__(self):
        # New variables
        self.rubric = Rubric()
        
        # Legacy
        
        self.a_array = range(64)
        self.a_array_0 = 0

        self.line_numbers_arranged = [0] * 64       # l()
        self.line_strings = [''] * 64       # l$()
        self.term_article = [0] * 64        # b()
        self.term_strings = [''] * 64       # t$()
        self.term_types = [0] * 64          # g()
        self.recent_symbol_types = [0] * 64 # t()
        self.recent_symbol_strings = [''] * 64  # s$()


        q_array = [0] * 64
        r_array = [0] * 64
        
        self.main()
        #pass

    def main(self):
        self.intro()
        self.print_hint()
        self.new_syllogism()
        self.request_input()

    def intro(self):
        self.cls()
        print("Syllogism Program Copyright (c) 1988 Richard Sharvy")
        print("Syllogism 1.0 (c) 2002 Richard Sharvy's estate")
        print("Ben Sharvy: luvnpeas99@yahoo.com or bsharvy@efn.org")
        print

    def cls(self):
        # clear the screen
        os.system("clear")

    def spaces(self, space_count):
        # print a specified number of space
        return (space_count * ' ')
        #return ' '.ljust(space_count)
        #str_list = []
        #for n in range(space_count):
        #   str_list.append(' ')
        #s = ''.join(str_list)
        #s = ''.join([' ' for n in range(space_count)])

    def print_hint(self):
        """ Print usage hint """
        if self.show_messages:
            print("Enter HELP for list of commands")

    def request_input(self):
        functions = {
            'new': self.new_syllogism,
            'sample': self.sample_syllogism,
            'help': self.print_commands,
            'syntax': self.print_syntax,
            'info': self.print_info,
            # 'dump': self.show_dump,
            'msg': self.toggle_messages,
            # 'substitute': self.substitute_terms,
            #'link': link(),
            #'link*': link(),
            'list': self.list_lines,
            'list*': self.list_lines,
        }

        line = ''
        while line != 'stop':
            print
            line = raw_input(prompt).lower()
            line = self.strip_string(line)
            if line == '':
                self.print_hint()
            else:
                if line in functions.keys():
                    function = functions[line]
                    if not line.endswith('*'):
                        function()
                    else:
                        function(True)
                else:
                    self.scan_line(line)
                    
        if self.show_messages:
            print("(Some versions support typing CONT to continue)")
        print
    
    def toggle_messages(self):
        self.show_messages = not self.show_messages
        state = ''
        if self.show_messages:
            state = 'on'
        else:
            state = 'off'
        print('Messages turned {0}'.format(state))

    def strip_string(self, string):
        punctuation = ('.', '?', '!')
        string = string.rstrip()
        while string[-1:] in punctuation:
            print(self.spaces(len(string)) + "^   Punctuation mark ignored")
            #line = line.rstrip('.?!')
            string = string[:-1]
            string = string.rstrip()
        string = string.lstrip()
        return string

    def print_commands(self):
        """ List valid inputs """
        # rem---List valid inputs--- : rem [am] 7660
        self.cls()
        print("Valid commands are:")
        print("   <n>  [ <statement> ]   Insert, delete, or replace premise number  <n> ")
        print(self.spaces(28) + "Examples:   10  All men are mortal")
        print(self.spaces(40) + "10")
        print("  DUMP" + self.spaces(15) + "Prints symbol table, distribution count, etc.")
        print("  HELP" + self.spaces(15) + "Prints this list")
        print("  INFO" + self.spaces(15) + "Gives information about syllogisms")
        print("  LIST" + self.spaces(15) + "Lists premises")
        print("  LIST*" + self.spaces(14) + "Same, but displays distribution analysis:")
        print(self.spaces(25) + "distributed positions marked with '*', ")
        print(self.spaces(25) + "designators marked with '+'")
        print("  LINK" + self.spaces(15) + "Lists premises in order of term-links (if possible)")
        print("  LINK*" + self.spaces(14) + "Same, but in distribution-analysis format")
        print("  MSG" + self.spaces(16) + "Turns on/off Printing of certain messages and warnings")
        print("  NEW" + self.spaces(16) + "Erases current syllogism")
        print("  SAMPLE" + self.spaces(13) + "Erases current syllogism and enters sample syllogism")
        print("  STOP" + self.spaces(15) + "Stops entire program")
        print("  SUBSTITUTE" + self.spaces(9) + "Allows uniform substitution of new terms in old premises")
        print("  SYNTAX" + self.spaces(13) + "Explains statement syntax, with examples")
        print("  /" + self.spaces(18) + "Asks program to draw conclusion")
        print("  /  <statement>" + self.spaces(5) + "Tests  <statement>  as conclusion")
        print(self.spaces(25) + "Note: this can be done even if there are no premises")
    
    def print_syntax(self):
        # rem--"syntax"-- : rem [am] 7960
        self.cls()
        print("Valid statement forms:")
        print("  All    <general term #1>   is/are       <general term #2>")
        print("  Some   <general term #1>   is/are       <general term #2>")
        print("  Some   <general term #1>   is/are not   <general term #2>")
        print("  No     <general term #1>   is/are       <general term #2>")
        print
        print("   <designator>      is/are       <general term>")
        print("   <designator>      is/are not   <general term>")
        print("   <designator A>    is/are       <designator B>")
        print("   <designator A>    is/are not   <designator B>")
        print
        print("Examples:")
        print("  All tall men are Greek gods             The teacher of Plato is wise")
        print("  Some cheese is tasty                    Socrates is not handsome")
        print("  Some cheese is not soft                 The teacher of Plato is Socrates")
        print("  No libertarians are cringing wimps      Socrates is not the teacher of Thales")
        print
        print("Since e.g. 'Socrates is grunch' is ambiguous ('grunch' could be")
        print("either a designator or a general term), the program will try to")
        print("resolve the ambiguity from other uses of the term in the syllogism.")
        print("The indefinite article 'sm' may be used with mass terms in predicates")
        print("(e.g. 'This puddle is sm ink') to ensure that the mass term is taken")
        print("as a general term rather than as a designator.")
    
    def print_info(self):
        # rem---Info--- : rem [am] 8290
        self.cls()
        print("   To use this program, enter a syllogism, one line at a time,")
        print("and  THEN  test conclusions or ask the program to draw a conclusion.")
        print
        print("   A syllogism as (mis)defined here is a (possibly empty) set of")
        print("numbered premises, each of a form specified in the SYNTAX list.")
        print("No term may occur more than twice.  Exactly two terms must occur")
        print("exactly once: these are the two 'end' terms, which will appear in")
        print("the conclusion.  Furthermore, each premise must have exactly one")
        print("term in common with its successor, for some ordering of the premises.")
        print("Example:")
        print("   10 Socrates is a Greek")
        print("   20 All men are mortal")
        print("   30 All Greeks are men")
        print("   40 No gods are mortal")
        print
        print("Note: using a '/' command to draw or test a conclusion does not")
        print("require you to stop.  You can continue, adding or deleting premises")
        print("and drawing and testing more conclusions.")
        print
        print("Reference:  H. Gensler, 'A Simplified Decision Procedure for Categor-")
        print("   ical Syllogisms,' Notre Dame J. of Formal Logic 14 (1973) 457-466.")

    def singularize(self, string):
        # divide by whitespace and remove blank items
        words = filter(None, string.split())
        #words_out = [plurals[word] for word in words if word in plurals.keys()]
        words_out = []
        for word in words:
            word = word.lower()
            if word in plurals.keys():
                words_out.append(plurals[word])
            else:
                if word.endswith('men'):
                    word = word[:-2] + 'an'
                elif word.endswith('s'):
                    if not word.endswith('ss') and not word.endswith('us') and not word.endswith('is') and not word.endswith("'s"):
                        word = word[:-1]
                        if word.endswith('xe'):
                            word = word[:-1]
                        elif word.endswith('ie'):
                            word = word[:-2] + 'y'
                        elif word.endswith('sse') or word.endswith('she') or word.endswith('che'):
                            y = word[:-1]
                words_out.append(word);
        return ' '.join(words_out)

    def show_parse_error_missing_copula(self):
        print("** Missing copula is/are")
        self.show_parse_error_help()
    def show_parse_error_missing_subject_term(self):
        print("** Subject term bad or missing")
        self.show_parse_error_help()
    def show_parse_error_missing_predicate(self):
        print("** Predicate term bad or missing")
        self.show_parse_error_help()
    def show_parse_error_help(self):
        if self.show_messages:
            print("Enter SYNTAX for help with statements")

    def sample_syllogism(self):
        """ Enter a sample syllogism. """
        # 8980 rem--sample--
        self.new_syllogism()
        for line in sample_lines:
            print(line)
            self.scan_line(line)

        if self.show_messages:
            print("Suggestion: try the LINK or LINK* command.")

    def list_lines(self, analyze=False):
        # rem---list--- : rem [am] 7460
        print(self.rubric.p(analyze))

    #def list_premises(self, analyze=False):
    #   for p in self.premise_list:
    #       print p

    def scan_line(self, line):
        """ Cover method to add a line. """
        self.rubric.enter_line(line)

    def new_syllogism(self):
        """ Remove all premises from the rubric. """
        self.rubric.reset()

    def show_error_invalid_cmd(self, i):
        print(self.spaces(spaces) + "^   Invalid numeral or command")


#class Premise:
#   line_num = ''
#   line_txt = ''
#   term_1 = ''
#   term_2 = ''
#   term_1_type = (-1)
#   term_2_type = (-1)
#
#   symbol_strings = []
#   symbol_types = []
#
#   def __init__(self, txt=''):
#       line_num = (-1)
#       line_txt = txt
#       term_1 = ''
#       term_2 = ''
#   
#   def parse_line(self):
#       pass
#
#   def split_line(self):
#       pass
#
#
#   def symbol_string_with_index(self, idx):
#       r = ''
#       if idx < len(symbol_strings):
#           r = symbol_strings[idx]
#       return r
#   
#   def symbol_type_with_index(self, idx):
#       r = ''
#       if idx < len(symbol_types):
#           r = symbol_types[idx]
#       return r

s = SyllogismController()

s = Rubric()
s.enter_line("10 all men are mortal")
s.enter_line("30 all men are mortal")
s.enter_line("30 a no men are mortal")
s.enter_line("401 all men are mortal")
s.enter_line("41 all men are mortal")
s.enter_line("4 all men are mortal")
s.enter_line("4012 all men are mortal")
s.enter_line("50 all men are mortal")

print(s)

#test_line1 = '10 all men are mortal'
#p = Premise(test_line1)

#s.new_syllogism()


#def contains_any(str, set):
#   flag = False
#    for c in set:
#        if c in str:
#           flag = True
#           break
#    return flag
#
#def contains_all(str, set):
#   flag = True
#    for c in set:
#        if c not in str:
#           flag = False
#           break
#    return flag##