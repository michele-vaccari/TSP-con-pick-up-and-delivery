from __future__ import annotations
from abc import ABC, abstractmethod

class Observer(ABC):
    """
    The Observer interface declares the update method, used by subjects.
    """

    @abstractmethod
    def new_solution_found(self, subject: Subject) -> None:
        pass

    @abstractmethod
    def new_best_solution_found(self, subject: Subject) -> None:
        pass

class Subject(ABC):
    """
    The Subject interface declares a set of methods for managing subscribers.
    """

    @abstractmethod
    def attach(self, observer: Observer) -> None:
        """
        Attach an observer to the subject.
        """
        pass

    @abstractmethod
    def detach(self, observer: Observer) -> None:
        """
        Detach an observer from the subject.
        """
        pass

    @abstractmethod
    def notify_new_solution(self) -> None:
        """
        Notify all observers about an event.
        """
        pass

    @abstractmethod
    def notify_best_new_solution(self) -> None:
        """
        Notify all observers about an event.
        """
        pass