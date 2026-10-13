import pytest

from src.aplication.exceptions.event_validation_error import EventValidationError


class TestEventValidationError:
    def test_exception_instantiation(self):
        error = EventValidationError("Test error message")
        assert str(error) == "Test error message"

    def test_exception_without_message(self):
        error = EventValidationError()
        assert isinstance(error, Exception)

    def test_exception_is_exception_subclass(self):
        assert issubclass(EventValidationError, Exception)

    def test_exception_can_be_raised(self):
        with pytest.raises(EventValidationError, match="Test error"):
            raise EventValidationError("Test error")

    def test_exception_can_be_caught_as_exception(self):
        try:
            raise EventValidationError("Test error")
        except Exception as e:
            assert isinstance(e, EventValidationError)
            assert str(e) == "Test error"

    def test_exception_docstring(self):
        assert EventValidationError.__doc__ == "Erro quando um evento do e-commerce não atende os requisitos de validação"