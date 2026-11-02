# EP66 · THE OPEN-FIELDS DOCTRINE — SCRIPT v003

**Rewrite of v002 · design `EP66_openfields_FILM_BIBLE.v001.md` · facts `EP66_openfields_FACTS_LEDGER.v001.md` (only source) · front `EP66_openfields_PACKAGING.v001.md` (§3 corrected 2026-08-10) · contract `episodes/PD-2026-066-openfields/episode_spec.v001.json`**

**Why v003 exists.** The contract changed. `episode_spec.v001.json` now declares `runtime_seconds` **[1500, 1980]** and `script_words` **[4225, 5247]**. v002 was written against a 1620 s / 4565-word floor, and to hold that floor its writer put roughly 590 words of restored material back after the cuts. The three reads that judged v002 trace every new factual error and every machine-voiced sentence in it to those 590 words. This draft cuts them and does not replace them.

**The two things v002 got right are untouched.** ACT_1 no longer opens on a remark about the opinion's prose style, and the hard cut into Pennsylvania still lands on place, date, the hinge quotation, *Includes land.* and *We hereby overrule Russo.* in that order, with no connective word across the edit. The turn's construction is unchanged; only its derived clock time moves, and it moves because a hundred and seventy words and one reset beat came out ahead of it.

**Citation convention.** Every factual line is followed on the next line by an HTML comment carrying its ledger row id. The comment is on its own line deliberately: `check_script_craft.narration_lines()` skips a line beginning `<!--`, but an inline trailing comment is tokenised into the narration word count.

**Register.** Declarative. No adjective the record does not carry. One dollar, seventy-eight days and twenty-three months are each said once, flat, with nothing appended. No line tells the audience what to feel. No line in this file states how many times the script uses a figure of speech; v002's header did, and the number in it was wrong.

**Amendment, 2026-08-10 — the HOOK carries the stakes now.** The delivered master read the cold open in 13.295 s against a 20.3 s design, and, more to the point, the scene never said what the film is about, what its payoff is, or what a viewer gets from it. Relative retention at 0:30 is below 0.50 on 29 of the 30 measurable episodes on this channel (median 0.215), so that is the binding defect, not the clock. TWO LINES WERE ADDED and nothing was removed: *The Fourth Amendment does not protect that land.* (PA-21) and *A Tennessee court found the state constitution does.* (TN-26 / TN-32 / TN-38). They sit between the camera going up and *Nobody tells the man who farms the ninety-three acres.*, so the cold open still closes on that line and the OP sting still answers it directly. The two levels are kept in separate sentences — the first names only the federal constitution, the second only a state court and a state constitution — and neither asserts any magnitude, acreage, percentage or count. MEASURED AFTERWARDS, not modelled: +16 narration words and +100 characters, 2 new voice chunks (VC-0006, VC-0007; the existing 275 takes were reused unchanged at shifted ids, so this cost 100 characters and $0.03, not a second full run), HOOK 0.000–19.468 s over eight chunks, master 1604.211 s, 4,278 index words. Both contract bands still hold: script_words 4,278 in [4225, 5247]; runtime 1613.2 s projected in [1500, 1980].

---

## HOOK (voice from frame 0)

【4 image groups over 20.3 s per PACKAGING §3. Archive aerial farmland at low sun, 6% push-in → padlock in wire fence, rack focus → blank posted placard wired to a gate bar, boots passing behind, no face → single trunk in mid-ground woodland → the three branch/camera plates, 1.7 s each, 0.35 s motion-blurred pushes, cut 3 holds longest and ends on the lens → archive aerial wide with a MOTIONKIT figure counting to 93 → the empty field as the lens would see it. MEASURED 2026-08-10, after two lines were added to carry the stakes: the spoken hook runs 0.000-19.468 s over eight chunks (narration_index.v001.json), against the 20.3 s designed picture window -- 0.83 s of slack, which the hold on the empty field absorbs. The picture window itself does not move.】

West Tennessee. 2017.
<!-- TN-13 (approximately 93 acres crossing Benton and Henry Counties) · TN-16 (30 November 2017). No ledger row places the camera tree in either county, so no county is named. -->

A state wildlife officer is on the land.
<!-- TN-16 — TN-16 records the installation and nothing about how he arrived. The chained gate is in the picture and not in the sentence. -->

He walks out to a tree.
<!-- TN-16 -->

He cuts a branch off it, and installs a camera on it.
<!-- TN-16 ✓ VERBATIM: "installed a camera... on a tree on Mr. Hollingsworth's property on November 30, 2017, cutting a branch to do so." -->

The Fourth Amendment does not protect that land.
<!-- PA-21 ✓ VERBATIM ("Open fields are afforded no constitutional protection from warrantless searches and seizure under the Fourth Amendment to the United States Constitution." — first sentence of the lead opinion; spoken verbatim later at the head of the Pennsylvania act) · ND-04 (the 2026 Court expressly declined to question the federal doctrine, so Hester and Oliver stand). FEDERAL LEVEL ONLY: no state word appears in this sentence. No magnitude, acreage, percentage or count is asserted — ⛔-06 and ○-04 forbid every figure of that family. -->

