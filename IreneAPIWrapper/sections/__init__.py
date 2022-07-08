from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from ..models import IreneAPIClient
    from ..models import CallBack


class InteractiveClient:
    def __init__(self):
        self.client: Optional[IreneAPIClient] = None


outer = InteractiveClient()
