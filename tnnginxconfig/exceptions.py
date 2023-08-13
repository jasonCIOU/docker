class ParameterError(Exception):
    """Exception raised for invalid parameters."""
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

class RuleConfigurationError(Exception):
    """Exception raised for errors in rule configurations."""
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)
class TNginxBaseEXception(Exception):
    pass

class TNginxParamError(TNginxBaseEXception):
    """Exception raised for invalid parameters."""
    pass

class RuleEXception(TNginxBaseEXception):
    """Base Exception for rule-specific errors."""
    pass

class RuleExistError(RuleEXception):
    """Exception raised when the rule already exists."""
    pass
