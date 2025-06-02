from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor, ConsoleSpanExporter

resource = Resource.create(attributes={
    SERVICE_NAME: "token-tracker-service"
})

# create tracer engine
tracerProvider = TracerProvider(resource=resource)
# init span processor that will send batch of traces to an endpoint (for now use console)
processor = BatchSpanProcessor(span_exporter=ConsoleSpanExporter())
tracerProvider.add_span_processor(span_processor=processor)

# hook everything up to enable tracing globally
trace.set_tracer_provider(tracer_provider=tracerProvider)