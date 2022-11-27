> WARNING - THIS IS NOT PRODUCTION CODE BUT SCIENCE FICTION!

> "Aramaki never engages in direct missions, but offers a great array of
   diplomatic support in return."
>
> [Ghost in the Shell Wiki](https://ghostintheshell.fandom.com/wiki/Daisuke_Aramaki)

## Aramaki creates a timeline ...

by watching your application as it works in its environment

## ... and helps your team discover interesting stories about your application ...

by providing a helpful user interface to put events into context and help them
make sense out of the timeline

## ... to move it forward.

by allowing your team to operate your application and its environment and move
it to a more desirable state.

# Stories that brought us here

## Monitoring

## It's 7am, someone needs to flush the cache again!

## Shall we use my Jira, your Redmine or her YouTrack?

 	-> projektspezifische, kleine lösungen mit hohem kooperationsgrad (hohe wirksamkeit) und zentrale team-spezifische ansätze (hohe effizienz) verheiraten

		-> custom code in einem zentralisiertem system

		-> ein zentrales system das an komplexität immer weiter wächst (overmodelling)

		-> unterschiedlichste leute und dynamik die sich in diesem ding zurecht finden müssen -> lieber kleinere systeme die für den jeweiligen kontext zugeschnitten sind

		-> aber trotzdem für einzelne teams auch wieder effiziente zentrale workflows unterstützen


## Feature Toggles

	entkoppeln von software-deployen und wann dann irgenwelches verhalten sich ändert.

	produktleute sollen selber das feature-toggle bedienen (in staging oder production)

	das ist halt relevant, weil wenn neue software-deployt ist dann gilt das neue verhalten, also marker ins grafana, dass sich da was geändert haben könnte

	-> das müsste an den toggle geknöpft werden

	und dann will man halt den zusammenhang wieder herstellen können

	und produkt-leute müssten für ein deployment das ergebnis-diff lesen könnnen

	wenn production deployment ist dann muss jmd von der technik, d.h. "nur zwischen 4 und 6" deployen
		-> das kann man dann mit lokalem code natürlich auch codifizieren dass das nicht geht, bzw. ein "in case of emergency" braucht

	-> feature-togglen ist das neue deployen (und braucht ähnliche regeln) und kann auch sein dass ein rollback nicht geht


## It's 3am and I haven't touched this system for a long time

Sometimes we need to get people into projects quickly. They need to orient
themselves on a technical and social level:

* What are the rules for things we can touch or we should escalate to someone
  else (internally or externally)?

* Where are the dashboards? Which are relevant?

* Is this thing always broken or did that just happen?

* What has been going on today and in the last days?

## Monthly reports

Big effort to write, hard to read, time not spent on coming up with a shared
understanding.

	-> UI für so ein Dreigestirn bei dem man kontextspezifisch und für alle Rollen Informationen gemeinsam aufbereiten kann und eine "Geschichte" des Ops-Ablaufs
	erzählen kann.

## Make vs. Buy

## I see your "NoOps" and raise you a "The Cloud is just someone else's computer"

Balancierte Kombination aus sozialer und technischer Interaktion -> neue Klasse
von werkzeugen

-> kein "noops"

-> dieses "devops" produkt löst das problem

-> sondern etwas um beides zu balancieren und zu integrieren

-> you always want to build everything yourselves
	-> well YOU always want to buy a product!


# The minimal viable product

We're currently still searching for the MVP feature set. We could go down the
route of implementing the foundational technologies (like ActivityPub, status
pages, issue management, the agent, encryption/authentication, federation and
some integrations for monitoring, ticket systems, chat and fediverse) and use
this stealthily as a replacement for our customer portal. We could then use this
to go deeper into the Aramaki vision based on the actual content we see and the
way that people interact with it.

Or we could try to identify a different MVP feature set that focuses on the
vision first. This is potentially too shallow as we wouldn't have sufficient
data that people can use and get excited about.

My personal preference would be to work in "open stealth" on the technology
first and then turn into a new mode of working that dives deeper into the
social aspects.


# Foundational thoughts

* We want to avoid another platformization approach. We think we as a community
  need to get better with new free/libra/open source projects and find
  and support business models that support open

* Provide a common technical vocabulary to pull data from many different sources
  into a common, distributed environment. We imagine this data to include
  application events, issues,

* Consider operating an application to be an effort in the complex domain:
  discover of previously unknown relationships and cooperation from multiple
  perspectives is important. This is to a large part a social issue that needs
  to be tackled and supported by proper technical solutions
  (cognitive augmentation vs. replacement).

* We consider a mixed audience that includes managers, developers, operators
  where in specific situations the competencies may not be clearly laid out
  along team or people boundaries but are intermingled in interesting ways.

* Support a federated approach (using ActivityPub) to help creating fractal
  remixes of your data into different contexts and create different stories for
  different teams and combinations of teams.

* We want to customize operations on a "per system" level and intend to do that
  by providing configuration and code for every system through a
  (Git) repository that tracks the history of the project's config (and could
  thus be re-integrated into the system's timeline itself).

  This customization could allow to distribute certain policy decisions
  (which has been a foundational aspect of designing systems for a long time)
  and providing an overall system that has "building block" characteristics.

  Instead of creating an overly complicated module in our centralized system on
  how to schedule maintenances, we could simply defer this to the customer's
  instance and he can choose to use one of the pre-made policies (which can be
  simplified from the current approach by providing multiple simple versions)
  or roll his own. This would not complicate our centralized code base which
  could quickly become too complicated (even when trying to make those things more
  pluggable and use a local "strategy" pattern we would still need to make changes
  to a centralized system which may not be possible in a timely manner and thus
  becoming an unnecessary contention point for users).

* A distributed system would also allow different customers to run different
  versions of the same plugin instead of running into the NxM problem. If a
  customer needs an old version of a ticket system plugin then it's fine if he
  runs that in his instance and others run newer versions on their instances.

* On top of the federated instance model we provide agents that that can perform
  specific tasks within a system. Agents might be interacting with messages
  from federated instances as well.

* We imagine an open, federated network that allows to assemble systems by using
  other systems in interesting ways, but also have sufficient capabilities to
  manage and recognize (temporary) trust between actors in a highly secure
  fashion.

* The fediverse technologies (ActivityPub and friends) appear to be an
  interesting approach to tackle this mixed social and technical challenge.

* batou showed us that a fractal design (self-similar structures) can be very
  powerful. The current design considers "Systems" to be a good starting point
  to answer the question "What is the /thing/ we managing here?". The can have
  subsystem and thus provide self-similarity. We might want to also use the
  word "Component" somewhere to indicate a leaf where it doesn't get more
  granular.

  Subsystems can be "remote" or internal and thus federation comes into play.
  I imagine subsystems could be "The Flying Circus Infrastructure" which in
  turn may be split up into data centers and subsystems therein ("storage" and "compute").

  This would help automatically routing certain information (there's a problem
  with this storage, but you only get to see messages about that fact if you
  use the actual affected systems.)

  We could also use multiple aggregate systems like: all subsystems from this
  data center versus all subsystems that are storage systems in all data
  centers. "Simple" aggregates might be useful to not require individual
  repositories to manage them but could be defined in one repository that
  ends up "generating" multiple aggregates dynamically.

  An interesting detail is whether those "anemic" aggregates may generate their
  own data in case that users might be subscribed to the smallest systems
  ("storage in this data center") and thus could miss notifications from the
  aggregates that might be relevant to them but do not fit the granularity of
  either subsystem.

  I decided to go with "System" after reading
  http://sysarch.pbworks.com/w/page/7241231/FrontPage#EverySystemConsistsofSubsystems
  again.

  * We also need to be aware to not scale by aggregration, but support scaling
    by decomposition and recombination.

    For example: instead of creating higher order status pages by simply using
    the summary status from a subordinate status page, we should
    (recursively) provide access to both the summary status as well as any
    intermediate layer data.

* We are currently searching for a scalable software architecture that is
  Pythonic and allows us to have compact code but also flexibility. We are
  trying to find a "Pythonic DDD" approach that reduces boilerplate and
  increases the expressiveness of the Domain Model. This is at an experimental
  stage at the moment, specifically around questions like:

  * Simplify by explicitly choosing some integrations to be "integral" to the
    domain language, like SQLAlchemy and ActivityPub - to avoid too many layers
    and ripping apart things that want to be discussed in the "ubiquitous
    language" naturally.

    SQLAlchemy's declarative base is an example here. We're considering to
    also use a mixin for objects that are aware of ActivityPub so that
    objects can easily say things like

	    def use(self, other):
	    	subsystem = Subsystem.create(system=self, id=other)
	    	self.publish(type="Use", object=subsystem)

    Mixins are a sharp tool and should be used sparely. However, we're
    investigating a balanced design here with the experience of Zope 2
    (everything's a mixin!) and Zope 3 (everything is disconnected and needs to
    be wired up explicitly).

    So, we're talking about potentially using mixins when a decision was made to
    include something in the ubuiqitous language of the domain.

  * Find a simplified/unified way to expose dependency injection, configuration,
    UoW/Transaction management, event handling, consistency boundaries/conflict
    domains. We call this "the context".

    A context can represent an instance of an application. This makes
    multi-tenancy interesting while overlapping with external config
    (like different database instances per tenant) and also seems interesting
    to help testing distributed systems in a simplified unit test environment
    without spawning myriads of actual processes.

  * We are currently trying to simplify by folding the DomainModel and the
    Service Layer together. If "sometimes a thing isn't a thing" is true, then
    maybe it's also OK to be on another thing?

  * We want to avoid a code structure where everything is grouped by "book
    colour" but focus the code on the domain model and then arrange contextual
    things around it.

  * The discussion around "aggregates" and repositories (as discussed
    internally, with friends and by going over and over the Cosmic Python book
    as well as the DDD red book) keeps going back to "it's a tradeoff".
    However, it feels like this ominous trade-off causes people to freeze up,
    being afraid to make a bad decision that is hard to adjust later on. We've
    also seen that this seems to push designs to so called anemic domains
    moving most logic into a very simple service layer and the repository.

  * The discussion around repositories is also unclear, as the decision between
    a collection oriented or a persistance oriented model seems to be driven by
    the choice of the backend technologie it seems like this distinction
    doesn't buy the flexibility that DDD aims for and then we feel like we
    never had to actually switch (suddenly) from a SQLAchemy based storage to a
    MongoDB storage. It actually seems more flexible to use SQLAlchemy and in the
    worst case implement a SQLAlchemy dialect for that ...

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
