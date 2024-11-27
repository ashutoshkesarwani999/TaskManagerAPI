project/
├── core/
│   ├── __init__.py
│   ├── security/
│   │   ├── __init__.py
│   │   ├── permissions.py      # Permission enums and base classes
│   │   ├── rbac.py            # RBAC configuration and checker
│   │   └── dependencies.py     # Security dependencies
│   └── config/
│       └── rbac_config.py      # RBAC configuration
└── app/
    ├── __init__.py
    ├── api/
    │   └── v1/
    │       ├── tasks.py        # Uses the permission checker
    │       └── users.py
    └── services/
        └── task_service.py


from enum import Enum
from typing import Dict, List, Set, Optional
from pydantic import BaseModel
from fastapi import HTTPException, Security
from fastapi.security import OAuth2PasswordBearer

class Permission(str, Enum):
    CREATE_TASK = "create_task"
    READ_TASK = "read_task"
    UPDATE_TASK = "update_task"
    DELETE_TASK = "delete_task"
    ASSIGN_TASK = "assign_task"
    MANAGE_USERS = "manage_users"
    VIEW_ANALYTICS = "view_analytics"
    MANAGE_ROLES = "manage_roles"
    ARCHIVE_TASK = "archive_task"
    MANAGE_TAGS = "manage_tags"

class Role(str, Enum):
    SUPER_ADMIN = "super_admin"
    ADMIN = "admin"
    MANAGER = "manager"
    TEAM_LEAD = "team_lead"
    MEMBER = "member"
    VIEWER = "viewer"

class RolePermissions(BaseModel):
    role: Role
    permissions: Set[Permission]
    description: str


class RBACConfig:
    def __init__(self):
        self.role_permissions: Dict[Role, Set[Permission]] = {
            Role.SUPER_ADMIN: {p for p in Permission},
            Role.ADMIN: {
                Permission.CREATE_TASK,
                Permission.READ_TASK,
                Permission.UPDATE_TASK,
                Permission.DELETE_TASK,
                Permission.ASSIGN_TASK,
                Permission.MANAGE_USERS,
                Permission.VIEW_ANALYTICS,
                Permission.ARCHIVE_TASK,
                Permission.MANAGE_TAGS
            },
            Role.MANAGER: {
                Permission.CREATE_TASK,
                Permission.READ_TASK,
                Permission.UPDATE_TASK,
                Permission.ASSIGN_TASK,
                Permission.VIEW_ANALYTICS,
                Permission.ARCHIVE_TASK,
                Permission.MANAGE_TAGS
            },
            Role.TEAM_LEAD: {
                Permission.CREATE_TASK,
                Permission.READ_TASK,
                Permission.UPDATE_TASK,
                Permission.ASSIGN_TASK,
                Permission.ARCHIVE_TASK
            },
            Role.MEMBER: {
                Permission.CREATE_TASK,
                Permission.READ_TASK,
                Permission.UPDATE_TASK
            },
            Role.VIEWER: {
                Permission.READ_TASK
            }
        }

    def get_role_permissions(self, role: Role) -> Set[Permission]:
        return self.role_permissions.get(role, set())

    def has_permission(self, role: Role, permission: Permission) -> bool:
        return permission in self.role_permissions.get(role, set())


from functools import wraps
from fastapi import Depends, HTTPException, status
from typing import List, Callable

class PermissionChecker:
    def __init__(self, required_permissions: List[Permission]):
        self.required_permissions = required_permissions
        self.rbac_config = RBACConfig()

    async def __call__(self, current_user: User = Depends(get_current_user)):
        for permission in self.required_permissions:
            has_permission = any(
                self.rbac_config.has_permission(role, permission)
                for role in current_user.roles
            )
            if not has_permission:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail=f"Permission denied: {permission}"
                )
        return current_user

def require_permissions(permissions: List[Permission]) -> Callable:
    return Depends(PermissionChecker(permissions))

# Usage example
@router.post("/tasks/")
async def create_task(
    task: TaskCreate,
    user: User = require_permissions([Permission.CREATE_TASK])
):
    # Implementation
    pass
