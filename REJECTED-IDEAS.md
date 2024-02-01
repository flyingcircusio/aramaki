# Rejected ideas

## Basing this off directly on top of ActivityPub

We considered basing this on ActivityPub-related technology. However, latching
onto an existing federation standard makes discovering the space that we want
to solve very hard and we're opting to be inspired by ActivityPub and take the
good things but keep it separate for now.

A major aspect is that implementing a federated system intended for public
consumption of the APIs means that things quickly need to be set in stone. We
don't want that for now and thus we can take inspiration but purposely do not
strive for interoperability on any level.

We may end up creating a specific way of interacting with the fediverse but that
isn't part of the core design.

## Making a perfect DDD implementation

We searched for a scalable software architecture that is Pythonic and allows us
to have compact code but also flexibility. We tried finiding a "Pythonic DDD"
approach that reduces boilerplate and increases the expressiveness of the
Domain Model. This was done at an experimental stage where ActivityPub as a core
technology was on the plate.

There is no general "yes"/"no" answer to the overall outcome, but we are not
striving for a perfect DDD implementation, but taking away a few keypoints.

* Simplify code by explicitly choosing some integrations to be "integral" to the
  domain language, like SQLAlchemy and ActivityPub - to avoid too many layers
  and ripping apart things that want to be discussed in the "ubiquitous
  language" naturally.

  SQLAlchemy's declarative base is an example here. We're considering to also
  use a mix-in for objects that are aware of ActivityPub so that objects can
  easily say things like

    def use(self, other):
    	subsystem = Subsystem.create(system=self, id=other)
    	self.publish(type="Use", object=subsystem)

  Mix-ins are a sharp tool and should be used sparely. However, we investigated
  a balanced design here with the experience of Zope 2 (everything's a mixin!)
  and Zope 3 (everything is disconnected and needs to be wired up explicitly).

  So, we're talking about potentially using mix-ins when a decision was made to
  include something in the ubuiqitous language of the domain.

* Find a simplified/unified way to expose dependency injection, configuration,
  UoW/Transaction management, event handling, consistency boundaries/conflict
  domains. We call this "the context".

  A context can represent an instance of an application. This makes
  multi-tenancy interesting while overlapping with external config
  (like different database instances per tenant) and also seems interesting to
  help testing distributed systems in a simplified unit test environment
  without spawning myriads of actual processes.

* We are currently trying to simplify by folding the DomainModel and the Service
  Layer together. If "sometimes a thing isn't a thing" is true, then maybe it's
  also OK to be on another thing?

* We want to avoid a code structure where everything is grouped by "book colour"
  but focus the code on the domain model and then arrange contextual things
  around it.

* The discussion around "aggregates" and repositories (as discussed internally,
  with friends and by going over and over the Cosmic Python book as well as the
  DDD red book) keeps going back to "it's a tradeoff". However, it feels like
  this ominous trade-off causes people to freeze up, being afraid to make a bad
  decision that is hard to adjust later on. We've also seen that this seems to
  push designs to so called anemic domains moving most logic into a very simple
  service layer and the repository.

* The discussion around repositories is also unclear, as the decision between a
  collection oriented or a persistance oriented model seems to be driven by the
  choice of the backend technologie it seems like this distinction doesn't buy
  the flexibility that DDD aims for and then we feel like we never had to
  actually switch (suddenly) from a SQLAchemy based storage to a MongoDB
  storage. It actually seems more flexible to use SQLAlchemy and in the worst
  case implement a SQLAlchemy dialect for that ...

* We currently think about a compacted layering like this:

  * Domain: Objects (Models) and Services (which can be class or instance
    methods on models or in modules). They do not directly link or import
    things that are "in the environment" but restrict themselves to speaking
    the "ubuiqitous language".

  * Application Context: a pseudo-singleton object that helps assemble the
    application structure as well as configure application instances. This
    drives persistenc and transactions, event handling and any services where
    the domain talks to the outside world.

  * UI/API: lets the outside world talk with your application. They bootstrap
    specific application contexts and bridge outside requests to the domain
    using the context.

* We discovered that events can be used in an interesting way. As their main
  job is to allow crossing aggregate boundaries and thus transaction borders
  (and thus help reduce lock contention on the database) we can implement
  them in a two-phase approach (currently using `yield`). The first phase of
  an event still has access to the original transaction and thus to live
  objects from the original aggregate. This can be used to construct a local
  context and retrieve data from the aggregate. After yielding the original
  transaction can commit and every event then gets called again. The event
  can now use the local data from the first phase (but not the original live
  objects as they have now lost their state) and is run in a fresh
  transaction for each event.

  This helps writing more compact event handlers that still allow to manage
  transaction boundaries with the desired properties.

  Example:

  	@context.handle("my-event")
  	def send_mail_about_event(order):
  		from = f"{order.seller.name} <{order.seller.email>}"
  		to = order.customer.email
  		subject = f"We want to inform you about about your order {order.id}"
  		body = "..."
  		yield
  		context.mail.send(to=to, from=from, subject=subject, body=content)

  A third option here is to also allow events to be run in an asynchronous fashion. However,
  yield does not help here as we would

  A unified approach could mean that we declare event handlers like

* We want to avoid spreading code out and creating duplicate data structures today
  if its unclear whether the separat

  Python is generally flexible enough to rework certain aspects quickly in the
  future. And tools like SQLAlchemy are flexible enough to adjust them to
  certain surprises or outside requirements with good precision.

  Also, in the DDD community everybody seems to have their own preferences
  where certain trade-offs lie. Our preference is to not turn a Python
  application into a Java application.

  One danger here is that we end up designing or working with a data model instead
  of a domain model.


## UI / Tech stack

* We investigated various frontend/backend combinations and thought 
  a reactive UI based on svelte + a data driven API would be best. After
  playing with this and then discovering htmx/hyperscript and reading
  through the (hypermedia systems book)[https://hypermedia.systems/] we
  decided to go down that route.
