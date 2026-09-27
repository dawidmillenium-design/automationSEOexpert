import re, sys

ADDITIONS = {}

def add(f, block):
    ADDITIONS[f] = block

add("navigating-video-regulations-and-compliance.html", """
<h2 class="text-2xl font-bold mt-8 mb-3">How Compliance Actually Affects Your Virality Score</h2>
<p class="mb-4">Compliance is not just a legal checkbox &mdash; it directly changes the mechanics of distribution. Platforms suppress or remove content that violates policy, which means a single copyright claim or missing disclosure can zero out an otherwise viral video's share velocity mid-spike. Three concrete effects: <strong>reach throttling</strong> (flagged videos stop being recommended before they ever reach a lookalike audience), <strong>monetization locks</strong> (a claimed video earns nothing even if it goes viral), and <strong>trust erosion</strong> (audiences increasingly screenshot undisclosed sponsorships, converting a campaign into a controversy). Treat compliance as insurance on your upside, not overhead.</p>
<h2 class="text-2xl font-bold mt-8 mb-3">Copyright, Fair Use and Music: What Creators Get Wrong</h2>
<p class="mb-4">The most common virality-killer is music. In-feed use of a platform's licensed library covers <em>that platform only</em>: download the clip, repost it elsewhere, and the license does not travel with it. "Fair use" is a defense argued in court, not a switch you flip by crediting the artist or keeping the clip under seven seconds. Practical rules: use royalty-free or platform-library audio for anything you plan to cross-post; get written synchronization licenses for campaigns running on owned channels; and archive proof of every license alongside the master file so a disputed claim can be resolved in hours, not weeks.</p>
<h2 class="text-2xl font-bold mt-8 mb-3">Disclosure Rules by Region (2026 Snapshot)</h2>
<div class="overflow-x-auto mb-4">
<table class="min-w-full text-sm border">
<thead class="bg-gray-100"><tr><th class="border p-2 text-left">Region</th><th class="border p-2 text-left">Regulator / rule</th><th class="border p-2 text-left">What it demands on video</th></tr></thead>
<tbody>
<tr><td class="border p-2">United States</td><td class="border p-2">FTC Endorsement Guides</td><td class="border p-2">Clear, unavoidable disclosure ("ad", "paid partnership") visible before the pitch &mdash; in the video itself, not only the description</td></tr>
<tr><td class="border p-2">United Kingdom</td><td class="border p-2">CAP / ASA guidelines</td><td class="border p-2">Marketing communications must be obviously identifiable; #ad at the start is the safe default</td></tr>
<tr><td class="border p-2">European Union</td><td class="border p-2">UCPD + national media laws</td><td class="border p-2">Hidden commercial communication prohibited; several member states require explicit labeling within the first seconds</td></tr>
<tr><td class="border p-2">Global privacy layer</td><td class="border p-2">GDPR / CCPA</td><td class="border p-2">Consent banners where video pages carry tracking pixels; no personal data shown on screen without permission</td></tr>
</tbody>
</table>
</div>
<p class="mb-4">Platform policies are stricter than most laws and change faster. TikTok's branded-content toggle, Instagram's Paid Partnership label and YouTube's "Includes paid promotion" checkbox are each mandatory for sponsored uploads &mdash; and using them costs almost nothing while ignoring them risks strikes that compound against your channel's distribution.</p>
<h2 class="text-2xl font-bold mt-8 mb-3">Accessibility: Captions Are Law in More Places Every Year</h2>
<p class="mb-4">Beyond reach, captions are becoming a legal requirement for commercial and public-sector video in a growing number of jurisdictions (EU Audiovisual Media Services rules, ADA-informed case law in the US, AODA in Canada). The good news: the caption work that keeps you compliant is the same work that lifts sound-off completion rates. Build one caption workflow and count the benefit twice. Aim for accurate, styled, readable subtitles rather than raw auto-captions &mdash; accuracy is both the legal standard and the retention standard.</p>
<h2 class="text-2xl font-bold mt-8 mb-3">Frequently Asked Questions</h2>
<p class="mb-1 font-semibold">Does a copyright claim stop a video from going viral?</p>
<p class="mb-4">Usually yes, on the claimed platform: blocks mute audio, halt recommendations or take the video down entirely during the dispute window &mdash; exactly when velocity matters most.</p>
<p class="mb-1 font-semibold">Is saying "#ad" in the caption enough?</p>
<p class="mb-4">Not reliably. Regulators require disclosures that are unavoidable; viewers who watch with descriptions collapsed never see it. Put the disclosure in the video and the metadata.</p>
<p class="mb-1 font-semibold">Do these rules apply to organic user-generated content?</p>
<p class="mb-4">To unpaid UGC, mostly no &mdash; but the moment you pay, gift product or repurpose a fan clip into ads, disclosure and licensing obligations attach to you, the brand.</p>
""")

