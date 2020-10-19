import re

def convert_list_to_string(org_list, seperator=' '):
    """ Convert list to string, by joining all item in list with given separator.
        Returns the concatenated string """
    return seperator.join(org_list)

def extract_all_numbers_from_a_string(the_string):
    theNumber = ''

    for word in the_string.split():
        for character in list(word):
            if character.isdigit():
                theNumber = theNumber + str(character)
    
    if theNumber == '': return the_string
    return theNumber

def extract_float_number_from_a_string(the_string):
    value = re.findall("\d+\.\d+", the_string)
    return value[0]

def set_not_Given_on_empty_strings(list_of_Attributes):
    for i in range (0,len(list_of_Attributes),1):
        if list_of_Attributes[i]== '':
            list_of_Attributes[i]= 'Not Given'        
    return list_of_Attributes  