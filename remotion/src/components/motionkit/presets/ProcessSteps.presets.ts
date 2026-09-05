import type {ComponentProps} from 'react';
import type {ProcessSteps} from '../ProcessSteps';

/**
 * ProcessSteps preset catalog — reusable "how it worked" flows for Prime
 * Documentary. Each preset is a generic, educational 3–5 step explainer of a
 * mechanism (a scheme, a legal process, a con) with NO real names, so it can be
 * dropped into any episode that needs to explain how something functioned.
 *
 * Usage: <ProcessSteps {...processStepsPresets['ponzi-scheme']} />
 * Timing (`dur`) is intentionally omitted so the component auto-fits the flow to
 * the composition; only set it when a shot needs a fixed on-screen duration.
 */
export const processStepsPresets = {
  // ── Financial fraud: how the money moved ────────────────────────────
  'ponzi-scheme': {
    steps: [
      {title: 'The Promise', desc: 'An operator pitches steady, above-market returns that never seem to lose.'},
      {title: 'Early Investors Paid', desc: 'The first backers are paid — but from later investors’ cash, not real profit.'},
      {title: 'Word Spreads', desc: 'Happy returns attract more money; the incoming flow keeps the illusion alive.'},
      {title: 'No Real Investment', desc: 'Little or nothing is actually invested; the books are fabricated.'},
      {title: 'The Collapse', desc: 'When withdrawals outpace new money, the scheme runs dry and falls apart.'},
    ],
  },
  'pyramid-scheme': {
    steps: [
      {title: 'Buy In', desc: 'A recruit pays a fee to join and is promised income from selling and recruiting.'},
      {title: 'Recruit Below You', desc: 'Real money comes from signing up new members, not from any product.'},
      {title: 'Money Flows Up', desc: 'Each layer’s fees flow upward to the people who joined earlier.'},
      {title: 'The Math Runs Out', desc: 'Recruitment must grow forever; the base cannot expand fast enough.'},
      {title: 'Bottom Layers Lose', desc: 'The newest and largest tier is left holding the losses.'},
    ],
  },
  'money-laundering': {
    steps: [
      {title: 'Placement', desc: 'Dirty cash enters the financial system through deposits or cash-heavy businesses.'},
      {title: 'Layering', desc: 'Funds are moved through transfers, shells and accounts to blur their origin.'},
      {title: 'Integration', desc: 'The money returns as clean-looking assets, salaries or investments.'},
    ],
  },
  'shell-company-fraud': {
    steps: [
      {title: 'Form a Shell', desc: 'A company is registered on paper with no real staff or operations.'},
      {title: 'Move Money Through It', desc: 'Invoices and transfers give illicit funds a legitimate-looking purpose.'},
      {title: 'Hide the Owner', desc: 'Nominees and layered entities conceal who actually controls the cash.'},
      {title: 'Withdraw Clean', desc: 'Funds re-emerge as loans, fees or dividends that appear ordinary.'},
    ],
  },
  'wire-fraud-sting': {
    steps: [
      {title: 'The Hook', desc: 'A convincing story reaches the target by phone, email or message.'},
      {title: 'Build Urgency', desc: 'A deadline or threat pressures the victim to act before thinking.'},
      {title: 'Request a Transfer', desc: 'The victim is guided to wire money to an account the fraudster controls.'},
      {title: 'Vanish', desc: 'Funds are quickly moved onward and the trail goes cold.'},
    ],
  },
  'insider-trading': {
    steps: [
      {title: 'Get the Secret', desc: 'Someone learns material news the public does not yet know.'},
      {title: 'Trade Ahead', desc: 'They buy or sell before the news breaks, or tip someone who does.'},
      {title: 'Price Moves', desc: 'When the information becomes public, the stock jumps or drops.'},
      {title: 'Bank the Gain', desc: 'The early trade turns the secret into an unfair, illegal profit.'},
    ],
  },
  'accounting-fraud': {
    steps: [
      {title: 'Miss the Target', desc: 'Real results fall short of what investors were promised.'},
      {title: 'Cook the Books', desc: 'Revenue is inflated or expenses hidden to fake healthy numbers.'},
      {title: 'Pass the Audit', desc: 'Complex entries and pressure keep reviewers from catching the gap.'},
      {title: 'The Gap Widens', desc: 'Each quarter needs a bigger lie to cover the last one.'},
      {title: 'Exposure', desc: 'A whistleblower, short-seller or cash shortfall finally reveals the hole.'},
    ],
  },

  // ── The con: how a swindle was run ──────────────────────────────────
  'the-con': {
    steps: [
      {title: 'Pick the Mark', desc: 'The con artist studies a target’s needs, hopes and blind spots.'},
      {title: 'Build Trust', desc: 'A credible persona and small favors lower the mark’s guard.'},
      {title: 'The Setup', desc: 'An irresistible opportunity is dangled, timed to feel exclusive.'},
      {title: 'The Sting', desc: 'The mark hands over money or access at the decisive moment.'},
      {title: 'The Blow-Off', desc: 'The con artist disappears before the victim realizes what happened.'},
    ],
  },
  'fake-heiress': {
    steps: [
      {title: 'Invent a Fortune', desc: 'A fabricated identity claims vast wealth just out of reach.'},
      {title: 'Live the Part', desc: 'Lavish spending and name-dropping make the story look real.'},
      {title: 'Borrow on Image', desc: 'The persona secures loans, favors and free luxury on future promises.'},
      {title: 'Stall the Bill', desc: 'Excuses and forged documents delay every payment that comes due.'},
      {title: 'The Unraveling', desc: 'A bounced payment exposes that the fortune never existed.'},
    ],
  },
  'romance-scam': {
    steps: [
      {title: 'Perfect Match', desc: 'A fake profile mirrors the target’s ideal partner.'},
      {title: 'Fast Devotion', desc: 'Intense affection builds emotional dependence within weeks.'},
      {title: 'The Crisis', desc: 'A sudden emergency requires money the "partner" cannot access.'},
      {title: 'Keep Asking', desc: 'One request becomes many as the victim tries to protect the bond.'},
      {title: 'Silence', desc: 'Once the money stops, the persona disappears without a trace.'},
    ],
  },
  'counterfeit-operation': {
    steps: [
      {title: 'Copy the Original', desc: 'Genuine goods or documents are studied to reproduce every detail.'},
      {title: 'Mass Produce', desc: 'Fakes are manufactured cheaply and at scale.'},
      {title: 'Blend Into Market', desc: 'Counterfeits enter real supply chains beside authentic stock.'},
      {title: 'Cash Out', desc: 'Buyers pay genuine prices for goods worth a fraction.'},
    ],
  },
  'art-forgery': {
    steps: [
      {title: 'Choose a Master', desc: 'A forger targets an artist whose style and market are well known.'},
      {title: 'Fake the Work', desc: 'Period materials and technique are copied to fool the eye.'},
      {title: 'Invent Provenance', desc: 'A false ownership history makes the piece seem authentic.'},
      {title: 'Sell Through Experts', desc: 'Auction houses and dealers unknowingly lend it credibility.'},
      {title: 'Detection', desc: 'Science or a paper-trail flaw eventually unmasks the fake.'},
    ],
  },

  // ── Search & seizure: how a phone or home is searched ───────────────
  'phone-search-warrant': {
    steps: [
      {title: 'Establish Cause', desc: 'Investigators gather facts suggesting evidence lives on the device.'},
      {title: 'Apply to a Judge', desc: 'A sworn affidavit describes the phone and exactly what they seek.'},
      {title: 'Warrant Issued', desc: 'A neutral judge signs off, limiting the scope of the search.'},
      {title: 'Search the Device', desc: 'Only the authorized data is extracted and examined.'},
      {title: 'Evidence or Suppression', desc: 'What is found may be used — unless the search broke the rules.'},
    ],
  },
  'search-warrant-home': {
    steps: [
      {title: 'Probable Cause', desc: 'Police assemble evidence that a crime and its proof are at an address.'},
      {title: 'Judicial Review', desc: 'A judge weighs the affidavit and defines what may be searched and seized.'},
      {title: 'Execute the Warrant', desc: 'Officers enter within the warrant’s limits on place and time.'},
      {title: 'Seize and Log', desc: 'Listed items are collected and documented as evidence.'},
    ],
  },
  'traffic-stop-to-arrest': {
    steps: [
      {title: 'The Stop', desc: 'An officer needs reasonable suspicion to pull a vehicle over.'},
      {title: 'Observation', desc: 'What is in plain view or admitted can expand the encounter.'},
      {title: 'Probable Cause', desc: 'Clear evidence of a crime justifies a search or arrest.'},
      {title: 'Arrest and Rights', desc: 'The person is detained and read their rights before questioning.'},
    ],
  },
  'chain-of-custody': {
    steps: [
      {title: 'Collect', desc: 'Evidence is gathered, labeled and sealed at the scene.'},
      {title: 'Log Every Hand', desc: 'Each transfer records who held it, when and why.'},
      {title: 'Secure Storage', desc: 'Items stay in a controlled locker until needed.'},
      {title: 'Present in Court', desc: 'An unbroken record lets a judge trust the evidence is genuine.'},
    ],
  },

  // ── Courts & appeals: how a case climbs the system ──────────────────
  'appeal-to-supreme-court': {
    steps: [
      {title: 'Trial Verdict', desc: 'A case is decided in the trial court, creating the record.'},
      {title: 'Appeal Filed', desc: 'The losing side argues a legal error changed the outcome.'},
      {title: 'Appeals Court Rules', desc: 'A panel reviews the law — not the facts — and issues a decision.'},
      {title: 'Petition the Top Court', desc: 'A request asks the highest court to take the case.'},
      {title: 'Landmark Ruling', desc: 'If accepted, the court’s decision can bind the entire country.'},
    ],
  },
  'criminal-trial': {
    steps: [
      {title: 'Charges Filed', desc: 'Prosecutors formally accuse the defendant of a crime.'},
      {title: 'Jury Selected', desc: 'Both sides shape an impartial panel to hear the evidence.'},
      {title: 'The Trial', desc: 'Witnesses, exhibits and cross-examination test each side’s story.'},
      {title: 'Deliberation', desc: 'Jurors weigh the evidence against the standard of proof.'},
      {title: 'Verdict', desc: 'The jury decides guilt beyond a reasonable doubt — or acquits.'},
    ],
  },
  'grand-jury-indictment': {
    steps: [
      {title: 'Present Evidence', desc: 'Prosecutors show a citizen panel their case in secret.'},
      {title: 'Weigh Probable Cause', desc: 'Jurors decide only whether charges are justified, not guilt.'},
      {title: 'Vote to Indict', desc: 'A majority returns an indictment that formally starts the case.'},
    ],
  },
  'wrongful-conviction-exoneration': {
    steps: [
      {title: 'The Conviction', desc: 'A defendant is found guilty on flawed or mistaken evidence.'},
      {title: 'New Evidence', desc: 'DNA, a recantation or hidden files cast doubt on the verdict.'},
      {title: 'Reopen the Case', desc: 'Lawyers petition a court to re-examine the conviction.'},
      {title: 'Review the Facts', desc: 'Judges test whether the original trial can still stand.'},
      {title: 'Exoneration', desc: 'The conviction is vacated and the person is cleared.'},
    ],
  },
  'civil-asset-forfeiture': {
    steps: [
      {title: 'Property Seized', desc: 'Authorities take cash or goods they link to suspected crime.'},
      {title: 'Case Against the Object', desc: 'The action targets the property itself, not a convicted person.'},
      {title: 'Owner Must Fight Back', desc: 'The burden often falls on the owner to prove innocence.'},
      {title: 'Return or Keep', desc: 'The property is returned, or kept by the agency that took it.'},
    ],
  },
  'whistleblower-exposure': {
    steps: [
      {title: 'Witness Wrongdoing', desc: 'An insider sees fraud, danger or abuse from within.'},
      {title: 'Gather Proof', desc: 'Documents and records are quietly preserved as evidence.'},
      {title: 'Report It', desc: 'The insider brings it to regulators, press or the courts.'},
      {title: 'Investigation Opens', desc: 'Authorities test the claims and demand records.'},
      {title: 'Consequences', desc: 'Findings can trigger fines, charges or sweeping reform.'},
    ],
  },
  'data-breach-anatomy': {
    steps: [
      {title: 'Find a Way In', desc: 'Attackers exploit a weak password, bug or tricked employee.'},
      {title: 'Move Quietly', desc: 'They expand access while staying hidden inside the network.'},
      {title: 'Exfiltrate Data', desc: 'Sensitive records are copied out to attacker-controlled systems.'},
      {title: 'Discovery', desc: 'Unusual activity or a ransom note reveals the intrusion.'},
      {title: 'Fallout', desc: 'Victims are notified and regulators weigh the damage.'},
    ],
  },
} satisfies Record<string, ComponentProps<typeof ProcessSteps>>;