add("genres-that-boost-video-virality.html", """
<h2 class="text-2xl font-bold mt-8 mb-3">Genre-by-Genre Playbook: Hooks, Length and Share Triggers</h2>
<div class="overflow-x-auto mb-4">
<table class="min-w-full text-sm border">
<thead class="bg-gray-100"><tr><th class="border p-2 text-left">Genre</th><th class="border p-2 text-left">Hook that works</th><th class="border p-2 text-left">Sweet-spot length</th><th class="border p-2 text-left">Primary share trigger</th></tr></thead>
<tbody>
<tr><td class="border p-2">Relatable comedy / POV</td><td class="border p-2">Name the exact situation in line one ("POV: your standup says 'quick question'")</td><td class="border p-2">7&ndash;20 s</td><td class="border p-2">Identity &mdash; "this is so me"</td></tr>
<tr><td class="border p-2">Satisfying / process</td><td class="border p-2">Open mid-transformation, tease the finished state</td><td class="border p-2">15&ndash;45 s, loopable</td><td class="border p-2">Completion itch &mdash; "you have to see the end"</td></tr>
<tr><td class="border p-2">Emotional storytelling</td><td class="border p-2">One specific human detail in the first frame</td><td class="border p-2">60&ndash;90 s</td><td class="border p-2">Meaning &mdash; sharing feels like doing good</td></tr>
<tr><td class="border p-2">Educational micro-lesson</td><td class="border p-2">Promise the payoff: "the 10-second fix for..."</td><td class="border p-2">30&ndash;60 s</td><td class="border p-2">Utility &mdash; saved and forwarded to one person</td></tr>
<tr><td class="border p-2">Challenges &amp; duets</td><td class="border p-2">Show the simplest possible entry version</td><td class="border p-2">10&ndash;30 s</td><td class="border p-2">Participation &mdash; viewers become creators</td></tr>
<tr><td class="border p-2">Behind-the-scenes</td><td class="border p-2">Reveal something polished products hide</td><td class="border p-2">45&ndash;90 s</td><td class="border p-2">Insider status &mdash; "look what really happens"</td></tr>
</tbody>
</table>
</div>
<h2 class="text-2xl font-bold mt-8 mb-3">Emerging Genre Bets for 2026</h2>
<ul class="list-disc ml-6 mb-4 space-y-2">
<li><strong>Lo-fi documentary snippets.</strong> Handheld, unscripted mini-truths outperform studio polish on feeds hungry for authenticity; ideal trust-builder for founders and small teams.</li>
<li><strong>AI-assisted spectacle.</strong> Surreal visuals created with generative video tools drive massive watch time, but pair them with honest labeling &mdash; undisclosed AI now carries its own backlash risk.</li>
<li><strong>Niche micro-trends over mega-challenges.</strong> Smaller participatory waves (specific audio memes, format remixes) have less competition and more loyal audiences than jumping on global challenge peaks.</li>
<li><strong>Serialized shorts.</strong> Episodic 30-second series convert one-time viewers into returning followers, compounding every future release's early-velocity signal.</li>
</ul>
<h2 class="text-2xl font-bold mt-8 mb-3">Frequently Asked Questions</h2>
<p class="mb-1 font-semibold">Should I stick to one winning genre?</p>
<p class="mb-4">Anchor on one primary genre so the algorithm learns who to show your videos to, then test adjacent formats in ~20% of slots to find your next lane without confusing your core audience.</p>
<p class="mb-1 font-semibold">Do genres perform differently per platform?</p>
<p class="mb-4">Strongly. Satisfying loops dominate Reels/TikTok; educational micro-lessons over-index on YouTube Shorts because search adds a second discovery path; emotional long-form still wins on Facebook's share-heavy feed.</p>
<p class="mb-1 font-semibold">Can a weak genre idea be rescued?</p>
<p class="mb-4">Often yes, by reframing: a flat product demo becomes a "wait, that's possible?" micro-lesson. The footage survives; the genre wrapper changes.</p>
""")

