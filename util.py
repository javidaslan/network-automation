#######################################################################
#                                                                     #
# This python module contains useful functions for different purposes #
#                                                                     #
#######################################################################

import textfsm
import os

def loadTemplate(template_file_path, input_string):
    ''' Creates a list of dictionaries from a TextFSM template.
    
    Keyword Arguments:
    template_file_path -- the file path to the desired TextFSM template
    input_string -- the string that should be used to base the dictionary on
    '''
    with open(str(os.path.dirname(os.path.abspath(__file__))) + '/' + template_file_path) as template:
        temp = textfsm.TextFSM(template)
        parsed_list = temp.ParseText(input_string)
        return_list = []
        for item in parsed_list:
            temp_dict = {}
            for i in range(len(temp.header)):
                temp_dict[temp.header[i]] = item[i].strip() if type(item[i]) is str else item[i]
            return_list.append(temp_dict)
    return return_list
