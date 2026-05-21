DEMO_TRANSCRIPTS = {
    "week_1": {
        "name": "Week 1 — Q3 Sprint Kickoff",
        "transcript": """Maya: Alright team, let's lock in the plan for Q3. Rohan, what's your take on the tech stack?
Rohan: I'd go with React on the frontend and FastAPI for the backend. It's what I know best and we can move fast.
Maya: Agreed. Let's make that official — React plus FastAPI. Rohan, can you have the base infrastructure up by Friday?
Rohan: Yes, that's doable.
Priya: I'll have the wireframes done by next Wednesday. I'm thinking three main screens — dashboard home, event explorer, and settings.
Maya: Perfect. On pricing — I think we go $29 per month to start. It's competitive with Amplitude's lower tiers.
Rohan: Works for me. One open question though — Mixpanel or Amplitude for the analytics layer? I haven't decided yet.
Maya: Let's table that for next week once Rohan has had time to test both APIs. Blocker worth noting — legal still hasn't signed off on our data processing agreement. That's going to block us from going public.
Rohan: Yeah that's on the critical path. We should push them.
Maya: I'll follow up with legal today. So to recap — React, FastAPI, $29 a month, launch target in eight weeks, Rohan owns infra by Friday, Priya owns wireframes by Wednesday."""
    },
    "week_2": {
        "name": "Week 2 — Infrastructure Review",
        "transcript": """Maya: Quick update round. Sam, welcome — you're joining us from the growth side starting today.
Sam: Thanks Maya, glad to be here.
Rohan: Infrastructure is done. But I ran into a problem with Mixpanel — their API rate limits are way too aggressive for what we need. We're going to hit the ceiling fast.
Maya: What's the alternative?
Rohan: Amplitude. Their API is cleaner and the limits are much higher.
Maya: Okay, let's make the call — we switch to Amplitude. Sam, can you reach out to their team and negotiate pricing?
Sam: On it. I'll try to get us a startup deal.
Priya: Wireframes are done. I'm showing three screens — dashboard home got a thumbs up from everyone I showed it to internally.
Maya: Love it. Let's approve the dashboard home design officially.
Rohan: One blocker — the legal DPA is still pending. It's now genuinely on the critical path. We cannot launch publicly without it.
Maya: Understood. I'll escalate. Rohan, integrate Amplitude by Thursday. Sam, close the Amplitude deal this week. Priya, start on the mobile responsive version."""
    },
    "week_3": {
        "name": "Week 3 — Beta Launch Planning",
        "transcript": """Sam: Good news — Amplitude deal is closed. $800 a month, includes 2 million events. Good terms for our stage.
Maya: Excellent. That's confirmed then. Rohan, how's the integration?
Rohan: At 70 percent. I need help with webhooks — that part is trickier than expected.
Maya: We'll get you support. Priya, mobile status?
Priya: Mobile responsive version will add about three days. I think it's worth it for the beta users.
Maya: Agreed. Now — legal update. We sent them the final DPA version yesterday. We're waiting on their signature. It could come any day.
Rohan: So we can't do a public launch yet.
Maya: Right. Decision: we do a soft launch with beta users only — no marketing, no press — while legal finishes.
Sam: We have 12 companies ready to go on the beta list.
Priya: I'll own the onboarding emails for the beta cohort.
Maya: Perfect. So Priya owns onboarding emails, Rohan finishes the Amplitude integration, Sam manages the beta list. Legal DPA is still the one thing blocking us from going wide."""
    }
}

DEMO_WORKSPACE = "demo-team-alpha"