add("the-importance-of-a-strong-call-to-action.html", """
<h2 class="text-2xl font-bold mt-8 mb-3">CTA Placement: Verbal, Visual and Timed</h2>
<p class="mb-4">Every effective video CTA works on three channels at once. <strong>Verbal:</strong> one plain sentence, spoken at natural pace ("follow for part two"). <strong>Visual:</strong> a short overlay or on-screen cue that survives sound-off viewing &mdash; an arrow sticker, a pinned comment prompt, the follow button itself animated. <strong>Timed:</strong> placed where attention actually is, not where your script ends. On short-form, the strongest window is mid-loop (viewers replaying your hook) or immediately after the payoff lands, before the scroll reflex kicks in. On longer videos, front-load a reason to stay ("stick around for..."), then ask once near the moment of peak satisfaction.</p>
<h2 class="text-2xl font-bold mt-8 mb-3">Match the Ask to the Platform's Native Behavior</h2>
<ul class="list-disc ml-6 mb-4 space-y-2">
<li><strong>TikTok / Reels:</strong> ask for shares and saves &mdash; both are cheap taps and heavily weighted ranking signals; "send this to the friend who needs it" outsells generic "share" phrasing.</li>
<li><strong>YouTube Shorts &rarr; long form:</strong> the related-video link is the CTA; say what the full video gives them, not just "watch my other video".</li>
<li><strong>Feed posts (X, LinkedIn, Facebook):</strong> comments extend distribution, so ask a genuine question people can answer in three words.</li>
<li><strong>Owned site / email:</strong> CTAs can push links, but keep to one destination; competing buttons split clicks and neither converts.</li>
</ul>
<h2 class="text-2xl font-bold mt-8 mb-3">Test One Variable at a Time: A Simple CTA Experiment</h2>
<p class="mb-4">Run a clean A/B: same edit, same hook, two exports differing only in the ask (e.g., "save this for later" vs "send this to someone who needs it"). Publish both to comparable audiences within 24 hours and compare <em>click-through on the action itself</em>, not total views. Two cycles per month is enough to find your audience's preferred verb; rotate seasonally because phrasing fatigue is real &mdash; a CTA that peaked last quarter often decays quietly.</p>
<h2 class="text-2xl font-bold mt-8 mb-3">Frequently Asked Questions</h2>
<p class="mb-1 font-semibold">Is "like and subscribe" a bad CTA?</p>
<p class="mb-4">It's a weak one: it asks for multiple actions with no reason attached. Name one action and one benefit ("subscribe so you don't miss part two").</p>
<p class="mb-1 font-semibold">Do CTAs hurt if placed too early?</p>
<p class="mb-4">Yes &mdash; asking before delivering value reads as a toll booth and raises drop-off. Tease early ("I'll show you the template at the end"), ask late, right after the payoff.</p>
<p class="mb-1 font-semibold">How many CTAs per video?</p>
<p class="mb-4">Exactly one primary ask. Secondary cues (pinned comment, bio link) may support the same action, but never compete with it.</p>
""")

add("common-mistakes-in-creating-viral-videos.html", """
<h2 class="text-2xl font-bold mt-8 mb-3">Mistake-by-Mistake Fixes</h2>
<div class="overflow-x-auto mb-4">
<table class="min-w-full text-sm border">
<thead class="bg-gray-100"><tr><th class="border p-2 text-left">Mistake</th><th class="border p-2 text-left">Symptom in analytics</th><th class="border p-2 text-left">Concrete fix</th></tr></thead>
<tbody>
<tr><td class="border p-2">Weak first 3 seconds</td><td class="border p-2">Hook rate under 60&ndash;70%</td><td class="border p-2">Cut the intro; open on the payoff or a named tension</td></tr>
<tr><td class="border p-2">No sound-off design</td><td class="border p-2">Completion collapses despite strong click-to-play</td><td class="border p-2">Burn styled captions; make the story legible muted</td></tr>
<tr><td class="border p-2">One file everywhere</td><td class="border p-2">Good on one platform, dead on others</td><td class="border p-2">Reframe + recaption per platform before posting</td></tr>
<tr><td class="border p-2">Overlong duration</td><td class="border p-2">Average watch % drops after minute one</td><td class="border p-2">Trim to the idea's natural length; split into parts</td></tr>
<tr><td class="border p-2">Confused CTA</td><td class="border p-2">Views fine, conversions near zero</td><td class="border p-2">One ask, stated verbally and visually after the payoff</td></tr>
<tr><td class="border p-2">Publish-and-abandon</td><td class="border p-2">Velocity stalls after hour one</td><td class="border p-2">Reply to every early comment; reshare clips natively</td></tr>
<tr><td class="border p-2">Trend-only content</td><td class="border p-2">Spiky views, no follower growth</td><td class="border p-2">Anchor trends to a repeatable format you own</td></tr>
<tr><td class="border p-2">Never measuring</td><td class="border p-2">Can't say why any video worked</td><td class="border p-2">Track hook, completion, share rate vs a baseline score</td></tr>
</tbody>
</table>
</div>
<h2 class="text-2xl font-bold mt-8 mb-3">Production and Pre-Publish Mistakes</h2>
<ul class="list-disc ml-6 mb-4 space-y-2">
<li><strong>Shooting landscape "just in case."</strong> If vertical is the target, shoot vertical; cropping later amputates composition and forces refitting captions onto faces.</li>
<li><strong>Over-polish.</strong> Studio-grade perfection reads as advertising on creator feeds; native-feeling beats expensive nearly every time outside of search-driven long form.</li>
<li><strong>Ignoring the thumbnail/first-frame.</strong> On feeds the opening frame <em>is</em> the thumbnail; pick it deliberately instead of accepting whatever the export defaulted to.</li>
<li><strong>No license trail.</strong> Music or clip without archived proof becomes a takedown risk precisely when the video takes off.</li>
<li><strong>Burying context in the caption field.</strong> Viewers decide from the video itself; put essential information on screen, not below it.</li>
</ul>
<h2 class="text-2xl font-bold mt-8 mb-3">Frequently Asked Questions</h2>
<p class="mb-1 font-semibold">Which single mistake costs the most?</p>
<p class="mb-4">The weak opening. Everything downstream &mdash; completion, shares, algorithmic push &mdash; inherits from whether the first three seconds survive, making it the highest-leverage fix in the list.</p>
<p class="mb-1 font-semibold">Are flops worth analyzing individually?</p>
<p class="mb-4">Only pattern-level. One flop is noise; five flops sharing a symptom (same low hook rate, same platform) are a diagnosable habit.</p>
""")

