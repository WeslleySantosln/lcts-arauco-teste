from enum import Enum


class DriverStatus(str, Enum):
    AVAILABLE = "available"
    ON_TRIP = "on_trip"
    RESTING = "resting"
    INACTIVE = "inactive"


class TruckStatus(str, Enum):
    AVAILABLE = "available"
    LOADING = "loading"
    IN_TRANSIT = "in_transit"
    UNLOADING = "unloading"
    MAINTENANCE = "maintenance"
    STOPPED = "stopped"


class DeliveryStatus(str, Enum):
    CREATED = "created"
    PLANNED = "planned"
    LOADING = "loading"
    IN_TRANSIT = "in_transit"
    DELIVERED = "delivered"
    DELAYED = "delayed"
    CANCELED = "canceled"


class LogisticsEventType(str, Enum):
    DELIVERY_CREATED = "delivery_created"
    DELIVERY_PLANNED = "delivery_planned"
    LOADING_STARTED = "loading_started"
    LOADING_FINISHED = "loading_finished"
    DEPARTED_ORIGIN = "departed_origin"
    IN_TRANSIT_UPDATE = "in_transit_update"
    STOP_STARTED = "stop_started"
    STOP_FINISHED = "stop_finished"
    ARRIVED_CUSTOMER = "arrived_customer"
    UNLOADING_STARTED = "unloading_started"
    UNLOADING_FINISHED = "unloading_finished"
    DELIVERY_COMPLETED = "delivery_completed"
    DELAY_REGISTERED = "delay_registered"
    OCCURRENCE_REGISTERED = "occurrence_registered"


class OccurrenceType(str, Enum):
    TRAFFIC = "traffic"
    WEATHER = "weather"
    MECHANICAL_FAILURE = "mechanical_failure"
    CUSTOMER_QUEUE = "customer_queue"
    ACCIDENT = "accident"
    DOCUMENT_ISSUE = "document_issue"
    ROUTE_DEVIATION = "route_deviation"


class OccurrenceSeverity(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"