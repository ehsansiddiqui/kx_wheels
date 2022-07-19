# Manual registration
import haystack
from kxwheels.apps.kx.models import WheelSize, TireSize
from kxwheels.apps.kx.indexes import WheelSizeIndex, TireSizeIndex

from kxwheels.apps.vehicle.models import Model
from kxwheels.apps.vehicle.indexes import ModelIndex

haystack.sites.site.register(WheelSize, WheelSizeIndex)
haystack.sites.site.register(TireSize, TireSizeIndex)
haystack.sites.site.register(Model, ModelIndex)
