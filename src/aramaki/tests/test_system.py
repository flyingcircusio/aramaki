def test_systems_see_subsystem_notifications(fcio, customer):
    from aramaki.system import System

    with fcio:
        storage = System.create(name="storage")
        compute = System.create(name="compute")
        assert compute.actor_id == "http://fcio.example.net/systems/compute"

        compute_actor_id = compute.actor_id

    with customer:
        website = System.create(name="website")
        assert website.actor_id == "http://customer.example.net/systems/website"

        website.use(compute_actor_id)
        website.add_notification("We just moved!")

    with fcio:
        compute = System.get(name="compute")
        compute.add_notification("Something is wrong!")

    with customer:
        website = System.get(name="website")
        assert [x.message for x in website.notifications] == [
            "We just moved!",
            "Something is wrong!",
        ]
