from enum import Enum

class UserRole(str, Enum):
    ADMIN = "admin"
    REVIEWER = "reviewer"
    ANALYST = "analyst"
    VIEWER = "viewer"