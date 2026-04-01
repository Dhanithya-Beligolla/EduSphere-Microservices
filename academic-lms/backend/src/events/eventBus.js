const EventEmitter2 = require('eventemitter2');

const eventBus = new EventEmitter2({
  wildcard: true,
  delimiter: '.',
  maxListeners: 20,
});

// Log all events in development
if (process.env.NODE_ENV === 'development') {
  eventBus.onAny((event, value) => {
    console.log(`📡 [Event] ${event}`, JSON.stringify(value, null, 2));
  });
}

module.exports = eventBus;