add("understanding-audience-feedback-for-virality.html", """
<h2 class="text-2xl font-bold mt-8 mb-3">Mining Comments Without Reading Every One</h2>
<p class="mb-4">At volume, comment sections need a triage system. Sort by replies-per-comment (not likes) to find threads where viewers argue, tag each other or ask follow-ups &mdash; those mark unresolved curiosity, your best content gaps. Tag recurring phrases verbatim ("where's the link", "part 2?", "this is so accurate"): repeated exact wording is a demand signal, and the phrase itself is usually the title of the next video. Watch the 24-hour window after upload closely; early comments predict the segment mix the algorithm will sample you into, so steer them actively with pinned questions.</p>
<h2 class="text-2xl font-bold mt-8 mb-3">From Feedback Loop to Content Calendar</h2>
<p class="mb-4">Close the loop with a simple cadence: weekly, pull the top three requested topics, the loudest objection and one confused question; each becomes either a new video (requests), a clarification inserted into your format (confusion) or a response piece (objections). Publicly credit the commenter who inspired a video &mdash; "@user asked for this" turns feedback into participation incentive and trains your audience to give better input. Track one meta-metric: the percentage of your published videos traceable to explicit audience demand. Healthy creator channels sit near half; near zero means you're guessing, near all means you've stopped leading the audience anywhere new.</p>
<h2 class="text-2xl font-bold mt-8 mb-3">Handling Negative Feedback</h2>
<p class="mb-4">Separate three kinds of criticism: <strong>signal</strong> (repeated, specific, actionable &mdash; "your captions cover the demo" is a fix), <strong>taste</strong> (repeated but subjective &mdash; segment-test it, don't capitulate), and <strong>noise</strong> (one-off hostility &mdash; ignore or hide, never argue mid-spike). Note that disagreement isn't always damage: high-reply-rate controversy videos often earn extra distribution, so before deleting a flame-war comment, check whether it's generating engagement or deterring it.</p>
<h2 class="text-2xl font-bold mt-8 mb-3">Frequently Asked Questions</h2>
<p class="mb-1 font-semibold">Do polls beat reading comments?</p>
<p class="mb-4">Polls measure stated preference; comments and watch-time reveal revealed preference. Trust behavior first, words second &mdash; audiences vote "educational" and share the funny one.</p>
<p class="mb-1 font-semibold">How much feedback is enough to act on?</p>
<p class="mb-4">Three independent mentions of the same specific request is a reasonable trigger; one mention is anecdote, ten is a queue.</p>
""")

add("analyzing-competitor-virality-scores.html", """
<h2 class="text-2xl font-bold mt-8 mb-3">Step-by-Step: Building a Competitor Virality Baseline</h2>
<ol class="list-decimal ml-6 mb-4 space-y-2">
<li><strong>Pick 5 competitors, not 50:</strong> two direct rivals, one aspirational leader, one fast riser, one format-crusher in an adjacent niche.</li>
<li><strong>Export their last 30 posts</strong> per platform (most tools and native analytics allow bulk listing) with view counts, estimated engagements and publish timestamps.</li>
<li><strong>Compute median, not mean,</strong> completion proxies and share-per-view ratios per competitor &mdash; one outlier hit distorts averages; medians reveal their true floor.</li>
<li><strong>Score each post 1&ndash;10 on hook, format and shareability</strong> using your own rubric; consistency matters more than precision.</li>
<li><strong>Chart hits vs flops on the same axes.</strong> Patterns emerge fast: a rival whose entire catalog is talking-heads yet still wins has solved something invisible in your data &mdash; usually topic selection.</li>
<li><strong>Refresh monthly.</strong> Competitive baselines decay; last quarter's playbook is this quarter's stale trend.</li>
</ol>
<h2 class="text-2xl font-bold mt-8 mb-3">Free Tools That Cover 90% of the Work</h2>
<ul class="list-disc ml-6 mb-4 space-y-2">
<li><strong>Native platform analytics</strong> for your own baseline &mdash; comparison is meaningless without it.</li>
<li><strong>Public third-party dashboards</strong> (creator-stats sites) for rough follower/view histories of big accounts.</li>
<li><strong>A spreadsheet + the above scoring rubric</strong> &mdash; genuinely sufficient; most paid competitor suites automate exactly this table at $99+/month.</li>
<li><strong>Google Trends</strong> to separate rising-topic luck from durable skill when a competitor spikes.</li>
</ul>
<h2 class="text-2xl font-bold mt-8 mb-3">Ethical Boundaries and Common Pitfalls</h2>
<p class="mb-4">Analyze strategy, never appropriate execution: formats, hooks and cadence are fair study; copying scripts, edits or brand elements is plagiarism that platforms now surface quickly and audiences punish publicly. The classic analytical traps: benchmarking against outliers ("they got 40M views" tells you nothing about their median), studying winners who bought their distribution, and treating competitor analysis as ideation &mdash; it tells you the gap, not the idea. Do it quarterly, in two hours, then close the tab and make things.</p>
<h2 class="text-2xl font-bold mt-8 mb-3">Frequently Asked Questions</h2>
<p class="mb-1 font-semibold">How do I estimate competitor completion rates?</p>
<p class="mb-4">You can't directly &mdash; proxy with view-vs-like/comment ratios and observed rewatches (loops); consistent ratio leaders are finishing their videos.</p>
<p class="mb-1 font-semibold">Should I copy a competitor's posting schedule?</p>
<p class="mb-4">Use it as evidence, not gospel: their timing works for their audience overlap. Test their slots against yours, keep whichever your own analytics reward.</p>
""")

