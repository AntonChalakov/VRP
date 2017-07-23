from .states.TenantState import TenantState
from .states.TechnicianState import TechnicianState
from .states.SpectatorState import SpectatorState
from .states.OperatorState import OperatorState
from . import message

STATE_FACTORY = {
		message.ROLES.TENANT:     TenantState,
		message.ROLES.TECHNICIAN: TechnicianState,
		message.ROLES.SPECTATOR:  SpectatorState,
		message.ROLES.OPERATOR:   OperatorState
}