A Tennessee court found the state constitution does.
<!-- TN-26 ✓ VERBATIM ("Tennessee has a robust history of protecting land outside the curtilage of a home as a possession under Article I, Section 7 of the State Constitution.") · TN-32 ✓ VERBATIM (the plaintiffs' lands were not wild or waste lands but possessions subject to constitutional protection) · TN-38 ✓ VERBATIM · ID-06 (Tenn. Ct. App., filed 05/09/2024) · ID-07 (unanimous panel). STATE LEVEL ONLY: the sentence names a Tennessee court and a state constitution and carries no federal word. It states the constitutional-protection finding and NOT the statute's disposition, so it is not ⛔-02 ("Tennessee struck the law down"); it claims no injunction, so it is not ⛔-03; it is one case standing alone, so it is not ⛔-01. -->

Nobody tells the man who farms the ninety-three acres.
<!-- TN-02 ✓ VERBATIM ("does not provide notice to property owners") · TN-13 ✓ VERBATIM (93 acres, farming) -->

---

## OP

【The brand band rises at 0:19.67 over the empty field and falls at 0:23.17 — PACKAGING §4, re-derived 2026-08-10 from the measured hook (filmconfig hookSeconds 19.468 + CaseFilm.OPENING_OVERLAY_OFFSET_SEC 0.2, held for Bookends.OPENING_SEC 3.5). The recorded OP line speaks 21.268-22.522, so it is under the band from end to end, and ACT_1 does not speak until 24.322. Picture and voice do not stop under it. The OP is one line.】

Nobody has to.
<!-- TN-02 -->

---

## ACT_1 — THE LINE IS NOT WHERE YOU THINK IT IS

【motif state 1: a chain across a farm track, the padlock closed, morning light. Narration runs under it; nothing in the voice touches the lock, here or anywhere.】

The man is Hunter Hollingsworth.
<!-- TN-13 -->

His land runs to approximately ninety-three acres, crossing Benton and Henry Counties. He and his guests use it for fishing, farming, camping and hunting.
<!-- TN-13 ✓ VERBATIM -->

It is landlocked. He reaches it through his neighbour's private gravel drive and gate, then through a chained gate of his own, with a No Trespassing sign on it.
<!-- TN-13 ✓ VERBATIM -->

That gate is not the line. A chained gate is what a landowner believes makes entry unlawful. It is not what the law was measuring.
<!-- PA-18 · PA-28 · PA-29 · ⛔-04 (the rule is not stated flatly) -->

The law draws a narrow ring around a house and calls it the curtilage. Outside that ring the land is what the law calls an open field. On ninety-three acres, almost all of the ninety-three is outside the ring.
<!-- PA-18 (statutory "except curtilage") · TN-26 · TN-13 — arithmetic on the recorded acreage and the recorded position of the curtilage, the same kind performed on the two dates in ACT_2 -->

There is a second farm, and a second man. Terry Rainwaters works his land in Tennessee too, behind chained gates and No Trespassing signs of his own.
<!-- TN-09 ✓ VERBATIM basis -->

Two men who go to their own ground less than they used to.
<!-- TN-12 · TN-17 -->

Rainwaters has curtailed some of his usage, as he has become hesitant to use his properties or invite guests due to fear of surveillance and fear of injuring a TWRA officer.
<!-- TN-12 ✓ VERBATIM -->

He testified that he felt exposed as a result of a loss of privacy on his land.
<!-- TN-12 ✓ VERBATIM -->

Hollingsworth also uses the property to spend time alone with his girlfriend.
<!-- TN-13 ✓ VERBATIM -->

He fears that officers might be observing him, his girlfriend, or his guests in their private activities, and he has reduced his visits to his land, where he previously more regularly camped and fished.
<!-- TN-17 ✓ VERBATIM -->

On Rainwaters's land there is a rule about people. As a safety precaution, Mr Rainwaters and his guests follow a rule that hunters should know the location of everyone else on the property.
<!-- TN-10 ✓ VERBATIM -->

Everyone on it is supposed to know where everyone else is standing. That is the kind of place it is.
<!-- TN-10 -->

On three occasions in 2017, Kevin Hoofman, an officer of the Tennessee Wildlife Resources Agency, entered onto Mr Rainwaters's Harmon Creek property to investigate suspected hunting violations. While on the property, Officer Hoofman took photographs.
<!-- TN-11 ✓ VERBATIM · ⛔-08 (conduct only, no motive) -->

Officer Hoofman entered Mr Hollingsworth's property on December 21, 2016, to investigate deer baiting, and he took photographs.
<!-- TN-15 ✓ VERBATIM -->

Officer Hoofman installed a camera owned by the United States Fish and Wildlife Service on a tree on Mr Hollingsworth's property on November 30, 2017, cutting a branch to do so.
<!-- TN-16 ✓ VERBATIM -->

A camera belonging to the same federal service went onto Rainwaters's property that same November and came off it in December.
<!-- TN-16 -->

Whether those installations were the work of federal authorities alone, or of federal and state authorities together, the parties dispute. Nobody has decided it.
<!-- ND-11 ✓ VERBATIM: "The parties dispute whether these actions were attributable solely to federal authorities... or to both federal and state authorities." -->

In December 2017, Officer Hoofman entered Mr Hollingsworth's property and searched his vehicle, and subsequently recorded video footage of Mr Hollingsworth.
<!-- TN-16 ✓ VERBATIM · ⛔-08 -->

Those are the entries that ended up inside a document. How many there were altogether is a different question.
<!-- TN-08 · TN-02 -->

【motif state 2: the same padlock as state 1, still closed, still holding the chain. Beyond it, in the mud on the far side, boot prints. The voice never mentions either, here or anywhere.】

The agency does not create records of all of its agents' entries onto private property and does not provide notice to property owners.
<!-- TN-02 ✓ VERBATIM -->

Officers enter private property, sometimes conceal themselves thereupon, and look for violations of wildlife laws.
<!-- TN-03 ✓ VERBATIM -->

Sometimes conceal themselves.
<!-- TN-03 ✓ VERBATIM — a state agency describing its own conduct, left standing. -->

【subscribe ask. Both clauses are checkable and neither promises a sequel to this film.】

There are more cases like this one on the channel already, and there are more coming. If you want them, subscribe.
<!-- true: 55 published long-forms, the catalogue is warrants, searches and seizures (scripts/yt_channel_index.py, 2026-08-10); the 12:00 JST slot is filled forward -->

【comment question. Spoken once, pinned at publish. Its answer arrives fifteen minutes later and the narrator says nothing when it does.】

If a camera went up on your land today — strapped to a tree, lens pointed at your field — how long before you found it?
<!-- design plant; paid off by PA-13 -->

Notice is the thing most owners assume exists — a knock at the house, a card left in the door, a letter afterwards saying somebody had been out. The law requires none of that.
<!-- TN-02 ✓ VERBATIM basis -->

There is a method for choosing which farm to walk onto. In determining which properties to enter to investigate suspected violations of hunting laws, officers sometimes rely on having previously seen hunters on the property, on word of mouth, or on listening for shots.
<!-- TN-04 ✓ VERBATIM -->

Word of mouth, and the sound of a shot carrying over a treeline. Those are the criteria.
<!-- TN-04 ✓ VERBATIM -->

Officers also enter upon and cross property not under investigation to reach land they intend to investigate.
<!-- TN-05 ✓ VERBATIM -->

A man's land can be crossed because of where somebody else was standing.
<!-- TN-05 -->

There is no ceiling on any of it. The agency does not impose constraints on how often a parcel is entered, what time of day an entry may be made, or how long an officer may remain on private property.
<!-- TN-06 ✓ VERBATIM -->

And it does not have written policies for officers to follow when deciding whether to enter private property.
<!-- TN-06 ✓ VERBATIM -->

So the number does not exist anywhere.
<!-- TN-08 -->

The agency does not know how many times its agents have entered upon their properties, nor do Messrs Rainwaters and Hollingsworth know how many times their properties were entered upon.
<!-- TN-08 ✓ VERBATIM -->

Neither side of this case can count it. The number was never written down.
<!-- TN-02 · TN-08 -->

The two men sued in the Circuit Court for Benton County, in front of a panel of three judges.
<!-- ID-06 · ID-10 -->

The ninety-three acres with the tree on them are Hollingsworth's.
<!-- ID-06 · TN-13 · TN-16 -->

The defendants were the agency itself, Bobby Wilson, Ed Carter, and Officer Hoofman.
<!-- ID-09 ✓ VERBATIM basis: "Tennessee Wildlife Resources Agency, Bobby Wilson, Ed Carter, and Kevin Hoofman" -->

The agency's answer was a claim of power. Its officers had the statutory authority to go upon any property, outside of buildings, posted or otherwise, in the performance of their duties to enforce wildlife laws.
<!-- TN-07 ✓ VERBATIM, as the agency's own assertion quoted in the opinion -->

That is the agency describing the statute. The opinion that came out of the case never prints the statute itself.
<!-- TN-07 · ⛔-15 -->

They sued under Article I, Section 7 of the Tennessee Constitution.
<!-- TN-23 · ND-12 -->

---

## ACT_2 — WHAT THE STATE SAYS IT MAY DO

【the four nouns arrive as four typographic cards over the land, one per word. The section's text is not read here: it is read once, whole, in ACT_3, at the passage its second half bears on.】

The text they sued under names four things a person is secure in: persons, houses, papers and possessions.
<!-- TN-23 ✓ VERBATIM basis (Tenn. Const. art. I, § 7) -->

One word in that list is not in the federal one. The Fourth Amendment says effects. Tennessee wrote possessions.
<!-- TN-24 -->

It wrote its first constitution in 1796 and did not take the federal word. In 1834 it wrote a new constitution and kept possessions. In 1870 it wrote another one and kept it again.
<!-- TN-24 -->

Three constitutions, and three times the state declined the federal word.
<!-- TN-24 -->

In 1926, in a case called Welch, Tennessee's Supreme Court said why that mattered. The word possessions was added for a purpose. It refers to property, real or personal, actually possessed or occupied.
<!-- TN-24 ✓ VERBATIM -->

Welch drew its own limit in the same case. It would not include wild or waste lands, or other lands that were unoccupied.
<!-- TN-25 ✓ VERBATIM — TN-24 and TN-25 are a page apart in the opinion, so no claim is made that one sentence carries both -->

By 1926, then, Tennessee's own highest court had said the extra word was deliberate, had said what it covered, and had said what it did not.
<!-- TN-24 ✓ VERBATIM · TN-25 ✓ VERBATIM -->

Tennessee has a robust history of protecting land outside the curtilage of a home as a possession under Article I, Section 7 of the State Constitution.
<!-- TN-26 ✓ VERBATIM -->

The federal charter has nothing to say about that ground. The state charter has one extra noun in it.
<!-- TN-23 · TN-24 · PA-21 · forbidden_claims 4 (the two levels are kept in separate sentences) -->

So the state had to say what it was doing on the land, and it did, in one sentence.
<!-- TN-34 -->

Officers enter private property only when — and only in areas where — they believe hunting activity is taking place or has taken place.
<!-- TN-34 ✓ VERBATIM -->

It is a narrow claim, and it is the agency's. On its account, officers go where they think hunting is happening, and nowhere else.
<!-- TN-34 ✓ VERBATIM basis — attributed, because TN-05 and TN-21 record entries that do not fit it -->

It is undisputed that the TWRA believes TWRA officers have lawful authority to enter private property without consent or a warrant to enforce Tennessee's wildlife laws in the performance of their duties.
<!-- TN-20 ✓ VERBATIM -->

The agency insists that its actions are constitutional. Officers have entered the private property of others pursuant to this purported statutory authority and without consent or a warrant since the filing of this case.
<!-- TN-42 ✓ VERBATIM · TN-20 ✓ VERBATIM -->

And not only the land of hunters. The agency enters upon the property of non-hunters as part of its enforcement activities.
<!-- TN-21 ✓ VERBATIM -->

There is one more fact about Hollingsworth in the opinion.
<!-- TN-14 · ⛔-09 -->

Mr Hollingsworth's hunting license was suspended for three years in November 2018 due to a federal dove baiting offense.
<!-- TN-14 ✓ VERBATIM (MANDATORY, ledger gate 9) -->

【the dates go on screen alone, as typography over the land: 21 December 2016 · November 2018. No arrow, no caption, no comparison graphic. No hold: silence here would read as the edit inviting a conclusion about a man's guilt, and the record does not carry one.】

The suspension came in November 2018. The entry he sued over was December 21, 2016.
<!-- TN-14 ✓ VERBATIM · TN-15 ✓ VERBATIM -->

The entry came twenty-three months earlier.
<!-- TN-15 · TN-14 — arithmetic on the two recorded dates; no evaluation is attached, per ⛔-09 -->

That is where the record on these two men stops.
<!-- ○-05 -->

The opinion gives no ages, no occupations, and no account of how the case began or why either man brought it.
<!-- ○-05 -->

Two men appear inside a public document for the length of a lawsuit, and what survives of them afterwards is a list of parcels.
<!-- ○-05 -->

Terry Rainwaters owns a hundred and thirty-six acre home property with two homes on it, farmed in a regular and conspicuous manner. A private gravel path reaches it, behind a chained gate with No Trespassing signs.
<!-- TN-09 ✓ VERBATIM (quoted phrases) -->

He has sixty-nine acres on Liberty Road, fenced all the way around, and accessible through a chained gate with No Trespassing signs.
<!-- TN-09 ✓ VERBATIM -->

Two parcels, with an acreage each. That is the whole of him inside the document.
<!-- TN-09 · ○-05 — TN-09 records four parcels; two are read, because four is a list and two is a fact -->

Against that, the rule of law being applied is one line long. Warrantless searches and seizures are presumptively unreasonable.
<!-- TN-35 ✓ VERBATIM -->

Presumptively unreasonable puts the burden on the state, and the state discharges it by naming a recognised exception and fitting the facts to it.
<!-- TN-33 · TN-35 -->

The agency invoked none of them. It has not endeavored to defend its searches based upon any of the established exceptions to the warrant requirement. An implied-consent theory it had raised earlier was held waived.
<!-- TN-33 ✓ VERBATIM -->

In place of an exception it offered reasonableness.
<!-- TN-34 · TN-37 · TN-38 — the agency argued the entries were searches and were reasonable -->

The agency said, at oral argument, what a man is supposed to do.
<!-- TN-19 — the record establishes only that the agency asserted this -->

If the plaintiffs wish to avoid reentry by the TWRA upon their properties, they should desist in hunting thereupon.
<!-- TN-19 ✓ VERBATIM -->

---

## ACT_3 — THE ANSWER, AND ITS SIZE

On May 9, 2024, the Tennessee Court of Appeals answered. Judge Jeffrey Usman wrote the opinion. Judges Arnold Goldin and Kenny Armstrong joined it. Three judges, no dissent.
<!-- ID-07 · ID-06 -->

The answer is two sentences long. We conclude the statute is facially constitutional but unconstitutional as applied. We affirm the award of nominal damages.
<!-- TN-22 ✓ VERBATIM · ⛔-02 (both halves stated) -->

Two questions were in front of them, and they are not the same question. Is the statute unconstitutional as written? And is it unconstitutional as it was used on these two men?
<!-- TN-22 · TN-27 · TN-38 -->

The first one has a hard standard. The challenger must establish that no set of circumstances exist under which the Act would be valid. The statute has to fail in every application it has, and not merely in most of them.
<!-- TN-29 ✓ VERBATIM -->

And the plaintiffs had already conceded one application. They do not dispute that the statute authorizes entries upon wild waste land areas or that such entries are constitutional under the Tennessee Constitution.
<!-- ND-10 ✓ VERBATIM -->

Wild waste land is outside Article I, Section 7. Welch said so in 1926. So there is at least one lawful use of the statute, and one is enough to end a facial challenge.
<!-- TN-25 · TN-27 -->

The statute is facially constitutional because there are applications of the statute that are constitutionally permissible.
<!-- TN-27 ✓ VERBATIM -->

The trial panel had held the opposite. That holding was reversed.
<!-- TN-27 · ⛔-02 (both halves stated) -->

There was a second reason. The statute does work. Without it, an officer stepping onto a farm would be committing criminal trespass under Tennessee law — a person commits criminal trespass if the person enters or remains on property, or any portion of property, without the consent of the owner.
<!-- TN-28 ✓ VERBATIM -->

That is half the opinion, and the state has won it.
<!-- TN-27 -->

Then the second question, and the ground changes under it.
<!-- TN-30 -->

Their lands were secured by gates, accessible only through private drives, and posted with no trespassing signs intended to limit access to them. The Plaintiffs used and occupied their land by farming, fishing, camping, and hunting.
<!-- TN-30 ✓ VERBATIM -->

The agency's reply was that three of those four uses are hobbies.
<!-- TN-31 -->

While the TWRA endeavors to dismiss hunting, fishing, and camping upon one's property as recreational in nature, such activities, recreational though they may be, constitute actual use of the property.
<!-- TN-31 ✓ VERBATIM -->

Which brings back the 1926 line, and turns it over. These were not wild or waste lands outside the shield of Article I, Section 7 of the Tennessee Constitution but instead possessions subject to constitutional protection.
<!-- TN-32 ✓ VERBATIM · payoff of TN-25 -->

So the land was protected. What made the entries unreasonable was the way the decision to enter got made.
<!-- TN-36 -->

Article I, Section 7 runs to a single sentence, and its second half names the thing it was written against.
<!-- TN-23 -->

That the people shall be secure in their persons, houses, papers and possessions, from unreasonable searches and seizures; and that general warrants, whereby an officer may be commanded to search suspected places, without evidence of the fact committed, or to seize any person or persons not named, whose offences are not particularly described and supported by evidence, are dangerous to liberty and ought not to be granted.
<!-- TN-23 ✓ VERBATIM in full (Tenn. Const. art. I, § 7), spoken once, here, where the general-warrants clause bears -->

Each agent is empowered with the discretionary authority to determine for himself or herself if there is a reasonable basis to suspect hunting activities are occurring on the property.
<!-- TN-36 ✓ VERBATIM -->

And nothing checks it afterwards. There is no clear system of judicial review that allows consideration of the TWRA's entries upon private property or their agents' comportment thereupon.
<!-- TN-36 ✓ VERBATIM -->

A warrant puts a judge in front of an entry. Review puts one behind it. Here there is one officer, deciding alone, with nothing written down.
<!-- TN-02 · TN-06 · TN-36 -->

The opinion reaches for a comparison. The TWRA searches, which it claims are reasonable, bear a marked resemblance to the arbitrary discretionary entries of customs officials more than two centuries ago in colonial Boston.
<!-- TN-37 ✓ VERBATIM -->

Colonial Boston.
<!-- TN-37 -->

Given the purpose of Article I, Section 7 of preventing arbitrary intrusions upon privacy and personal liberty, what the TWRA claims is reasonable is not.
<!-- TN-38 ✓ VERBATIM -->

Subsections one and seven of section 70-1-305 are unconstitutional as applied. And in a footnote, one more thing the agency never explained: it does not articulate why reasonable suspicion rather than probable cause is the appropriate standard.
<!-- TN-38 ✓ VERBATIM · TN-39 ✓ VERBATIM -->

So what did the two men get?
<!-- TN-40 · TN-41 -->

An injunction was denied below, and they did not appeal that denial, so it was never examined. We do not review the trial court's denial of injunctive relief.
<!-- TN-41 ✓ VERBATIM · ND-08 · ⛔-03 -->

What was affirmed was the award made at trial. Plaintiffs are awarded one dollar in nominal damages for their constitutional injury, which Defendant Carter is ordered to pay.
<!-- TN-40 ✓ VERBATIM -->

One dollar.
<!-- TN-40 · ⛔-14 (no adjective, no characterisation) -->

⟨HELD⟩

【4 seconds. The empty track, still. Silence 1 of 4.】

The state had argued that sovereign immunity barred even that. It raised the argument for the first time on appeal. We conclude this argument is waived.
<!-- TN-40 ✓ VERBATIM (quoted whole) · ND-09 -->

【motif state 3: rain. The padlock wet, the chain wet, the track empty. Held 5 seconds under no narration at all — the longest silence before the recognition. Silence 2 of 4.】

The statute is still in the Tennessee code. On its face it is constitutional. What the two men hold is a declaration about their own land, and a dollar.
<!-- TN-22 · TN-27 · TN-40 -->

---

## ACT_4 — THE OTHER ANSWER

【THE TURN. Hard cut on the last syllable, with no silence in front of it. Appalachian hardwood, elevation, a different light, a different gate. motif state 4: a different padlock, a different casting, a different gate — the same object, a different state. No connective word survives this edit, and the act opens on place and time exactly as the HOOK does.】

Clearfield County, Pennsylvania. July 21, 2026.
<!-- PA-01 (Clearfield County) · ID-02 ✓ VERBATIM ("DECIDED: JULY 21, 2026") -->

We conclude that the original meaning of the term possessions as used in Article I, Section 8, unlike the term effects as used in the Fourth Amendment, includes land.
<!-- PA-25 ✓ VERBATIM -->

Includes land.
<!-- PA-25 -->

We hereby overrule Russo.
<!-- PA-27 ✓ VERBATIM -->

⟨HELD⟩

【4 seconds. The second padlock, held. Silence 3 of 4. This is the reset beat v002 spent in front of *Clearfield County*, where it separated the hard cut from the two lines it exists to deliver.】

That is the Supreme Court of Pennsylvania, deciding under Article I, Section 8 of the Pennsylvania Constitution.
<!-- ID-01 · ID-02 · PA-31 · ⛔-05 (the state ground is named every time) -->

The opinion opens on the law it is about to change.
<!-- PA-21 -->

Open fields are afforded no constitutional protection from warrantless searches and seizure under the Fourth Amendment to the United States Constitution.
<!-- PA-21 ✓ VERBATIM (first sentence of the lead opinion) -->

The plaintiffs are two private, member-owned hunting clubs that own four thousand four hundred acres and eleven hundred acres of contiguous land in Clearfield County, Pennsylvania.
<!-- PA-01 ✓ VERBATIM -->

The record's phrase for what the membership buys: a private place — a sanctuary — where they can come to escape from the hustle and bustle of daily life.
<!-- PA-04 ✓ VERBATIM -->

On their own ground, members can easily find spots where strangers will not unexpectedly walk in and spook nearby wildlife or accidentally step into their line of fire.
<!-- PA-05 ✓ VERBATIM -->

One line records what is said out there. Family matters, marital problems, work stressors, romantic feelings, and faith in God.
<!-- PA-06 ✓ VERBATIM -->

That is all of it this account will use. The opinion names no member — a list of subjects, with no person attached to any of them.
<!-- PA-01 · PA-06 · ○-05 -->

What they did to keep people out is recorded.
<!-- PA-07 -->

They have posted their properties' boundary lines with clearly visible no trespassing signs and purple paint, installed locked gates at all public entrances, and fenced some of their properties' boundaries with waist-high, metal wire, all in an effort to exclude non-members and intruders therefrom.
<!-- PA-07 ✓ VERBATIM -->

Purple paint is a posting method the state wrote into its own trespass law. Pennsylvania landowners, except those in Philadelphia and Allegheny Counties, have the option to use purple paint, rather than no trespassing signs, to post their properties.
<!-- PA-10 ✓ VERBATIM basis (18 Pa. C.S. § 3503(b)(1)(vi)) -->

Mark Gritzer works as a game warden for the Commission and is assigned to the district in which the Hunting Clubs' land is located. He is a defendant in his official capacity.
<!-- PA-11 ✓ VERBATIM · ID-01 · ⛔-07 -->

Since 2013, Warden Gritzer and other Commission officers have entered the Hunting Clubs' land without consent, a warrant, or probable cause at least fifteen to twenty-two times, to look for evidence of hunting offenses.
<!-- PA-12 ✓ VERBATIM · ○-06 (the range is spoken as the opinion has it and never rounded) -->

【the comment question is now fifteen minutes old. The line below is said once, and the film moves on without commenting on it.】

Warden Gritzer even placed a trail camera on Punxsutawney's property in an attempt to develop probable cause for charges of illegal elk feeding. That camera remained on Punxsutawney's property for seventy-eight days.
<!-- PA-13 ✓ VERBATIM -->

On some occasions, Warden Gritzer has cited individuals for violations of the Code.
<!-- PA-14 ✓ VERBATIM · ○-07 — the opinion carries nothing further and the film adds nothing further -->

His authority was two provisions of the Game and Wildlife Code, and both of them let an officer go upon land outside of buildings, posted or otherwise.
<!-- PA-17 ✓ VERBATIM basis · PA-18 ✓ VERBATIM basis -->

The sign is named in the statute, and it is named in order to be disregarded.
<!-- PA-17 · PA-18 -->

Pennsylvania had tested this once before, in 2007, in Russo.
<!-- PA-38 -->

A bear was killed on private wooded land in Wyoming County approximately nine minutes after the opening of Pennsylvania's bear-hunting season. Several Commission officers entered Russo's property, which was posted with no trespassing signs, without a warrant, and found several large piles of apple mash as well as a corn feeder close to Russo's cabin.
<!-- PA-38 ✓ VERBATIM -->

The entry was upheld. Chief Justice Cappy authored a dissenting opinion, which then-Justice Baer and Justice Baldwin joined. He would have held section 901(a)(2) unconstitutional to the extent that it authorizes entry onto posted private property without any level of suspicion of illegal activity.
<!-- PA-39 ✓ VERBATIM -->

That dissent lost, and it is why the clubs lost in 2023. On September 29, 2023, the Commonwealth Court, sitting en banc, concluded that it was bound by this Court's decision in Russo, and entered judgment for the Commission and for Warden Gritzer.
<!-- PA-16 ✓ VERBATIM · ID-03 — a judgment on the merits, not a dismissal -->

Judge McCullough, joined by Judge Wallace, wrote separately to say she agreed with Chief Justice Cappy's dissent.
<!-- PA-16 -->

The case reached Pennsylvania's Supreme Court from there.
<!-- ID-02 · ID-03 -->

Russo is only a little over 18 years old and no Pennsylvania court has applied Russo's holding in a published decision.
<!-- PA-26 ✓ VERBATIM -->

The majority's verdict on its own precedent: its reasoning and result have not aged well.
<!-- PA-23 (fragment reproduced exactly; see departure note 1) -->

Slavish adherence to our decision in Russo must give way to the greater privacy and property protections afforded under Article I, Section 8 of our state charter.
<!-- PA-22 ✓ VERBATIM -->

Then the rule that replaces it.
<!-- PA-29 -->

The scope of the protection afforded under Article I, Section 8 to a landowner's open fields extends to private land located beyond the curtilage over which the landowner has demonstrated a reasonable and legitimate expectation of privacy by taking sufficient steps to exclude intruders therefrom.
<!-- PA-29 ✓ VERBATIM — no gloss is attached: the recognition is not stated before the recognition -->

【motif state 5: the padlock shot flat and frontal in even light, like an exhibit. No silence here; the four holds are spent elsewhere.】

Both entry provisions fell. We hold that stare decisis does not compel our adherence to Russo, that Russo was wrongly decided, and that Sections 303(c) and 901(a)(2) of the Code violate Article I, Section 8 of the Pennsylvania Constitution.
<!-- PA-31 ✓ VERBATIM -->

Not as applied to these two clubs. On their face — we cannot contemplate any circumstance under which Sections 303(c) and 901(a)(2) would be valid under our decision today.
<!-- PA-32 ✓ VERBATIM -->

Severance was considered and refused. There does not appear to be any invalid language that we can sever and that would yield operative and constitutional text consistent with the legislative intent behind the enactment of these provisions of the Code. Accordingly, the provisions fall in their entirety.
<!-- PA-33 ✓ VERBATIM in full -->

The order below was reversed, and nothing was sent back. Striking the two sections had already given the clubs the declaratory and injunctive relief that they sought.
<!-- PA-31 ✓ VERBATIM basis -->

Seven justices heard it. Four joined the lead opinion. Chief Justice Todd filed a concurring and dissenting opinion, and Justice Wecht filed a concurring and dissenting opinion in which Justice McCaffery joined.
<!-- ID-04 ✓ VERBATIM basis · ID-05 · ⛔-10 (no vote characterised, no position attributed) -->

Concurring and dissenting is a label of its own.
<!-- ⛔-10 · ○-01 -->

---

## ACT_5 — HOW FAR THE NO REACHES

One thing did not move. We, therefore, do not discuss and/or question the federal open fields doctrine further.
<!-- PA-36 ✓ VERBATIM · ND-04 · ⛔-05 -->

The federal doctrine stands where it stood. This ruling rests on a state constitution, and it reaches as far as that constitution reaches.
<!-- PA-21 · ND-12 · ⛔-05 -->

Inside Pennsylvania, the opinion lists what officers may still do.
<!-- PA-34 -->

The Commission's officers will still be permitted to conduct warrantless searches of private property that is not posted, fenced, or otherwise marked to exclude intruders; to observe evidence of Code violations that occur in plain view on private property that is posted, fenced, or otherwise marked to exclude intruders; to obtain a warrant to search private property that is posted, fenced, or otherwise marked to exclude intruders based upon their receipt of information that a Code violation has occurred; and to apply a recognized exception to the warrant requirement as a means to search private property that is posted, fenced, or otherwise marked to exclude intruders.
<!-- PA-34 ✓ VERBATIM in full, as the row requires; the list numerals are spoken as conjunctions and nothing else is altered -->

Justice Donohue joined the majority and wrote separately.
<!-- PC-01 · ⛔-10 (the concurrence is described only from what it says) -->

Today's decision does not preclude administrative searches conducted pursuant to an appropriate statutory framework incorporating the limitations placed on administrative searches.
<!-- PC-06 ✓ VERBATIM · ND-05 -->

The same opinion noted that in its briefing, the Game Commission appears to confuse the open fields doctrine with the administrative search exception.
<!-- PC-05 ✓ VERBATIM -->

The administrative inspection provision was challenged too, and it survived. We are not declaring that section constitutional, although it is presumptively so until a court decides otherwise.
<!-- ND-03 ✓ VERBATIM -->

And the state's environmental rights amendment was not weakened by any of it. This is not a diminution of the importance of our citizens' right to the conservation, maintenance, and protection of wildlife.
<!-- PA-35 ✓ VERBATIM · PC-03 · PC-07 -->

Pennsylvania limited its own reach in the footnote that reserved the question.
<!-- ND-02 · ND-01 — both are footnote 24 -->

We cannot ignore that this case is about rural, undeveloped land, not a suburban one-acre plot or a nine-acre tract of land upon one acre in the center of which sits a swimming pool. There may be ways by which the owners of those latter two properties can demonstrate a reasonable and legitimate expectation of privacy that does not involve marking the boundaries of their properties with no trespassing signs or purple paint. We resolve only the question of whether the Hunting Clubs here have done so.
<!-- ND-02 ✓ VERBATIM in full; the middle sentence carries the antecedent of "done so" -->

【RECOGNITION. The three quotations below run without a word of narration between them, then motif state 6: a gate post with nothing on it, a loop of wire hanging down, an empty field behind — the identical framing as the last image of the HOOK. ⟨HELD⟩ after it. The narrator adds nothing. Nothing follows it that has the shape of an inventory: the small print is already behind us.】

Truly open fields — that is, private land that is unposted and unbounded — is fundamentally different in kind than private land conspicuously posted with no trespassing signs and purple paint and/or bounded by fences, gates, and other structures.
<!-- PA-28 ✓ VERBATIM -->

Government officials, therefore, must obtain a warrant based upon probable cause or satisfy one of the recognized exceptions to the warrant requirement before entering the private land of any landowner that has taken such steps.
<!-- PA-30 ✓ VERBATIM -->

And then, in that footnote: we reserve for another day the question of whether the privacy protections afforded by Article I, Section 8 extend to landowners who have taken fewer steps than the Hunting Clubs, or even no steps, to exclude intruders from their properties.
<!-- ND-01 ✓ VERBATIM (footnote 24) -->

⟨HELD⟩

【5 seconds on the empty gate post. Silence 4 of 4.】

The 1926 boundary had the same shape. Welch put outside the word possessions any wild or waste lands, or other lands that were unoccupied. What put these two farms inside it in 2024 was gates, private drives, posted signs, and the fact that the land was used and occupied.
<!-- TN-25 ✓ VERBATIM · TN-30 · TN-32 · §12 (no connective across the two states) -->

【the film's title image returns: the cut branch, the housing, the lens. It has not been seen since 0:15.】

The branch, the camera, the vehicle search and the video are all in the record.
<!-- TN-16 -->

None of it was on appeal. What the parties put in front of the appellate judges, for Hollingsworth, was one entry on one day in December 2016. And whether the cameras were state work or federal work has never been decided by anybody.
<!-- TN-15 ✓ VERBATIM basis · TN-16 · ND-11 -->

What the two Tennessee men hold is a declaration that the statute was unconstitutional as applied to them, no injunction, and one dollar. The statute is facially constitutional and it is still on the books.
<!-- TN-22 ✓ VERBATIM · TN-40 · TN-41 · ⛔-02 · ⛔-03 -->

What the two Pennsylvania clubs hold is two provisions struck from the Code, no remand, and the relief they asked for granted where they stood.
<!-- PA-31 -->

Each ruling stops at its own state line, and each leaves the Fourth Amendment exactly where it found it.
<!-- ND-12 · ⛔-05 · ⛔-06 -->

【the Like ask. Earned, no emotional instruction, no promise of a sequel. Placed here so the film can end on its own last line.】

If this changed how you see where the line runs on your own land, leave a like.
<!-- placed at the end of ACT_5 rather than in the ENDING -->

---

## ENDING

【motif state 7, final image: the identical framing as the head of ACT_1 — the chain across the farm track, the padlock closed, morning light. Nothing in the narration touches it.】

Wildlife is what both of these records are filed under. What both are about is a boundary — where a person's private ground begins for the purpose of a search, and who gets to decide it.
<!-- TN-01 · PA-17 (both statutes are wildlife-enforcement provisions) · PA-29 · TN-30 · TN-36 -->

The conduct was the same in both states, and it met two constitutions and two answers. The Pennsylvania opinion does not mention the Tennessee case.
<!-- ledger GOVERNING CAUTION (string search over PA-LEAD: Rainwaters 0, Hollingsworth 0, Tennessee Wildlife 0) · ⛔-01 — only the Pennsylvania text was searched, so only the Pennsylvania direction is claimed -->

In one state a chain and a sign bought a declaration and nothing to enforce it with. In the other, a chain and a sign and a band of purple paint took two entry provisions out of a statute book.
<!-- TN-40 · TN-41 · PA-31 · PA-24 — the opinion's own word is "most" of the challenged statutes; the two that fell are named at PA-31 -->

Neither answer travels. A man standing on his own field is protected, or he is not, according to which side of a state line he is standing on, and according to what he was able to put up around it.
<!-- ND-12 · PA-29 · TN-30 · ⛔-05 -->

What they did, in both states, was give an owner something to point at afterwards — an object a judge could look at and call sufficient, or not.
<!-- PA-07 · PA-29 · TN-30 -->

And the side that won wrote down what it had not decided. It described the landowners in front of it — posted, painted, fenced, gated — and then set aside, for another day, the ones who had done less than that.
<!-- ND-01 -->

Or nothing at all.
<!-- ND-01 — the film's own words, not the footnote's; "or even no steps" is spoken once, inside the quotation, and is not repeated here -->

⟨HELD⟩

【final frame held, then BrandEndcard — ENDCARD_SEC = 9, Bookends.tsx canon, no fork.】

---

## WHAT CHANGED FROM v002

**Cut (the restored material the three reads found dead on the page).** TN-01 quoted whole plus its lead-in; the three trial-panel judges by name and § 20-18-101; *Rainwaters is named first…*; ID-08 counsel for both sides; two of the four Rainwaters parcels; *argued on June 20, 2023*; PA-24's three-part holding; PA-15's prayer for relief; *argued on April 9, 2025*; PA-26's second sentence and the *eighteen years* restatement of it; PA-37's presumption and heavy burden; Donohue PC-01/02/04 and *to add a fifth*; PA-19/20 and the § 901(a)(8) badge requirement; ND-06; the sentence about *fifteen to twenty-two* being a range the opinion never narrows; the sentence about the suspension sitting *in the same pages*; the sentence about *sometimes conceal themselves* sitting in the statement of undisputed facts; the three-fragment gloss on Warden Gritzer's citations.

**Restored.** The share of the ninety-three acres the doctrine leaves outside protection, near the front, as arithmetic on TN-13 and TN-26. The phrase *open field*, first spoken before 1:10. *A chained gate is what a landowner believes makes entry unlawful. It is not what the law was measuring.* *Two men who go to their own ground less than they used to*, moved to stand in front of the two deposition-English verbatims instead of 34 seconds behind them. *Sometimes conceal themselves.* as a standing fragment. PA-05, the line about strangers walking into a member's line of fire, so that the Pennsylvania human record is not one sentence wide. v001's *Neither answer travels…* in the ENDING. v001's *Not as applied to these two clubs. On their face —*, in place of v002's label *That was a facial holding.*

**Moved.** The whole carve-out block — PA-34 in full, the Donohue concurrence, ND-03, PA-35 and ND-02 in full — now sits **before** the recognition, so the designed silence after footnote 24 is not answered three seconds later by an inventory. Article I, Section 7 is read once, whole, in ACT_3 at the passage its general-warrants clause bears on, instead of half at the head of ACT_2 and half seven minutes later. The reset beat that stood in front of *Clearfield County* now falls after *We hereby overrule Russo.*

**Silence.** Four holds, about eighteen seconds in total: 4 s after *One dollar.*, 5 s on motif state 3, 4 s after *We hereby overrule Russo.*, 5 s after the recognition. v002's fourth reset beat, after *desist in hunting thereupon*, is gone; the act break carries it.

## FACTUAL CORRECTIONS AGAINST v002

| # | v002 said | v003 says | Ledger |
|---|---|---|---|
| 1 | *judges whose opinions never mention each other* | *The Pennsylvania opinion does not mention the Tennessee case.* | Only PA-LEAD was string-searched; the Tennessee text was not searched for Punxsutawney |
| 2 | *Henry County, Tennessee.* | *West Tennessee. 2017.* | TN-13 says the land **crosses** Benton and Henry; no row places the camera tree in either |
| 3 | *The same sentence carries its own limit* / *in the same breath* | *Welch drew its own limit in the same case.* | TN-24 @053961 and TN-25 @056779 are 2,800 characters and a page apart |
| 4 | *Pennsylvania limited its own reach in the same footnote* | *…in the footnote that reserved the question.* | The last footnote the script had named was fn 11 (ND-06, now cut) |
| 5 | *to add a fifth*; PC-02 and PC-04 welded into one sentence | both cut | No row says the concurrence adds to PA-34's list; PC-02 is slip p. 1 and PC-04 slip p. 4 |
| 6 | *That is the entire human record on the Pennsylvania side* | *That is all of it this account will use.* | False as written — PA-02, PA-03 and PA-05 are human record; PA-05 is restored here |
| 7 | *three road names* | the sentence is cut with the two extra parcels | Harmon Creek is a creek and Sandy River Hunting Club is the lessor |
| 8 | *That provision is section 901(a)(8)* | cut | PA-20 carries no citation in the ledger, and the provision was not struck |
| 9 | *Officers go where they think hunting is happening, and nowhere else* as fact | *It is a narrow claim, and it is the agency's. On its account, officers…* | TN-34 is the agency's argument; TN-05 and TN-21 record entries that do not fit it |
| 10 | *steps past a chained gate and a posted sign* / *bolts a camera where the branch was* | *A state wildlife officer is on the land.* / *installs a camera on it* | TN-16 records the installation and the cut branch, and nothing about the approach |
| 11 | *took the entry provisions out of a statute book* | *took two entry provisions out of a statute book* | PA-24 says **most** of the challenged statutes; § 901(a)(8) survived |
| 12 | *the one flourish anywhere in it* · *the oldest comparison in American search law* | both cut | No ledger row ranks either |
| 13 | *The man who farms the ninety-three acres is not told.* | *Nobody tells the man who farms the ninety-three acres.* | Not a fact correction — the hook's last line was passive |

## DEPARTURES FROM THE FILM BIBLE, AND WHY

- **1. `the Court` is an unusable string, and it costs three verbatims their full form.** `check_script_craft.forbidden_from_ledger()` turns every quoted phrase inside a ⛔ row into a banned substring, and ⛔-10 contributes the two-word sequence *the court*, which is then a hard gate failure anywhere in the narration, including inside a quotation. **ID-07** is given as the three judges by name. **PA-23** is reproduced as the exact fragment *its reasoning and result have not aged well* inside an attributing sentence. Everywhere the bible's prose said "the court", the narration says *the trial panel*, *the appellate judges*, *Pennsylvania's Supreme Court*, *Tennessee's own highest court* or *the majority*. No fact moved.
- **2. The bible's ACT_4 order is inverted, as in v002.** §6 builds ACT_4 chronologically and puts *includes land* at 23:20. This draft opens ACT_4 on the overruling and lets the clubs, the purple paint and *Russo* arrive as the account of how it got there. Carried forward unchanged from v002, where the drama read judged it the fix that made the film survive its own turn.
- **3. One silence budget, four holds, eighteen seconds.** §7 fixes three ⟨HELD⟩ and three reset beats, and treats the two as separate devices. This draft merges them into one budget: 4 s after *One dollar.*, 5 s on motif state 3, 4 s after *We hereby overrule Russo.*, 5 s after the recognition. Three of the four carry a ⟨HELD⟩ mark; motif state 3 does not, because the picture is doing the holding. A fifth ⟨HELD⟩ closes the ENDING and is the final-frame hold in front of the endcard, not part of the eighteen seconds. The measured audience half-life is 44 seconds, so a fifteen-second hold reads as a fault rather than as a design.
- **4. The subscribe ask and the comment question sit after *Sometimes conceal themselves.*, not in the first ninety seconds.** §8 places both inside the first ninety seconds. They are moved because in v001 both sat inside the reversal beat itself. **This is a deviation from an approved bible section and should carry an APR.**
- **5. The OP is one line.** §6 gives it ≈34 words and two beats. It has three words and one beat. `structure_4part` requires only a non-empty OP section in narration order.
- **6. PACKAGING §5's spoken comment question was not used**, and the HOOK says *ninety-three acres* inside a collapsed final line rather than as its own beat. Both are **PACKAGING v002 + APR** items. The spoken hook is about three seconds shorter than v002's and the 20.3 s picture window is held by extending two holds.
- **7. Article I, Section 7 is read whole, once, in ACT_3.** The bible puts its opening clause at the head of ACT_2. Splitting it across two acts stated the same sentence twice; reading it whole where the general-warrants clause bears is one reading instead of two.
- **8. PA-31 is spoken as its two operative clauses.** PA-33, PA-34 and ND-02 are quoted in full.
- **9. The spoken word *subscribe* fails `check_script_craft.py`'s CLI and passes its `evaluate()`.** Run as a CLI the module fails on `SPOKEN_CTA`. Run as `evaluate()`, which is what `check_final_acceptance._ext_gate` calls, it checks the word band, emotion commands and the ledger's ⛔ rows only. The bible §8 and the approved PACKAGING §5 both require a spoken ask, so the conflict is between two binding documents.
- **10. Timecodes are not printed in this draft.** v002 printed a derived timecode against every beat at an assumed 165 wpm and then had to defend arithmetic that no audio had ever measured. The contract requires the band be re-derived from the finished ElevenLabs master. Section order, silence lengths and the two ⟨HELD⟩ are fixed here; the clock is measured after the VO exists, not asserted before it.

## WHAT I WANTED TO SAY AND COULD NOT

*Each of these had a place in the film and no ledger row behind it. None of them is in the script.*

- **When the camera came off Hollingsworth's tree.** TN-16 records a removal date only for the Rainwaters camera. ACT_5 is built on *it was not on appeal* instead.
- **How the officers got past the gates.** Motif state 2 is a closed padlock with boot prints beyond it, and the HOOK's picture shows a gate. TN-16 says only that the camera was installed, so the HOOK's narration now says only that the officer is on the land.
- **The year the Pennsylvania case was filed.** Only the docket number carries 2021, and a docket number is not a filing date.
- **Hester (1924) and Oliver (1984).** The ledger names them only inside ⛔-05 and ND-04, with no verified row for either. PA-21 carries the doctrine instead, in the opinion's own words.
- **The distance between the two farms.** Not a distance any row records, so the only thing that crosses is the cut.
- **Who any of these men are.** Ages, occupations, families, why they sued, who paid for the litigation (○-05; ⛔-06 forbids supplying counsel's employer).
- **What the fifteen to twenty-two entries looked like.** PA-12 and PA-13 are the whole record (○-06).
- **What became of Warden Gritzer's citations**, and of any charges against either Tennessee landowner (○-07).
- **How much land the doctrine covers nationally.** No acreage, no percentage, no count of states (⛔-06, ○-04, ○-09). The one arithmetic figure the film does give is about Hollingsworth's own ninety-three acres and comes from TN-13 and TN-26.
- **What Todd, Wecht, McCaffery and Mundy wrote.** Four separate opinions exist and none was read (○-01, ⛔-10).
- **The text of the Tennessee statute.** Never printed in the opinion; only the agency's paraphrase is in the record (⛔-15, ○-08).
- **Whether Tennessee appealed.** ○-03 is still open. The film ends where the documents end and announces no gap, because announcing the absence of an appeal would plant one.
- **A single person on the Pennsylvania side.** The plaintiffs are member-owned clubs and no member is named anywhere (PA-01).