add("factors-affecting-video-virality-score.html", """
<h2 class="text-2xl font-bold mt-8 mb-3">Weighting the Factors: Where to Spend Effort First</h2>
<p class="mb-4">Not all factors deserve equal hours. Based on how consistently they move outcomes across audits, rank your effort roughly like this: <strong>(1) Hook strength and opening seconds</strong> &mdash; gates every downstream metric; <strong>(2) Topic-audience fit</strong> &mdash; determines who the algorithm samples you to; <strong>(3) Shareability of the payoff</strong> &mdash; the difference between views and spread; <strong>(4) Format-native execution</strong> (aspect ratio, captions, pacing); <strong>(5) Timing and trend alignment</strong>; <strong>(6) Production quality</strong> &mdash; real, but last, because polish multiplies a weak idea by a nicer zero. A useful mental model: early-stage factors are <em>multipliers</em> (hook rate x completion x share rate), later ones are <em>modifiers</em>. Fix multipliers first.</p>
<h2 class="text-2xl font-bold mt-8 mb-3">Quick Diagnostic: Which Factor Is Killing Your Video?</h2>
<ul class="list-disc ml-6 mb-4 space-y-2">
<li><strong>Low views but healthy engagement ratios</strong> &rarr; distribution problem: topic fit, trend timing, account history.</li>
<li><strong>Views spike then flatline within an hour</strong> &rarr; velocity failure: weak share trigger or poor first-hour community management.</li>
<li><strong>High clicks, terrible completion</strong> &rarr; hook promises the video doesn't keep &mdash; clickbait tax.</li>
<li><strong>Great completion, few shares</strong> &rarr; content is pleasant but identity-light: nobody gains status sending it.</li>
<li><strong>Good everywhere except saves</strong> &rarr; utility gap: add a reference-worthy element (checklist, template, numbers).</li>
</ul>
<h2 class="text-2xl font-bold mt-8 mb-3">Frequently Asked Questions</h2>
<p class="mb-1 font-semibold">Do hashtags and posting time matter as much as content?</p>
<p class="mb-4">Far less. They shift initial sampling conditions; content factors set the ceiling. A great video posted "badly" still travels; a weak one posted perfectly dies politely.</p>
<p class="mb-1 font-semibold">Which factor is most overrated?</p>
<p class="mb-4">Equipment-driven production quality. Feeds reward native-feeling content; budgets improve consistency and safety, not virality odds per se.</p>
""")

