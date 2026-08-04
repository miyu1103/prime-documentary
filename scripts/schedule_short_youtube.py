#!/usr/bin/env python3
"""Schedule a Short for future public publication on YouTube (privacy=private + publishAt).

Uploads the coverfirst render as PRIVATE with status.publishAt set to a future UTC time;
YouTube flips it to public automatically at that time. Sets the (<2MB) thumbnail via API.
Cover frame (bold thumbnail) is baked into the first 0.7s so the Shorts feed reads it too.

Usage: python scripts/schedule_short_youtube.py --short 09 --publish-at 2026-06-29T03:00:00Z [--dry-run]
(12:00 JST == 03:00Z. The owner's standing rule: schedule every day at 12:00 JST.)
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "scripts"))

from pd_factory.providers import load_env
from pd_factory.providers.youtube import _access_token
from upload_episode import CHANNEL_ALLOWLIST, get_channel_id, sha256_file, upload_chunks

OUT = ROOT / "remotion" / "out"

CONFIG: dict[str, dict] = {
    "01": {
        # destination for the funnel link; ensure_funnel_description() verifies it is public
        "longform": "cQFql7tT1fE",
        "ep": "PD-2026-001-miranda",
        "rev": "v001",
        "title": "Why Do Police Read You Your Rights? #Shorts",
        "description": (
            "Police read you your rights — and it isn't out of politeness.\n\n"
            "Decades ago, you could be questioned alone for hours, with no warning at all. Cornered, some "
            "people confessed to things they never did.\n\n"
            "In 1966, in Miranda v. Arizona, the Supreme Court drew a line: before questioning someone in "
            "custody, police must warn them of their rights — to stay silent, and to a lawyer.\n\n"
            "It isn't a courtesy. It's a fix built into the system. Without the warning, a confession can "
            "be thrown out of court. A few seconds changed every arrest in America.\n\n"
            "Watch the full story on the channel.\n\n"
            "#Shorts #Miranda #SupremeCourt #MirandaRights #Law #CriminalJustice #Documentary"
        ),
        "tags": ["Shorts", "Miranda", "Supreme Court", "Miranda Rights", "Miranda v Arizona", "Law", "Criminal Justice", "Documentary"],
        "video_sha256": "b691021c50cd7d7ab8a30a72c2d82019eced78bffcb8498e0c7390e1f4277978",
        "thumb_sha256": "3aca2e766115d5fc76cbe84e016c48e5790ddaae0bcf3f4cb0e75117404f6798",
    },
    "02": {
        # destination for the funnel link; ensure_funnel_description() verifies it is public
        "longform": "ch2hQ5jhDmQ",
        "ep": "PD-2026-002-gideon",
        "rev": "v001",
        "title": "Can't Afford a Lawyer? A Pencil Letter Changed Everything #Shorts",
        "description": (
            "If you can't afford a lawyer, does the court just give you one for free?\n\n"
            "One man was charged with a crime. Too poor to hire a lawyer, he asked the court for one — "
            "and was told no. He was convicted.\n\n"
            "From his prison cell, with a pencil, he wrote a petition to the Supreme Court. In 1963, in "
            "Gideon v. Wainwright, the justices ruled nine to zero: if you can't pay, the state must "
            "provide you a lawyer.\n\n"
            "One handwritten letter changed courtrooms across America.\n\n"
            "Watch the full story on the channel.\n\n"
            "#Shorts #Gideon #SupremeCourt #RightToCounsel #Law #CriminalJustice #Documentary"
        ),
        "tags": ["Shorts", "Gideon", "Supreme Court", "Right to Counsel", "Gideon v Wainwright", "Public Defender", "Law", "Documentary"],
        "video_sha256": "d25e95a0cb1749920dc5d46083ab715b2fb2b9acae650da6a0f1b3a667e18f00",
        "thumb_sha256": "c805540a7cabc2970b7bcb88b81163512a08073a4594b601b8218aaa14d76a60",
    },
    "03": {
        # destination for the funnel link; ensure_funnel_description() verifies it is public
        "longform": "An0to4U0hJQ",
        "ep": "PD-2026-003-mapp",
        "rev": "v001",
        "title": "Police Searched Illegally — Can They Still Use It? #Shorts",
        "description": (
            "Police search a home illegally and find something. Can they still use it against you?\n\n"
            "In 1957, officers forced their way into a woman's house without a valid warrant. The suspect "
            "they were after wasn't there. Instead, they found some books — and charged her with a "
            "different crime.\n\n"
            "In 1961, in Mapp v. Ohio, the Supreme Court ruled that evidence from an illegal search can't "
            "be used in court — in any state. Sometimes a guilty person goes free, because the police "
            "broke the rules.\n\n"
            "Watch the full story on the channel.\n\n"
            "#Shorts #MappVOhio #SupremeCourt #FourthAmendment #ExclusionaryRule #Law #Documentary"
        ),
        "tags": ["Shorts", "Mapp v Ohio", "Supreme Court", "Fourth Amendment", "Exclusionary Rule", "Search and Seizure", "Law", "Documentary"],
        "video_sha256": "a40e70ed3b0918d3430bfadc311d03e9676d7ab6e42ec248b709956194bf7c5a",
        "thumb_sha256": "68edf414849082144aca476fd3bee245f63bd33a68812ebcc1b0d5b4e99e990b",
    },
    "04": {
        # destination for the funnel link; ensure_funnel_description() verifies it is public
        "longform": "waA4XJ9bYcE",
        "ep": "PD-2026-004-ftx",
        "rev": "v001",
        "title": "$8 Billion Vanished From a Crypto Exchange — Where Did It Go? #Shorts",
        "description": (
            "A crypto exchange was holding billions of its customers' dollars. Then about eight billion of "
            "it went missing.\n\n"
            "FTX was one of the biggest crypto exchanges in the world, and its founder was its most trusted "
            "face. But hidden in the code was a secret exception: a private trading firm could pull customer "
            "deposits almost without limit.\n\n"
            "When everyone asked for their money back, it wasn't there. In 2023, a jury found the founder "
            "guilty in one of the largest frauds in U.S. history. Even in crypto, spending customers' money "
            "is theft.\n\n"
            "Watch the full story on the channel.\n\n"
            "#Shorts #FTX #CryptoCollapse #Fraud #Crypto #FinancialCrime #Documentary"
        ),
        "tags": ["Shorts", "FTX", "Crypto", "Crypto Collapse", "Fraud", "Financial Crime", "Wall Street", "Documentary"],
        "video_sha256": "41979cc1acfc6b92a419a6fb66b3a4dab8572d23cfa0425ac4faef831ea8d22d",
        "thumb_sha256": "1d281f6d11114efc15c68b9b81c28355b02c12b48094fb8bbd2867a067974848",
    },
    "05": {
        # destination for the funnel link; ensure_funnel_description() verifies it is public
        "longform": "sphERPA4gAc",
        "ep": "PD-2026-005-madoff",
        "rev": "v001",
        "title": "Steady Returns for Decades — and Almost Zero Real Trades #Shorts",
        "description": (
            "For decades, he paid steady profits. In reality, he was barely investing the money at all.\n\n"
            "His was one of the most trusted names on Wall Street, with smooth, steady returns year after "
            "year. But investigators found there were almost no real trades.\n\n"
            "The profits were just new investors' money handed to old ones — a Ponzi scheme. It collapsed "
            "in 2008, and he was sentenced to a hundred and fifty years in prison. Returns that look too "
            "smooth can be the warning sign.\n\n"
            "Watch the full story on the channel.\n\n"
            "#Shorts #Madoff #PonziScheme #WallStreet #Fraud #FinancialCrime #Documentary"
        ),
        "tags": ["Shorts", "Madoff", "Ponzi Scheme", "Wall Street", "Fraud", "Financial Crime", "Investing", "Documentary"],
        "video_sha256": "7c4b9dbe30a5209aa3dd69deb411254ca221c080aa6a2db8bd811f637c36e179",
        "thumb_sha256": "93ba3bebc30d9d515dafd0b53eafdb69a9d8f0f5a9c2b7fb84ad718e8a65be99",
    },
    "09": {
        # destination for the funnel link; ensure_funnel_description() verifies it is public
        "longform": "m-uWzgWHGPg",
        "ep": "PD-2026-009-timbs",
        "rev": "v001",
        "title": "Can Police Take Your Property Without a Conviction? #Shorts",
        "description": (
            "Civil forfeiture can let the government take your car, your cash, even your house — "
            "without ever convicting you of a crime.\n\n"
            "An Indiana man's $42,000 SUV, bought with his late father's life-insurance money, was "
            "seized over a small drug sale — about four times the most he could be fined.\n\n"
            "In Timbs v. Indiana (2019), the Supreme Court ruled 9-0 that the ban on excessive fines "
            "applies to the states too. He got his car back.\n\n"
            "Watch the full story on the channel.\n\n"
            "#Shorts #SupremeCourt #CivilForfeiture #Timbs #EighthAmendment #Law #Documentary"
        ),
        "tags": ["Shorts", "Supreme Court", "Civil Forfeiture", "Timbs v Indiana", "Eighth Amendment", "Excessive Fines", "Law", "Documentary"],
        "video_sha256": "d862b3ee3cf79d610cb742dff594ff23c93b13dab46501e6a7f62448c19632d8",
        "thumb_sha256": "7f59ce5f3afb958655d55ac765bc5e8bbf95d6344569196d891587f23b2697cd",
    },
    "10": {
        # destination for the funnel link; ensure_funnel_description() verifies it is public
        "longform": "89SQoRgAD7U",
        "ep": "PD-2026-010-kelo",
        "rev": "v001",
        "title": "Can the Government Take Your Home for a Private Company? #Shorts",
        "description": (
            "Can the government take your home — in good condition — and hand the land to a private "
            "developer?\n\n"
            "In 2005, in New London, Connecticut, Susette Kelo's little pink house was condemned for a "
            "redevelopment plan of offices and a hotel.\n\n"
            "In Kelo v. City of New London (2005), the Supreme Court ruled 5-4 that economic development "
            "can count as 'public use.' The homes were torn down — and the project was never built. "
            "The land sat empty for years.\n\n"
            "Watch the full story on the channel.\n\n"
            "#Shorts #SupremeCourt #EminentDomain #Kelo #PropertyRights #FifthAmendment #Law #Documentary"
        ),
        "tags": ["Shorts", "Supreme Court", "Eminent Domain", "Kelo", "Property Rights", "Fifth Amendment", "Law", "Documentary"],
        "video_sha256": "e0e824bf31308c9b31e99e3528030b9970eabc1f5551cf0374b2549704f9c992",
        "thumb_sha256": "676e6ca434773d6d68993ef4828ddf6fc7a984ae66bf6d5154438ac7dbe2d90d",
    },
    "11": {
        # destination for the funnel link; ensure_funnel_description() verifies it is public
        "longform": "cSfe3iGnBBM",
        "ep": "PD-2026-011-mahanoy",
        "rev": "v001",
        "title": "Can Your School Punish You for a Post Made at Home? #Shorts",
        "description": (
            "Can your school punish you for something you posted off campus — on the weekend, from home?\n\n"
            "A 14-year-old who didn't make the varsity cheer team vented on Snapchat, and was suspended "
            "from the team for a year.\n\n"
            "In Mahanoy Area School District v. B.L. (2021), the Supreme Court ruled 8-1 that schools "
            "generally can't punish ordinary off-campus speech — though threats and harassment are different.\n\n"
            "Watch the full story on the channel.\n\n"
            "#Shorts #SupremeCourt #FreeSpeech #FirstAmendment #StudentRights #Law #Documentary"
        ),
        "tags": ["Shorts", "Supreme Court", "Free Speech", "First Amendment", "Student Rights", "Mahanoy", "Law", "Documentary"],
        "video_sha256": "a6d6d1c6a8582a6c2efb47b817c486ea600bdc0e383707e4cc169768f9ca36ef",
        "thumb_sha256": "3a795b0cd661b5abd84405921ffce390c9199d2ae6d0952ff1d4637bccf90370",
    },
    "12": {
        # destination for the funnel link; ensure_funnel_description() verifies it is public
        "longform": "1pox44KsaV8",
        "ep": "PD-2026-012-arbitration",
        "rev": "v001",
        "title": "Did You Sign Away Your Right to Sue? #Shorts",
        "description": (
            "You may have given up your right to sue — the moment you tapped \"I agree.\"\n\n"
            "Buried in many phone, bank, and job contracts is a forced-arbitration clause: disputes go "
            "to private arbitration instead of court, often with no class action.\n\n"
            "It traces back to about $30 in tax on a \"free\" phone. In AT&T Mobility v. Concepcion "
            "(2011), the Supreme Court ruled 5-4 that companies can enforce these clauses. In 2018, "
            "Epic Systems v. Lewis extended it to the workplace.\n\n"
            "Watch the full story on the channel.\n\n"
            "#Shorts #SupremeCourt #Arbitration #ConsumerRights #ClassAction #Law #Documentary"
        ),
        "tags": ["Shorts", "Supreme Court", "Arbitration", "Forced Arbitration", "Consumer Rights", "Class Action", "Law", "Documentary"],
        "video_sha256": "fc451cc63bd36a5298a7daec35c831d2847f872ec0998c8419a0abac6d66b78e",
        "thumb_sha256": "61a3a086298bc96f5b5433b749e29057bdc7086f00e9f3866572d8561c591a1d",
    },
    "13": {
        # destination for the funnel link; ensure_funnel_description() verifies it is public
        "longform": "g5yFmDt48oU",
        "ep": "PD-2026-013-king",
        "rev": "v001",
        "title": "Arrested? Police Can Take Your DNA — and Keep It #Shorts",
        "description": (
            "Get arrested — even by mistake — and police can take your DNA and store it in a national "
            "database.\n\n"
            "In 2009, a man arrested for assault was swabbed at booking. That sample matched an unsolved "
            "case from years earlier, and he was convicted of it.\n\n"
            "In Maryland v. King (2013), the Supreme Court ruled 5-4 that booking DNA swabs are legal, "
            "like fingerprints. But four justices — from both ends of the bench — dissented, calling it "
            "a search of your body for crimes you're not even suspected of.\n\n"
            "Watch the full story on the channel.\n\n"
            "#Shorts #SupremeCourt #DNA #FourthAmendment #Privacy #Law #Documentary"
        ),
        "tags": ["Shorts", "Supreme Court", "DNA", "Maryland v King", "Fourth Amendment", "Privacy", "Law", "Documentary"],
        "video_sha256": "f1f41f7d3af35dc45ce5cc500d742ab0334acb9f361709f02d1257096abade87",
        "thumb_sha256": "5c988bb5dda1dec2b9da1ca0eb32050bdf2c7e43efbc898c6f061b7b16d3ab9d",
    },
    "14": {
        # destination for the funnel link; ensure_funnel_description() verifies it is public
        "longform": "Sz8zPUoBANM",
        "ep": "PD-2026-014-lange",
        "rev": "v001",
        "title": "Can Police Chase You Into Your Own Home? #Shorts",
        "description": (
            "An officer chases you over something minor, and you step inside your home. Can he follow "
            "you in?\n\n"
            "One man was just playing his music too loud. An officer flipped on his lights, the man "
            "pulled into his own garage — and the officer stuck his foot under the closing door and "
            "walked in.\n\n"
            "In Lange v. California (2021), the Supreme Court ruled 9-0 that chasing a minor offense, by "
            "itself, does not automatically let police enter your home. They need a warrant or a real "
            "emergency. Your home is still the hardest place for the state to enter.\n\n"
            "Watch the full story on the channel.\n\n"
            "#Shorts #SupremeCourt #FourthAmendment #Police #Privacy #Law #Documentary"
        ),
        "tags": ["Shorts", "Supreme Court", "Fourth Amendment", "Lange v California", "Hot Pursuit", "Police", "Privacy", "Law", "Documentary"],
        "video_sha256": "70fe90dea67c38cbbc475463ac9e36ebdb6ebb644e3ad16500fdef97a6e1f4b7",
        "thumb_sha256": "1c2819b03f2c7cbd110e109597222762dc7f2dce279a10c243aa9e3942ae75b8",
    },
    "15": {
        # destination for the funnel link; ensure_funnel_description() verifies it is public
        "longform": "LXFjJqE6vKU",
        "ep": "PD-2026-015-theranos",
        "rev": "v001",
        "title": "When Does a Bold Promise Become a Crime? #Shorts",
        "description": (
            "One drop of blood to run every test — a nine-billion-dollar company. But the machine "
            "didn't work.\n\n"
            "Its founder was hailed as the next Steve Jobs. Then whistleblowers said the device didn't "
            "work as advertised — many tests were quietly run on other companies' machines, and the "
            "finger-prick results were unreliable, even as investors poured in hundreds of millions.\n\n"
            "In 2022, a jury convicted the founder of defrauding investors. The line was intent: not "
            "failure, but knowingly misleading people. A bold promise can become a crime when the "
            "deception is deliberate.\n\n"
            "Watch the full story on the channel.\n\n"
            "#Shorts #Theranos #Fraud #Startup #WhiteCollar #Law #Documentary"
        ),
        "tags": ["Shorts", "Theranos", "Fraud", "Investor Fraud", "Startup", "White Collar Crime", "Law", "Documentary"],
        "video_sha256": "a48d542533057e408024ff63101b4223de91574d1f672e4578cc524cec6b0148",
        "thumb_sha256": "7b1266d39723981a7b234e376733c48afa2a3987c0af5595a4017ec4eb152ae6",
    },
    "16": {
        # destination for the funnel link; ensure_funnel_description() verifies it is public
        "longform": "marQjsCagh0",
        "ep": "PD-2026-016-titan",
        "rev": "v001",
        "title": "The World Counted Down 4 Days. They Were Already Gone. #Shorts",
        "description": (
            "The world watched a four-day countdown to save them. They were already gone.\n\n"
            "In June 2023, five people sealed inside an experimental submersible called Titan dove toward "
            "the Titanic, two and a half miles down. They had been warned: the company's own safety chief "
            "was fired for flagging the hull, experts had called the design catastrophic, and it was "
            "steered with a game controller.\n\n"
            "Ninety minutes down came a last message — \"All good here.\" Then silence. The hull imploded "
            "in an instant, on that first day. In 2025, the U.S. Coast Guard called the loss preventable.\n\n"
            "Watch the full story on the channel.\n\n"
            "#Shorts #Titan #OceanGate #Titanic #Submersible #Documentary"
        ),
        "tags": ["Shorts", "Titan", "OceanGate", "Titanic", "Submersible", "Coast Guard", "Documentary"],
        "video_sha256": "ac332218f4b3264e88b1d0c5582bc617ef0ddc3517fa6a05f34e077ac9a95976",
        "thumb_sha256": "ca526482ae9117237646f22b442873107fb9e952e20853aa05eb7e0f7d41c52a",
    },
    "17": {
        # destination for the funnel link; ensure_funnel_description() verifies it is public
        "longform": "vikfOBHullI",
        "ep": "PD-2026-017-onecoin",
        "rev": "v001",
        "title": "She Sold a Crypto That Prosecutors Say Never Existed #Shorts",
        "description": (
            "She sold a cryptocurrency that, prosecutors say, never really existed.\n\n"
            "OneCoin launched in 2014 in Bulgaria: you bought token packages and got paid to recruit "
            "more buyers. But prosecutors say — and the co-founder admitted in a guilty plea — there was "
            "no real blockchain; the price was just numbers the company controlled.\n\n"
            "Prosecutors cite OneCoin's own records showing more than four billion euros in sales. "
            "Charged in secret in 2017, founder Ruja Ignatova flew to Athens and vanished. The FBI has "
            "placed her on its Ten Most Wanted list, with a reward of up to five million dollars. She is "
            "charged, not convicted — and still missing.\n\n"
            "Watch the full story on the channel.\n\n"
            "#Shorts #OneCoin #CryptoScam #RujaIgnatova #FBI #TrueCrime #Documentary"
        ),
        "tags": ["Shorts", "OneCoin", "Crypto", "Ruja Ignatova", "FBI Most Wanted", "Fraud Case", "True Crime", "Documentary"],
        "video_sha256": "3725e260e689bd21cfceb80475b96d0ae6fa43867d2fd6dc02a2374b31834e19",
        "thumb_sha256": "7fe59a8a5cb072ada5083ac6339c1b01dda3379a044f6510b2017b06b9c10b08",
    },
    "18": {
        # destination for the funnel link; ensure_funnel_description() verifies it is public
        "longform": "5Jap-0h43A4",
        "ep": "PD-2026-018-flashcrash",
        "rev": "v001",
        "title": "$1 Trillion Vanished in 36 Minutes — Then Came Back #Shorts",
        "description": (
            "In about 36 minutes, nearly a trillion dollars vanished from the U.S. stock market — "
            "then most of it came back.\n\n"
            "On May 6, 2010, the market fell roughly a thousand points in minutes. Some famous shares "
            "briefly traded for as little as a penny before prices recovered.\n\n"
            "Investigators later traced part of the order imbalance to a trader working from a London "
            "bedroom, placing huge orders he intended to cancel — a tactic the law calls spoofing. He "
            "pleaded guilty to spoofing and wire fraud, but not to causing the crash. In 2020 he was "
            "sentenced to time served plus one year of home incarceration, after cooperating with "
            "authorities. No serious account blames one person alone: a roughly four-billion-dollar "
            "sell order and panicking automated systems were part of it too.\n\n"
            "Watch the full story on the channel.\n\n"
            "#Shorts #FlashCrash #StockMarket #Spoofing #WallStreet #Finance #Documentary"
        ),
        "tags": ["Shorts", "Flash Crash", "Stock Market", "Spoofing", "Wall Street", "2010 Flash Crash", "Finance", "Documentary"],
        "video_sha256": "8576f9abc611db062405903de3b2b626bd946038207d7825d4886f2540db2694",
        "thumb_sha256": "7ba736c62a48f6553f9d49575a9e656655e64542f607d6f455412500495a5dc5",
    },
    "19": {
        # destination for the funnel link; ensure_funnel_description() verifies it is public
        "longform": "j8U8c4BB_GQ",
        "ep": "PD-2026-019-varsityblues",
        "rev": "v001",
        "title": "How Did Wealthy Parents Sneak Their Kids Into Elite Colleges? #Shorts",
        "description": (
            "Wealthy parents paid to slip their kids into top colleges through what prosecutors called "
            "a secret \"side door.\"\n\n"
            "In March 2019, prosecutors unsealed Operation Varsity Blues and arrested about fifty people. "
            "The mastermind, Rick Singer, ran a counseling business and a foundation prosecutors described "
            "as a sham charity. Parents paid roughly twenty-five million dollars to buy fake athletic "
            "recruiting spots — children labeled as recruits for sports they never played, with staged "
            "photos — while others paid to have a proctor secretly take the SAT or fix the answers.\n\n"
            "Actress Felicity Huffman pleaded guilty to fixing her daughter's test. Lori Loughlin and her "
            "husband paid five hundred thousand dollars for fake crew spots and pleaded guilty to fraud "
            "conspiracy. The schools were treated as victims, not suspects. In all, fifty-five were charged "
            "and fifty-three convicted — almost all by guilty plea, not by trial.\n\n"
            "Watch the full story on the channel.\n\n"
            "#Shorts #VarsityBlues #CollegeAdmissions #TrueCrime #Documentary"
        ),
        "tags": ["Shorts", "Varsity Blues", "College Admissions Scandal", "Rick Singer", "True Crime", "Documentary"],
        "video_sha256": "8234996b2cf035fabdfa620284a1b1267cf3013c6debff5bd991bcab31b2f152",
        "thumb_sha256": "fcc6f8bbb1746e06b2bbbd228b39c98e6f3bc4b8efa2be94b855ab6539fd42a0",
    },
    "20": {
        # destination for the funnel link; ensure_funnel_description() verifies it is public
        "longform": "1h267U6PY0I",
        "ep": "PD-2026-020-gardner",
        "rev": "v001",
        "title": "The Biggest Art Heist in History Is Still Unsolved #Shorts",
        "description": (
            "It is often called the biggest art heist in history — and the empty frames still hang on "
            "the wall.\n\n"
            "On March 18, 1990, in Boston, two men dressed as police talked their way into the Isabella "
            "Stewart Gardner Museum, handcuffed the guards in the basement, and were inside about "
            "eighty-one minutes. They took thirteen works, cutting a Rembrandt and a Vermeer from their "
            "frames. The haul is estimated at around half a billion dollars, though the art is "
            "unsellable, and not one of the thirteen has ever been found.\n\n"
            "The FBI has said it believes it knows who did it, but has never publicly named them and says "
            "they are now dead. The window to charge the theft has closed, and a ten-million-dollar reward "
            "still stands. The empty frames remain on display, exactly where the paintings were.\n\n"
            "Watch the full story on the channel.\n\n"
            "#Shorts #GardnerHeist #ArtHeist #Unsolved #TrueCrime #Documentary"
        ),
        "tags": ["Shorts", "Gardner Museum Heist", "Art Heist", "Unsolved Mystery", "True Crime", "Documentary"],
        "video_sha256": "5f2b9dcfa4e8cd50c2e78b99a353a8bf92e8c837c975766eeb40938704a6e281",
        "thumb_sha256": "0f28a60589ca60d4b86cc3746426db78c5f960db77fb188b7faedf673ed97ef7",
    },
    "21": {
        # destination for the funnel link; ensure_funnel_description() verifies it is public
        "longform": "tt7U1XgjCU4",
        "ep": "PD-2026-021-dbcooper",
        "rev": "v001",
        "title": "He Jumped From a Plane With $200,000 and Vanished #Shorts",
        "description": (
            "He jumped out of a plane with two hundred thousand dollars — and vanished forever.\n\n"
            "On November 24, 1971, a calm man in a dark suit, ticketed as \"Dan Cooper,\" hijacked a "
            "flight from Portland to Seattle with a note claiming he had a bomb. He demanded two hundred "
            "thousand dollars and four parachutes, released the passengers, then had the crew fly low "
            "toward Mexico City. A little after 8 p.m., he lowered the plane's rear stairs and parachuted "
            "into a freezing night over Washington.\n\n"
            "The FBI chased it for forty-five years — the only unsolved hijacking in U.S. aviation "
            "history. In 1980, a boy found about fifty-eight hundred dollars of the cash by a river, and "
            "the serial numbers matched — the only money ever recovered. In 2016 the FBI suspended the "
            "case. Suspended, not solved.\n\n"
            "Watch the full story on the channel.\n\n"
            "#Shorts #DBCooper #Unsolved #Skyjacking #TrueCrime #Documentary"
        ),
        "tags": ["Shorts", "D.B. Cooper", "Skyjacking", "Unsolved Mystery", "FBI", "True Crime", "Documentary"],
        "video_sha256": "2314c4f51d331e2b2e36d66e750e9ad7b6e39806dd685f18083260e3d372fcac",
        "thumb_sha256": "f95dc1390ca4bdde799ec19d868f5a29ffb9fb35afe5b4476a7e802ec1bfb730",
    },
    "22": {
        # destination for the funnel link; ensure_funnel_description() verifies it is public
        "longform": "mj9qEKPRatE",
        "ep": "PD-2026-022-milken",
        "rev": "v001",
        "title": "Charged With 98 Counts, He Pleaded Guilty to Just 6 #Shorts",
        "description": (
            "He was charged with ninety-eight counts — and pleaded guilty to six.\n\n"
            "Michael Milken built the high-yield, or \"junk,\" bond market, financing companies the big "
            "banks had shut out. In 1987, his pay was reported at around five hundred fifty million "
            "dollars. After a cooperating witness pointed investigators his way, a 1989 indictment "
            "charged him with ninety-eight counts, including RICO racketeering — but those were "
            "accusations, and the case never went to trial.\n\n"
            "In 1990 he pleaded guilty to six felony counts; the RICO charge and the other ninety-two "
            "were dropped. He paid about six hundred million dollars — a two-hundred-million-dollar fine "
            "plus four hundred million in restitution — and was barred from the securities industry for "
            "life. In 2020 he received a full presidential pardon, which is clemency, not a finding of "
            "innocence: the guilty plea stands, and it did not lift the lifetime ban.\n\n"
            "Watch the full story on the channel.\n\n"
            "#Shorts #MichaelMilken #JunkBonds #WallStreet #Finance #Documentary"
        ),
        "tags": ["Shorts", "Michael Milken", "Junk Bonds", "Wall Street", "White Collar", "Finance", "Documentary"],
        "video_sha256": "a0b3bb20633168f7c9c35b81a2c8873a7423e98b0f8126eaec128ff754a3dc59",
        "thumb_sha256": "257c916886d0b0ff37bd1e6c41cfd26523fe9f952befdc43799e631fb34c0c2d",
    },
    "24": {
        # destination for the funnel link; ensure_funnel_description() verifies it is public
        "longform": "rYV4rxtQCV0",
        "ep": "PD-2026-024-rajaratnam",
        "rev": "v001",
        "title": "The FBI Caught a Billionaire Trader With the Mob's Favorite Tool #Shorts",
        "description": (
            "To catch a billionaire trader, the FBI used the same tool it used on the mob: wiretaps.\n\n"
            "Raj Rajaratnam ran the Galleon Group, a hedge fund that at its peak managed about seven "
            "billion dollars. His sources sat inside the companies themselves — an Intel executive, a "
            "McKinsey partner, an IBM executive — each charged separately. It was the first major "
            "insider-trading case built on court-authorized wiretaps, and prosecutors played the jury his "
            "own phone calls.\n\n"
            "On May 11, 2011, a jury convicted him on all fourteen counts. He was sentenced to eleven "
            "years — at the time, prosecutors called it the longest insider-trading sentence in American "
            "history — and ordered to forfeit nearly fifty-four million dollars. In 2013 an appeals court "
            "upheld the wiretaps as lawful. In a separate trial, a Goldman Sachs director was convicted "
            "of feeding him boardroom secrets.\n\n"
            "Watch the full story on the channel.\n\n"
            "#Shorts #Rajaratnam #InsiderTrading #WallStreet #Finance #Documentary"
        ),
        "tags": ["Shorts", "Raj Rajaratnam", "Insider Trading", "Galleon Group", "Wall Street", "Finance", "Documentary"],
        "video_sha256": "0b0e30c171fdbe926feac6944f8d03d53f64ab7de7d885b1f60363e0afa3f53b",
        "thumb_sha256": "b925d25786380901425e23b8afb338f61fc8fdb742fa0c1afd1e048e987dde12",
    },
    "25": {
        # destination for the funnel link; ensure_funnel_description() verifies it is public
        "longform": "rrftLmSVivk",
        "ep": "PD-2026-025-kyllo",
        "rev": "v001",
        "title": "He Never Set Foot on the Property — So Why Did the Supreme Court Call It a \"Search\"? #Shorts",
        "description": (
            "A federal agent scanned a home's heat from a public street without ever touching it — and "
            "the Supreme Court still called it a search.\n\n"
            "On a freezing night in January 1992, an agent sat in a car on a public street in Florence, "
            "Oregon, and pointed a thermal-imaging device at Danny Kyllo's home. The garage roof and one "
            "wall glowed hot — to the agent, the sign of indoor grow lamps. That reading helped win a "
            "warrant, and inside were more than a hundred marijuana plants. But the device never saw "
            "through the wall; it only measured heat drifting into the open air.\n\n"
            "In Kyllo v. United States (2001), the Court split five to four. Justice Scalia wrote that "
            "using a device not in general public use to learn what is inside a home is a search that "
            "needs a warrant, drawing a line at the front door he called firm and bright. The dissent "
            "called it merely reading heat off the outside. The ruling did not ban thermal imaging — it "
            "required a warrant first.\n\n"
            "Watch the full story on the channel.\n\n"
            "#Shorts #Kyllo #FourthAmendment #SupremeCourt #Privacy #Documentary"
        ),
        "tags": ["Shorts", "Kyllo v United States", "Fourth Amendment", "Supreme Court", "Privacy", "Documentary"],
        "video_sha256": "e7ee388910026a8f88b649b3995c8c7711ca97124860f788f56733b3c2db72bd",
        "thumb_sha256": "a442516b5b26ea52c16224eec3bb87944b49bf9f7446a0cca13e1b454a4bc9fb",
    },
    "26": {
        # destination for the funnel link; ensure_funnel_description() verifies it is public
        "longform": "68oWZRiOnB8",
        "ep": "PD-2026-026-katz",
        "rev": "v001",
        "title": "How Did the FBI Record Him Without Ever Touching the Phone Booth? #Shorts",
        "description": (
            "The FBI recorded every word he said in a glass phone booth — and never once opened the "
            "door. The Supreme Court still called it an illegal search.\n\n"
            "In Los Angeles in the mid-1960s, agents taped a hidden microphone to the outside of a public "
            "phone booth that Charles Katz used to place illegal betting calls, and never set foot inside. "
            "For nearly forty years the rule had been simple: no physical trespass, no search. But Katz "
            "had shut the door to keep his words private.\n\n"
            "In Katz v. United States (1967), the Court ruled seven to one that the Fourth Amendment "
            "\"protects people, not places.\" Recording him without a warrant was unconstitutional — not "
            "because wiretapping is banned, but because it needed a judge's permission first. Justice "
            "Harlan's concurrence gave the \"reasonable expectation of privacy\" test that still governs "
            "surveillance today.\n\n"
            "Watch the full story on the channel.\n\n"
            "#Shorts #Katz #FourthAmendment #SupremeCourt #Privacy #Documentary"
        ),
        "tags": ["Shorts", "Katz v United States", "Fourth Amendment", "Supreme Court", "Privacy", "Documentary"],
        "video_sha256": "4d75eb1e4db91f9783705ea425f9e85a88c9f6d55aa5b67fa62efa2e6e90f9d7",
        "thumb_sha256": "9844dda73784c6bc59ee64d17e15865312119af4dd5fac535c2df30deec892dd",
    },
    "27": {
        # destination for the funnel link; ensure_funnel_description() verifies it is public
        "longform": "tpAKfHKuwqY",
        "ep": "PD-2026-027-rodriguez",
        "rev": "v001",
        "title": "The Traffic Stop Was Already Over — So How Was It Unconstitutional? #Shorts",
        "description": (
            "The traffic stop was already over — the warning written, the papers handed back. So how "
            "did the next seven minutes break the Constitution?\n\n"
            "Just after midnight in Nebraska, a K-9 officer pulled over Dennys Rodriguez for drifting "
            "onto the shoulder, ran the checks, wrote a warning, and handed everything back. But he then "
            "held Rodriguez seven to eight more minutes, waited for a second unit, and walked a drug dog "
            "around the car.\n\n"
            "In Rodriguez v. United States (2015), the Supreme Court ruled six to three. A stop, Justice "
            "Ginsburg wrote, becomes unlawful when it is \"prolonged beyond the time reasonably required "
            "to complete the mission.\" Once the traffic work is done, the clock stops — holding a driver "
            "for a dog needs its own reasonable suspicion. The Court did not ban dog sniffs, and it did "
            "not set Rodriguez free; it sent the case back.\n\n"
            "Watch the full story on the channel.\n\n"
            "#Shorts #Rodriguez #FourthAmendment #SupremeCourt #TrafficStop #Documentary"
        ),
        "tags": ["Shorts", "Rodriguez v United States", "Fourth Amendment", "Supreme Court", "Traffic Stop", "Documentary"],
        "video_sha256": "38b8f9f4a70726621a582032194b89c778585ca6b2abbf2de12fc191a6d3257b",
        "thumb_sha256": "f78dbd2d5b6572d565aa8aaaaea9fa02cd4fe9a51dc89db90a803b0c6f7fb5cc",
    },
    "23": {
        # destination for the funnel link; ensure_funnel_description() verifies it is public
        "longform": "FTm1icKgycU",
        "ep": "PD-2026-023-swartz",
        "rev": "v001",
        "title": "The Website He Took From Didn't Even Want Him Charged #Shorts",
        "description": (
            "If you're struggling, you can call or text 988 — the Suicide & Crisis Lifeline (U.S.).\n\n"
            "Aaron Swartz was a programming prodigy who, as a teenager, co-authored the RSS specification "
            "and helped build the technical layer of Creative Commons. Over MIT's open network he "
            "downloaded about 4.8 million scholarly articles — most of the JSTOR archive.\n\n"
            "JSTOR settled with him and said it did not want him prosecuted; MIT stayed neutral. Federal "
            "prosecutors charged him anyway — four counts, then thirteen. On paper the charges stacked to "
            "a theoretical maximum of about 35 years, but prosecutors signaled a plea of roughly six "
            "months, and legal scholars said that headline wildly overstated what he really faced.\n\n"
            "Aaron Swartz died by suicide on January 11, 2013, at age 26. His family said the "
            "prosecution's overreach contributed to his death. He was charged, never tried or convicted.\n\n"
            "If you or someone you know is struggling, call or text 988 (U.S. Suicide & Crisis Lifeline). "
            "Watch the full story on the channel.\n\n"
            "#Shorts #AaronSwartz #OpenAccess #988 #Documentary"
        ),
        "tags": ["Shorts", "Aaron Swartz", "Open Access", "JSTOR", "988 Lifeline", "Documentary"],
        "video_sha256": "261ab2ee6f2c9ba30f9c5100c90fd4356156e3d2911cee3fca2a071a503c39b4",
        "thumb_sha256": "960e5747ee74c6b95eba00db639cc46406092f2282ab7d327df07fcaf918d989",
    },
    "28": {
        # destination for the funnel link; ensure_funnel_description() verifies it is public
        "longform": "YhEJHK279f8",
        "ep": "PD-2026-028-forfeiture",
        "rev": "v001",
        "title": "His Son Sold $40 of Drugs — So the City Tried to Take His Parents' House #Shorts",
        "description": (
            "A court moved to seize a family's home — not because they broke the law, but because their "
            "house supposedly did.\n\n"
            "Christos Sourovelis, a house painter in northeast Philadelphia, had broken no law and was "
            "charged with nothing. But in March 2014 his twenty-two-year-old son sold about forty dollars "
            "of heroin to a police informant — so the city moved against the house itself. Using civil "
            "forfeiture, prosecutors won an order to seize and seal the home with no family member "
            "present. In these cases the property is the defendant — \"the State versus one house\" — and "
            "innocent owners can be left to prove their own home did nothing wrong.\n\n"
            "It wasn't unusual: between 2002 and 2014 Philadelphia used forfeiture to take more than "
            "twelve hundred homes and over fifty million dollars in cash — a typical cash seizure about "
            "one hundred seventy-eight dollars — with money flowing back into police and prosecutor "
            "budgets. The family and the Institute for Justice filed a class action, and in 2018 the city "
            "agreed to dismantle the program and repay millions. A court did not rule the law "
            "unconstitutional; the city agreed to change it.\n\n"
            "Watch the full story on the channel.\n\n"
            "#Shorts #CivilForfeiture #PropertyRights #InstituteForJustice #Documentary"
        ),
        "tags": ["Shorts", "Civil Forfeiture", "Property Rights", "Philadelphia", "Institute for Justice", "Documentary"],
        "video_sha256": "04d4c73f40652545cc5b11daa5de053072f12de1e750899b30031e1c88e9c9a9",
        "thumb_sha256": "0d0ff6e22c1075245b45ec70a37cd67c3504542ae8d49d7ee2ca9a2dd9e1d5ac",
    },
    "29": {
        # destination for the funnel link; ensure_funnel_description() verifies it is public
        "longform": "Qyad4FejCIc",
        "ep": "PD-2026-029-hinton",
        "rev": "v001",
        "title": "He Spent 30 Years on Death Row for a Bullet That Matched Nothing #Shorts",
        "description": (
            "For thirty years, Anthony Ray Hinton sat on Alabama's death row for two 1985 murders he did "
            "not commit.\n\n"
            "There was no eyewitness, no fingerprint, and no confession. The entire case rested on a claim "
            "that the bullets came from an old revolver found at his mother's house. At trial his court-"
            "appointed lawyer, mistakenly believing he could spend only about a thousand dollars, hired a "
            "firearms witness who struggled to defend the analysis. Hinton was convicted and sentenced to "
            "death.\n\n"
            "Years later the Equal Justice Initiative and attorney Bryan Stevenson took his case. Independent "
            "firearms experts re-examined the evidence and could not tie the bullets to that gun — or to "
            "each other. In 2014 the U.S. Supreme Court ruled 9-0 that his original defense had been "
            "constitutionally inadequate. When the state re-tested the evidence, its own experts could not "
            "make a match, and the charges were dropped. In April 2015 Anthony Ray Hinton walked free — one "
            "of the longest-serving death-row exonerees in U.S. history.\n\n"
            "Watch the full story on the channel.\n\n"
            "#Shorts #DeathRow #Exoneration #EqualJusticeInitiative #Documentary"
        ),
        "tags": ["Shorts", "Death Row", "Exoneration", "Anthony Ray Hinton", "Equal Justice Initiative", "Documentary"],
        "video_sha256": "0eaa536f7ff644d3cb7fa241ede239423c10787cc01e412a9b1ee37479fb4ffe",
        "thumb_sha256": "d9df1a51af9e47a927aad6f4c6bf472dc07c2c81f0691383eff48323ae895ea9",
    },
    "30": {
        # destination for the funnel link; ensure_funnel_description() verifies it is public
        "longform": "5L_HCGJxX_U",
        "ep": "PD-2026-030-cotton",
        "rev": "v001",
        "title": "She Was Certain He Attacked Her — Then DNA Proved She'd Named the Wrong Man #Shorts",
        "description": (
            "Jennifer Thompson was attacked in 1984 and made a point of memorizing her attacker's face so "
            "she could one day identify him. She picked Ronald Cotton — from a photo array, and then again "
            "from a live lineup. She was sure.\n\n"
            "But Cotton was the only person who appeared in both the photos and the lineup, and when she was "
            "told she had 'done great,' a tentative guess hardened into total certainty. Cotton was "
            "convicted and served about eleven years. Another man, Bobby Poole, later resembled the "
            "descriptions — and in 1995 DNA testing cleared Cotton and matched Poole. Cotton was exonerated "
            "and freed.\n\n"
            "What happened next is the rarest part: Jennifer Thompson and Ronald Cotton met, and the woman "
            "whose memory sent an innocent man to prison became his friend and co-author, traveling the "
            "country to explain how a sincere, confident witness can still be wrong — and how eyewitness "
            "identification can fail even when no one is lying. This is not a story about blame; it's about "
            "how memory works.\n\n"
            "Watch the full story on the channel.\n\n"
            "#Shorts #Eyewitness #Exoneration #DNA #Documentary"
        ),
        "tags": ["Shorts", "Eyewitness", "Exoneration", "DNA", "Ronald Cotton", "Documentary"],
        "video_sha256": "3e5102a74a97528e28f711f95bf496b43d48712f061a38f1f8c0d9e51e0b4bfc",
        "thumb_sha256": "e4156b61d9d2b66e177d69b9b4854caf40ed7622fe582936b5daa52d7f6312ef",
    },
    "31": {
        # destination for the funnel link; ensure_funnel_description() verifies it is public
        "longform": "YQIhk2dKZHU",
        "ep": "PD-2026-031-unlock",
        "rev": "v001",
        "title": "Police Can Force Your Thumb to Unlock a Phone — But Maybe Not Your Passcode #Shorts",
        "description": (
            "Your phone holds your whole life — and after Riley v. California (2014), police generally need "
            "a warrant to search it. But a warrant to search is not the same as forcing you to open it, and "
            "that is where the law splits.\n\n"
            "Courts have drawn a line between your mind and your body. Many judges hold that a passcode is a "
            "product of your mind — something you know — so forcing you to reveal it can raise Fifth "
            "Amendment self-incrimination concerns. A fingerprint or face scan, by contrast, is often "
            "treated more like a physical trait, closer to giving a fingerprint at booking — no 'thought' "
            "required.\n\n"
            "The result is a genuine split. In one 2024 case a court allowed police to compel a thumb to "
            "unlock a phone; other courts have refused to force the same act. State and federal courts "
            "disagree, and the U.S. Supreme Court has not yet resolved it. Nothing here is legal advice — "
            "it's a look at an unsettled question that touches almost everyone who owns a phone.\n\n"
            "Watch the full story on the channel.\n\n"
            "#Shorts #FifthAmendment #DigitalPrivacy #Law #Documentary"
        ),
        "tags": ["Shorts", "Fifth Amendment", "Digital Privacy", "Phone Unlock", "Law", "Documentary"],
        "video_sha256": "94d95db948ddd51e46d812c8b932f3e0ee6866174430568fbb798b9ff82176c2",
        "thumb_sha256": "7a6f146d81bd0fa2148313e47177d6e0c9edd0e565e4772eda246837b84b2249",
    },
    "32": {
        # destination for the funnel link; ensure_funnel_description() verifies it is public
        "longform": "bXATF9ZnKLE",
        "ep": "PD-2026-032-carsearch",
        "rev": "v001",
        "title": "Police Can Search Your Car Without a Warrant — But Not the One Spot Touching Your House #Shorts",
        "description": (
            "The police can search your car without a warrant — and they have been able to for a hundred "
            "years. But there is one place that power still cannot follow it.\n\n"
            "The rule dates to 1925 and a Prohibition-era case, Carroll v. United States. Agents tore open a "
            "bootlegger's seat cushions and pulled out sixty-eight bottles of liquor — with no warrant. The "
            "Supreme Court held that a car is not a house: because a vehicle can be driven away before a "
            "warrant is ever signed, officers with probable cause may search it on the spot. That is the "
            "'automobile exception.'\n\n"
            "But probable cause is the catch. Being pulled over is not, by itself, permission to search, and "
            "a hunch is not enough — an officer needs a real, articulable reason. And the search reaches "
            "only where the thing they are looking for could actually fit: chasing a stolen television does "
            "not justify opening a tiny pill bottle.\n\n"
            "The limit was drawn in Collins v. Virginia. An officer walked up a private driveway, lifted a "
            "tarp off a motorcycle he believed was stolen, and confirmed it. In 2018, by a vote of 8-1, the "
            "Supreme Court said no: the strip of driveway pressed against your home is 'curtilage' — treated "
            "as part of the house — and the car-search power stops there. As the Court put it, the exception "
            "'extends no further than the automobile itself.' This is general history, not legal advice.\n\n"
            "Watch the full story on the channel.\n\n"
            "#Shorts #FourthAmendment #KnowYourRights #SupremeCourt #Documentary"
        ),
        "tags": ["Shorts", "Fourth Amendment", "Car Search", "Automobile Exception", "Collins v Virginia", "Documentary"],
        "video_sha256": "79d3055b4129fdf2dc130d546126684c0433a230f382d6d5f44a783e7be04b04",
        "thumb_sha256": "6b76ae5cf8aadf3028eb02296a95e8e1655234d9761a238cc0d63f21eea43da4",
    },
    "33": {
        # destination for the funnel link; ensure_funnel_description() verifies it is public
        "longform": "rU2vk9XL4vY",
        "ep": "PD-2026-033-tyler",
        "rev": "v001",
        "title": "The County Took Her Home Over a $15,000 Debt — Then Kept an Extra $25,000 #Shorts",
        "description": (
            "You owe the county fifteen thousand dollars in property taxes. They seize your home, sell it "
            "for forty thousand — and keep every dollar, including the twenty-five thousand that had nothing "
            "to do with the debt. Can they do that?\n\n"
            "That is what happened to Geraldine Tyler. At ninety-four, she owed about fifteen thousand "
            "dollars in property taxes and penalties on her Minneapolis condo. Hennepin County, Minnesota "
            "seized the condo, sold it for forty thousand dollars, kept the full amount, and left her with "
            "nothing — pocketing roughly twenty-five thousand dollars in surplus that was hers.\n\n"
            "The Fifth Amendment says that when the government takes your property, it owes you just "
            "compensation. That surplus belonged to Tyler, not the county. In 2023, the Supreme Court agreed "
            "— unanimously, nine to zero. Chief Justice Roberts wrote that a taxpayer must 'render unto "
            "Caesar what is Caesar's, but no more,' and that keeping the surplus was an unconstitutional "
            "taking. The Court did not reach the Eighth Amendment question. Most states already required the "
            "surplus be returned; now what critics call 'home equity theft' is barred nationwide. This is "
            "general history, not legal advice.\n\n"
            "Watch the full story on the channel.\n\n"
            "#Shorts #SupremeCourt #PropertyRights #FifthAmendment #Documentary"
        ),
        "tags": ["Shorts", "Supreme Court", "Property Rights", "Home Equity Theft", "Fifth Amendment", "Documentary"],
        "video_sha256": "850529ca1974c5ca2c73a5dd1e7253d8f792cfd3fa33f2922a5a83f64c868eb4",
        "thumb_sha256": "c342283431c2ac532ceb329d6385c70b73c443c032c739b121af71be80a86b51",
    },
    "34": {
        # destination for the funnel link; ensure_funnel_description() verifies it is public
        "longform": "6ozsIfwqrP0",
        "ep": "PD-2026-034-rolin",
        "rev": "v001",
        "title": "You Can Legally Fly With Cash — But the Airport Can Take It and Charge You With Nothing #Shorts",
        "description": (
            "Carrying cash on a domestic flight is completely legal — there is no limit and no form to file. "
            "The only federal cash-reporting requirement applies to international travel with more than "
            "$10,000. So how does someone lose their savings at the airport without being charged with a "
            "crime?\n\n"
            "Terry Rolin had saved about eighty-two thousand dollars in cash over a lifetime. When his "
            "daughter flew with it to deposit it in the bank, agents at the airport stopped her and seized "
            "every dollar — on suspicion alone. No one was charged with any crime.\n\n"
            "This is civil forfeiture: the government moves against the money itself, and the owner has to go "
            "to court to prove their own cash is innocent. The Institute for Justice sued on behalf of "
            "travelers in a class action (Brown v. TSA). The case ended in a 2022 settlement, and by 2025 the "
            "DEA had ended its program of seizing cash at airports. Terry's savings were returned — but many "
            "people never get that far. This is general information, not legal advice.\n\n"
            "Watch the full story on the channel.\n\n"
            "#Shorts #CivilForfeiture #KnowYourRights #InstituteForJustice #Documentary"
        ),
        "tags": ["Shorts", "Civil Forfeiture", "Property Rights", "Airport", "Institute for Justice", "Documentary"],
        "video_sha256": "3d61ba61c719460c45b9e79921178d402a8ec581065a221e320823358220208f",
        "thumb_sha256": "f196069750610d79f3620eb2840089773885d9dfbd107b033422e23039558a72",
    },
    "35": {
        # destination for the funnel link; ensure_funnel_description() verifies it is public
        "longform": "Xc_PxdC_75c",
        "ep": "PD-2026-035-hinders",
        "rev": "v001",
        "title": "She Ran a Cash Restaurant and Broke No Law — So Why Did the IRS Empty Her Bank Account? #Shorts",
        "description": (
            "Carole Hinders ran a small, cash-only restaurant in Iowa for decades. She deposited her "
            "earnings at the bank in amounts under ten thousand dollars. For that alone, the IRS seized her "
            "entire bank account — nearly thirty-three thousand dollars — without ever charging her with a "
            "crime.\n\n"
            "The law is called 'structuring': deliberately breaking up deposits to dodge the bank's "
            "ten-thousand-dollar cash-reporting requirement. But keeping deposits under that amount is not, "
            "by itself, a crime when the money is legal — and every dollar of hers was honest restaurant "
            "income. Under civil forfeiture, the government took the money first and left her to fight to get "
            "it back.\n\n"
            "As cases like hers drew national attention, the IRS announced it would stop seizing money from "
            "people with no criminal case. Carole's money was returned, and Congress later passed a reform to "
            "curb the practice. This is general history, not legal advice.\n\n"
            "Watch the full story on the channel.\n\n"
            "#Shorts #CivilForfeiture #Structuring #KnowYourRights #Documentary"
        ),
        "tags": ["Shorts", "Civil Forfeiture", "Structuring", "IRS", "Property Rights", "Documentary"],
        "video_sha256": "d9d6c5cf36614e1a7fc108b9144526a4548b9ab7f129c423794b8ae5b9653cfb",
        "thumb_sha256": "df98c3cd93b6b7ff2f37c5976cd6b0e504797f69927b0ad82b8fa6765890a983",
    },
    "36": {
        # destination for the funnel link; ensure_funnel_description() verifies it is public
        "longform": "XWYWAgkExH4",
        "ep": "PD-2026-007-riley",
        "rev": "v001",
        "title": "Police Wanted to Search Your Entire Phone — Legally? #Shorts",
        "description": (
            "Police pull you over for expired tags — and after you're arrested, a detective wants to scroll "
            "through everything on your phone. With no warrant.\n\n"
            "Your photos, your messages, your location history — more private than a search of your entire "
            "house, all sitting in your pocket. After David Riley was arrested, a detective searched his "
            "phone and used what was on it to tie him to a shooting.\n\n"
            "In 2014, the Supreme Court said no — unanimously. A phone is not just another pocket. Searching "
            "it needs a warrant. This is general history, not legal advice.\n\n"
            "Watch the full story on the channel.\n\n"
            "#Shorts #FourthAmendment #Privacy #KnowYourRights #SupremeCourt #Documentary"
        ),
        "tags": ["Shorts", "Riley v California", "Supreme Court", "Fourth Amendment", "phone search", "privacy", "know your rights", "Documentary"],
        "video_sha256": "5c4b350455247f79092fb67c5b59357f61c42c1180dd72ef3b4b14ba4a8f29cc",
        "thumb_sha256": "cc5d805ddf0abec2a1d8723f7ab008baba329bf7dd57214d8f5ec4168462484f",
    },
    "37": {
        # destination for the funnel link; ensure_funnel_description() verifies it is public
        "longform": "An0to4U0hJQ",
        "ep": "PD-2026-003-mapp",
        "rev": "v001",
        "title": "Police Broke In With a Warrant That Didn't Exist — Then What? #Shorts",
        "description": (
            "Police forced their way into a woman's home with a warrant that didn't exist — and searched "
            "everything she owned.\n\n"
            "For most of American history, evidence taken in an illegal search could still be used to convict "
            "you. Then officers pushed into Dollree Mapp's home, waving a piece of paper they claimed was a "
            "warrant, and searched her entire house.\n\n"
            "In 1961, the Supreme Court drew the line: evidence from an illegal search can't be used against "
            "you — in any state. This is general history, not legal advice.\n\n"
            "Watch the full story on the channel.\n\n"
            "#Shorts #FourthAmendment #ExclusionaryRule #KnowYourRights #SupremeCourt #Documentary"
        ),
        "tags": ["Shorts", "Mapp v Ohio", "Supreme Court", "Fourth Amendment", "exclusionary rule", "illegal search", "know your rights", "Documentary"],
        "video_sha256": "b4c7a74d54d2e36ae8766d342f8d18664c310535ae04fab312a72d21ba7cd3e9",
        "thumb_sha256": "2cf9701b3d1b80eed4d72ed2c455479d8f5841f094cf4ee26e2280cbe544e114",
    },
    "86": {
        # destination for the funnel link; ensure_funnel_description() verifies it is public
        "longform": "marQjsCagh0",
        "ep": "PD-2026-016-titan",
        "rev": "v001",
        "title": "More than three dozen professionals signed one letter in 2018. The dives went on #Shorts",
        "description": "More than three dozen professionals signed one letter in 2018. The dives went on.\n\nWhat did the letter actually say — and what happened after it was sent?\n\nPrime Documentary covers the cases that quietly decide what the state may do to you. The full episode is linked at the top.\n\n#Shorts #Titan #OceanGate #Submersible #Safety #Documentary",
        "tags": ["Shorts", "Titan", "OceanGate", "Submersible", "Safety", "Law", "Documentary"],
        "video_sha256": "f52877cf93e8bd301e3e1921fab7cd669076a3650c05ac7ec00cbaef0261289b",
        "thumb_sha256": "1f1bd46f7c31afca08777c6c0f633bb8a56441f35e48923a5cbff37d8dcb4ef3",
    },
    "87": {
        # destination for the funnel link; ensure_funnel_description() verifies it is public
        "longform": "marQjsCagh0",
        "ep": "PD-2026-016-titan",
        "rev": "v001",
        "title": "It happened in the seam between everyone's rules and no one's #Shorts",
        "description": "It happened in the seam between everyone's rules and no one's.\n\nIf no regulator had authority, who was ever supposed to say no?\n\nPrime Documentary covers the cases that quietly decide what the state may do to you. The full episode is linked at the top.\n\n#Shorts #Titan #OceanGate #Submersible #Safety #Documentary",
        "tags": ["Shorts", "Titan", "OceanGate", "Submersible", "Safety", "Law", "Documentary"],
        "video_sha256": "6d00193a22073878a89db49cef5198ea003bcf9bbabeb34a0ef6e48b4551f31a",
        "thumb_sha256": "47e326d4d3f66909e536adc8d3ffe26bebff49d88f566e97c8f66bcdcfcfd3f0",
    },
    "88": {
        # destination for the funnel link; ensure_funnel_description() verifies it is public
        "longform": "bYcqabvvxak",
        "ep": "PD-2026-006-terry",
        "rev": "v001",
        "title": "A frisk is not a search. That difference is the entire rule #Shorts",
        "description": "A frisk is not a search. That difference is the entire rule.\n\nWhat happens to something an officer finds after he has gone past that line?\n\nPrime Documentary covers the cases that quietly decide what the state may do to you. The full episode is linked at the top.\n\n#Shorts #TerryvOhio #StopandFrisk #SupremeCourt #FourthAmendment #Documentary",
        "tags": ["Shorts", "Terry v Ohio", "Stop and Frisk", "Supreme Court", "Fourth Amendment", "Law", "Documentary"],
        "video_sha256": "875e772fe6b8d089dceba8c392be1bc50bbf6e79ccd8caec58855d427cd4f904",
        "thumb_sha256": "65687f2564852e8a75a372aec5744767c19db19cde64eb81a7398a7a10bd77cb",
    },
    "89": {
        # destination for the funnel link; ensure_funnel_description() verifies it is public
        "longform": "bYcqabvvxak",
        "ep": "PD-2026-006-terry",
        "rev": "v001",
        "title": "The argument that won was about the officer, not the suspect #Shorts",
        "description": "The argument that won was about the officer, not the suspect.\n\nThe Court held both truths at once — so which one wins when they collide?\n\nPrime Documentary covers the cases that quietly decide what the state may do to you. The full episode is linked at the top.\n\n#Shorts #TerryvOhio #StopandFrisk #SupremeCourt #FourthAmendment #Documentary",
        "tags": ["Shorts", "Terry v Ohio", "Stop and Frisk", "Supreme Court", "Fourth Amendment", "Law", "Documentary"],
        "video_sha256": "6d4adb634d41a66f40c35bfc488eb7f6d6f8ab78ce7edb1a451d3af599d816b2",
        "thumb_sha256": "3342e93f1262bf7c1469d467ab503c31e1ea1e2ea18b7e1889f0d9052384d868",
    },
    "90": {
        # destination for the funnel link; ensure_funnel_description() verifies it is public
        "longform": "SOu4Y1NkGGY",
        "ep": "PD-2026-037-florence",
        "rev": "v001",
        "title": "He was not even driving. He was the passenger #Shorts",
        "description": "He was not even driving. He was the passenger.\n\nOnce the record was wrong, was there anything he could have done to stop it?\n\nPrime Documentary covers the cases that quietly decide what the state may do to you. The full episode is linked at the top.\n\n#Shorts #FlorencevBurlington #StripSearch #SupremeCourt #CivilRights #Documentary",
        "tags": ["Shorts", "Florence v Burlington", "Strip Search", "Supreme Court", "Civil Rights", "Law", "Documentary"],
        "video_sha256": "28ad66f6cea6f1a4d2c8c67abb26027b13f365017ae8468d5e1074cd49ac2ad7",
        "thumb_sha256": "15bf881e83c0dcabb566a4f08a3c044f40a5c5c9bbd99001db3838ad59f67a04",
    },
    "91": {
        # destination for the funnel link; ensure_funnel_description() verifies it is public
        "longform": "SOu4Y1NkGGY",
        "ep": "PD-2026-037-florence",
        "rev": "v001",
        "title": "His own words for it: scared, petrified, humiliated #Shorts",
        "description": "His own words for it: scared, petrified, humiliated.\n\nHe could have let it go. Why did he spend seven years on it instead?\n\nPrime Documentary covers the cases that quietly decide what the state may do to you. The full episode is linked at the top.\n\n#Shorts #FlorencevBurlington #StripSearch #SupremeCourt #CivilRights #Documentary",
        "tags": ["Shorts", "Florence v Burlington", "Strip Search", "Supreme Court", "Civil Rights", "Law", "Documentary"],
        "video_sha256": "43bc798a665f9fbbd879635954f49d45aee58b1fa6261478290496af090ef03b",
        "thumb_sha256": "6fd61c3f96408e88c10e649f4133577d046fd287e8bfd705ed9b14917dc625e0",
    },
    "92": {
        # destination for the funnel link; ensure_funnel_description() verifies it is public
        "longform": "tt7U1XgjCU4",
        "ep": "PD-2026-021-dbcooper",
        "rev": "v002",
        "title": "The name the world knows him by was never even his #Shorts",
        "description": "The name the world knows him by was never even his.\n\nIf the FBI never had a name, what did fifty years of investigation actually produce?\n\nPrime Documentary covers the cases that quietly decide what the state may do to you. The full episode is linked at the top.\n\n#Shorts #DBCooper #Hijacking #FBI #Unsolved #Documentary",
        "tags": ["Shorts", "D B Cooper", "Hijacking", "FBI", "Unsolved", "Law", "Documentary"],
        # v002: re-rendered - mid-roll kinetic typography (2 beats), look approved 2026-08-04
        "video_sha256": "7a981acd28ab6596fb0954c849fc7d324a967588db777804f2b8a3a38a4da568",
        "thumb_sha256": "962292b81419a3917312db2d55ed849c1338df002d43a1a2307ee8871425652c",
    },
    "93": {
        # destination for the funnel link; ensure_funnel_description() verifies it is public
        "longform": "tt7U1XgjCU4",
        "ep": "PD-2026-021-dbcooper",
        "rev": "v002",
        "title": "He did not pick that plane by accident. He picked the one with a door in its tail #Shorts",
        "description": "He did not pick that plane by accident. He picked the one with a door in its tail.\n\nHow much else was planned — and what did that planning tell investigators about him?\n\nPrime Documentary covers the cases that quietly decide what the state may do to you. The full episode is linked at the top.\n\n#Shorts #DBCooper #Hijacking #FBI #Unsolved #Documentary",
        "tags": ["Shorts", "D B Cooper", "Hijacking", "FBI", "Unsolved", "Law", "Documentary"],
        # v002: re-rendered - mid-roll kinetic typography (2 beats), look approved 2026-08-04
        "video_sha256": "20fd50976022da71ef5f979061b4bbf9b564f6d4276774d0392808b03d68a0ad",
        "thumb_sha256": "8f7377f58ecbea4d828a4cd7f5efab450d70782fd2c288ca10b7d3477bd1a5f5",
    },
    "94": {
        # destination for the funnel link; ensure_funnel_description() verifies it is public
        "longform": "sphERPA4gAc",
        "ep": "PD-2026-005-madoff",
        "rev": "v002",
        "title": "One man handed regulators the arithmetic. For nearly ten years, nobody ran it down #Shorts",
        "description": "One man handed regulators the arithmetic. For nearly ten years, nobody ran it down.\n\nHe was right for a decade and it changed nothing. Why did nobody act?\n\nPrime Documentary covers the cases that quietly decide what the state may do to you. The full episode is linked at the top.\n\n#Shorts #Madoff #Ponzi #SEC #Fraud #Documentary",
        "tags": ["Shorts", "Madoff", "Ponzi", "SEC", "Fraud", "Law", "Documentary"],
        # v002: re-rendered - mid-roll kinetic typography (2 beats), look approved 2026-08-04
        "video_sha256": "76a30b9383fd6d4dac67704b51b4fba4cb53259f2293c17b03afa9f564e380ee",
        "thumb_sha256": "6cccc35ebe2ce4eb52fe28388a44a69fa7a36bf3b74c17905974c2727c2948b2",
    },
    "95": {
        # destination for the funnel link; ensure_funnel_description() verifies it is public
        "longform": "sphERPA4gAc",
        "ep": "PD-2026-005-madoff",
        "rev": "v002",
        "title": "In December 2008 he told his own sons the business was one big lie #Shorts",
        "description": "In December 2008 he told his own sons the business was one big lie.\n\nThe money was gone long before 2008. Where did it actually go?\n\nPrime Documentary covers the cases that quietly decide what the state may do to you. The full episode is linked at the top.\n\n#Shorts #Madoff #Ponzi #SEC #Fraud #Documentary",
        "tags": ["Shorts", "Madoff", "Ponzi", "SEC", "Fraud", "Law", "Documentary"],
        # v002: re-rendered - mid-roll kinetic typography (2 beats), look approved 2026-08-04
        "video_sha256": "0f7d131c69d83c637f4f5a110f8e312da4f64bd496a5ea9626e9e5697c20bc6e",
        "thumb_sha256": "b1d455c696abbb346761257c9be5032006be422db98f6442b1969ccc79c9b37b",
    },
    "96": {
        # destination for the funnel link; ensure_funnel_description() verifies it is public
        "longform": "Qyad4FejCIc",
        "ep": "PD-2026-029-hinton",
        "rev": "v002",
        "title": "In 2002 someone finally did the one thing his first defence never did: test the bullets #Shorts",
        "description": "In 2002 someone finally did the one thing his first defence never did: test the bullets.\n\nThe evidence failed in 2002. Why did Alabama keep him for thirteen more years?\n\nPrime Documentary covers the cases that quietly decide what the state may do to you. The full episode is linked at the top.\n\n#Shorts #AnthonyRayHinton #DeathRow #WrongfulConviction #Alabama #Documentary",
        "tags": ["Shorts", "Anthony Ray Hinton", "Death Row", "Wrongful Conviction", "Alabama", "Law", "Documentary"],
        # v002: re-rendered - mid-roll kinetic typography (2 beats), look approved 2026-08-04
        "video_sha256": "d19125ae801ae7429eca0f40f4b60670b11ced1a9483cb1e2cbf31ac058db14d",
        "thumb_sha256": "d911c06195823e37cd275a424baa94a03c99233da4a59bbd7bcf0403d9324690",
    },
    "97": {
        # destination for the funnel link; ensure_funnel_description() verifies it is public
        "longform": "Qyad4FejCIc",
        "ep": "PD-2026-029-hinton",
        "rev": "v002",
        "title": "He walked out in 2015. The two murders he was condemned for were never solved #Shorts",
        "description": "He walked out in 2015. The two murders he was condemned for were never solved.\n\nNobody with the power to stop it ever checked. How was that possible for thirty years?\n\nPrime Documentary covers the cases that quietly decide what the state may do to you. The full episode is linked at the top.\n\n#Shorts #AnthonyRayHinton #DeathRow #WrongfulConviction #Alabama #Documentary",
        "tags": ["Shorts", "Anthony Ray Hinton", "Death Row", "Wrongful Conviction", "Alabama", "Law", "Documentary"],
        # v002: re-rendered - mid-roll kinetic typography (2 beats), look approved 2026-08-04
        "video_sha256": "1d3c09f7ffe79c51d6f0e0e67e27b6f9443b522050232251e0cf53eaa2a91937",
        "thumb_sha256": "096551b3e93f3c283758514ad01728537d81378fa75a1f752c77b9c53fe98c7e",
    },
    "98": {
        # destination for the funnel link; ensure_funnel_description() verifies it is public
        "longform": "Sz8zPUoBANM",
        "ep": "PD-2026-014-lange",
        "rev": "v002",
        "title": "The Court did not say police can never follow you in. It said there is no automatic yes #Shorts",
        "description": "The Court did not say police can never follow you in. It said there is no automatic yes.\n\nIf it is not automatic, what does an officer have to show instead?\n\nPrime Documentary covers the cases that quietly decide what the state may do to you. The full episode is linked at the top.\n\n#Shorts #LangevCalifornia #HotPursuit #SupremeCourt #FourthAmendment #Documentary",
        "tags": ["Shorts", "Lange v California", "Hot Pursuit", "Supreme Court", "Fourth Amendment", "Law", "Documentary"],
        # v002: re-rendered - mid-roll kinetic typography (2 beats), look approved 2026-08-04
        "video_sha256": "c362d5c9c0b44efada2f2369db48924d717fa735136a43644f3137e732e4c58b",
        "thumb_sha256": "f3b4a2990f46c2ec1143ff561a098909441d841e31d61dd539f28e0690d26366",
    },
    "99": {
        # destination for the funnel link; ensure_funnel_description() verifies it is public
        "longform": "Sz8zPUoBANM",
        "ep": "PD-2026-014-lange",
        "rev": "v002",
        "title": "The baseline nobody states out loud: without a warrant, your door stays shut #Shorts",
        "description": "The baseline nobody states out loud: without a warrant, your door stays shut.\n\nHow narrow is narrow — what actually counts as an emergency?\n\nPrime Documentary covers the cases that quietly decide what the state may do to you. The full episode is linked at the top.\n\n#Shorts #LangevCalifornia #HotPursuit #SupremeCourt #FourthAmendment #Documentary",
        "tags": ["Shorts", "Lange v California", "Hot Pursuit", "Supreme Court", "Fourth Amendment", "Law", "Documentary"],
        # v002: re-rendered - mid-roll kinetic typography (2 beats), look approved 2026-08-04
        "video_sha256": "b0dd96e2c810f0b5099dc0c882c3911828f84ebf184227fa87590946591a4fe0",
        "thumb_sha256": "9dc63f309fe7cf728a93280d5a7d0b7f5fae1a6cd50efd1512925047b98cadf4",
    },
}


def write_json(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def ensure_funnel_description(token: str, cfg: dict) -> str:
    """Return the description with a live long-form link on line one, or refuse to upload.

    A Short that ships without a route to its long-form is a dead end, and we shipped 46 of them:
    an audit on 2026-08-02 found 0 of 46 public Shorts carried a link, with 4,391 views sitting
    behind them. Long-form converts ~3.67 subscribers per 1,000 views against 0.77 on Shorts, so
    that gap is the most expensive thing on the channel. Backfilling afterwards is not a fix,
    because the next upload reopens the hole. This closes it at the source.

    On Shorts the description sits behind a tap, so the URL goes on the FIRST line; anything
    further down is invisible in practice.

    Refuses when the destination is missing, not public, or is itself a Short. A link to a private
    video is worse than no link: it looks like a route and is not one.
    """
    vid = cfg.get("longform")
    if not vid:
        raise SystemExit("this Short's CONFIG has no 'longform' video id. Every Short must name "
                         "the long-form it feeds before it can be uploaded.")
    req = urllib.request.Request(
        "https://www.googleapis.com/youtube/v3/videos"
        f"?part=snippet,status,contentDetails&id={vid}",
        headers={"Authorization": f"Bearer {token}"},
    )
    with urllib.request.urlopen(req, timeout=60) as resp:
        body = json.loads(resp.read().decode())
    items = body.get("items", [])
    if not items:
        raise SystemExit(f"long-form {vid} not found on the channel — refusing to upload")
    v = items[0]
    privacy = v["status"].get("privacyStatus")
    if privacy != "public":
        raise SystemExit(
            f"long-form {vid} is '{privacy}'. A Short must not point at a destination the viewer "
            f"cannot open. Publish the long-form first, or schedule this Short after it."
        )
    dur = v["contentDetails"].get("duration", "")
    mins = re.search(r"(\d+)M", dur)
    if "H" not in dur and (not mins or int(mins.group(1)) < 4):
        raise SystemExit(f"'long-form' {vid} has duration {dur} — that is a Short, not a destination")

    url = f"https://www.youtube.com/watch?v={vid}"
    desc = cfg["description"]
    if url in "\n".join(desc.splitlines()[:3]):
        return desc
    return f"▶ FULL CASE: {v['snippet']['title']}\n{url}\n\n{desc}"


def initiate_upload(token: str, file_size: int, cfg: dict, publish_at: str) -> str:
    snippet = {
        "title": cfg["title"],
        "description": ensure_funnel_description(token, cfg),
        "tags": cfg["tags"],
        "categoryId": "27",
        "defaultLanguage": "en",
        "defaultAudioLanguage": "en",
    }
    status = {
        "privacyStatus": "private",
        "publishAt": publish_at,
        "selfDeclaredMadeForKids": False,
        "containsSyntheticMedia": True,
        "license": "youtube",
        "embeddable": True,
        "publicStatsViewable": True,
    }
    body = json.dumps({"snippet": snippet, "status": status}).encode("utf-8")
    req = urllib.request.Request(
        "https://www.googleapis.com/upload/youtube/v3/videos?uploadType=resumable&part=snippet,status",
        data=body,
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json; charset=UTF-8",
            "X-Upload-Content-Type": "video/mp4",
            "X-Upload-Content-Length": str(file_size),
        },
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=60) as resp:
        upload_url = resp.headers.get("Location", "")
    if not upload_url.startswith("https://www.googleapis.com/"):
        raise RuntimeError(f"Unexpected upload URL host: {upload_url[:80]}")
    return upload_url


def set_thumbnail(token: str, video_id: str, thumb: Path) -> dict:
    req = urllib.request.Request(
        f"https://www.googleapis.com/upload/youtube/v3/thumbnails/set?videoId={video_id}",
        data=thumb.read_bytes(),
        headers={"Authorization": f"Bearer {token}", "Content-Type": "image/png"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=180) as resp:
        return json.loads(resp.read().decode("utf-8"))


def delete_video(token: str, video_id: str) -> int:
    req = urllib.request.Request(
        f"https://www.googleapis.com/youtube/v3/videos?id={video_id}",
        headers={"Authorization": f"Bearer {token}"},
        method="DELETE",
    )
    with urllib.request.urlopen(req, timeout=60) as resp:
        return resp.status


def get_state(token: str, video_id: str) -> dict:
    req = urllib.request.Request(
        f"https://www.googleapis.com/youtube/v3/videos?part=snippet,status,processingDetails&id={video_id}",
        headers={"Authorization": f"Bearer {token}"},
    )
    with urllib.request.urlopen(req, timeout=60) as resp:
        return json.loads(resp.read().decode("utf-8"))


def compact(state: dict) -> dict:
    items = state.get("items") or []
    item = items[0] if items else {}
    st = item.get("status", {})
    pr = item.get("processingDetails", {})
    sn = item.get("snippet", {})
    return {
        "id": item.get("id"),
        "title": sn.get("title"),
        "privacyStatus": st.get("privacyStatus"),
        "publishAt": st.get("publishAt"),
        "uploadStatus": st.get("uploadStatus"),
        "processingStatus": pr.get("processingStatus"),
    }


# Binding from short182 on (the EP62-65 slate). Shorts below this number were designed before
# the funnel became a build requirement; they warn instead of failing so an in-flight batch is
# not bricked. Measured 2026-08-02: 46 published shorts, 4,391 views, ZERO links to a long-form.
FUNNEL_BINDING_FROM = 182


def _funnel_gate(short_no: int) -> None:
    """Refuse to schedule a Short whose corridor to the long-form is incomplete."""
    import check_short_funnel as csf

    rec_paths = csf._records([short_no])
    if not rec_paths:
        msg = (f"short{short_no}: no 09_package/short{short_no}_funnel.v001.json -- the five "
               f"funnel layers are unrecorded, so nothing can prove this short leads anywhere")
        if short_no >= FUNNEL_BINDING_FROM:
            raise RuntimeError(msg)
        print(f"WARN {msg} (pre-{FUNNEL_BINDING_FROM}, not blocking)")
        return
    rec = json.loads(rec_paths[0].read_text(encoding="utf-8"))
    worklist = csf.WORKLIST.read_text(encoding="utf-8") if csf.WORKLIST.is_file() else ""
    problems = csf.check_record(rec, csf._load_spoken(rec), worklist)
    if not problems:
        vid = rec.get("funnel_long_video_id")
        print(f"OK funnel: short{short_no} loops and carries all five layers to {vid}")
        return
    detail = "\n    - ".join(problems)
    msg = f"short{short_no}: funnel incomplete ({len(problems)})\n    - {detail}"
    if short_no >= FUNNEL_BINDING_FROM:
        raise RuntimeError(msg)
    print(f"WARN {msg}")


def main(argv: list[str]) -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    ap = argparse.ArgumentParser()
    ap.add_argument("--short", required=True, choices=sorted(CONFIG))
    ap.add_argument("--publish-at", required=True, help="RFC3339 UTC, e.g. 2026-06-29T03:00:00Z (=12:00 JST)")
    ap.add_argument("--replace", help="video_id of a prior scheduled upload to DELETE before re-scheduling (rework)")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args(argv)

    if not re.match(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$", args.publish_at):
        raise RuntimeError("--publish-at must be RFC3339 UTC like 2026-06-29T03:00:00Z")
    cfg = CONFIG[args.short]
    short_id = f"short{args.short}"
    video = OUT / f"{short_id}_yt_coverfirst.mp4"
    thumb = OUT / f"{short_id}_thumb.png"
    pkg = ROOT / "episodes" / cfg["ep"] / "09_package"
    result_path = pkg / f"{short_id}_youtube_schedule_result.{cfg['rev']}.json"

    if result_path.exists() and not args.replace:
        raise RuntimeError(f"Refusing duplicate: {result_path.relative_to(ROOT)} exists (pass --replace to rework)")
    for p in (video, thumb):
        if not p.exists():
            raise RuntimeError(f"Missing artifact: {p}")
    av, at = sha256_file(video), sha256_file(thumb)
    if av != cfg["video_sha256"]:
        raise RuntimeError(f"Video hash mismatch: expected {cfg['video_sha256']} actual {av}")
    if at != cfg["thumb_sha256"]:
        raise RuntimeError(f"Thumb hash mismatch: expected {cfg['thumb_sha256']} actual {at}")
    _funnel_gate(int(args.short))
    print(f"OK {short_id}: scheduled publish at {args.publish_at} (12:00 JST)")
    print(f"OK title: {cfg['title']}")
    if args.dry_run:
        print("DRY_RUN_OK no external writes performed")
        return 0

    token = _access_token(load_env())
    channel_id = get_channel_id(token)
    if channel_id not in CHANNEL_ALLOWLIST:
        raise RuntimeError(f"Channel {channel_id!r} not allowlisted")

    if args.replace:
        code = delete_video(token, args.replace)
        print(f"OK deleted superseded scheduled video {args.replace} (HTTP {code})")
        if result_path.exists():
            bak = result_path.with_suffix(result_path.suffix + ".superseded")
            result_path.replace(bak)
            print(f"OK archived old result -> {bak.name}")

    # An upload costs 1600 of the 10,000 daily units, so six is the hard ceiling per Pacific day.
    # Check before sending a hundred megabytes: on 2026-08-03 the allowance ran out mid-session
    # and the failure arrived as an opaque 403 after the bytes were already on the wire.
    from yt_quota import UNITS, assert_budget, record, remaining
    assert_budget(UNITS["videos.insert"] + UNITS["thumbnails.set"],
                  what=f"scheduling {args.short}")

    upload_url = initiate_upload(token, video.stat().st_size, cfg, args.publish_at)
    print(f"OK upload started ({video.stat().st_size/1e6:.1f} MB)")
    video_id = upload_chunks(upload_url, token, video)
    record("videos.insert")
    if not video_id:
        raise RuntimeError("Upload returned no video_id")
    print(f"OK uploaded (private, scheduled) video_id={video_id} "
          f"[quota left today ~{remaining()}]")

    thumb_status = thumb_error = None
    try:
        thumb_status = set_thumbnail(token, video_id, thumb)
        record("thumbnails.set")
        print("OK thumbnail set via API")
    except urllib.error.HTTPError as e:
        thumb_error = {"code": e.code, "reason": str(e.reason), "body": e.read().decode("utf-8", errors="replace")}
        print(f"WARN thumbnail set HTTP {e.code}; cover frame is baked in")

    # brief wait so processing/publishAt are reflected
    state = {}
    for _ in range(10):
        state = get_state(token, video_id)
        c = compact(state)
        if c.get("uploadStatus") in {"processed", "uploaded"}:
            break
        time.sleep(8)
    c = compact(state)
    if c.get("privacyStatus") != "private" or not c.get("publishAt"):
        raise RuntimeError(f"Schedule not confirmed: privacy={c.get('privacyStatus')} publishAt={c.get('publishAt')}")

    now = datetime.now(timezone.utc).isoformat()
    result = {
        "schema_version": "1.0.0",
        "episode_id": cfg["ep"],
        "short_id": short_id,
        "platform": "youtube",
        "revision": cfg["rev"],
        "mode": "scheduled",
        "video_id": video_id,
        "watch": f"https://youtu.be/{video_id}",
        "studio": f"https://studio.youtube.com/video/{video_id}/edit",
        "channel_id": channel_id,
        "privacy": c.get("privacyStatus"),
        "publishAt": c.get("publishAt"),
        "publishAt_requested": args.publish_at,
        "title": cfg["title"],
        "description": cfg["description"],
        "tags": cfg["tags"],
        "video_file": str(video.relative_to(ROOT)).replace("\\", "/"),
        "video_sha256": "sha256:" + cfg["video_sha256"],
        "thumbnail_file": str(thumb.relative_to(ROOT)).replace("\\", "/"),
        "thumbnail_sha256": "sha256:" + cfg["thumb_sha256"],
        "thumbnail_set": thumb_status is not None,
        "thumbnail_status": thumb_status,
        "thumbnail_error": thumb_error,
        "cover_frame_baked_in": True,
        "cover_frame_duration_sec": 0.7,
        "madeForKids": False,
        "containsSyntheticMedia": True,
        "external_upload": True,
        "public_publish": False,
        "owner_instruction": "1日1本・毎回12:00 JST予約・各本オーナーが一度OK",
        "scheduled_at": now,
        "youtube_state_compact": c,
        "youtube_state": state,
    }
    write_json(result_path, result)
    print(json.dumps({
        "short": short_id,
        "video_id": video_id,
        "watch": f"https://youtu.be/{video_id}",
        "privacy": c.get("privacyStatus"),
        "publishAt": c.get("publishAt"),
        "thumbnail_set": thumb_status is not None,
        "result": str(result_path.relative_to(ROOT)).replace("\\", "/"),
    }, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
