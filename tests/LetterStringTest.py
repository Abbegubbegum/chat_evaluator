import re
from typing import List, Tuple, Union
from .BaseTests import MessageTest

format_regex = r"^\"?(\w+) - (\w+)\"?$"

class FormatTest(MessageTest):
  def test(self, message: str, previous_messages: list[str]) -> bool:
    return re.match(format_regex, message) is not None
  
class LetterStringGrow(MessageTest):
  def test(self, message: str, previous_messages: list[str]) -> bool:
    parsed_message = parse_message(message)

    if parsed_message is None:
      return False

    if len(previous_messages) == 0:
      return len(parsed_message[1]) == 1

    parsed_previous_message = parse_message(previous_messages[-1])
    
    if parsed_previous_message is None:
      return False

    return len(parsed_message[1]) == len(parsed_previous_message[1]) + 1
  
class LetterStringExistsInWord(MessageTest):
  def test(self, message: str, previous_messages: list[str]) -> bool:
    parsed_message = parse_message(message)

    if parsed_message is None:
      return False

    return parsed_message[1] in parsed_message[0]
  
class WordHasNotBeenUsed(MessageTest):
  def test(self, message: str, previous_messages: list[str]) -> bool:
    parsed_message = parse_message(message)

    if parsed_message is None:
      return False
    
    parsed_previous_messages = [parse_message(previous_message) for previous_message in previous_messages]

    parsed_previous_messages = [previous_message for previous_message in parsed_previous_messages if previous_message is not None]

    return all(parsed_message[0] not in previous_message[0] for previous_message in parsed_previous_messages)

class CheaterAssessement(MessageTest):
  def __init__(self) -> None:
    super().__init__()
    self.other_tests: List[MessageTest] = [LetterStringGrow(), LetterStringExistsInWord(), WordHasNotBeenUsed()]

  def test(self, message: str, previous_messages: list[str]) -> bool:
    parsed_message = parse_message(message)
    
    if len(previous_messages) == 0:
      return parsed_message is not None

    passed_other_tests = all(other_test.test(previous_messages[-1], previous_messages[:-1]) for other_test in self.other_tests)


    return passed_other_tests if parsed_message is not None else not passed_other_tests 



def parse_message(message: str) -> Union[Tuple[str, str], None]:
  message_match = re.match(format_regex, message)

  return (message_match.group(1), message_match.group(2)) if message_match is not None else None