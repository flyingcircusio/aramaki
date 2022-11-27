
# Architecture-related

* implement async event handlers (internal async + redis)

* clean up the context management classes. we already tried that once, however,
  the current event handling code is ugly, but cleaning it up in a generic
  fashion made our heads explode and we never ended up with working code when
  trying to make it a composite structure.

  It's interesting the way it is right now, but it also feels yuck, not yum.

* consider extracting the "meta" code into a separate package

# Business

* invoicing?

# Open Source / Community

see foundational notes, plugins are an obvious thing, however, I'd like
to also use the federation approach to help people cooperate on stuff

# Security

* "In case of emergency" commands with offline signatures

* Browser-based strong authentication with yubikeys that also provide
  signed "session keys" that can impersonate the use for a while.


# Other Features that could be interesting for MVP mass

* implementing federated "announcements" (current incidents, planned maintenances)

* implementing a way to automate maintenance response: "The FCIO wants to
  perform maintenance on this VM, when would be a good time?"

  We currently implement this in our centralized config management database.
  However, the use cases are becoming more and more specialized and it's way
  too

* federated uptime testing ("can someone poke URL XYZ every now and then?
  thanks, my friends!")

  this could also be implemented with a "token" system where we avoid "leeching".
  a point system or a ratio system (like in traditional FTP sites) could be
  relevant here.

* inventory management (disk tracking)

* adhoc discoveries (run this command, if it supports json output help the user
  manage the responses from a large fleet)

* Action triggers ("clear cache", "toggle feature")

* status pages - custom code in the system repo, allow "mirrored" status pages
  in different instances to make different decisions about "we need to act"
  vs "the system is actually down"

* ticket system integrations (youtrack, ji)

  * 1:1 tickets with separate workflows (ticket X in your jira is ticket Y in my youtrack)

  * fully separate tickets

  * a shared view of "whats currently open" to help jour fixe discussions

# The Vision

* "the timeline"

* UI to support sense making, linking and contextualization

  review complex method catalog for inspiration

* should be involve someone specialized for this to help iterate on a good
  UX/UI and informational archicture designs?

# Activity Pub-related

https://www.w3.org/TR/activitypub
https://www.w3.org/TR/activitystreams-vocabulary
https://www.w3.org/TR/activitystreams-vocabulary
https://www.w3.org/TR/json-ld

* Consider how to structure the general model of objects and activities.
  This is a big item regarding creating a good domain model vs. data model!

* Are outboxes actually a thing or do applications generally just

* federation-based user management: someone can invite people / (groups?)
  from other instances to help manage a system -> federated single sign on
  support.

* What is a good actor model (systems are actors. should there be smaller things or bigger things actors to?)

  * where to users via mastodon/fediverse subscribe to to get maintenance/downtime infos?
    can they subscribe something and then filter by tag?

* After a system starts using another system, either deliver
  activities for any ongoing concerns (push) or retrieve current
  concerns from the outbox (pull).

* Unified internal and external routing activity objects

	@context.activitypub.handle(type="Accept", object_type="Use")
	def use_request_accepted(self, activity):
		pass

* implement the inbox entry point and the

* review and compare rdflib / pyld handling


# User Interface

I'm sure we want to go down the API-only + Svelte+Tailwind route. However, I don't want to do that currently as I'm still searching for the MVP feature set.