add("collaboration-in-viral-video-production.html", """
<h2 class="text-2xl font-bold mt-8 mb-3">Structuring the Collab So Both Audiences Actually Show Up</h2>
<p class="mb-4">Most collabs underperform because the logistics kill the algorithm: both parties posting identical files days apart splits the velocity signal. Better patterns in order of strength: <strong>native co-creation</strong> (one party films, both appear, single canonical post plus a reaction/behind-the-scenes follow-up), <strong>sequential duets/stitches</strong> that reference each other explicitly, and <strong>split-shoot series</strong> ("I'll finish their video, they'll finish mine") published simultaneously. Agree beforehand on who hosts the primary upload &mdash; usually the smaller partner, since borrowed reach compounds hardest there &mdash; and pin each other in comments within minutes of publishing.</p>
<h2 class="text-2xl font-bold mt-8 mb-3">Common Collaboration Failure Modes</h2>
<ul class="list-disc ml-6 mb-4 space-y-2">
<li><strong>Audience mismatch dressed as chemistry.</strong> Overlap matters more than size: a 10K creator in your exact niche beats a 1M creator three niches away.</li>
<li><strong>Division-of-labor drift.</strong> Unclear ownership of editing, captions and posting causes double-posts (which platforms treat as spam) or silent non-posts.</li>
<li><strong>Value asymmetry.</strong> One partner always lends reach, the other always lends ideas; resentment ends the pipeline after round two.</li>
<li><strong>Waterfall silence.</strong> Announcing a collab without tagging, pins or comment seeding wastes the cross-pollination window entirely.</li>
<li><strong>Chasing clout over craft.</strong> Collaborations built for follower-count optics produce awkward content both audiences feel instantly.</li>
</ul>
<h2 class="text-2xl font-bold mt-8 mb-3">Frequently Asked Questions</h2>
<p class="mb-1 font-semibold">How many collabs should a channel run?</p>
<p class="mb-4">Roughly one in four to one in six posts &mdash; enough to keep importing fresh audiences, not enough to blur your own identity.</p>
<p class="mb-1 font-semibold">Brands or creators for first collabs?</p>
<p class="mb-4">Start with peers at similar size; brand collaborations add contract complexity and disclosure obligations you'll manage far better once your format instincts are proven.</p>
""")

add("top-10-video-virality-tools.html", """
<h2 class="text-2xl font-bold mt-8 mb-3">How to Choose (and Combine) Tools: A Decision Guide</h2>
<p class="mb-4">Tools fall into four jobs, and most stacks fail by buying three dashboards and covering none of them well. Pick one tool per job: <strong>(1) Native measurement</strong> &mdash; platform analytics remain the ground truth for reach, retention curves and traffic sources; everything else triangulates around them. <strong>(2) Cross-platform aggregation</strong> &mdash; one dashboard comparing your handle's performance everywhere, essential once you post on 3+ surfaces. <strong>(3) Competitor and trend intelligence</strong> &mdash; external catalogs of others' posts and rising topics; buy only if competitor cadence materially affects your planning. <strong>(4) Prediction/testing</strong> &mdash; pre-publish scoring and A/B utilities; valuable mainly for teams shipping high volumes where a 5% lift compounds. Budget rule: free tiers of jobs 1&ndash;2 cover solo creators entirely; spend money only where a job currently blocks a decision.</p>
<h2 class="text-2xl font-bold mt-8 mb-3">Data Hygiene: Making Tool Numbers Comparable</h2>
<ul class="list-disc ml-6 mb-4 space-y-2">
<li><strong>Pick one denominator</strong> (per-view share rate, per-reach engagement rate) and compute it identically across tools &mdash; vendors define metrics differently and silently.</li>
<li><strong>Log manually what tools miss:</strong> DM shares, saves-to-comments gut feel, sales calls mentioning a video. Shadow metrics rarely appear in dashboards.</li>
<li><strong>Snapshot weekly into a spreadsheet</strong> you control; platforms delete historical depth and vendors lose your exports.</li>
<li><strong>Flag API lag:</strong> overnight view counts routinely revise 10&ndash;20%; judge trends over 7-day windows, never day-over-day.</li>
</ul>
<h2 class="text-2xl font-bold mt-8 mb-3">Frequently Asked Questions</h2>
<p class="mb-1 font-semibold">Can tools predict if my video goes viral?</p>
<p class="mb-4">They predict probability bands from format and topic similarity &mdash; useful for choosing between drafts, useless as guarantees. Treat scores as ranking aids, not verdicts.</p>
<p class="mb-1 font-semibold">Which single tool if I can only have one?</p>
<p class="mb-4">Your strongest platform's native analytics, studied properly, beats any third-party suite. Buy aggregation only after native data stops answering your questions.</p>
""")

add("the-impact-of-video-quality-on-virality.html", """
<h2 class="text-2xl font-bold mt-8 mb-3">Where Quality Genuinely Matters (and Where It Doesn't)</h2>
<p class="mb-4">Quality is not one dial but several, moving in opposite directions depending on placement. <strong>Audio quality is non-negotiable everywhere</strong> &mdash; viewers forgive soft visuals but swipe instantly on muffled or clipping sound; a $50 lav mic outperforms any camera upgrade per dollar. <strong>Lighting ranks second:</strong> a bright, face-lit phone shot beats a dark cinematic mirrorless clip. <strong>Resolution and color grading matter mainly on search-driven surfaces</strong> (YouTube long-form, product explainers) where intent is deliberate. <strong>Camera-brand prestige matters nowhere</strong> on feeds &mdash; native-feeling handheld footage regularly outperforms studio output precisely because it doesn't read as an ad.</p>
<h2 class="text-2xl font-bold mt-8 mb-3">The Cost-Benefit Curve of Polish</h2>
<p class="mb-4">There's a known shape to quality ROI: the jump from "unintelligible" to "clear" (good audio, legible captions, decent light) captures most of the available gain; the jump from "clear" to "cinematic" buys little distribution and sometimes costs it. Beyond clarity, reinvest budget into <em>quantity and iteration speed</em> &mdash; more tested hooks and formats beat one gorgeous video per month in nearly every algorithmic environment. The exception is category-defining brand work: hero campaigns, flagship demos, award-bait pieces, where polish itself is the message. Run a two-tier pipeline: 80% fast "clear" content feeding your learning loop, 20% polished anchor pieces feeding your brand.</p>
<h2 class="text-2xl font-bold mt-8 mb-3">Frequently Asked Questions</h2>
<p class="mb-1 font-semibold">Does 4K help my reach?</p>
<p class="mb-4">Indirectly at best. Platforms transcode everything; 4K acquisition gives crop headroom and future-proofing, but viewers never see "4K" &mdash; they see lighting, framing and sound.</p>
<p class="mb-1 font-semibold">Is bad quality ever a feature?</p>
<p class="mb-4">Yes &mdash; lo-fi signals authenticity and spontaneity, core drivers of relatable-genre shares. The trick is choosing informality deliberately, not accidentally failing at competence.</p>
""")

