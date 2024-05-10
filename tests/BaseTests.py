from abc import ABC, abstractmethod
from typing import Union

class IndependentTest(ABC):
  @abstractmethod
  def test(self, message: str) -> bool:
    assert False, "This method must be implemented in a subclass"

class DependentTest(ABC):
  @abstractmethod
  def test(self, message: str, previous_messages: list[str]) -> bool:
    assert False, "This method must be implemented in a subclass"

class GameTest(ABC):
  @abstractmethod
  def test(self, message_history: list[str]) -> bool:
    assert False, "This method must be implemented in a subclass"


TestType = Union[IndependentTest, DependentTest, GameTest]