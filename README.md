# Aramaki - a federated DevOps control plane

> "Aramaki never engages in direct missions, but offers a great array of
   diplomatic support in return."
>
> [Ghost in the Shell Wiki](https://ghostintheshell.fandom.com/wiki/Daisuke_Aramaki)

## Vision

* Watching your application as it works in its environment
* providing a helpful user interface to put events into context
  and help make sense out of the time line
* allowing a multi-disciplinary team to operate the application and its
  environment and move it to more desirable states

## Problems we want to solve

### It's 3am – someone needs to flush the Varnish cache again

It's 3am and I haven't touched this system/project for a long time. How did that
work in *this* project and did someone just do that already?

Sometimes we need to get people into projects quickly. They need to orient
themselves on a technical and social level:

* What are the rules for things we can touch or we should escalate to someone
  else (internally or externally)?

* Where are the dashboards? Which are relevant?

* Is this thing always broken or did that just happen?

* What has been going on today and in the last days?


### Support workflows from multiple, overlapping perspectives

For example in monitoring: infrastructure teams want performing reviews of thousands of alerts across dozens of projects, application operations teams reviewing other aspects of the same projects, a customer or developer reviewing the monitoring situation of a single project.

### Shall we use my Jira, your Gitlab or her YouTrack?

Allow fine grained customization without having to have a single centralised
instance that requires over-modelling the world and then creating contradicting
situations when handled in multi-tenant scenarios. This is what we think
federation will solve. Also, this should create smaller customer/project
specific systems that are easier to understand and compose.

### Reduce the amount of third party tools

Especially to avoid ending up with an ever-changing cacophony of questionable
license/business strategies that are built for bait-and-switch around selling a product instead of delivering a service.

In our case, we currently want to get rid of Sensu and Consul, as well as
outside monitoring tools.

### Improve communication between project owners, developers, and ops

This is a social problem we want to provide good assistance for. 

One interesting aspect here is that we want to provide regular reviews. We want
to avoid writing reports that aren't read.


## Things we want to avoid

We are dangerously close to second-system-syndrome as well as not-invented-here.
Nevertheless, we thought about this deeply and will integrate with existing
systems where it makes sense, but will implement light-weight solutions reduce
integration complexity where reasonable. Especially we do not want to create a
system that simply is a cacophony of random third party services just cobbled
together.

This is not intended to become a "NoOps" product that solves all social problems. This is intended to implement a form of "cogntive augmentation" for people to cooperate. 

This is about balancing technical and social interactions and providing a way to
integrate them.

This should also not become a closed platform solution. We think that – as a
professional community – we need to get better with new FLOSS projects to find
and support business models that stay open and don't perform switch-and-bait.


## The minimal *viable* product

The minimal viable product will be a mixture between showing the proper foundational technologie with a federated approach and adding a variety of 
specific use cases to get a sense of the landscape and what is needed in
actual situations.

So the major milestones will be:

* a server that can federate with other servers (using websockets)
* an agent that can be asked to perform actions and send observations to its server
* a data model around projects (to be renamed!) that can be interacted with from multiple servers
* have a proper security model for agents, servers and especially around
  federation.

Specific use cases in the beginning:

* monitoring and review (to replace Sensu and Uchiwa)
* alerting
* inventory management
* ticket system integration


# Foundational thoughts

* We want to avoid another platformization approach. We think that – as a
  professional community of developers an operators – we need to get better
  with new FOSS projects to find and support sustainable business models.

* Provide a common technical vocabulary to pull data from many different sources
  into a common, distributed environment. We imagine this data to include
  application events, tickets/issues, information about code and more.

* Consider operating an application to be an effort in the complex domain: it's
  important to discover previously unknown relationships and cooperating from
  multiple perspectives. This is to a large part a social issue that needs to
  be tackled and supported by proper technical solutions(cognitive augmentation
  vs. replacement).

* We consider a mixed audience that includes managers, developers, operators
  where in specific situations the competencies may not be clearly laid out
  along team or people boundaries but are intermingled in interesting ways.

* Create multiple smaller systems that can be customized and adapted easily vs.
  one centralized system.

* We might want to customize operations on a "per system" level and intend to do
  that by providing configuration and code for every system through a
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

* Take inspiration from the ActivityPub/Fediverse approach without implementing
  it as a core technology. See the `REJECTED-IDEAS.md` for details.

* Take inspiration from Domain Driven Design without following their
  implementation ideas 1:1. Also see `REJECTED-IDEAS.md` for details.

* batou showed us that a fractal design (using self-similar structures) can be
  very powerful. The current design considers "Systems" to be a good starting
  point to answer the question "What is the /thing/ we managing here?". Systems
  can have subsystems and can be aggregated. We might want to also use the
  word "Component" somewhere to indicate a leaf where it doesn't get more
  granular.

  (Sub-)Systems can be "remote" or internal and thus federation comes into play.

  I imagine subsystems could be "The Flying Circus Infrastructure" which in turn
  may be split up into data centers and subsystems therein
  ("storage" and "compute").

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

* Systems are aggregated top down, not bottom up: a subsystem doesn't have a parent,
  but systems can aggregated other systems - which in turn means a system can be a 
  subsystem for multiple higher level systems.

  This relationship is intended to make larger, complex systems more manageable.
  Inversely, aggregating a subsystem into a larger system may not cause the
  actual thing the subsystem represent to break! (E.g. adding an environment to
  a project must not - in the general case - cause the application to stop
  working because of e.g. IP addresses changing)

* We also need to be aware to not scale by aggregration, but support scaling by
  decomposition and recombination.

  For example: instead of creating higher order status pages by simply using the
  summary status from a subordinate status page, we should(recursively) provide
  access to both the summary status as well as any intermediate layer data.