add("creating-shareable-video-content.html", """
<h2 class="text-2xl font-bold mt-8 mb-3">Share Triggers by Emotion: What People Send and Why</h2>
<div class="overflow-x-auto mb-4">
<table class="min-w-full text-sm border">
<thead class="bg-gray-100"><tr><th class="border p-2 text-left">Emotion</th><th class="border p-2 text-left">Sharing motive</th><th class="border p-2 text-left">Example framing</th></tr></thead>
<tbody>
<tr><td class="border p-2">Awe</td><td class="border p-2">Giving others a spectacle they'd never seek</td><td class="border p-2">"Watch what this restoration reveals"</td></tr>
<tr><td class="border p-2">Amusement</td><td class="border p-2">Bonding through shared humor codes</td><td class="border p-2">"This is literally our team standup"</td></tr>
<tr><td class="border p-2">Validation</td><td class="border p-2">Expressing an identity or opinion safely via proxy</td><td class="border p-2">"Finally someone said it about [industry habit]"</td></tr>
<tr><td class="border p-2">Care</td><td class="border p-2">Warning or protecting someone specific</td><td class="border p-2">"Send this to anyone buying a used car"</td></tr>
<tr><td class="border p-2">Hope/pride</td><td class="border p-2">Aligning with uplifting stories</td><td class="border p-2">Comeback and kindness narratives</td></tr>
<tr><td class="border p-2">Outrage*</td><td class="border p-2">Status through moral signaling</td><td class="border p-2">Powerful but poisons brands &mdash; rarely worth engineering</td></tr>
</tbody>
</table>
</div>
<h2 class="text-2xl font-bold mt-8 mb-3">Designing the "Send This To..." Moment</h2>
<p class="mb-4">The strongest share architecture makes the recipient specific. "Send this to your co-founder" outperforms "share this" because it converts an abstract action into a relationship move already queued in the viewer's head. Write your videos backward from one imagined conversation: which exact person would forward this, to whom, with what caption? If you can't name the pair ("new manager &rarr; their mentor", "dog owner &rarr; dog-owner group chat"), the concept likely lacks a share spine. Then engineer the artifact to survive the send: self-contained (no prior episodes required), captioned (DM previews autoplay muted), and short enough to finish inside the preview loop.</p>
<h2 class="text-2xl font-bold mt-8 mb-3">Frequently Asked Questions</h2>
<p class="mb-1 font-semibold">Do share-bait lines ("tag someone who...") still work?</p>
<p class="mb-4">Diminishingly and shallowly &mdash; tagged comments inflate engagement without deepening spread, and platforms increasingly discount obvious bait. Specific-recipient framing drives real DM forwards instead.</p>
<p class="mb-1 font-semibold">Private shares vs public reposts: which matters?</p>
<p class="mb-4">For conversion and trust, private DM/share-sheet forwards are the higher-intent signal &mdash; and they're invisible in most dashboards, so track them with occasional "how did you find this?" prompts.</p>
""")

