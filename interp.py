import re
from collections import OrderedDict 

#########################
# Example input:
# x_1=2;y_2=x_1;
#
# PLEASE ENTER INPUT AS SINGLE STREAM OF CHARACTERS.
#
# PLEASE DO NOT INCLUDE SPACES (WHITE SPACE) IN THE INPUT!
#########################

class Token(object):
    def __init__(self, type, value):
        self.type = type
        self.value = value


class Interpreter(object):
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.current_token = None
        self.current_char = self.text[self.pos]
        self.symbolDict = []

    # Helper method for verifying if an identifier
    # was already previously initialized.
    def checkSymbolDict(self, valueInput):
      booleanValue = False
      for i in range(len(self.symbolDict)):
        if str(self.symbolDict[i][0]) == valueInput:
          booleanValue = True
      
      return booleanValue

    # Output the symbolDictionary.
    def output(self):
      for i in range(len(self.symbolDict)):
        for j in range(len(self.symbolDict[i])-1):
          print(str(self.symbolDict[i][j]) + " = " + str(self.symbolDict[i][j+1]))

    # Increment the text character counter.
    def nextPos(self):
        self.pos += 1
        if self.pos > len(self.text) - 1:
            self.current_char = None
        else:
            self.current_char = self.text[self.pos]

    def error(self, text):
        raise Exception(text)

    # Helper method for determining if character is a letter.
    def isLetter(self, character):
      if (re.search("[_*a-zA-Z]", character)):
        return True
      else:
        return False

    # Return lexeme as an identifier if valid.
    def Identifier(self, char):
      result = ''
      while self.pos < len(self.text) - 0:
        if not self.isLetter(self.text[self.pos]) and not self.text[self.pos].isdigit():
          break

        result = result + self.text[self.pos]
        self.nextPos()

      return str(result)

    def isLiteral(self, text):
      if (re.search("^0?[1-9]+", text)):
        return True
      else:
        return False 
    
    def integer(self):
        """Return a (multidigit) integer consumed from the input."""
        result = ''
        while self.current_char is not None and self.current_char.isdigit():
            result = result + self.current_char
            self.nextPos()
        return result

    # Find (and create an instance of) the next token based on
    # the current character.
    def find_next_token(self):
        text = self.text

        if self.pos > len(text) - 1:
            return Token('EOF', None)

        if self.current_char.isdigit():
            x = self.integer()
            token = Token('INTEGER', x)

            # Modify the last appended list element with the accepted digit value
            #self.a[len(self.a)-1][1] = int(self.current_char)
           # self.nextPos()
            return token

        g = self.Identifier(self.current_char)
        if g:
            token = Token('IDENTIFIER', g)
      
            return token

        if self.current_char == '+':
            token = Token('PLUS', self.current_char)
            self.pos += 1
            return token
        
        if self.current_char == '=':
            token = Token('EQUALS', self.current_char)
            self.nextPos()
            return token
        
        if self.current_char == ';':
            token = Token('SEMI', ';')
            self.nextPos()
            return token

        self.error()

    # Helper method for retrieving the instantiated token(s).
    def fetch_next_token(self, token_type):
        if self.current_token.type == token_type:
            self.current_token = self.find_next_token()
        else:
            self.error('Error fetching token')

    # Parse the token(s) in expected order and throw
    # error exceptions as neccesary.
    def parse(self):
        self.current_token = self.find_next_token()

        while self.current_token.type is not 'EOF':
          identifier = self.current_token
          if identifier.type is not 'IDENTIFIER':
            self.error('Expected an <IDENTIFIER>')
            break
          else:
           # Un-comment for debugging purposes. 
           # print(identifier.value)
           
            self.symbolDict.append([identifier.value,str(0)])
            self.fetch_next_token('IDENTIFIER')

          operation = self.current_token
          if operation.type is not 'EQUALS':
            self.error('Expected an <EQUALS>')
            break
          else:
            self.fetch_next_token('EQUALS')

          rhs = self.current_token
          if rhs.type is not 'INTEGER':
            if rhs.type is 'IDENTIFIER':
              if self.checkSymbolDict(rhs.value):
                self.symbolDict[len(self.symbolDict)-1][1] = str(self.symbolDict[len(self.symbolDict)-2][1])
                self.fetch_next_token('IDENTIFIER')
                break
              else:
                self.error(rhs.value + " not initialized.")
            self.error('Expected an <INTEGER>')
            break
          else:
            if self.isLiteral(rhs.value):
              self.symbolDict[len(self.symbolDict)-1][1] = str(rhs.value)
              self.fetch_next_token('INTEGER')
            else:
              self.error('Expected an <LITERAL>')

          semi = self.current_token
          if semi.type is 'EOF':
            self.error('Expected a <SEMI>')
            break
          else:
            self.fetch_next_token('SEMI')
        
        return 


def main():
    while True:
        try:
            text = input('> ')
        except EOFError:
            break
        if not text:
            continue
        interpreter = Interpreter(text)
        interpreter.parse()
        interpreter.output()


if __name__ == '__main__':
    main()
