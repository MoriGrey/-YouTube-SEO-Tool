"""
Team Collaboration Module
Manages user roles, shared workspaces, collaboration features, and activity logs.

AGI Paradigm: Contextual Modularity
- Isolated team management with clear interfaces
- Role-based access control
- Activity tracking and audit trails
"""

import os
import json
from typing import Dict, Any, List, Optional
from datetime import datetime
from enum import Enum
from pathlib import Path


class UserRole(Enum):
    """User role enumeration."""
    OWNER = "owner"
    ADMIN = "admin"
    MEMBER = "member"
    VIEWER = "viewer"


class TeamManager:
    """
    Team collaboration manager.
    
    Features:
    - User roles and permissions
    - Shared workspaces
    - Activity logs
    - Collaboration features
    """
    
    def __init__(self, data_dir: Optional[str] = None):
        """
        Initialize team manager.
        
        Args:
            data_dir: Directory for storing team data
        """
        if data_dir is None:
            project_root = Path(__file__).parent.parent.parent
            data_dir = project_root / "data" / "teams"
        
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)
        
        # Permissions mapping
        self.permissions = {
            UserRole.OWNER: ["read", "write", "delete", "manage_users", "manage_workspace"],
            UserRole.ADMIN: ["read", "write", "delete", "manage_users"],
            UserRole.MEMBER: ["read", "write"],
            UserRole.VIEWER: ["read"]
        }
    
    def create_workspace(
        self,
        workspace_name: str,
        owner_username: str,
        description: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Create a new shared workspace.
        
        Args:
            workspace_name: Name of the workspace
            owner_username: Username of the workspace owner
            description: Optional workspace description
        
        Returns:
            Workspace information dictionary
        """
        workspace_id = f"ws_{int(datetime.now().timestamp())}"
        
        workspace = {
            "workspace_id": workspace_id,
            "name": workspace_name,
            "description": description or "",
            "created_at": datetime.now().isoformat(),
            "owner": owner_username,
            "members": {
                owner_username: {
                    "role": UserRole.OWNER.value,
                    "joined_at": datetime.now().isoformat(),
                    "permissions": self.permissions[UserRole.OWNER]
                }
            },
            "settings": {
                "public": False,
                "allow_invites": True
            },
            "activity_log": []
        }
        
        # Save workspace
        workspace_file = self.data_dir / f"{workspace_id}.json"
        with open(workspace_file, "w", encoding="utf-8") as f:
            json.dump(workspace, f, indent=2)
        
        # Log activity
        self._log_activity(workspace_id, owner_username, "workspace_created", {
            "workspace_name": workspace_name
        })
        
        return workspace
    
    def add_member(
        self,
        workspace_id: str,
        username: str,
        role: UserRole = UserRole.MEMBER,
        invited_by: Optional[str] = None
    ) -> bool:
        """
        Add a member to a workspace.
        
        Args:
            workspace_id: ID of the workspace
            username: Username to add
            role: Role to assign
            invited_by: Username who invited (for logging)
        
        Returns:
            True if successful
        """
        workspace = self.get_workspace(workspace_id)
        if not workspace:
            return False
        
        if username in workspace["members"]:
            return False  # Already a member
        
        workspace["members"][username] = {
            "role": role.value,
            "joined_at": datetime.now().isoformat(),
            "permissions": self.permissions[role]
        }
        
        self._save_workspace(workspace)
        
        # Log activity
        self._log_activity(workspace_id, invited_by or username, "member_added", {
            "username": username,
            "role": role.value
        })
        
        return True
    
    def remove_member(
        self,
        workspace_id: str,
        username: str,
        removed_by: str
    ) -> bool:
        """Remove a member from workspace."""
        workspace = self.get_workspace(workspace_id)
        if not workspace:
            return False
        
        if username not in workspace["members"]:
            return False
        
        # Cannot remove owner
        if workspace["members"][username]["role"] == UserRole.OWNER.value:
            return False
        
        del workspace["members"][username]
        self._save_workspace(workspace)
        
        # Log activity
        self._log_activity(workspace_id, removed_by, "member_removed", {
            "username": username
        })
        
        return True
    
    def update_member_role(
        self,
        workspace_id: str,
        username: str,
        new_role: UserRole,
        updated_by: str
    ) -> bool:
        """Update a member's role."""
        workspace = self.get_workspace(workspace_id)
        if not workspace:
            return False
        
        if username not in workspace["members"]:
            return False
        
        # Cannot change owner role
        if workspace["members"][username]["role"] == UserRole.OWNER.value:
            return False
        
        workspace["members"][username]["role"] = new_role.value
        workspace["members"][username]["permissions"] = self.permissions[new_role]
        
        self._save_workspace(workspace)
        
        # Log activity
        self._log_activity(workspace_id, updated_by, "role_updated", {
            "username": username,
            "new_role": new_role.value
        })
        
        return True
    
    def get_workspace(self, workspace_id: str) -> Optional[Dict[str, Any]]:
        """Get workspace by ID."""
        workspace_file = self.data_dir / f"{workspace_id}.json"
        if not workspace_file.exists():
            return None
        
        with open(workspace_file, "r", encoding="utf-8") as f:
            return json.load(f)
    
    def list_workspaces(self, username: Optional[str] = None) -> List[Dict[str, Any]]:
        """List all workspaces, optionally filtered by member."""
        workspaces = []
        
        for workspace_file in self.data_dir.glob("*.json"):
            try:
                with open(workspace_file, "r", encoding="utf-8") as f:
                    workspace = json.load(f)
                
                if username is None or username in workspace["members"]:
                    # Include member count and summary
                    workspace["member_count"] = len(workspace["members"])
                    workspace["activity_count"] = len(workspace.get("activity_log", []))
                    workspaces.append(workspace)
            except Exception:
                continue
        
        return sorted(workspaces, key=lambda x: x["created_at"], reverse=True)
    
    def check_permission(
        self,
        workspace_id: str,
        username: str,
        permission: str
    ) -> bool:
        """Check if user has specific permission in workspace."""
        workspace = self.get_workspace(workspace_id)
        if not workspace:
            return False
        
        if username not in workspace["members"]:
            return False
        
        user_permissions = workspace["members"][username].get("permissions", [])
        return permission in user_permissions
    
    def get_activity_log(
        self,
        workspace_id: str,
        limit: int = 50,
        username: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """Get activity log for workspace."""
        workspace = self.get_workspace(workspace_id)
        if not workspace:
            return []
        
        activities = workspace.get("activity_log", [])
        
        # Filter by username if specified
        if username:
            activities = [a for a in activities if a.get("username") == username]
        
        # Sort by timestamp (newest first) and limit
        activities.sort(key=lambda x: x.get("timestamp", ""), reverse=True)
        return activities[:limit]
    
    def _log_activity(
        self,
        workspace_id: str,
        username: str,
        action: str,
        details: Optional[Dict[str, Any]] = None
    ):
        """Log an activity in workspace."""
        workspace = self.get_workspace(workspace_id)
        if not workspace:
            return
        
        activity = {
            "timestamp": datetime.now().isoformat(),
            "username": username,
            "action": action,
            "details": details or {}
        }
        
        if "activity_log" not in workspace:
            workspace["activity_log"] = []
        
        workspace["activity_log"].append(activity)
        
        # Keep only last 1000 activities
        if len(workspace["activity_log"]) > 1000:
            workspace["activity_log"] = workspace["activity_log"][-1000:]
        
        self._save_workspace(workspace)
    
    def _save_workspace(self, workspace: Dict[str, Any]):
        """Save workspace to file."""
        workspace_id = workspace["workspace_id"]
        workspace_file = self.data_dir / f"{workspace_id}.json"
        
        with open(workspace_file, "w", encoding="utf-8") as f:
            json.dump(workspace, f, indent=2)
    
    def share_channel_data(
        self,
        workspace_id: str,
        channel_handle: str,
        shared_by: str
    ) -> bool:
        """Share channel data with workspace members."""
        if not self.check_permission(workspace_id, shared_by, "write"):
            return False
        
        # Log activity
        self._log_activity(workspace_id, shared_by, "channel_shared", {
            "channel_handle": channel_handle
        })
        
        return True
    
    def get_shared_channels(self, workspace_id: str) -> List[str]:
        """Get list of shared channels in workspace."""
        workspace = self.get_workspace(workspace_id)
        if not workspace:
            return []
        
        # Extract shared channels from activity log
        shared_channels = []
        for activity in workspace.get("activity_log", []):
            if activity.get("action") == "channel_shared":
                channel = activity.get("details", {}).get("channel_handle")
                if channel and channel not in shared_channels:
                    shared_channels.append(channel)
        
        return shared_channels