add("impact-of-branding-on-video-virality.html", """
<h2 class="text-2xl font-bold mt-8 mb-3">Brand Safety vs Brand Blandness: Walking the Line</h2>
<p class="mb-4">Virality requires friction-free emotion; brands require reputational control. The failure mode isn't choosing either extreme but oscillating between them: legal-approved focus-grouped content that's bland enough to be ignored, punctuated by risk-chasing stunts that trigger backlash. The stable middle is a documented <strong>edge policy</strong>: three to five explicit statements of what you will joke about, critique, or dramatize &mdash; signed off once, reused forever ("we satirize workplace absurdities, never protected classes, politics or competitors' failures"). Within those rails, creators move fast without asking permission per post; outside them, nothing ships. Brands with such written boundaries publish bolder work <em>and</em> incident fewer crises than brands relying on case-by-case approval anxiety.</p>
<h2 class="text-2xl font-bold mt-8 mb-3">Making Brand Elements Sharable Instead of Skippable</h2>
<ul class="list-disc ml-6 mb-4 space-y-2">
<li><strong>Own a format, not just a logo.</strong> The strongest modern branding asset is a recognizable recurring structure (cold-open style, visual gag, segment device) people identify before any watermark appears.</li>
<li><strong>Place marks late and small.</strong> Intros with logo stingers bleed completion; a corner bug appearing after the hook preserves recall without costing the first three seconds.</li>
<li><strong>Let product enter as plot, not packaging.</strong> "We fixed X with Y" narrative embeds the brand in the payoff; beauty shots of boxes embed it in the skip.</li>
<li><strong>Sound signatures travel further than visuals</strong> in muted feeds &mdash; reserve audio branding for moments when sound is likely on (long-form, TV-adjacent placements).</li>
<li><strong>Make merch-adjacent content shareable:</strong> designs fans <em>want</em> on screen turn brand exposure into identity expression rather than interruption.</li>
</ul>
<h2 class="text-2xl font-bold mt-8 mb-3">Frequently Asked Questions</h2>
<p class="mb-1 font-semibold">Does heavy branding reduce shares?</p>
<p class="mb-4">Overtly promotional framing does &mdash; people avoid forwarding material that makes <em>them</em> the ad. Subtle, format-level brand presence barely moves share rates while improving attribution.</p>
<p class="mb-1 font-semibold">B2B or regulated industries: any room for viral formats?</p>
<p class="mb-4">Plenty &mdash; regulatory constraints shape claims, not creativity. Process reveals, industry-absurdity satire within policy, and utility micro-lessons all clear compliance review easily.</p>
""")

add("leveraging-influencers-for-video-virality.html", """
<h2 class="text-2xl font-bold mt-8 mb-3">Micro vs Macro Influencers: The Real Economics</h2>
<p class="mb-4">Cost scales roughly linearly with follower count; results don't. Micro-influencers (10K&ndash;100K) typically deliver 2&ndash;5x the engagement rate of macros, sit closer to niche purchase communities, and cost little enough per collaboration that you can run <em>several simultaneous</em> tests instead of one expensive bet. Macros buy guaranteed reach and halo credibility &mdash; appropriate for launches needing saturation, less so for proving a concept. A defensible allocation: 70% of influencer budget on 4&ndash;8 aligned micros testing hooks and formats, 30% on one macro amplification reserved for a concept already validated by the micro cohort. Judge deals on engaged-audience overlap with your buyer persona, not headline followers &mdash; fake-follower audits take minutes and routinely halve a shortlist.</p>
<h2 class="text-2xl font-bold mt-8 mb-3">Contracts: What to Lock Down Before Filming</h2>
<ul class="list-disc ml-6 mb-4 space-y-2">
<li><strong>Usage rights and window:</strong> can you repost their cut to your channels and run it as an ad? For how long? Whitelisting/allow-list access beats file handoffs for paid amplification.</li>
<li><strong>Exclusivity scope:</strong> category lockouts priced explicitly &mdash; vague "no competitor work" clauses cause disputes at renewal.</li>
<li><strong>Approval flow:</strong> creator drafts, brand checks claims/compliance once, revisions capped &mdash; endless brand edits destroy the native tone you hired them for.</li>
<li><strong>Disclosure obligations:</strong> platform branded-content toggles and regional ad labels spelled out as contractual requirements, protecting both sides.</li>
<li><strong>Performance levers, not guarantees:</strong> contract for deliverables and posting windows; never promise virality in either direction.</li>
</ul>
<h2 class="text-2xl font-bold mt-8 mb-3">Frequently Asked Questions</h2>
<p class="mb-1 font-semibold">Pay per post or per performance?</p>
<p class="mb-4">Flat fee plus bonus thresholds aligns incentives without starving creators for uncontrollable algorithm variance; pure commission models attract only accounts willing to game their own traffic.</p>
<p class="mb-1 font-semibold">When does gifting product replace payment?</p>
<p class="mb-4">Below ~10K followers occasionally, where genuine enthusiasm exists &mdash; but disclose it anyway, and expect nothing operationally: gifted posts aren't deliverables.</p>
""")

ANCHOR = '<h2 class="text-2xl font-bold mt-8 mb-3">Related guides</h2>'

def main():
    done = []
    for f, block in ADDITIONS.items():
        t = open(f).read()
        marker = block.strip()[:60]
        if marker in t:
            print("skip (already enriched):", f)
            continue
        idx = t.find(ANCHOR)
        assert idx != -1, f"{f}: anchor not found"
        t = t[:idx] + block.strip() + "\n" + t[idx:]
        open(f, 'w').write(t)
        done.append(f)
    print("updated", len(done), "files:", *done, sep="\n  ")

if __name__ == "__main__":
    main()
