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
        "rev": "v003",
        "title": "He walked out in 2015. The two murders he was condemned for were never solved #Shorts",
        "description": "He walked out in 2015. The two murders he was condemned for were never solved.\n\nNobody with the power to stop it ever checked. How was that possible for thirty years?\n\nPrime Documentary covers the cases that quietly decide what the state may do to you. The full episode is linked at the top.\n\n#Shorts #AnthonyRayHinton #DeathRow #WrongfulConviction #Alabama #Documentary",
        "tags": ["Shorts", "Anthony Ray Hinton", "Death Row", "Wrongful Conviction", "Alabama", "Law", "Documentary"],
        # v002: re-rendered - mid-roll kinetic typography (2 beats), look approved 2026-08-04
        # v003: re-rendered - archive rebind across all four drives + AI-generated clips removed
        "video_sha256": "ab7345b0e43024dd61e84080d72b759bb69eda3eab4e2f9907e41a6619c967e9",
        "thumb_sha256": "096551b3e93f3c283758514ad01728537d81378fa75a1f752c77b9c53fe98c7e",
    },
    "98": {
        # destination for the funnel link; ensure_funnel_description() verifies it is public
        "longform": "Sz8zPUoBANM",
        "ep": "PD-2026-014-lange",
        "rev": "v003",
        "title": "The Court did not say police can never follow you in. It said there is no automatic yes #Shorts",
        "description": "The Court did not say police can never follow you in. It said there is no automatic yes.\n\nIf it is not automatic, what does an officer have to show instead?\n\nPrime Documentary covers the cases that quietly decide what the state may do to you. The full episode is linked at the top.\n\n#Shorts #LangevCalifornia #HotPursuit #SupremeCourt #FourthAmendment #Documentary",
        "tags": ["Shorts", "Lange v California", "Hot Pursuit", "Supreme Court", "Fourth Amendment", "Law", "Documentary"],
        # v002: re-rendered - mid-roll kinetic typography (2 beats), look approved 2026-08-04
        # v003: re-rendered - archive rebind across all four drives + AI-generated clips removed
        "video_sha256": "1ae50283396a3573ecea23cc1bf284d649ca9927e457591aca4bf73011e33447",
        "thumb_sha256": "f3b4a2990f46c2ec1143ff561a098909441d841e31d61dd539f28e0690d26366",
    },
    "99": {
        # destination for the funnel link; ensure_funnel_description() verifies it is public
        "longform": "Sz8zPUoBANM",
        "ep": "PD-2026-014-lange",
        "rev": "v003",
        "title": "The baseline nobody states out loud: without a warrant, your door stays shut #Shorts",
        "description": "The baseline nobody states out loud: without a warrant, your door stays shut.\n\nHow narrow is narrow — what actually counts as an emergency?\n\nPrime Documentary covers the cases that quietly decide what the state may do to you. The full episode is linked at the top.\n\n#Shorts #LangevCalifornia #HotPursuit #SupremeCourt #FourthAmendment #Documentary",
        "tags": ["Shorts", "Lange v California", "Hot Pursuit", "Supreme Court", "Fourth Amendment", "Law", "Documentary"],
        # v002: re-rendered - mid-roll kinetic typography (2 beats), look approved 2026-08-04
        # v003: re-rendered - archive rebind across all four drives + AI-generated clips removed
        "video_sha256": "028bc3ea8b406e0a7952ea25b32061ff5cbb9e1313482d4e344cc512f3190e64",
        "thumb_sha256": "9dc63f309fe7cf728a93280d5a7d0b7f5fae1a6cd50efd1512925047b98cadf4",
    },
    "100": {
        # destination for the funnel link; ensure_funnel_description() verifies it is public
        "longform": "tYZuE76Hwdc",
        "ep": "PD-2026-041-thompson",
        "rev": "v002",
        "title": "He won his freedom, then the Supreme Court took the money back #Shorts",
        "description": "He won his freedom, then the Supreme Court took the money back.\n\nIf one buried report is not enough, what would ever be enough?\n\nPrime Documentary covers the cases that quietly decide what the state may do to you. The full episode is linked at the top.\n\n#Shorts #ConnickvThompson #ProsecutorialMisconduct #Brady #DeathRow #Documentary",
        "tags": ["Shorts", "Connick v Thompson", "Prosecutorial Misconduct", "Brady", "Death Row", "Law", "Documentary"],
        # v001: this render already carries the mid-roll kinetic typography
        # v002: re-rendered - archive rebind across all four drives + AI-generated clips removed
        "video_sha256": "8d25e810f6833cc4d9015385ca9a418fdbdb64c9435417db5544842d52cc48ec",
        "thumb_sha256": "fe1bfba0da0c45dc900928474036d3f1cbcc958e782c0be2fba5dc9a16474574",
    },
    "101": {
        # destination for the funnel link; ensure_funnel_description() verifies it is public
        "longform": "tYZuE76Hwdc",
        "ep": "PD-2026-041-thompson",
        "rev": "v002",
        "title": "Louisiana set his execution date while the proof sat in a drawer #Shorts",
        "description": "Louisiana set his execution date while the proof sat in a drawer.\n\nThe report existed the whole time. Who decided it would never be handed over?\n\nPrime Documentary covers the cases that quietly decide what the state may do to you. The full episode is linked at the top.\n\n#Shorts #ConnickvThompson #WrongfulConviction #Brady #DeathRow #Documentary",
        "tags": ["Shorts", "Connick v Thompson", "Wrongful Conviction", "Brady", "Death Row", "Law", "Documentary"],
        # v001: this render already carries the mid-roll kinetic typography
        # v002: re-rendered - archive rebind across all four drives + AI-generated clips removed
        "video_sha256": "5a8be3c5d3808df13716bda2bac6a4a38bf21c72e91d7affbdfaf786bc580296",
        "thumb_sha256": "c42c31d51205012e1d513a2f1ff33f5b16bb1e0b978ab7d178798e795006be70",
    },
    "102": {
        # destination for the funnel link; ensure_funnel_description() verifies it is public
        "longform": "yRwxBfrOY5o",
        "ep": "PD-2026-043-caniglia",
        "rev": "v002",
        "title": "The excuse came from a 1973 case about a car. They used it on a house #Shorts",
        "description": "The excuse came from a 1973 case about a car. They used it on a house.\n\nOnce the caretaking excuse is gone, what can officers still do at your door?\n\nPrime Documentary covers the cases that quietly decide what the state may do to you. The full episode is linked at the top.\n\n#Shorts #CanigliavStrom #CommunityCaretaking #FourthAmendment #WelfareCheck #Documentary",
        "tags": ["Shorts", "Caniglia v Strom", "Community Caretaking", "Fourth Amendment", "Welfare Check", "Law", "Documentary"],
        # v001: this render already carries the mid-roll kinetic typography
        # v002: re-rendered - archive rebind across all four drives + AI-generated clips removed
        "video_sha256": "97e1a050bedcf0e65fe4bc89aecd168e897394bb711cfd2c3b9e377222a37c7b",
        "thumb_sha256": "7313f36a712e6de660bd0facf99276506870551f88d7dfb0ab5d7502301c9dff",
    },
    "103": {
        # destination for the funnel link; ensure_funnel_description() verifies it is public
        "longform": "yRwxBfrOY5o",
        "ep": "PD-2026-043-caniglia",
        "rev": "v002",
        "title": "The Court did not say police can never come in for your safety #Shorts",
        "description": "The Court did not say police can never come in for your safety.\n\nSo where exactly is the line between help and a search?\n\nPrime Documentary covers the cases that quietly decide what the state may do to you. The full episode is linked at the top.\n\n#Shorts #CanigliavStrom #ExigentCircumstances #FourthAmendment #WelfareCheck #Documentary",
        "tags": ["Shorts", "Caniglia v Strom", "Exigent Circumstances", "Fourth Amendment", "Welfare Check", "Law", "Documentary"],
        # v001: this render already carries the mid-roll kinetic typography
        # v002: re-rendered - archive rebind across all four drives + AI-generated clips removed
        "video_sha256": "cef830955a26a06f0d6d3f4471e52a9ad77fd78aa05e9bc5ec232ce2ce73478f",
        "thumb_sha256": "b030f601526dcea9b04d1e5cafe98a29294ed2b0fdbbee4471e1319d61e3c522",
    },
    "104": {
        # destination for the funnel link; ensure_funnel_description() verifies it is public
        "longform": "vikfOBHullI",
        "ep": "PD-2026-017-onecoin",
        "rev": "v001",
        "title": "Regulators warned. Germany ordered it stopped. It kept selling #Shorts",
        "description": "Regulators warned. Germany ordered it stopped. It kept selling.\n\nNone of it was hidden. So why did the warnings not stop it?\n\nPrime Documentary covers the cases that quietly decide what the state may do to you. The full episode is linked at the top.\n\n#Shorts #Onecoin #Law #Documentary",
        "tags": ["Shorts", "Onecoin", "Law", "Documentary"],
        # v001: generated from the design by gen_short_publish_config.py
        "video_sha256": "f0528b0ccab4a62d0bf383de9261ade9edafa3df218724f4d34e1346bc55b8bb",
        "thumb_sha256": "a05a17d468aa249d57800039fd03550090854ec175d454fa4c7b135a9e1a5143",
    },
    "105": {
        # destination for the funnel link; ensure_funnel_description() verifies it is public
        "longform": "vikfOBHullI",
        "ep": "PD-2026-017-onecoin",
        "rev": "v001",
        "title": "From the inside it could not be seen. They had built a world with no exits #Shorts",
        "description": "From the inside it could not be seen. They had built a world with no exits.\n\nIf the exits were closed, what did the first doubters actually hear back?\n\nPrime Documentary covers the cases that quietly decide what the state may do to you. The full episode is linked at the top.\n\n#Shorts #Onecoin #Law #Documentary",
        "tags": ["Shorts", "Onecoin", "Law", "Documentary"],
        # v001: generated from the design by gen_short_publish_config.py
        "video_sha256": "36339feae2b948ef2d749ce1c024b491fb4966cf6123c4602a7e364014f30a87",
        "thumb_sha256": "9e87cb863ec764ad9a47731f83173cf96397ed7ffb545261550db630e2079a2d",
    },
    "106": {
        # destination for the funnel link; ensure_funnel_description() verifies it is public
        "longform": "5L_HCGJxX_U",
        "ep": "PD-2026-030-cotton",
        "rev": "v001",
        "title": "In 1997 she sat down across from the man she had sent to prison #Shorts",
        "description": "In 1997 she sat down across from the man she had sent to prison.\n\nWhat did he say back to her?\n\nPrime Documentary covers the cases that quietly decide what the state may do to you. The full episode is linked at the top.\n\n#Shorts #Cotton #Law #Documentary",
        "tags": ["Shorts", "Cotton", "Law", "Documentary"],
        # v001: generated from the design by gen_short_publish_config.py
        "video_sha256": "8b53ed19f4f38b0ffc5840fdd724d928978ab65a59c1356c2667dac679ae7c8b",
        "thumb_sha256": "4030ca3c5d95369f1fb50ec9ed76d122a0ac16847d3aabf2c07c8907611ac8a0",
    },
    "107": {
        # destination for the funnel link; ensure_funnel_description() verifies it is public
        "longform": "5L_HCGJxX_U",
        "ep": "PD-2026-030-cotton",
        "rev": "v001",
        "title": "The problem was never that she was not certain enough #Shorts",
        "description": "The problem was never that she was not certain enough.\n\nIf certainty is not the test, what is?\n\nPrime Documentary covers the cases that quietly decide what the state may do to you. The full episode is linked at the top.\n\n#Shorts #Cotton #Law #Documentary",
        "tags": ["Shorts", "Cotton", "Law", "Documentary"],
        # v001: generated from the design by gen_short_publish_config.py
        "video_sha256": "b6c7f355992a527c52d1d723652dd09565ea56e945d44c57566ba71a02cdc0d6",
        "thumb_sha256": "f8be10ed890c14131247938f7bc906a0a1cef4a5738911de62e0402c6acc9867",
    },
    "108": {
        # destination for the funnel link; ensure_funnel_description() verifies it is public
        "longform": "FTm1icKgycU",
        "ep": "PD-2026-023-swartz",
        "rev": "v001",
        "title": "On 18 January 2012 the internet went dark. He was one of the people who made it happen #Shorts",
        "description": "On 18 January 2012 the internet went dark. He was one of the people who made it happen.\n\nHe beat a bill the whole industry expected to pass. How?\n\nPrime Documentary covers the cases that quietly decide what the state may do to you. The full episode is linked at the top.\n\n#Shorts #Swartz #Law #Documentary",
        "tags": ["Shorts", "Swartz", "Law", "Documentary"],
        # v001: generated from the design by gen_short_publish_config.py
        "video_sha256": "c1e0a4ba16856ca6c8dc1a1cc06295bf77fc89e3ec00785a378c18786292f20d",
        "thumb_sha256": "cb8d8fbfc53704b4cd6d8899ebf7f266d83687c41909643f04f32a3c95724195",
    },
    "109": {
        # destination for the funnel link; ensure_funnel_description() verifies it is public
        "longform": "FTm1icKgycU",
        "ep": "PD-2026-023-swartz",
        "rev": "v001",
        "title": "Nobody ever proved what he meant to do with the four point eight million files #Shorts",
        "description": "Nobody ever proved what he meant to do with the four point eight million files.\n\nIf the intent was never proven, what were the thirteen counts actually built on?\n\nPrime Documentary covers the cases that quietly decide what the state may do to you. The full episode is linked at the top.\n\n#Shorts #Swartz #Law #Documentary",
        "tags": ["Shorts", "Swartz", "Law", "Documentary"],
        # v001: generated from the design by gen_short_publish_config.py
        "video_sha256": "4e20671e86199e8639118f9c522aede4be8477a2b46305ee244333e1a7af4436",
        "thumb_sha256": "c3319b71331790e929a80a1d274b5a9df369b2967b625919895f594f1381aa93",
    },
    "110": {
        # destination for the funnel link; ensure_funnel_description() verifies it is public
        "longform": "cQFql7tT1fE",
        "ep": "PD-2026-001-miranda",
        "rev": "v001",
        "title": "Miranda was never one man's case: three other appeals were folded in before it reached #Shorts",
        "description": "Miranda was never one man's case: three other appeals were folded in before it reached.\n\nWhat the four warnings actually have to cover, and why two justices said the majority reached beyond what the Constitution required.\n\nPrime Documentary covers the cases that quietly decide what the state may do to you. The full episode is linked at the top.\n\n#Shorts #Miranda #Law #Documentary",
        "tags": ["Shorts", "Miranda", "Law", "Documentary"],
        # v001: generated from the design by gen_short_publish_config.py
        "video_sha256": "1f74d3ebaa1c8e2ba009d02a8b0300d19bd8cea3d4f6acffa92ed2bb3a444054",
        "thumb_sha256": "b5ca8f2fb5e8486bde09f5cf5571fedb59de5a3fe3f899198ac4d08281c3402a",
    },
    "111": {
        # destination for the funnel link; ensure_funnel_description() verifies it is public
        "longform": "An0to4U0hJQ",
        "ep": "PD-2026-003-mapp",
        "rev": "v001",
        "title": "The most famous objection to the Mapp rule was written by a New York judge in 1926 #Shorts",
        "description": "The most famous objection to the Mapp rule was written by a New York judge in 1926.\n\nWhich exceptions the justices carved out after 1961, and how much of the original rule is left.\n\nPrime Documentary covers the cases that quietly decide what the state may do to you. The full episode is linked at the top.\n\n#Shorts #Mapp #Law #Documentary",
        "tags": ["Shorts", "Mapp", "Law", "Documentary"],
        # v001: generated from the design by gen_short_publish_config.py
        "video_sha256": "c7a257118d3be7e9e2f5fcbdb46141fd5ceeb4f199f1e203690b79bcc1b8a0ec",
        "thumb_sha256": "9ac45d472f3349ef609cbde6b22d75c7ecbd0f585a257b3c2ed3b332c26ce790",
    },
    "112": {
        # destination for the funnel link; ensure_funnel_description() verifies it is public
        "longform": "XWYWAgkExH4",
        "ep": "PD-2026-007-riley",
        "rev": "v001",
        "title": "Get a warrant came with an off switch and a hard edge: in a real emergency police still do #Shorts",
        "description": "Get a warrant came with an off switch and a hard edge: in a real emergency police still do.\n\nWho owns the location trail the phone sends out by itself, and what the Court said about it four years later.\n\nPrime Documentary covers the cases that quietly decide what the state may do to you. The full episode is linked at the top.\n\n#Shorts #Riley #Law #Documentary",
        "tags": ["Shorts", "Riley", "Law", "Documentary"],
        # v001: generated from the design by gen_short_publish_config.py
        "video_sha256": "16d29caffb6b52434fffefafa226f9677f686011611d5b4281fc5794654cf126",
        "thumb_sha256": "f6cfbbc495752be044fe438dfbe3675e4d7a14dcae1a19a660a97ea2dc3c71b7",
    },
    "113": {
        # destination for the funnel link; ensure_funnel_description() verifies it is public
        "longform": "zE3nCUlUmLY",
        "ep": "PD-2026-008-carpenter",
        "rev": "v001",
        "title": "The reason nobody needed a warrant for Timothy Carpenter's twelve thousand location points #Shorts",
        "description": "The reason nobody needed a warrant for Timothy Carpenter's twelve thousand location points.\n\nWhat the third-party doctrine says about every other record a company holds about you, and whether the Court touched it.\n\nPrime Documentary covers the cases that quietly decide what the state may do to you. The full episode is linked at the top.\n\n#Shorts #Carpenter #Law #Documentary",
        "tags": ["Shorts", "Carpenter", "Law", "Documentary"],
        # v001: generated from the design by gen_short_publish_config.py
        "video_sha256": "dcd6847b8cf8c4afdaaec04239368765398235aa6a741cfdc8ee46b68ee4413c",
        "thumb_sha256": "1987470d329ce2a7f6ea52499953152173c1818e2f62647ed82d17020cefc220",
    },
    "114": {
        # destination for the funnel link; ensure_funnel_description() verifies it is public
        "longform": "zE3nCUlUmLY",
        "ep": "PD-2026-008-carpenter",
        "rev": "v001",
        "title": "Carpenter was five to four, and the four who lost warned that the majority had swapped #Shorts",
        "description": "Carpenter was five to four, and the four who lost warned that the majority had swapped.\n\nWhich of your other trails \u2014 searches, purchases, messages \u2014 the same logic reaches, and which it leaves exposed.\n\nPrime Documentary covers the cases that quietly decide what the state may do to you. The full episode is linked at the top.\n\n#Shorts #Carpenter #Law #Documentary",
        "tags": ["Shorts", "Carpenter", "Law", "Documentary"],
        # v001: generated from the design by gen_short_publish_config.py
        "video_sha256": "889e722134f442d6a7fe1b34bb0604cbdb0326a8d1816f9b5ba6c0fb115e61e1",
        "thumb_sha256": "7a916ba683def98bcdc872f76f91047e6fe343f219bc62e663705fa086dc53b2",
    },
    "115": {
        # destination for the funnel link; ensure_funnel_description() verifies it is public
        "longform": "m-uWzgWHGPg",
        "ep": "PD-2026-009-timbs",
        "rev": "v002",
        "title": "Forfeiture works by filing the case against your property instead of against you #Shorts",
        "description": "Forfeiture works by filing the case against your property instead of against you.\n\nWhere the limit on all of this finally came from, and why it is older than the country.\n\nPrime Documentary covers the cases that quietly decide what the state may do to you. The full episode is linked at the top.\n\n#Shorts #Timbs #Law #Documentary",
        "tags": ["Shorts", "Timbs", "Law", "Documentary"],
        # v001: generated from the design by gen_short_publish_config.py
        # v002: re-rendered - 16:9 ShortThumbYT thumbnail replaces the vertical cover, which YouTube letterboxed
        "video_sha256": "4797940a11400fbb81bf81257d2e80a07ec8ee04edf05dff4161011f800fa127",
        "thumb_sha256": "06ca74aa067871734f66179538005b166228813c5575bd47d64ec909aa01f91a",
    },
    "116": {
        # destination for the funnel link; ensure_funnel_description() verifies it is public
        "longform": "m-uWzgWHGPg",
        "ep": "PD-2026-009-timbs",
        "rev": "v002",
        "title": "The unanimous win did not abolish forfeiture and did not even declare the seizure of the car #Shorts",
        "description": "The unanimous win did not abolish forfeiture and did not even declare the seizure of the car.\n\nWhy two justices agreed with the result but insisted the Court had taken the wrong route to get there.\n\nPrime Documentary covers the cases that quietly decide what the state may do to you. The full episode is linked at the top.\n\n#Shorts #Timbs #Law #Documentary",
        "tags": ["Shorts", "Timbs", "Law", "Documentary"],
        # v001: generated from the design by gen_short_publish_config.py
        # v002: re-rendered - 16:9 ShortThumbYT thumbnail replaces the vertical cover, which YouTube letterboxed
        "video_sha256": "8011aab22b40e24de36168d0db71c31fa0ac2d37a86b6b3eb15dfd1129dbd012",
        "thumb_sha256": "ae36127ca4593b7c8764ae5919ba2e649b268ae880cdaf44b151559579eb10a5",
    },
    "117": {
        # destination for the funnel link; ensure_funnel_description() verifies it is public
        "longform": "89SQoRgAD7U",
        "ep": "PD-2026-010-kelo",
        "rev": "v002",
        "title": "Justice O'Connor's dissent is the part nobody quotes: after Kelo, any home could be taken #Shorts",
        "description": "Justice O'Connor's dissent is the part nobody quotes: after Kelo, any home could be taken.\n\nWhat the country did about the ruling afterward, and why forty state reforms changed less than people assume.\n\nPrime Documentary covers the cases that quietly decide what the state may do to you. The full episode is linked at the top.\n\n#Shorts #Kelo #Law #Documentary",
        "tags": ["Shorts", "Kelo", "Law", "Documentary"],
        # v001: generated from the design by gen_short_publish_config.py
        # v002: re-rendered - 16:9 ShortThumbYT thumbnail replaces the vertical cover, which YouTube letterboxed
        "video_sha256": "b1a0ca3f1996a2320d7e4a8340688cab4b36c8968975e82e239504776f7cfe9d",
        "thumb_sha256": "43f498927f4e9406564282c3caf39efeed5ab8a76b6735c15c5d4bfc0528bc0f",
    },
    "118": {
        # destination for the funnel link; ensure_funnel_description() verifies it is public
        "longform": "89SQoRgAD7U",
        "ep": "PD-2026-010-kelo",
        "rev": "v002",
        "title": "Roughly forty states rewrote their eminent domain laws after Kelo and many of those reforms #Shorts",
        "description": "Roughly forty states rewrote their eminent domain laws after Kelo and many of those reforms.\n\nWhat happened to Susette Kelo's pink house itself.\n\nPrime Documentary covers the cases that quietly decide what the state may do to you. The full episode is linked at the top.\n\n#Shorts #Kelo #Law #Documentary",
        "tags": ["Shorts", "Kelo", "Law", "Documentary"],
        # v001: generated from the design by gen_short_publish_config.py
        # v002: re-rendered - 16:9 ShortThumbYT thumbnail replaces the vertical cover, which YouTube letterboxed
        "video_sha256": "d0ff03b08e5b79da380520534d3f09d82babb8914538f66b699c3c0a46fdfa99",
        "thumb_sha256": "21b40dd304e7526858f6953a30133ba6f68add379e973990314c3d098cea4b82",
    },
    "119": {
        # destination for the funnel link; ensure_funnel_description() verifies it is public
        "longform": "cSfe3iGnBBM",
        "ep": "PD-2026-011-mahanoy",
        "rev": "v002",
        "title": "The school's entire case rested on disruption, and the disruption turned out to be a few #Shorts",
        "description": "The school's entire case rested on disruption, and the disruption turned out to be a few.\n\nThe one justice who dissented, and the history he said the majority was discarding.\n\nPrime Documentary covers the cases that quietly decide what the state may do to you. The full episode is linked at the top.\n\n#Shorts #Mahanoy #Law #Documentary",
        "tags": ["Shorts", "Mahanoy", "Law", "Documentary"],
        # v001: generated from the design by gen_short_publish_config.py
        # v002: re-rendered - 16:9 ShortThumbYT thumbnail replaces the vertical cover, which YouTube letterboxed
        "video_sha256": "b67e0dc883e882f07a74ae6fd4a29d824fdc180757830b15038de3832f193590",
        "thumb_sha256": "56e72c71a160b2da0fcdc59f6c5f9499d3a9252fbeeae6ba77b4207961b115d3",
    },
    "120": {
        # destination for the funnel link; ensure_funnel_description() verifies it is public
        "longform": "cSfe3iGnBBM",
        "ep": "PD-2026-011-mahanoy",
        "rev": "v002",
        "title": "The Court protected the student and then deliberately refused to say where the line #Shorts",
        "description": "The Court protected the student and then deliberately refused to say where the line.\n\nThe 1969 case that set the old test, and why the phone made that test stop working.\n\nPrime Documentary covers the cases that quietly decide what the state may do to you. The full episode is linked at the top.\n\n#Shorts #Mahanoy #Law #Documentary",
        "tags": ["Shorts", "Mahanoy", "Law", "Documentary"],
        # v001: generated from the design by gen_short_publish_config.py
        # v002: re-rendered - 16:9 ShortThumbYT thumbnail replaces the vertical cover, which YouTube letterboxed
        "video_sha256": "90877a6e68fb9b108172890de4f5bd9be49a43a4d3c0e602c7ac7b4e234c79bf",
        "thumb_sha256": "df7985314eaacc7b6466bbb18265fcad870a1dc9e384f370312d01d14990184e",
    },
    "121": {
        # destination for the funnel link; ensure_funnel_description() verifies it is public
        "longform": "1pox44KsaV8",
        "ep": "PD-2026-012-arbitration",
        "rev": "v002",
        "title": "Both rulings were five to four, and the dissents said what the majorities would not #Shorts",
        "description": "Both rulings were five to four, and the dissents said what the majorities would not.\n\nThe 1925 law that made all of this possible, and why it sat quiet for most of a century before companies found it.\n\nPrime Documentary covers the cases that quietly decide what the state may do to you. The full episode is linked at the top.\n\n#Shorts #Arbitration #Law #Documentary",
        "tags": ["Shorts", "Arbitration", "Law", "Documentary"],
        # v001: generated from the design by gen_short_publish_config.py
        # v002: re-rendered - 16:9 ShortThumbYT thumbnail replaces the vertical cover, which YouTube letterboxed
        "video_sha256": "264c3fc624baf7dfe370da507ca855ae6103f395c98300be9feebf8133e44d98",
        "thumb_sha256": "f8a3baa724da877a7f8dc16ffc83c5b7f93e7332d19b472004e1f3dc56dd2b64",
    },
    "122": {
        # destination for the funnel link; ensure_funnel_description() verifies it is public
        "longform": "1pox44KsaV8",
        "ep": "PD-2026-012-arbitration",
        "rev": "v002",
        "title": "You never signed the clause at all: it attaches when you activate a phone, open an account #Shorts",
        "description": "You never signed the clause at all: it attaches when you activate a phone, open an account.\n\nWhere lawmakers and regulators are still fighting to claw this back, and for which kinds of claims.\n\nPrime Documentary covers the cases that quietly decide what the state may do to you. The full episode is linked at the top.\n\n#Shorts #Arbitration #Law #Documentary",
        "tags": ["Shorts", "Arbitration", "Law", "Documentary"],
        # v001: generated from the design by gen_short_publish_config.py
        # v002: re-rendered - 16:9 ShortThumbYT thumbnail replaces the vertical cover, which YouTube letterboxed
        "video_sha256": "a7830c47abb2d49b6096cd84aff1cff564a3c6d7dfb2ea4acc97a26e0cc3a032",
        "thumb_sha256": "0e8a202ec85d9bc4669aab808aad05fffa3b52bb61fc96e5de140ef68384940d",
    },
    "130": {
        # destination for the funnel link; ensure_funnel_description() verifies it is public
        "longform": "g5yFmDt48oU",
        "ep": "PD-2026-013-king",
        "rev": "v002",
        "title": "The majority's whole case rests on one word, identification, and Justice Kennedy defined it #Shorts",
        "description": "The majority's whole case rests on one word, identification, and Justice Kennedy defined it.\n\nWhy did the Court's most conservative justice and three of its most liberal justices end up on the same side against that definition?\n\nPrime Documentary covers the cases that quietly decide what the state may do to you. The full episode is linked at the top.\n\n#Shorts #King #Law #Documentary",
        "tags": ["Shorts", "King", "Law", "Documentary"],
        # v001: generated from the design by gen_short_publish_config.py
        # v002: re-rendered - 16:9 ShortThumbYT thumbnail replaces the vertical cover, which YouTube letterboxed
        "video_sha256": "e636400b1cb5d67742bb7c97d89f30f89db7e91061a26bfdb966f27fd9694882",
        "thumb_sha256": "b4ff4a4f49f3c9498aafd1df9d88253ddc3eb8e598e7758ce0afaadbc746622b",
    },
    "131": {
        # destination for the funnel link; ensure_funnel_description() verifies it is public
        "longform": "g5yFmDt48oU",
        "ep": "PD-2026-013-king",
        "rev": "v002",
        "title": "A fingerprint reveals a pattern, while a DNA sample is a blueprint of your relatives #Shorts",
        "description": "A fingerprint reveals a pattern, while a DNA sample is a blueprint of your relatives.\n\nIf the law reads only a narrow set of markers today, who decides when that limit moves?\n\nPrime Documentary covers the cases that quietly decide what the state may do to you. The full episode is linked at the top.\n\n#Shorts #King #Law #Documentary",
        "tags": ["Shorts", "King", "Law", "Documentary"],
        # v001: generated from the design by gen_short_publish_config.py
        # v002: re-rendered - 16:9 ShortThumbYT thumbnail replaces the vertical cover, which YouTube letterboxed
        "video_sha256": "b24cc81f6704225d9702cca7229559406bc2daa546a7cf86fcd26c1fcc882b2c",
        "thumb_sha256": "c532f6601faad5ef7e5c4ab8184f7dd685e8f77bc9d00cb08d6fb078ac7ccbce",
    },
    "132": {
        # destination for the funnel link; ensure_funnel_description() verifies it is public
        "longform": "rrftLmSVivk",
        "ep": "PD-2026-025-kyllo",
        "rev": "v002",
        "title": "The rule protecting your home from a heat scan is tied to how rare the device is, so #Shorts",
        "description": "The rule protecting your home from a heat scan is tied to how rare the device is, so.\n\nWhich of today's ordinary sensors has already crossed from exotic into general public use?\n\nPrime Documentary covers the cases that quietly decide what the state may do to you. The full episode is linked at the top.\n\n#Shorts #Kyllo #Law #Documentary",
        "tags": ["Shorts", "Kyllo", "Law", "Documentary"],
        # v001: generated from the design by gen_short_publish_config.py
        # v002: re-rendered - 16:9 ShortThumbYT thumbnail replaces the vertical cover, which YouTube letterboxed
        "video_sha256": "d4ff990592acbdd5048aa5ade9d38deea30d34d50db8ac2071effb554854b628",
        "thumb_sha256": "46532e627fd6627ce8926e8dbf7ff2c1abf95d65661c73ab5444270f64e8b5b2",
    },
    "133": {
        # destination for the funnel link; ensure_funnel_description() verifies it is public
        "longform": "rrftLmSVivk",
        "ep": "PD-2026-025-kyllo",
        "rev": "v002",
        "title": "Kyllo never banned thermal imaging and never freed Danny Kyllo; it sent the case back #Shorts",
        "description": "Kyllo never banned thermal imaging and never freed Danny Kyllo; it sent the case back.\n\nOnce the thermal evidence was set aside, did the warrant against Kyllo still stand?\n\nPrime Documentary covers the cases that quietly decide what the state may do to you. The full episode is linked at the top.\n\n#Shorts #Kyllo #Law #Documentary",
        "tags": ["Shorts", "Kyllo", "Law", "Documentary"],
        # v001: generated from the design by gen_short_publish_config.py
        # v002: re-rendered - 16:9 ShortThumbYT thumbnail replaces the vertical cover, which YouTube letterboxed
        "video_sha256": "4d72b1ebe48529a240440690c8698ca46d1062b85edf9506af65affb2163a248",
        "thumb_sha256": "d2138e541bd4ed98907419c38e41d377bd34b3b9841b9dd899503a45ae38ecc8",
    },
    "134": {
        # destination for the funnel link; ensure_funnel_description() verifies it is public
        "longform": "68oWZRiOnB8",
        "ep": "PD-2026-026-katz",
        "rev": "v002",
        "title": "The one justice who dissented argued that a spoken sentence cannot be seized #Shorts",
        "description": "The one justice who dissented argued that a spoken sentence cannot be seized.\n\nIf the Constitution's words never mention conversations, where did the Court find the authority to protect them?\n\nPrime Documentary covers the cases that quietly decide what the state may do to you. The full episode is linked at the top.\n\n#Shorts #Katz #Law #Documentary",
        "tags": ["Shorts", "Katz", "Law", "Documentary"],
        # v001: generated from the design by gen_short_publish_config.py
        # v002: re-rendered - 16:9 ShortThumbYT thumbnail replaces the vertical cover, which YouTube letterboxed
        "video_sha256": "336ac3396c65fec06c66f3ff64835ad9006eee0237b90b46087795efc4d8600b",
        "thumb_sha256": "0803939f30174b1b6159339456449bea54bd39864bbc3c98e139c89b20fa0eb4",
    },
    "135": {
        # destination for the funnel link; ensure_funnel_description() verifies it is public
        "longform": "68oWZRiOnB8",
        "ep": "PD-2026-026-katz",
        "rev": "v002",
        "title": "Katz anchored your privacy to what society is still prepared to accept as reasonable, so it #Shorts",
        "description": "Katz anchored your privacy to what society is still prepared to accept as reasonable, so it.\n\nWhose expectations does a judge actually measure when he decides what society finds reasonable?\n\nPrime Documentary covers the cases that quietly decide what the state may do to you. The full episode is linked at the top.\n\n#Shorts #Katz #Law #Documentary",
        "tags": ["Shorts", "Katz", "Law", "Documentary"],
        # v001: generated from the design by gen_short_publish_config.py
        # v002: re-rendered - 16:9 ShortThumbYT thumbnail replaces the vertical cover, which YouTube letterboxed
        "video_sha256": "b71a1073172c093fbc75a255429b12914f2f9cdb7d256315c6ecb0142c4796f0",
        "thumb_sha256": "64ba77f084661cbb744f976a4ba11ab9386e8c76ca46a69d6b7c9b511b3cdca8",
    },
    "136": {
        # destination for the funnel link; ensure_funnel_description() verifies it is public
        "longform": "tpAKfHKuwqY",
        "ep": "PD-2026-027-rodriguez",
        "rev": "v002",
        "title": "The government argued seven minutes was too slight for the Constitution to count #Shorts",
        "description": "The government argued seven minutes was too slight for the Constitution to count.\n\nHad the dog walked the car before the warning instead of after it, would anything have changed?\n\nPrime Documentary covers the cases that quietly decide what the state may do to you. The full episode is linked at the top.\n\n#Shorts #Rodriguez #Law #Documentary",
        "tags": ["Shorts", "Rodriguez", "Law", "Documentary"],
        # v001: generated from the design by gen_short_publish_config.py
        # v002: re-rendered - 16:9 ShortThumbYT thumbnail replaces the vertical cover, which YouTube letterboxed
        "video_sha256": "dbef8a2a63a8f6b92f11349a227790281f063241b078922e2e2224e825256ce6",
        "thumb_sha256": "99185c09b0527ea87ed92e932958a86e8e9435e10f679c46b30088c9fc0e96f3",
    },
    "137": {
        # destination for the funnel link; ensure_funnel_description() verifies it is public
        "longform": "tpAKfHKuwqY",
        "ep": "PD-2026-027-rodriguez",
        "rev": "v002",
        "title": "Two justices dissented and argued the majority's timing rule punishes the officer who pauses #Shorts",
        "description": "Two justices dissented and argued the majority's timing rule punishes the officer who pauses.\n\nDid the officer in fact have independent grounds to keep the driver waiting, which is the question the case was sent back to answer?\n\nPrime Documentary covers the cases that quietly decide what the state may do to you. The full episode is linked at the top.\n\n#Shorts #Rodriguez #Law #Documentary",
        "tags": ["Shorts", "Rodriguez", "Law", "Documentary"],
        # v001: generated from the design by gen_short_publish_config.py
        # v002: re-rendered - 16:9 ShortThumbYT thumbnail replaces the vertical cover, which YouTube letterboxed
        "video_sha256": "8346ea651c661002c33a973d2850793a830b2ba8cd88cc0d4ad21b00a3eb5a32",
        "thumb_sha256": "03b5f506fd80508e54fe5e67c1217b0ed381a0cf6b251b4c14454c2f2a667de6",
    },
    "138": {
        # destination for the funnel link; ensure_funnel_description() verifies it is public
        "longform": "YQIhk2dKZHU",
        "ep": "PD-2026-031-unlock",
        "rev": "v002",
        "title": "The phone that is a fortress in your living room becomes an open book at the border, where #Shorts",
        "description": "The phone that is a fortress in your living room becomes an open book at the border, where.\n\nDoes the one judge who ruled a warrant is required at the border bind anyone yet?\n\nPrime Documentary covers the cases that quietly decide what the state may do to you. The full episode is linked at the top.\n\n#Shorts #Unlock #Law #Documentary",
        "tags": ["Shorts", "Unlock", "Law", "Documentary"],
        # v001: generated from the design by gen_short_publish_config.py
        # v002: re-rendered - 16:9 ShortThumbYT thumbnail replaces the vertical cover, which YouTube letterboxed
        "video_sha256": "2f27e244f89f7d9dd205e28c16082ae81a4e8c3b81ed982166bc7c6714bc19e2",
        "thumb_sha256": "567e1e8c64f1b1b725f1c7c814bd0736a2f9bb5eaf56b553812a8c7b7e86adb2",
    },
    "139": {
        # destination for the funnel link; ensure_funnel_description() verifies it is public
        "longform": "YQIhk2dKZHU",
        "ep": "PD-2026-031-unlock",
        "rev": "v002",
        "title": "The 2024 ruling that let officers press a man's thumb came with a hint that the answer flips #Shorts",
        "description": "The 2024 ruling that let officers press a man's thumb came with a hint that the answer flips.\n\nIf a flicker of choice is what the Fifth Amendment protects, where does that leave the face scan you set up for convenience?\n\nPrime Documentary covers the cases that quietly decide what the state may do to you. The full episode is linked at the top.\n\n#Shorts #Unlock #Law #Documentary",
        "tags": ["Shorts", "Unlock", "Law", "Documentary"],
        # v001: generated from the design by gen_short_publish_config.py
        # v002: re-rendered - 16:9 ShortThumbYT thumbnail replaces the vertical cover, which YouTube letterboxed
        "video_sha256": "b7aea484330e090841caad77ef8515d153c7bd2398216f9a02357e1461a5fc4a",
        "thumb_sha256": "36a5d42f807d17643e12335f0a4028bd40f493d0d109d40aa08d58edcbc7529a",
    },
    "140": {
        # destination for the funnel link; ensure_funnel_description() verifies it is public
        "longform": "GGW1SIAAgkY",
        "ep": "PD-2026-044-tekoh",
        "rev": "v002",
        "title": "Justice Alito's majority called the Miranda warnings a protective fence around the Fifth #Shorts",
        "description": "Justice Alito's majority called the Miranda warnings a protective fence around the Fifth.\n\nIf the warning is only a fence, what happens to the earlier ruling that called Miranda a constitutional rule?\n\nPrime Documentary covers the cases that quietly decide what the state may do to you. The full episode is linked at the top.\n\n#Shorts #Tekoh #Law #Documentary",
        "tags": ["Shorts", "Tekoh", "Law", "Documentary"],
        # v001: generated from the design by gen_short_publish_config.py
        # v002: re-rendered - 16:9 ShortThumbYT thumbnail replaces the vertical cover, which YouTube letterboxed
        "video_sha256": "9c2948f3cbda8be8e3051c449ba92e9f540de06b7626c9fdaa01fed8522d81a7",
        "thumb_sha256": "7ac548e9acac3f01073fd875c938cf9eb82fc3ab2b2bcb319656ebb65fe8dbdc",
    },
    "141": {
        # destination for the funnel link; ensure_funnel_description() verifies it is public
        "longform": "GGW1SIAAgkY",
        "ep": "PD-2026-044-tekoh",
        "rev": "v002",
        "title": "Justice Kagan's dissent warned that a right no remedy can back up slowly stops feeling like #Shorts",
        "description": "Justice Kagan's dissent warned that a right no remedy can back up slowly stops feeling like.\n\nIs Miranda a constitutional rule or only a safeguard, which is the question the two sides never resolved?\n\nPrime Documentary covers the cases that quietly decide what the state may do to you. The full episode is linked at the top.\n\n#Shorts #Tekoh #Law #Documentary",
        "tags": ["Shorts", "Tekoh", "Law", "Documentary"],
        # v001: generated from the design by gen_short_publish_config.py
        # v002: re-rendered - 16:9 ShortThumbYT thumbnail replaces the vertical cover, which YouTube letterboxed
        "video_sha256": "d5de783c3f50195369acb30eb71e3b36707a1481a637f5367bea9a21ac1e87d6",
        "thumb_sha256": "37b85d74b5409acb71acbad6b5d7ced5a36be1672f480ebfe800e3b99204ff65",
    },
    "142": {
        # destination for the funnel link; ensure_funnel_description() verifies it is public
        "longform": "bSnyfsulna8",
        "ep": "PD-2026-048-glover",
        "rev": "v002",
        "title": "The lone dissenter wrote that the majority had paved the road to reasonable suspicion based #Shorts",
        "description": "The lone dissenter wrote that the majority had paved the road to reasonable suspicion based.\n\nHow much would it have taken for the deputy to check who was actually driving?\n\nPrime Documentary covers the cases that quietly decide what the state may do to you. The full episode is linked at the top.\n\n#Shorts #Glover #Law #Documentary",
        "tags": ["Shorts", "Glover", "Law", "Documentary"],
        # v001: generated from the design by gen_short_publish_config.py
        # v002: re-rendered - 16:9 ShortThumbYT thumbnail replaces the vertical cover, which YouTube letterboxed
        "video_sha256": "f58b32dfb5c21e27f5a6cdbab4ee53a37bd17fba0a4d6f02446e607f09785ffd",
        "thumb_sha256": "44a3781b9b06c2215583a43bcc1c0c164e4106a178b6a864ab3bcc57173d6fbc",
    },
    "143": {
        # destination for the funnel link; ensure_funnel_description() verifies it is public
        "longform": "bSnyfsulna8",
        "ep": "PD-2026-048-glover",
        "rev": "v002",
        "title": "A concurrence turned the whole stop on one word in the record, revoked rather than #Shorts",
        "description": "A concurrence turned the whole stop on one word in the record, revoked rather than.\n\nIf the record had said suspended over an unpaid fee, would the same stop have survived?\n\nPrime Documentary covers the cases that quietly decide what the state may do to you. The full episode is linked at the top.\n\n#Shorts #Glover #Law #Documentary",
        "tags": ["Shorts", "Glover", "Law", "Documentary"],
        # v001: generated from the design by gen_short_publish_config.py
        # v002: re-rendered - 16:9 ShortThumbYT thumbnail replaces the vertical cover, which YouTube letterboxed
        "video_sha256": "2c63a8fc2ce9f088a85da17bf252de0b520af03228ac12f26f54e16b0072f833",
        "thumb_sha256": "42a368d89bf102092d858d1f649b3431fe07db38ac7ce46b131209f13294453c",
    },
    "144": {
        # destination for the funnel link; ensure_funnel_description() verifies it is public
        "longform": "2pLWw_vhfI8",
        "ep": "PD-2026-049-strieff",
        "rev": "v002",
        "title": "If you are one of the many Americans carrying a small outstanding warrant, an unlawful stop #Shorts",
        "description": "If you are one of the many Americans carrying a small outstanding warrant, an unlawful stop.\n\nDoes anything in the ruling stop an officer from stopping people at random to go looking for that warrant?\n\nPrime Documentary covers the cases that quietly decide what the state may do to you. The full episode is linked at the top.\n\n#Shorts #Strieff #Law #Documentary",
        "tags": ["Shorts", "Strieff", "Law", "Documentary"],
        # v001: generated from the design by gen_short_publish_config.py
        # v002: re-rendered - 16:9 ShortThumbYT thumbnail replaces the vertical cover, which YouTube letterboxed
        "video_sha256": "b3c5b61dc99e17ab567eb1252eca775f8bedfb6117e2ef95efc84b677cc3470d",
        "thumb_sha256": "80ecb81e292543ba246dd726b9edb0058c31773d43bfa01f0f51cac15f22ab42",
    },
    "145": {
        # destination for the funnel link; ensure_funnel_description() verifies it is public
        "longform": "2pLWw_vhfI8",
        "ep": "PD-2026-049-strieff",
        "rev": "v002",
        "title": "A second dissent in the same case went after arithmetic, arguing the ruling raises #Shorts",
        "description": "A second dissent in the same case went after arithmetic, arguing the ruling raises.\n\nIf the exclusionary rule exists to remove that temptation, what is left of it after this?\n\nPrime Documentary covers the cases that quietly decide what the state may do to you. The full episode is linked at the top.\n\n#Shorts #Strieff #Law #Documentary",
        "tags": ["Shorts", "Strieff", "Law", "Documentary"],
        # v001: generated from the design by gen_short_publish_config.py
        # v002: re-rendered - 16:9 ShortThumbYT thumbnail replaces the vertical cover, which YouTube letterboxed
        "video_sha256": "e3c90e5665250b057bcef6d809dfe18ac95c58838e50bd8d60d145a4452ed091",
        "thumb_sha256": "05692146e1b4ea0e4bd31217ce6fa08d33934246b764fcfb3e6f7bef0440290d",
    },
    "150": {
        # destination for the funnel link; ensure_funnel_description() verifies it is public
        "longform": "ch2hQ5jhDmQ",
        "ep": "PD-2026-002-gideon",
        "rev": "v002",
        "title": "Twenty years earlier the Supreme Court had already answered his exact question #Shorts",
        "description": "Twenty years earlier the Supreme Court had already answered his exact question.\n\nThousands of prisoners write to the Supreme Court every year. Why did the justices take this one letter?\n\nPrime Documentary covers the cases that quietly decide what the state may do to you. The full episode is linked at the top.\n\n#Shorts #Gideon #Law #Documentary",
        "tags": ["Shorts", "Gideon", "Law", "Documentary"],
        # v001: generated from the design by gen_short_publish_config.py
        # v002: re-rendered - 16:9 ShortThumbYT thumbnail replaces the vertical cover, which YouTube letterboxed
        "video_sha256": "353773eeac8c64c79a06172f941f0894bedc86d368318b96898d4f557a46a992",
        "thumb_sha256": "0b1a57ee0f9d6fa04f91f94942953611f86722f2ac24639fa854741ca3bc2e54",
    },
    "151": {
        # destination for the funnel link; ensure_funnel_description() verifies it is public
        "longform": "ch2hQ5jhDmQ",
        "ep": "PD-2026-002-gideon",
        "rev": "v002",
        "title": "Winning at the Supreme Court did not set him free. It sent him back to the same courtroom #Shorts",
        "description": "Winning at the Supreme Court did not set him free. It sent him back to the same courtroom.\n\nThe Court could create the right with a stroke of a pen. Who was ever going to pay for it?\n\nPrime Documentary covers the cases that quietly decide what the state may do to you. The full episode is linked at the top.\n\n#Shorts #Gideon #Law #Documentary",
        "tags": ["Shorts", "Gideon", "Law", "Documentary"],
        # v001: generated from the design by gen_short_publish_config.py
        # v002: re-rendered - 16:9 ShortThumbYT thumbnail replaces the vertical cover, which YouTube letterboxed
        "video_sha256": "5ffd73b0b41b51ae4ed2435e678a53d54383db861c8842132931940c73666273",
        "thumb_sha256": "e4b4a87bbaf5d64a1a2dd48dd79b622e58e1a441307271947a29cf4886e38919",
    },
    "152": {
        # destination for the funnel link; ensure_funnel_description() verifies it is public
        "longform": "waA4XJ9bYcE",
        "ep": "PD-2026-004-ftx",
        "rev": "v002",
        "title": "The week a million people asked for their money back at the same time, and the exchange #Shorts",
        "description": "The week a million people asked for their money back at the same time, and the exchange.\n\nThe money was not set on fire. So where did eight billion dollars actually go?\n\nPrime Documentary covers the cases that quietly decide what the state may do to you. The full episode is linked at the top.\n\n#Shorts #Ftx #Law #Documentary",
        "tags": ["Shorts", "Ftx", "Law", "Documentary"],
        # v001: generated from the design by gen_short_publish_config.py
        # v002: re-rendered - 16:9 ShortThumbYT thumbnail replaces the vertical cover, which YouTube letterboxed
        "video_sha256": "1c08f7454b0c2cfd95034a107ec96c9da3a2af53f2fd5dcb63b620a331721b1e",
        "thumb_sha256": "8ecf0ed60c3ea751ddda2fb724579596181d8df024d435868104da736b23da95",
    },
    "153": {
        # destination for the funnel link; ensure_funnel_description() verifies it is public
        "longform": "waA4XJ9bYcE",
        "ep": "PD-2026-004-ftx",
        "rev": "v002",
        "title": "The witnesses who ended him were not investigators. They were the people who built the thing #Shorts",
        "description": "The witnesses who ended him were not investigators. They were the people who built the thing.\n\nTwenty-five years for an eight-billion-dollar fraud. Too much, too little, or exactly right?\n\nPrime Documentary covers the cases that quietly decide what the state may do to you. The full episode is linked at the top.\n\n#Shorts #Ftx #Law #Documentary",
        "tags": ["Shorts", "Ftx", "Law", "Documentary"],
        # v001: generated from the design by gen_short_publish_config.py
        # v002: re-rendered - 16:9 ShortThumbYT thumbnail replaces the vertical cover, which YouTube letterboxed
        "video_sha256": "6c89a4ea2ce365806fcb82064d3a6977419cc90aeaad0f549a653e8e8836ecc3",
        "thumb_sha256": "82a03fc158fe68969c800fd8a32ddb26b813ec1a7dc5f37d3bc42b9b143b881d",
    },
    "154": {
        # destination for the funnel link; ensure_funnel_description() verifies it is public
        "longform": "LXFjJqE6vKU",
        "ep": "PD-2026-015-theranos",
        "rev": "v002",
        "title": "The jury convicted her on four counts, acquitted her on the patient counts, and could not #Shorts",
        "description": "The jury convicted her on four counts, acquitted her on the patient counts, and could not.\n\nIf the machine gave patients wrong answers, why did those charges not stick to her?\n\nPrime Documentary covers the cases that quietly decide what the state may do to you. The full episode is linked at the top.\n\n#Shorts #Theranos #Law #Documentary",
        "tags": ["Shorts", "Theranos", "Law", "Documentary"],
        # v001: generated from the design by gen_short_publish_config.py
        # v002: re-rendered - 16:9 ShortThumbYT thumbnail replaces the vertical cover, which YouTube letterboxed
        "video_sha256": "6e9c3a7726b3fe0dadcbe3c6f5b93b7279aae9f963a07cae7623665413b9304c",
        "thumb_sha256": "75a40bad049f1e3d00828877543338ddeb0bf51284017528b1a750fee83b26e8",
    },
    "155": {
        # destination for the funnel link; ensure_funnel_description() verifies it is public
        "longform": "LXFjJqE6vKU",
        "ep": "PD-2026-015-theranos",
        "rev": "v002",
        "title": "The board of household names was not oversight. It was the reason nobody looked #Shorts",
        "description": "The board of household names was not oversight. It was the reason nobody looked.\n\nWhen somebody finally did look, what did they find inside the machine?\n\nPrime Documentary covers the cases that quietly decide what the state may do to you. The full episode is linked at the top.\n\n#Shorts #Theranos #Law #Documentary",
        "tags": ["Shorts", "Theranos", "Law", "Documentary"],
        # v001: generated from the design by gen_short_publish_config.py
        # v002: re-rendered - 16:9 ShortThumbYT thumbnail replaces the vertical cover, which YouTube letterboxed
        "video_sha256": "4f0c477cf3ed28453365fd254168b33daf788e8eb0a203d7857895f472c8235c",
        "thumb_sha256": "f714cf2bc9eb6d010dd3034d064cf50ca449d780725465605b148d1a06f966af",
    },
    "156": {
        # destination for the funnel link; ensure_funnel_description() verifies it is public
        "longform": "5Jap-0h43A4",
        "ep": "PD-2026-018-flashcrash",
        "rev": "v002",
        "title": "The safety net ordinary people had set up to protect their savings is what sold those #Shorts",
        "description": "The safety net ordinary people had set up to protect their savings is what sold those.\n\nThe market came back inside an hour. So why did it take five years to work out what had pushed it?\n\nPrime Documentary covers the cases that quietly decide what the state may do to you. The full episode is linked at the top.\n\n#Shorts #Flashcrash #Law #Documentary",
        "tags": ["Shorts", "Flashcrash", "Law", "Documentary"],
        # v001: generated from the design by gen_short_publish_config.py
        # v002: re-rendered - 16:9 ShortThumbYT thumbnail replaces the vertical cover, which YouTube letterboxed
        "video_sha256": "83b32636bf07f96960e5c9991ee53eb0ae3da92ab58349df80ea83aa3b4c7758",
        "thumb_sha256": "b881e21a9b21834c5512f5c4a25081cd263073ad7bbe0e9a045081f60b07b4d6",
    },
    "157": {
        # destination for the funnel link; ensure_funnel_description() verifies it is public
        "longform": "5Jap-0h43A4",
        "ep": "PD-2026-018-flashcrash",
        "rev": "v002",
        "title": "He took tens of millions off the fastest machines on earth, and by the time they arrested #Shorts",
        "description": "He took tens of millions off the fastest machines on earth, and by the time they arrested.\n\nHow does one man in a bedroom lean hard enough on the largest market on earth to make it bend?\n\nPrime Documentary covers the cases that quietly decide what the state may do to you. The full episode is linked at the top.\n\n#Shorts #Flashcrash #Law #Documentary",
        "tags": ["Shorts", "Flashcrash", "Law", "Documentary"],
        # v001: generated from the design by gen_short_publish_config.py
        # v002: re-rendered - 16:9 ShortThumbYT thumbnail replaces the vertical cover, which YouTube letterboxed
        "video_sha256": "82ab71100151427ca71835b25c4c440981428c259f1c58de7ef8871dc1823028",
        "thumb_sha256": "9334ca7695e13484cb587c376efcbaf216f1f209989796371803c6315dbaa920",
    },
    "158": {
        # destination for the funnel link; ensure_funnel_description() verifies it is public
        "longform": "j8U8c4BB_GQ",
        "ep": "PD-2026-019-varsityblues",
        "rev": "v002",
        "title": "They did not just buy the seat. They wrote the bribe off on their taxes #Shorts",
        "description": "They did not just buy the seat. They wrote the bribe off on their taxes.\n\nParents paid roughly twenty-five million dollars. What exactly were they told they were guaranteed?\n\nPrime Documentary covers the cases that quietly decide what the state may do to you. The full episode is linked at the top.\n\n#Shorts #Varsityblues #Law #Documentary",
        "tags": ["Shorts", "Varsityblues", "Law", "Documentary"],
        # v001: generated from the design by gen_short_publish_config.py
        # v002: re-rendered - 16:9 ShortThumbYT thumbnail replaces the vertical cover, which YouTube letterboxed
        "video_sha256": "87bb300b741b0c8feb33eb85f0ca4cac01348213507912f8e9113f43837c3d10",
        "thumb_sha256": "5e9dee42f1aa0f2e657c5f42ee28cbc8cc90f3841300fb099e208fdc92079f91",
    },
    "159": {
        # destination for the funnel link; ensure_funnel_description() verifies it is public
        "longform": "j8U8c4BB_GQ",
        "ep": "PD-2026-019-varsityblues",
        "rev": "v002",
        "title": "For every child pushed through the side door, an honest student got a thinner envelope #Shorts",
        "description": "For every child pushed through the side door, an honest student got a thinner envelope.\n\nSo how do you manufacture a recruited athlete out of a child who has never played the sport?\n\nPrime Documentary covers the cases that quietly decide what the state may do to you. The full episode is linked at the top.\n\n#Shorts #Varsityblues #Law #Documentary",
        "tags": ["Shorts", "Varsityblues", "Law", "Documentary"],
        # v001: generated from the design by gen_short_publish_config.py
        # v002: re-rendered - 16:9 ShortThumbYT thumbnail replaces the vertical cover, which YouTube letterboxed
        "video_sha256": "4c4f13b1a321375cfc737df7400a93d5d3459ef1bc5616005b0b7c95ee81e1a9",
        "thumb_sha256": "41340e7ca8b452378f733a0535b07fd982f84f91bdfee950e013b66909e5409f",
    },
    "160": {
        # destination for the funnel link; ensure_funnel_description() verifies it is public
        "longform": "1h267U6PY0I",
        "ep": "PD-2026-020-gardner",
        "rev": "v002",
        "title": "What they left on the walls is stranger than what they took, and after thirty years nobody #Shorts",
        "description": "What they left on the walls is stranger than what they took, and after thirty years nobody.\n\nSo who does the FBI actually believe walked into that museum?\n\nPrime Documentary covers the cases that quietly decide what the state may do to you. The full episode is linked at the top.\n\n#Shorts #Gardner #Law #Documentary",
        "tags": ["Shorts", "Gardner", "Law", "Documentary"],
        # v001: generated from the design by gen_short_publish_config.py
        # v002: re-rendered - 16:9 ShortThumbYT thumbnail replaces the vertical cover, which YouTube letterboxed
        "video_sha256": "f1234842fb6137788e500addd20693a8250ea3c7c3f75eaebeb882ed2c29505f",
        "thumb_sha256": "ce285e317bde560540b8efff75e2acc8be56e93e12d73d2282e1fc4daedc3a34",
    },
    "161": {
        # destination for the funnel link; ensure_funnel_description() verifies it is public
        "longform": "1h267U6PY0I",
        "ep": "PD-2026-020-gardner",
        "rev": "v002",
        "title": "The FBI followed the paintings out of Boston as far as Philadelphia, and then lost them #Shorts",
        "description": "The FBI followed the paintings out of Boston as far as Philadelphia, and then lost them.\n\nTen million dollars has been sitting on the table for years. Why has nobody taken it?\n\nPrime Documentary covers the cases that quietly decide what the state may do to you. The full episode is linked at the top.\n\n#Shorts #Gardner #Law #Documentary",
        "tags": ["Shorts", "Gardner", "Law", "Documentary"],
        # v001: generated from the design by gen_short_publish_config.py
        # v002: re-rendered - 16:9 ShortThumbYT thumbnail replaces the vertical cover, which YouTube letterboxed
        "video_sha256": "7a61f60a5f406c0c41f9d7f58ec49786351115fb4636f9d353d55ec39a9d963c",
        "thumb_sha256": "f87d58fb235a9fdab9315c0cd6a46871eb80fe5b173d1ba4c55c6b60c9df338a",
    },
    "162": {
        # destination for the funnel link; ensure_funnel_description() verifies it is public
        "longform": "mj9qEKPRatE",
        "ep": "PD-2026-022-milken",
        "rev": "v002",
        "title": "One sheet of paper from his firm could put any company in America into play overnight #Shorts",
        "description": "One sheet of paper from his firm could put any company in America into play overnight.\n\nWhere in all of that did he stop bending the rules and start breaking them?\n\nPrime Documentary covers the cases that quietly decide what the state may do to you. The full episode is linked at the top.\n\n#Shorts #Milken #Law #Documentary",
        "tags": ["Shorts", "Milken", "Law", "Documentary"],
        # v001: generated from the design by gen_short_publish_config.py
        # v002: re-rendered - 16:9 ShortThumbYT thumbnail replaces the vertical cover, which YouTube letterboxed
        "video_sha256": "a63531ca1004e6a556356d2b5ca4bcfd38fd7c7222940a1d9987e27efaab2f1d",
        "thumb_sha256": "fbe51ccfe9ad43cbf96d13f5ca55c57318e560f3873bde2c4f44c78ae8a33495",
    },
    "163": {
        # destination for the funnel link; ensure_funnel_description() verifies it is public
        "longform": "mj9qEKPRatE",
        "ep": "PD-2026-022-milken",
        "rev": "v002",
        "title": "Weeks out of prison he was told he had months to live, and he is still here decades later #Shorts",
        "description": "Weeks out of prison he was told he had months to live, and he is still here decades later.\n\nA record fine, a lifetime ban, and a presidential pardon. Which of those actually stuck?\n\nPrime Documentary covers the cases that quietly decide what the state may do to you. The full episode is linked at the top.\n\n#Shorts #Milken #Law #Documentary",
        "tags": ["Shorts", "Milken", "Law", "Documentary"],
        # v001: generated from the design by gen_short_publish_config.py
        # v002: re-rendered - 16:9 ShortThumbYT thumbnail replaces the vertical cover, which YouTube letterboxed
        "video_sha256": "9395ba824c0401573292ba451636f6d4e45ff1b5b22afffd5832ab55c9549c53",
        "thumb_sha256": "256172e5bd255df94fa35b6056179a70ca955f69b0824387df1069025371c060",
    },
    "164": {
        # destination for the funnel link; ensure_funnel_description() verifies it is public
        "longform": "rYV4rxtQCV0",
        "ep": "PD-2026-024-rajaratnam",
        "rev": "v002",
        "title": "The argument that had protected the top of Wall Street for a generation died the moment #Shorts",
        "description": "The argument that had protected the top of Wall Street for a generation died the moment.\n\nA wiretap on a man in a good suit. How did a federal judge ever agree to that?\n\nPrime Documentary covers the cases that quietly decide what the state may do to you. The full episode is linked at the top.\n\n#Shorts #Rajaratnam #Law #Documentary",
        "tags": ["Shorts", "Rajaratnam", "Law", "Documentary"],
        # v001: generated from the design by gen_short_publish_config.py
        # v002: re-rendered - 16:9 ShortThumbYT thumbnail replaces the vertical cover, which YouTube letterboxed
        "video_sha256": "1072fb01c9dc308d8a68952a02ee41a9e4dd6843d68eacae0188502dcb390030",
        "thumb_sha256": "59aca605851affda65553dd7fcdb9d35d01f58e4a701715b4d0a010880249a60",
    },
    "165": {
        # destination for the funnel link; ensure_funnel_description() verifies it is public
        "longform": "rYV4rxtQCV0",
        "ep": "PD-2026-024-rajaratnam",
        "rev": "v002",
        "title": "You do not have to own a single share for this one to have been taken out of your pocket #Shorts",
        "description": "You do not have to own a single share for this one to have been taken out of your pocket.\n\nYou can see the suspicious trade on a chart. How do you ever prove a whisper?\n\nPrime Documentary covers the cases that quietly decide what the state may do to you. The full episode is linked at the top.\n\n#Shorts #Rajaratnam #Law #Documentary",
        "tags": ["Shorts", "Rajaratnam", "Law", "Documentary"],
        # v001: generated from the design by gen_short_publish_config.py
        # v002: re-rendered - 16:9 ShortThumbYT thumbnail replaces the vertical cover, which YouTube letterboxed
        "video_sha256": "23667cf1ab206f691bd48c6817729cfa515b0f7387e6ec7225308b57440a7507",
        "thumb_sha256": "0c813ad2c44cca0180dcb8baa591a67feb60fbe9f45ec35847ad862cdf573bc7",
    },
    "170": {
        # destination for the funnel link; ensure_funnel_description() verifies it is public
        "longform": "YhEJHK279f8",
        "ep": "PD-2026-028-forfeiture",
        "rev": "v002",
        "title": "The room where Philadelphia decided who kept their house had no judge in it and no lawyer #Shorts",
        "description": "The room where Philadelphia decided who kept their house had no judge in it and no lawyer.\n\nWho forced the city to shut Courtroom 478, and what it cost them to do it.\n\nPrime Documentary covers the cases that quietly decide what the state may do to you. The full episode is linked at the top.\n\n#Shorts #Forfeiture #Law #Documentary",
        "tags": ["Shorts", "Forfeiture", "Law", "Documentary"],
        # v001: generated from the design by gen_short_publish_config.py
        # v002: re-rendered - 16:9 ShortThumbYT thumbnail replaces the vertical cover, which YouTube letterboxed
        "video_sha256": "44a1e134fc8bcfc1f1df4f9b19bafc30a22dd52ff04f3b59338bf1106e959565",
        "thumb_sha256": "aa0007f7619720d7f29fc7edac4af8f8c18268e241872a9302c6fe0f65d3cea8",
    },
    "171": {
        # destination for the funnel link; ensure_funnel_description() verifies it is public
        "longform": "YhEJHK279f8",
        "ep": "PD-2026-028-forfeiture",
        "rev": "v002",
        "title": "To get back into the home the city had sealed, the parents had to sign an agreement barring #Shorts",
        "description": "To get back into the home the city had sealed, the parents had to sign an agreement barring.\n\nWhat they did after they got the house back, when they could simply have walked away.\n\nPrime Documentary covers the cases that quietly decide what the state may do to you. The full episode is linked at the top.\n\n#Shorts #Forfeiture #Law #Documentary",
        "tags": ["Shorts", "Forfeiture", "Law", "Documentary"],
        # v001: generated from the design by gen_short_publish_config.py
        # v002: re-rendered - 16:9 ShortThumbYT thumbnail replaces the vertical cover, which YouTube letterboxed
        "video_sha256": "c2b6ff1781801379b1d3eb8fd64fe9a844d29df563d17c11ff12baecd02b6372",
        "thumb_sha256": "b046d87005834cffc47bbb3b943e8050754eef9e880ae116d2382c89c7913b37",
    },
    "172": {
        # destination for the funnel link; ensure_funnel_description() verifies it is public
        "longform": "gR_nzXIyIlk",
        "ep": "PD-2026-036-williams",
        "rev": "v002",
        "title": "Your driver's license photo already sits in a lineup that runs every time a camera catches #Shorts",
        "description": "Your driver's license photo already sits in a lineup that runs every time a camera catches.\n\nWhat happened to the man the software picked, and how a ranked guess became probable cause.\n\nPrime Documentary covers the cases that quietly decide what the state may do to you. The full episode is linked at the top.\n\n#Shorts #Williams #Law #Documentary",
        "tags": ["Shorts", "Williams", "Law", "Documentary"],
        # v001: generated from the design by gen_short_publish_config.py
        # v002: re-rendered - 16:9 ShortThumbYT thumbnail replaces the vertical cover, which YouTube letterboxed
        "video_sha256": "cab8949e65b6c72067183571e4813a32bbde69fedb2feda364eb5868d5c05b04",
        "thumb_sha256": "e23806d803d979b402db7e4231aacb31885601bbbdf5960ed76df987e9864da2",
    },
    "173": {
        # destination for the funnel link; ensure_funnel_description() verifies it is public
        "longform": "gR_nzXIyIlk",
        "ep": "PD-2026-036-williams",
        "rev": "v002",
        "title": "The settlement that banned face-match arrests binds one police department, and people keep #Shorts",
        "description": "The settlement that banned face-match arrests binds one police department, and people keep.\n\nHow the software picked his face out of millions in the first place.\n\nPrime Documentary covers the cases that quietly decide what the state may do to you. The full episode is linked at the top.\n\n#Shorts #Williams #Law #Documentary",
        "tags": ["Shorts", "Williams", "Law", "Documentary"],
        # v001: generated from the design by gen_short_publish_config.py
        # v002: re-rendered - 16:9 ShortThumbYT thumbnail replaces the vertical cover, which YouTube letterboxed
        "video_sha256": "877d00a7057ee71021fa9b207d762b2c68de65b2ed621bf5e00361e2eb5f5706",
        "thumb_sha256": "2a075a2ad0aadea9f0b46f04a786ca70bcd395630b81cdb34cec76ac57b4915a",
    },
    "174": {
        # destination for the funnel link; ensure_funnel_description() verifies it is public
        "longform": "Pmh6h5SfWw4",
        "ep": "PD-2026-038-kidsforcash",
        "rev": "v002",
        "title": "Pennsylvania erased thousands of those convictions and could not give back one night any #Shorts",
        "description": "Pennsylvania erased thousands of those convictions and could not give back one night any.\n\nWhy a judge was sending children away in the first place.\n\nPrime Documentary covers the cases that quietly decide what the state may do to you. The full episode is linked at the top.\n\n#Shorts #Kidsforcash #Law #Documentary",
        "tags": ["Shorts", "Kidsforcash", "Law", "Documentary"],
        # v001: generated from the design by gen_short_publish_config.py
        # v002: re-rendered - 16:9 ShortThumbYT thumbnail replaces the vertical cover, which YouTube letterboxed
        "video_sha256": "522e62b7b74d36224b4a769ab9ede74c2950b5cda573ed84a1b79a7b03197830",
        "thumb_sha256": "2c064b0967d68c180a97ecfc1673c10d12b968120976915698bdaeec0e7034bc",
    },
    "175": {
        # destination for the funnel link; ensure_funnel_description() verifies it is public
        "longform": "X40EbUw5kzQ",
        "ep": "PD-2026-039-frazier",
        "rev": "v002",
        "title": "Officers may speak a lie about the evidence, and one Florida court held they may not print #Shorts",
        "description": "Officers may speak a lie about the evidence, and one Florida court held they may not print.\n\nWhat a spoken lie about a fingerprint took from a man with the comprehension of a ten-year-old.\n\nPrime Documentary covers the cases that quietly decide what the state may do to you. The full episode is linked at the top.\n\n#Shorts #Frazier #Law #Documentary",
        "tags": ["Shorts", "Frazier", "Law", "Documentary"],
        # v001: generated from the design by gen_short_publish_config.py
        # v002: re-rendered - 16:9 ShortThumbYT thumbnail replaces the vertical cover, which YouTube letterboxed
        "video_sha256": "c734f14ec0d23198b7ae1a5e4ecb305316aa5b69598f40ea5b948411fd04e88e",
        "thumb_sha256": "adf421ca9c810bd7cfc32d7e4ddcbc319308a2ae2ff94c3cc5bdfb4c17816369",
    },
    "176": {
        # destination for the funnel link; ensure_funnel_description() verifies it is public
        "longform": "X40EbUw5kzQ",
        "ep": "PD-2026-039-frazier",
        "rev": "v002",
        "title": "Roughly ten states now bar police from lying to a child in an interrogation, and not one #Shorts",
        "description": "Roughly ten states now bar police from lying to a child in an interrogation, and not one.\n\nWhat that lie did to a twenty-four-year-old the law counted as an adult.\n\nPrime Documentary covers the cases that quietly decide what the state may do to you. The full episode is linked at the top.\n\n#Shorts #Frazier #Law #Documentary",
        "tags": ["Shorts", "Frazier", "Law", "Documentary"],
        # v001: generated from the design by gen_short_publish_config.py
        # v002: re-rendered - 16:9 ShortThumbYT thumbnail replaces the vertical cover, which YouTube letterboxed
        "video_sha256": "69e3e2f9d6a0f06547fd66e90376cd92dc7c6d5350273acde83346ba1e5d3a9d",
        "thumb_sha256": "2f1183fd5aedb9f8b4bb8dc2e2e0a70417ece676985ce4aa73facf0e68545b2a",
    },
    "177": {
        # destination for the funnel link; ensure_funnel_description() verifies it is public
        "longform": "4uuY6G0LmHo",
        "ep": "PD-2026-040-lech",
        "rev": "v002",
        "title": "Whether a family is paid for a house police lawfully destroyed turns on which city they #Shorts",
        "description": "Whether a family is paid for a house police lawfully destroyed turns on which city they.\n\nWhat nineteen hours of police entry did to one house in Colorado, and what its owner was offered afterwards.\n\nPrime Documentary covers the cases that quietly decide what the state may do to you. The full episode is linked at the top.\n\n#Shorts #Lech #Law #Documentary",
        "tags": ["Shorts", "Lech", "Law", "Documentary"],
        # v001: generated from the design by gen_short_publish_config.py
        # v002: re-rendered - 16:9 ShortThumbYT thumbnail replaces the vertical cover, which YouTube letterboxed
        "video_sha256": "6ea6a58ad7a28fd8df58712b45c93f13c6d5bc32654fd02ae4d2dbd0647dd62d",
        "thumb_sha256": "33ee1ca9cf108176f1a16cfac9e5530c067f7f8ca52d11ca84043c01373ceb60",
    },
    "178": {
        # destination for the funnel link; ensure_funnel_description() verifies it is public
        "longform": "4uuY6G0LmHo",
        "ep": "PD-2026-040-lech",
        "rev": "v002",
        "title": "Two justices wrote that this question needs further percolation in the lower courts #Shorts",
        "description": "Two justices wrote that this question needs further percolation in the lower courts.\n\nWhose house it was, and what nineteen hours of police entry left of it.\n\nPrime Documentary covers the cases that quietly decide what the state may do to you. The full episode is linked at the top.\n\n#Shorts #Lech #Law #Documentary",
        "tags": ["Shorts", "Lech", "Law", "Documentary"],
        # v001: generated from the design by gen_short_publish_config.py
        # v002: re-rendered - 16:9 ShortThumbYT thumbnail replaces the vertical cover, which YouTube letterboxed
        "video_sha256": "6a987b3693d12574268175d878f3d2cc42c8177b365f1d2f1b057aab56b4178a",
        "thumb_sha256": "b3e0967dccdc0a0c7457c2971dd236b72eb059189100b437c822400910df1151",
    },
    "179": {
        # destination for the funnel link; ensure_funnel_description() verifies it is public
        "longform": "Enok7A7wGBA",
        "ep": "PD-2026-042-young",
        "rev": "v002",
        "title": "The Supreme Court kept the knock-and-announce rule and took away the only punishment #Shorts",
        "description": "The Supreme Court kept the knock-and-announce rule and took away the only punishment.\n\nWhat that remaining remedy was actually worth to a woman whose door was the wrong one.\n\nPrime Documentary covers the cases that quietly decide what the state may do to you. The full episode is linked at the top.\n\n#Shorts #Young #Law #Documentary",
        "tags": ["Shorts", "Young", "Law", "Documentary"],
        # v001: generated from the design by gen_short_publish_config.py
        # v002: re-rendered - 16:9 ShortThumbYT thumbnail replaces the vertical cover, which YouTube letterboxed
        "video_sha256": "11d84d0e9c7257d258f9bc592e1d93f2d870d31dd8d80b348aafead91c442a2a",
        "thumb_sha256": "86ccaeeed6171d0344e7e7e8813339a17a471d0428309b1194686bae56cf10eb",
    },
    "180": {
        # destination for the funnel link; ensure_funnel_description() verifies it is public
        "longform": "AxOlQ2NIaBU",
        "ep": "PD-2026-045-cleveland",
        "rev": "v002",
        "title": "An Alabama judge looked at how his own state's courts collected fines from poor people #Shorts",
        "description": "An Alabama judge looked at how his own state's courts collected fines from poor people.\n\nWhat that machine had already done to one woman in Montgomery before anyone moved to stop it.\n\nPrime Documentary covers the cases that quietly decide what the state may do to you. The full episode is linked at the top.\n\n#Shorts #Cleveland #Law #Documentary",
        "tags": ["Shorts", "Cleveland", "Law", "Documentary"],
        # v001: generated from the design by gen_short_publish_config.py
        # v002: re-rendered - 16:9 ShortThumbYT thumbnail replaces the vertical cover, which YouTube letterboxed
        "video_sha256": "e93e84a3fc56ad9231466be83178a25fd21d117cfdb67f345f1959918a43b967",
        "thumb_sha256": "a823ba4a224ffc400c239cd1ec736c49f56607fdd3214edb711be11fd537194e",
    },
    "181": {
        # destination for the funnel link; ensure_funnel_description() verifies it is public
        "longform": "AxOlQ2NIaBU",
        "ep": "PD-2026-045-cleveland",
        "rev": "v002",
        "title": "The 1983 rule against jailing people for being broke was written for a man who had been laid #Shorts",
        "description": "The 1983 rule against jailing people for being broke was written for a man who had been laid.\n\nWhy that rule never reached a courtroom in Montgomery three decades later.\n\nPrime Documentary covers the cases that quietly decide what the state may do to you. The full episode is linked at the top.\n\n#Shorts #Cleveland #Law #Documentary",
        "tags": ["Shorts", "Cleveland", "Law", "Documentary"],
        # v001: generated from the design by gen_short_publish_config.py
        # v002: re-rendered - 16:9 ShortThumbYT thumbnail replaces the vertical cover, which YouTube letterboxed
        "video_sha256": "5961f3709133035fc411b077936b0412c1e8836f7cdf31ee11ef2a73246644e7",
        "thumb_sha256": "3e216e3940869ce2ef1daba6855546bcef35a804238c0488e9f8a6b5e1116484",
    },
    "182": {
        # destination for the funnel link; ensure_funnel_description() verifies it is public
        "longform": "hC5KE6IqmhM",
        "ep": "PD-2026-046-tlo",
        "rev": "v002",
        "title": "The two-part test means a lawful school search can become an unlawful one halfway through #Shorts",
        "description": "The two-part test means a lawful school search can become an unlawful one halfway through.\n\nHow far did the search of that one purse actually go before anyone asked whether it was still lawful?\n\nPrime Documentary covers the cases that quietly decide what the state may do to you. The full episode is linked at the top.\n\n#Shorts #Tlo #Law #Documentary",
        "tags": ["Shorts", "Tlo", "Law", "Documentary"],
        # v001: generated from the design by gen_short_publish_config.py
        # v002: re-rendered - 16:9 ShortThumbYT thumbnail replaces the vertical cover, which YouTube letterboxed
        "video_sha256": "4a9efd95f1bd034d804ec3fc9281c05452f63fb101a4c1fe1330cde2d4fdb6ed",
        "thumb_sha256": "ee6affd16ee13149275fcc2e3d69ba569aadcbf059011b456d899f0ddd565785",
    },
    "183": {
        # destination for the funnel link; ensure_funnel_description() verifies it is public
        "longform": "hC5KE6IqmhM",
        "ep": "PD-2026-046-tlo",
        "rev": "v002",
        "title": "The lowered school standard was written for educators alone, and the Court kept a higher #Shorts",
        "description": "The lowered school standard was written for educators alone, and the Court kept a higher.\n\nWhat did the Court say a school official may do on his own authority, and where exactly does that authority stop?\n\nPrime Documentary covers the cases that quietly decide what the state may do to you. The full episode is linked at the top.\n\n#Shorts #Tlo #Law #Documentary",
        "tags": ["Shorts", "Tlo", "Law", "Documentary"],
        # v001: generated from the design by gen_short_publish_config.py
        # v002: re-rendered - 16:9 ShortThumbYT thumbnail replaces the vertical cover, which YouTube letterboxed
        "video_sha256": "cf517a490c2076716879660c055e37094e95e9f0663ef667fd7c7cc5792a39ce",
        "thumb_sha256": "5ed6802a71f4d6e88683f0d02b345c238b4de8b0e1d8584e7eff936664a161ff",
    },
    "184": {
        # destination for the funnel link; ensure_funnel_description() verifies it is public
        "longform": "i95peRcdtz4",
        "ep": "PD-2026-047-atwater",
        "rev": "v002",
        "title": "Every heavy thing done to Gail Atwater that afternoon happened before any finding of guilt #Shorts",
        "description": "Every heavy thing done to Gail Atwater that afternoon happened before any finding of guilt.\n\nIf a cell was never available as her punishment, what did the Supreme Court say the police were still permitted to do to her?\n\nPrime Documentary covers the cases that quietly decide what the state may do to you. The full episode is linked at the top.\n\n#Shorts #Atwater #Law #Documentary",
        "tags": ["Shorts", "Atwater", "Law", "Documentary"],
        # v001: generated from the design by gen_short_publish_config.py
        # v002: re-rendered - 16:9 ShortThumbYT thumbnail replaces the vertical cover, which YouTube letterboxed
        "video_sha256": "8b55ae809d5db74fb2071f24bb44d117e82431dbbd19dc0e54f8d37ef25b60aa",
        "thumb_sha256": "7863db0ef3223dba9a90bbae239265efeff968b1c5cc8c47fe1ecbf122ea844d",
    },
    "185": {
        # destination for the funnel link; ensure_funnel_description() verifies it is public
        "longform": "i95peRcdtz4",
        "ep": "PD-2026-047-atwater",
        "rev": "v002",
        "title": "The majority handed the remedy to legislatures, so protection against an arrest like hers #Shorts",
        "description": "The majority handed the remedy to legislatures, so protection against an arrest like hers.\n\nWhat did the majority itself call the arrest, in the same opinion in which it held that the Constitution permits it?\n\nPrime Documentary covers the cases that quietly decide what the state may do to you. The full episode is linked at the top.\n\n#Shorts #Atwater #Law #Documentary",
        "tags": ["Shorts", "Atwater", "Law", "Documentary"],
        # v001: generated from the design by gen_short_publish_config.py
        # v002: re-rendered - 16:9 ShortThumbYT thumbnail replaces the vertical cover, which YouTube letterboxed
        "video_sha256": "95292579bed57299a13905c366caff1dc370c7681560e4c60d1980926cc80383",
        "thumb_sha256": "7e03f5592039ac227885f2d3ac9a4cec4b9ebea7e222c791dc11d8e65dc4220e",
    },
    "186": {
        # destination for the funnel link; ensure_funnel_description() verifies it is public
        "longform": "l7-oHSNEIjc",
        "ep": "PD-2026-051-willingham",
        "rev": "v002",
        "title": "Each of the arson indicators had an ordinary explanation: flashover makes the pour patterns #Shorts",
        "description": "Each of the arson indicators had an ordinary explanation: flashover makes the pour patterns.\n\nIf the fire was never a crime, why did every court that reviewed the case let the execution go forward?\n\nPrime Documentary covers the cases that quietly decide what the state may do to you. The full episode is linked at the top.\n\n#Shorts #Willingham #Law #Documentary",
        "tags": ["Shorts", "Willingham", "Law", "Documentary"],
        # v001: generated from the design by gen_short_publish_config.py
        # v002: re-rendered - 16:9 ShortThumbYT thumbnail replaces the vertical cover, which YouTube letterboxed
        "video_sha256": "19b1135d619b78baf90a73882412283afda37d3972870d9895af24731ca28b07",
        "thumb_sha256": "1e027b091206f09df70de77228f960fc1007941caee9967a2f0da55c0023fec5",
    },
    "187": {
        # destination for the funnel link; ensure_funnel_description() verifies it is public
        "longform": "l7-oHSNEIjc",
        "ep": "PD-2026-051-willingham",
        "rev": "v002",
        "title": "Texas built a commission to ask whether the science was reliable, and the meeting where #Shorts",
        "description": "Texas built a commission to ask whether the science was reliable, and the meeting where.\n\nWhat had the state's own expert found in the fire evidence that made a scheduled public meeting worth stopping?\n\nPrime Documentary covers the cases that quietly decide what the state may do to you. The full episode is linked at the top.\n\n#Shorts #Willingham #Law #Documentary",
        "tags": ["Shorts", "Willingham", "Law", "Documentary"],
        # v001: generated from the design by gen_short_publish_config.py
        # v002: re-rendered - 16:9 ShortThumbYT thumbnail replaces the vertical cover, which YouTube letterboxed
        "video_sha256": "66ed05221d4f62eff5a5c9da428fa0a015f83934a40097cbfb458ff66023bd20",
        "thumb_sha256": "f9806e87cb53232d02dbe7ef3da9c924840d9b4d2b07f8f9dd4a473d4a75ccb4",
    },
    "188": {
        # destination for the funnel link; ensure_funnel_description() verifies it is public
        "longform": "67gynOvKf1M",
        "ep": "PD-2026-052-morton",
        "rev": "v002",
        "title": "The alibi was not disproved, it was engineered away: a stomach-contents estimate moved #Shorts",
        "description": "The alibi was not disproved, it was engineered away: a stomach-contents estimate moved.\n\nIf nothing in that house pointed to him, what was already sitting in the sheriff's own file that the jury never saw?\n\nPrime Documentary covers the cases that quietly decide what the state may do to you. The full episode is linked at the top.\n\n#Shorts #Morton #Law #Documentary",
        "tags": ["Shorts", "Morton", "Law", "Documentary"],
        # v001: generated from the design by gen_short_publish_config.py
        # v002: re-rendered - 16:9 ShortThumbYT thumbnail replaces the vertical cover, which YouTube letterboxed
        "video_sha256": "e6b19cb0d80619ed2007af60471822ff4f001af5ff621538aa5f4bf84e2ae8f0",
        "thumb_sha256": "54b5ca66ee28669ef4cd0effdddcc0e9514ca8dd63ea32d46832d4a4852db2a6",
    },
    "189": {
        # destination for the funnel link; ensure_funnel_description() verifies it is public
        "longform": "67gynOvKf1M",
        "ep": "PD-2026-052-morton",
        "rev": "v002",
        "title": "The successor district attorney spent roughly six years fighting the DNA test itself, so #Shorts",
        "description": "The successor district attorney spent roughly six years fighting the DNA test itself, so.\n\nWhat did the laboratory find on that bandana, and whose name came back with it?\n\nPrime Documentary covers the cases that quietly decide what the state may do to you. The full episode is linked at the top.\n\n#Shorts #Morton #Law #Documentary",
        "tags": ["Shorts", "Morton", "Law", "Documentary"],
        # v001: generated from the design by gen_short_publish_config.py
        # v002: re-rendered - 16:9 ShortThumbYT thumbnail replaces the vertical cover, which YouTube letterboxed
        "video_sha256": "463315edd3e6d71d9a55dbce06f63477244bd3ee388f70cb28c376bc6747ac2e",
        "thumb_sha256": "760159329e421b1c3640709b413f977e74ea37b7f75bdfb4c9768c40f7613a29",
    },
    "190": {
        # destination for the funnel link; ensure_funnel_description() verifies it is public
        "longform": "bXATF9ZnKLE",
        "ep": "PD-2026-032-carsearch",
        "rev": "v002",
        "title": "The automobile exception no longer requires any emergency at all: the Court has held #Shorts",
        "description": "The automobile exception no longer requires any emergency at all: the Court has held.\n\nIf the car being a car is emergency enough, is there any ground left where that power finally stops?\n\nPrime Documentary covers the cases that quietly decide what the state may do to you. The full episode is linked at the top.\n\n#Shorts #Carsearch #Law #Documentary",
        "tags": ["Shorts", "Carsearch", "Law", "Documentary"],
        # v001: generated from the design by gen_short_publish_config.py
        # v002: re-rendered - 16:9 ShortThumbYT thumbnail replaces the vertical cover, which YouTube letterboxed
        "video_sha256": "6a168fc28af9b8509ff434adff0d0027c9d6abaeec679e57359c6415ef51974a",
        "thumb_sha256": "291a0683925a136ed110f69a6f083afade7748c4fcf60a96032f8f61d7874024",
    },
    "191": {
        # destination for the funnel link; ensure_funnel_description() verifies it is public
        "longform": "bXATF9ZnKLE",
        "ep": "PD-2026-032-carsearch",
        "rev": "v002",
        "title": "Three limits on the car-search power that sit on the public road itself: an arrest does not #Shorts",
        "description": "Three limits on the car-search power that sit on the public road itself: an arrest does not.\n\nWhich of these limits an officer actually has to respect at your own window, and where the car-search power finally runs out of road.\n\nPrime Documentary covers the cases that quietly decide what the state may do to you. The full episode is linked at the top.\n\n#Shorts #Carsearch #Law #Documentary",
        "tags": ["Shorts", "Carsearch", "Law", "Documentary"],
        # v001: generated from the design by gen_short_publish_config.py
        # v002: re-rendered - 16:9 ShortThumbYT thumbnail replaces the vertical cover, which YouTube letterboxed
        "video_sha256": "a395f6fc1806e4417233b36cffbb7bc436cd987890190280e8b2067b52ba7c4f",
        "thumb_sha256": "d8be4b66239936463ffab8e2ab4fdf13196dda1dad8c49b333a2a0b6ee76468c",
    },
    "192": {
        # destination for the funnel link; ensure_funnel_description() verifies it is public
        "longform": "rU2vk9XL4vY",
        "ep": "PD-2026-033-tyler",
        "rev": "v002",
        "title": "Her lawyers stopped arguing about a Minnesota statute and argued eight hundred years of law #Shorts",
        "description": "Her lawyers stopped arguing about a Minnesota statute and argued eight hundred years of law.\n\nWhat nine justices did when a county's modern statute was set against a rule that old.\n\nPrime Documentary covers the cases that quietly decide what the state may do to you. The full episode is linked at the top.\n\n#Shorts #Tyler #Law #Documentary",
        "tags": ["Shorts", "Tyler", "Law", "Documentary"],
        # v001: generated from the design by gen_short_publish_config.py
        # v002: re-rendered - 16:9 ShortThumbYT thumbnail replaces the vertical cover, which YouTube letterboxed
        "video_sha256": "6e49d6c6ed1f76df65c03fc86b9254bcff10b4306f9384f9065b68dd66908e0d",
        "thumb_sha256": "029f16a2fa869c3e2f8410aba81addabcbb31b061565bf64f1100b171337d694",
    },
    "193": {
        # destination for the funnel link; ensure_funnel_description() verifies it is public
        "longform": "rU2vk9XL4vY",
        "ep": "PD-2026-033-tyler",
        "rev": "v002",
        "title": "The debt began at about two thousand three hundred dollars and grew itself into roughly #Shorts",
        "description": "The debt began at about two thousand three hundred dollars and grew itself into roughly.\n\nWhat the highest court in the country said about a debt that had multiplied itself six times over.\n\nPrime Documentary covers the cases that quietly decide what the state may do to you. The full episode is linked at the top.\n\n#Shorts #Tyler #Law #Documentary",
        "tags": ["Shorts", "Tyler", "Law", "Documentary"],
        # v001: generated from the design by gen_short_publish_config.py
        # v002: re-rendered - 16:9 ShortThumbYT thumbnail replaces the vertical cover, which YouTube letterboxed
        "video_sha256": "3898bf8fd880abb0358b185b1e2899839242dd6ba13b70af8a0917df366e3b78",
        "thumb_sha256": "0cf9ff073e08c5f278ffd31c99384daa32fecb94ec54fcd4bd30c86237693c87",
    },
    "194": {
        # destination for the funnel link; ensure_funnel_description() verifies it is public
        "longform": "6ozsIfwqrP0",
        "ep": "PD-2026-034-rolin",
        "rev": "v002",
        "title": "The mechanics that make an airport seizure work: the case is filed against the money itself #Shorts",
        "description": "The mechanics that make an airport seizure work: the case is filed against the money itself.\n\nWhat it took for one family to get their own savings back out of that machine.\n\nPrime Documentary covers the cases that quietly decide what the state may do to you. The full episode is linked at the top.\n\n#Shorts #Rolin #Law #Documentary",
        "tags": ["Shorts", "Rolin", "Law", "Documentary"],
        # v001: generated from the design by gen_short_publish_config.py
        # v002: re-rendered - 16:9 ShortThumbYT thumbnail replaces the vertical cover, which YouTube letterboxed
        "video_sha256": "9f044edc1a51ee7a0f2a0e58a1a82b76961bfc4b0bd8bd07ba4bd940ed18d7b7",
        "thumb_sha256": "1b318feef34de6f7801cbbdd8998e0d5e775ecd302e80112c644fde892b881e3",
    },
    "195": {
        # destination for the funnel link; ensure_funnel_description() verifies it is public
        "longform": "6ozsIfwqrP0",
        "ep": "PD-2026-034-rolin",
        "rev": "v002",
        "title": "The measured size of airport cash seizure, from a Justice Department watchdog's own count #Shorts",
        "description": "The measured size of airport cash seizure, from a Justice Department watchdog's own count.\n\nWhat happened to the one traveler whose case put those numbers in front of a court.\n\nPrime Documentary covers the cases that quietly decide what the state may do to you. The full episode is linked at the top.\n\n#Shorts #Rolin #Law #Documentary",
        "tags": ["Shorts", "Rolin", "Law", "Documentary"],
        # v001: generated from the design by gen_short_publish_config.py
        # v002: re-rendered - 16:9 ShortThumbYT thumbnail replaces the vertical cover, which YouTube letterboxed
        "video_sha256": "4405b63e725160db4f3dcb009cbec6924cd23a68910e2e36312c21813b555a96",
        "thumb_sha256": "680b4cea7013a7489ea2078b550859119bf4cb391d5787203913b15f11ee4d43",
    },
    "196": {
        # destination for the funnel link; ensure_funnel_description() verifies it is public
        "longform": "Xc_PxdC_75c",
        "ep": "PD-2026-035-hinders",
        "rev": "v002",
        "title": "Two owners caught by the same structuring theory ended opposite ways: a store owner in North #Shorts",
        "description": "Two owners caught by the same structuring theory ended opposite ways: a store owner in North.\n\nWhy two words in a dismissal order decided which of them the law would make whole.\n\nPrime Documentary covers the cases that quietly decide what the state may do to you. The full episode is linked at the top.\n\n#Shorts #Hinders #Law #Documentary",
        "tags": ["Shorts", "Hinders", "Law", "Documentary"],
        # v001: generated from the design by gen_short_publish_config.py
        # v002: re-rendered - 16:9 ShortThumbYT thumbnail replaces the vertical cover, which YouTube letterboxed
        "video_sha256": "77053c1a30a9314cbca218452073da9f48b67486a8b28b85ce178c0d6391a2d8",
        "thumb_sha256": "11a66cdfce705cb29c1b510fca6e03aed95cbee3d0c6b696efa73cf47a517279",
    },
    "197": {
        # destination for the funnel link; ensure_funnel_description() verifies it is public
        "longform": "Xc_PxdC_75c",
        "ep": "PD-2026-035-hinders",
        "rev": "v002",
        "title": "A Treasury watchdog measured these structuring seizures and found nine in ten #Shorts",
        "description": "A Treasury watchdog measured these structuring seizures and found nine in ten.\n\nWhat it finally took to close the specific trap that number exposed, and how much of the power survived.\n\nPrime Documentary covers the cases that quietly decide what the state may do to you. The full episode is linked at the top.\n\n#Shorts #Hinders #Law #Documentary",
        "tags": ["Shorts", "Hinders", "Law", "Documentary"],
        # v001: generated from the design by gen_short_publish_config.py
        # v002: re-rendered - 16:9 ShortThumbYT thumbnail replaces the vertical cover, which YouTube letterboxed
        "video_sha256": "6c372a9c0927338717055f88393f8c09cb46f74c44eeae4c860ec8cefdcf13d6",
        "thumb_sha256": "310ff9606229b7b4931c974666c28f8de9f86d54927316e971ac0c224e6f172d",
    },
    "200": {
        # destination for the funnel link; ensure_funnel_description() verifies it is public
        "longform": "H8j_K1x9Dog",
        "ep": "PD-2026-053-norfolk",
        "rev": "v002",
        "title": "Every DNA exclusion made the state's theory bigger instead of smaller, until it required #Shorts",
        "description": "Every DNA exclusion made the state's theory bigger instead of smaller, until it required.\n\nWhy did Virginia accept a guilty plea from a DNA-excluded sailor six weeks after its own laboratory identified the real killer?\n\nPrime Documentary covers the cases that quietly decide what the state may do to you. The full episode is linked at the top.\n\n#Shorts #Norfolk #Law #Documentary",
        "tags": ["Shorts", "Norfolk", "Law", "Documentary"],
        # v001: generated from the design by gen_short_publish_config.py
        # v002: re-rendered - 16:9 ShortThumbYT thumbnail replaces the vertical cover, which YouTube letterboxed
        "video_sha256": "504119b5114a1eebab0a6184ef476b7723055bd33433a69528f109be4aba71ea",
        "thumb_sha256": "db06779ab146eb3262c34c10be83e9ed08860e3340892ca77f4f9ad6766ce779",
    },
    "201": {
        # destination for the funnel link; ensure_funnel_description() verifies it is public
        "longform": "PfdEpNQyaQQ",
        "ep": "PD-2026-054-flowers",
        "rev": "v002",
        "title": "Reporters walked into rural Mississippi courthouse storerooms and counted every juror #Shorts",
        "description": "Reporters walked into rural Mississippi courthouse storerooms and counted every juror.\n\nIf those jury records were sitting in the storerooms the whole time, why did it take reporters rather than a court to add them up?\n\nPrime Documentary covers the cases that quietly decide what the state may do to you. The full episode is linked at the top.\n\n#Shorts #Flowers #Law #Documentary",
        "tags": ["Shorts", "Flowers", "Law", "Documentary"],
        # v001: generated from the design by gen_short_publish_config.py
        # v002: re-rendered - 16:9 ShortThumbYT thumbnail replaces the vertical cover, which YouTube letterboxed
        "video_sha256": "e969fcc4130e284bb82715f815a7a41190876d067e78147c86195942d9d7580d",
        "thumb_sha256": "ed51ca93fbd509d2495bb6b7dae275c9668281ed89beaca66fe29d216dd4fca3",
    },
    "202": {
        # destination for the funnel link; ensure_funnel_description() verifies it is public
        "longform": "Iw-EPUD2nHg",
        "ep": "PD-2026-055-burge",
        "rev": "v002",
        "title": "Illinois gave prosecutors three years to charge these crimes, so the clock on every provable #Shorts",
        "description": "Illinois gave prosecutors three years to charge these crimes, so the clock on every provable.\n\nIf every provable crime had expired, what was the one thing left that a federal jury could still convict him of?\n\nPrime Documentary covers the cases that quietly decide what the state may do to you. The full episode is linked at the top.\n\n#Shorts #Burge #Law #Documentary",
        "tags": ["Shorts", "Burge", "Law", "Documentary"],
        # v001: generated from the design by gen_short_publish_config.py
        # v002: re-rendered - 16:9 ShortThumbYT thumbnail replaces the vertical cover, which YouTube letterboxed
        "video_sha256": "670c1fac74d466a4229f32a88485dbdc643812620b00ec89f69907ba475968ae",
        "thumb_sha256": "8211567d2f9b1c42d4289eb00cea94ef5833a91332653b2bd80ef82262b98778",
    },
    "203": {
        # destination for the funnel link; ensure_funnel_description() verifies it is public
        "longform": "4FlCaOVpln0",
        "ep": "PD-2026-056-postoffice",
        "rev": "v002",
        "title": "A helpline told hundreds of sub-postmasters the same sentence, one call at a time, and being #Shorts",
        "description": "A helpline told hundreds of sub-postmasters the same sentence, one call at a time, and being.\n\nWho finally told the sub-postmasters, in writing, that they were not the only one, and how many years did that take?\n\nPrime Documentary covers the cases that quietly decide what the state may do to you. The full episode is linked at the top.\n\n#Shorts #Postoffice #Law #Documentary",
        "tags": ["Shorts", "Postoffice", "Law", "Documentary"],
        # v001: generated from the design by gen_short_publish_config.py
        # v002: re-rendered - 16:9 ShortThumbYT thumbnail replaces the vertical cover, which YouTube letterboxed
        "video_sha256": "f3b191bcbb487c88e5de0ffbd7a186f34226506b4cd733d4cb5111b4a5dc6694",
        "thumb_sha256": "c1ad0597237d48a972da17ae5c8c41d0df16bae66a4a78f8f3da732e5cb43324",
    },
    "204": {
        # destination for the funnel link; ensure_funnel_description() verifies it is public
        "longform": "4FlCaOVpln0",
        "ep": "PD-2026-056-postoffice",
        "rev": "v002",
        "title": "The Post Office investigated, charged and prosecuted its own sub-postmasters, holding all #Shorts",
        "description": "The Post Office investigated, charged and prosecuted its own sub-postmasters, holding all.\n\nIn England and Wales, who decided that a company could prosecute its own people without the police ever being involved?\n\nPrime Documentary covers the cases that quietly decide what the state may do to you. The full episode is linked at the top.\n\n#Shorts #Postoffice #Law #Documentary",
        "tags": ["Shorts", "Postoffice", "Law", "Documentary"],
        # v001: generated from the design by gen_short_publish_config.py
        # v002: re-rendered - 16:9 ShortThumbYT thumbnail replaces the vertical cover, which YouTube letterboxed
        "video_sha256": "82d66aa2df8234df404b50d5a6ec6b0d72b7b8a1ea64a469e81c3ec0e02e3b10",
        "thumb_sha256": "6c2ec2acc82e9158de89680c7667959ab09abc353c192db185807a6191bb1480",
    },
    "205": {
        # destination for the funnel link; ensure_funnel_description() verifies it is public
        "longform": "4FlCaOVpln0",
        "ep": "PD-2026-056-postoffice",
        "rev": "v002",
        "title": "In 2010 the Post Office put on paper what an honest look at its computer would cost it #Shorts",
        "description": "In 2010 the Post Office put on paper what an honest look at its computer would cost it.\n\nWho gave the instruction that the minutes about the defects should be destroyed, and what happened to the people who carried it out?\n\nPrime Documentary covers the cases that quietly decide what the state may do to you. The full episode is linked at the top.\n\n#Shorts #Postoffice #Law #Documentary",
        "tags": ["Shorts", "Postoffice", "Law", "Documentary"],
        # v001: generated from the design by gen_short_publish_config.py
        # v002: re-rendered - 16:9 ShortThumbYT thumbnail replaces the vertical cover, which YouTube letterboxed
        "video_sha256": "f3cb15d99578b88b280e2511037d7e79cc919a65d3d9e9593aa4d1711d44b34d",
        "thumb_sha256": "cda1b93f49d3095adc6e5c2807a4a6f81ef7c75bfaced72908199e623d40db4e",
    },
    "250": {
        # destination for the funnel link; ensure_funnel_description() verifies it is public
        "longform": "KPYLtYYODLE",
        "ep": "PD-2026-057-fieldtest",
        "rev": "v002",
        "title": "The whole procedure that turned a crumb into a felony charge was a colour change #Shorts",
        "description": "The whole procedure that turned a crumb into a felony charge was a colour change.\n\nIf the American government determined in writing in 1978 that this test proves nothing, why is it still riding in patrol cars?\n\nPrime Documentary covers the cases that quietly decide what the state may do to you. The full episode is linked at the top.\n\n#Shorts #Fieldtest #Law #Documentary",
        "tags": ["Shorts", "Fieldtest", "Law", "Documentary"],
        # v001: generated from the design by gen_short_publish_config.py
        # v002: re-rendered - 16:9 ShortThumbYT thumbnail replaces the vertical cover, which YouTube letterboxed
        "video_sha256": "ba13bf63405fb12195a2f9127f119e33a51879178e28ddb254cddc25c838cdf9",
        "thumb_sha256": "665f57a98a1e9680dc25e3eb3e94c3f167556fae6c8e34024a834a98d8409f39",
    },
    "251": {
        # destination for the funnel link; ensure_funnel_description() verifies it is public
        "longform": "KPYLtYYODLE",
        "ep": "PD-2026-057-fieldtest",
        "rev": "v002",
        "title": "People who had done nothing pleaded guilty five times faster than people who really had #Shorts",
        "description": "People who had done nothing pleaded guilty five times faster than people who really had.\n\nWhat was sitting in a sealed envelope in the property room while she was confessing to it in open court?\n\nPrime Documentary covers the cases that quietly decide what the state may do to you. The full episode is linked at the top.\n\n#Shorts #Fieldtest #Law #Documentary",
        "tags": ["Shorts", "Fieldtest", "Law", "Documentary"],
        # v001: generated from the design by gen_short_publish_config.py
        # v002: re-rendered - 16:9 ShortThumbYT thumbnail replaces the vertical cover, which YouTube letterboxed
        "video_sha256": "1ca01a622d35cac3b1ff67ae2df416e19c1927d175b0efb9e976183b96fb24f1",
        "thumb_sha256": "2f5c440bba831c1c2aedf37f242a37b41c600b5d7c1b3702cba6b391120b666f",
    },
    "252": {
        # destination for the funnel link; ensure_funnel_description() verifies it is public
        "longform": "KPYLtYYODLE",
        "ep": "PD-2026-057-fieldtest",
        "rev": "v002",
        "title": "The office that won every one of those convictions went back through its own files #Shorts",
        "description": "The office that won every one of those convictions went back through its own files.\n\nWhat happened to the hundred and seventy-two convictions that were still standing after the office finished counting?\n\nPrime Documentary covers the cases that quietly decide what the state may do to you. The full episode is linked at the top.\n\n#Shorts #Fieldtest #Law #Documentary",
        "tags": ["Shorts", "Fieldtest", "Law", "Documentary"],
        # v001: generated from the design by gen_short_publish_config.py
        # v002: re-rendered - 16:9 ShortThumbYT thumbnail replaces the vertical cover, which YouTube letterboxed
        "video_sha256": "1ae253c5c59c7b2f79d65219504e73f4e07f34b5c03fca5e3345d9809f972314",
        "thumb_sha256": "c3e13bbe96d39fdb849f3873d5f30c20af73876d7ac52a6204f323ae2112bb34",
    },
    "253": {
        # destination for the funnel link; ensure_funnel_description() verifies it is public
        "longform": "J97Rh1qOTPA",
        "ep": "PD-2026-058-lejeune",
        "rev": "v002",
        "title": "The Marine Corps' own laboratory wrote nine words about the drinking water in March 1981 #Shorts",
        "description": "The Marine Corps' own laboratory wrote nine words about the drinking water in March 1981.\n\nWho was still drinking that water in the six years between the form and the last plant closing?\n\nPrime Documentary covers the cases that quietly decide what the state may do to you. The full episode is linked at the top.\n\n#Shorts #Lejeune #Law #Documentary",
        "tags": ["Shorts", "Lejeune", "Law", "Documentary"],
        # v001: generated from the design by gen_short_publish_config.py
        # v002: re-rendered - 16:9 ShortThumbYT thumbnail replaces the vertical cover, which YouTube letterboxed
        "video_sha256": "96d6b2ce7e746a3f6fcb926d468f8da16db20ca41e15204351a3a943770ec7b3",
        "thumb_sha256": "c5bb4be68ddc6974f702419efd48188e697717682bf793bd818dfa3b76dd1e53",
    },
    "254": {
        # destination for the funnel link; ensure_funnel_description() verifies it is public
        "longform": "J97Rh1qOTPA",
        "ep": "PD-2026-058-lejeune",
        "rev": "v002",
        "title": "A retired drill instructor with no legal or scientific training built the only archive #Shorts",
        "description": "A retired drill instructor with no legal or scientific training built the only archive.\n\nWhat was on the form he finally pried loose, and why had the families never been told?\n\nPrime Documentary covers the cases that quietly decide what the state may do to you. The full episode is linked at the top.\n\n#Shorts #Lejeune #Law #Documentary",
        "tags": ["Shorts", "Lejeune", "Law", "Documentary"],
        # v001: generated from the design by gen_short_publish_config.py
        # v002: re-rendered - 16:9 ShortThumbYT thumbnail replaces the vertical cover, which YouTube letterboxed
        "video_sha256": "0087a281338a5addef43c047b324155f4efaa83990fc703b53e796bb6683cb46",
        "thumb_sha256": "682efc13aa9fe4872a3247a9f8992cc00d646bada7a759cd49279eefc332e3a8",
    },
    "255": {
        # destination for the funnel link; ensure_funnel_description() verifies it is public
        "longform": "J97Rh1qOTPA",
        "ep": "PD-2026-058-lejeune",
        "rev": "v002",
        "title": "Congress removed every legal barrier standing in front of Camp Lejeune claimants, and four #Shorts",
        "description": "Congress removed every legal barrier standing in front of Camp Lejeune claimants, and four.\n\nWhat happens to four hundred and eight thousand claims when the court's October deadline passes?\n\nPrime Documentary covers the cases that quietly decide what the state may do to you. The full episode is linked at the top.\n\n#Shorts #Lejeune #Law #Documentary",
        "tags": ["Shorts", "Lejeune", "Law", "Documentary"],
        # v001: generated from the design by gen_short_publish_config.py
        # v002: re-rendered - 16:9 ShortThumbYT thumbnail replaces the vertical cover, which YouTube letterboxed
        "video_sha256": "e7d2686b0c80b2ddfe9feaa6296e94c9ac0b5e6234c04791ef3665b4d74e4489",
        "thumb_sha256": "10d75644ef09719a6489a5e4a144ba9e566d48ca892c231a3169cc3aff62d168",
    },
    "256": {
        # destination for the funnel link; ensure_funnel_description() verifies it is public
        "longform": "Wo-SvvGsv8g",
        "ep": "PD-2026-059-robosigning",
        "rev": "v002",
        "title": "There was no mortgage on the house, and the bank foreclosed on it twice because six separate #Shorts",
        "description": "There was no mortgage on the house, and the bank foreclosed on it twice because six separate.\n\nHow does a bank produce a sworn court document about a house nobody has ever looked at?\n\nPrime Documentary covers the cases that quietly decide what the state may do to you. The full episode is linked at the top.\n\n#Shorts #Robosigning #Law #Documentary",
        "tags": ["Shorts", "Robosigning", "Law", "Documentary"],
        # v001: generated from the design by gen_short_publish_config.py
        # v002: re-rendered - 16:9 ShortThumbYT thumbnail replaces the vertical cover, which YouTube letterboxed
        "video_sha256": "9e34cc4789a2c3a9079619b2a5e78fe3e1481f31e9d86a03a855e07910aff6ad",
        "thumb_sha256": "3fdbc9ff22c9a304d797b7c9950d36ae0f301472b84a334beed4ba5e5c771fdf",
    },
    "257": {
        # destination for the funnel link; ensure_funnel_description() verifies it is public
        "longform": "Wo-SvvGsv8g",
        "ep": "PD-2026-059-robosigning",
        "rev": "v002",
        "title": "One man signed ten thousand sworn foreclosure documents a month, and a working month #Shorts",
        "description": "One man signed ten thousand sworn foreclosure documents a month, and a working month.\n\nIf nobody was reading the affidavits, how many of the houses taken on them were the wrong houses?\n\nPrime Documentary covers the cases that quietly decide what the state may do to you. The full episode is linked at the top.\n\n#Shorts #Robosigning #Law #Documentary",
        "tags": ["Shorts", "Robosigning", "Law", "Documentary"],
        # v001: generated from the design by gen_short_publish_config.py
        # v002: re-rendered - 16:9 ShortThumbYT thumbnail replaces the vertical cover, which YouTube letterboxed
        "video_sha256": "8ec1a83c6843276d511cb08f1909795e38eb00a1ec04e81060fe46729e7998cd",
        "thumb_sha256": "30d431f796d8c2354a571011ca321a02e57730d0998becb247af39eb6430155b",
    },
    "258": {
        # destination for the funnel link; ensure_funnel_description() verifies it is public
        "longform": "Wo-SvvGsv8g",
        "ep": "PD-2026-059-robosigning",
        "rev": "v002",
        "title": "A company in a Georgia office park produced more than a million forged mortgage documents #Shorts",
        "description": "A company in a Georgia office park produced more than a million forged mortgage documents.\n\nHow many American families lost a house on a document that was manufactured?\n\nPrime Documentary covers the cases that quietly decide what the state may do to you. The full episode is linked at the top.\n\n#Shorts #Robosigning #Law #Documentary",
        "tags": ["Shorts", "Robosigning", "Law", "Documentary"],
        # v001: generated from the design by gen_short_publish_config.py
        # v002: re-rendered - 16:9 ShortThumbYT thumbnail replaces the vertical cover, which YouTube letterboxed
        "video_sha256": "6497ceda7ef091c9e746765c607df575a511896212e671b1bd61970782ffb0fa",
        "thumb_sha256": "de56b0aaf5ab7f1e34945dbc6899f1d4a76141e6a59bf794b471b82f299c9183",
    },
    "259": {
        # destination for the funnel link; ensure_funnel_description() verifies it is public
        "longform": "Atla22DlJcU",
        "ep": "PD-2026-062-greene",
        "rev": "v001",
        "title": "The process servers knew children removed posted writs, but the record does not say #Shorts",
        "description": "The process servers knew children removed posted writs, but the record does not say.\n\nIf a paper on the door is unreliable, what notice does due process require instead?\n\nPrime Documentary covers the cases that quietly decide what the state may do to you. The full episode is linked at the top.\n\n#Shorts #Greene #Law #Documentary",
        "tags": ["Shorts", "Greene", "Law", "Documentary"],
        # v001: generated from the design by gen_short_publish_config.py
        "video_sha256": "6a03809bd0441257a461e966a951579e031cd763eac0dd9a793ef948f49a478d",
        "thumb_sha256": "0f534ee8345a06b773f036be6a7de0d22ed8945239fee9920d266c793b3f7196",
    },
    "260": {
        # destination for the funnel link; ensure_funnel_description() verifies it is public
        "longform": "Atla22DlJcU",
        "ep": "PD-2026-062-greene",
        "rev": "v001",
        "title": "Kentucky's procedure treated one unanswered visit as enough to post immediately, even though #Shorts",
        "description": "Kentucky's procedure treated one unanswered visit as enough to post immediately, even though.\n\nWhy was the sheriff's name on a case about a housing authority's paper?\n\nPrime Documentary covers the cases that quietly decide what the state may do to you. The full episode is linked at the top.\n\n#Shorts #Greene #Law #Documentary",
        "tags": ["Shorts", "Greene", "Law", "Documentary"],
        # v001: generated from the design by gen_short_publish_config.py
        "video_sha256": "8a0472b7e705860ccc4973c6cd68f57c6628e5cfebb0e0c1aa8bad42ccfe19f5",
        "thumb_sha256": "d8752be516a94d36ec1a8185e0be84b825a3e04a829eb343718c910464dec8a8",
    },
    "261": {
        # destination for the funnel link; ensure_funnel_description() verifies it is public
        "longform": "Atla22DlJcU",
        "ep": "PD-2026-062-greene",
        "rev": "v001",
        "title": "The dissent answered the majority's preference for mail with stolen mailboxes and evidence #Shorts",
        "description": "The dissent answered the majority's preference for mail with stolen mailboxes and evidence.\n\nIf neither the door nor the mail is perfectly reliable, what process is enough?\n\nPrime Documentary covers the cases that quietly decide what the state may do to you. The full episode is linked at the top.\n\n#Shorts #Greene #Law #Documentary",
        "tags": ["Shorts", "Greene", "Law", "Documentary"],
        # v001: generated from the design by gen_short_publish_config.py
        "video_sha256": "238c47ad71b5e1726eb2334584938686b70bfdd80a0df5772bbcc69f4a12965f",
        "thumb_sha256": "14c50b5b5af362e2627678297938aef094842e1c2644bb25c0a2a65899b2b713",
    },
    "262": {
        # destination for the funnel link; ensure_funnel_description() verifies it is public
        "longform": "D5zX7PcL6zQ",
        "ep": "PD-2026-063-correa",
        "rev": "v001",
        "title": "The hospital did not explicitly refuse screening; it gave a critically ill woman a number #Shorts",
        "description": "The hospital did not explicitly refuse screening; it gave a critically ill woman a number.\n\nWhat does emergency law require a hospital to do, and what finding did the appeals court decline to review?\n\nPrime Documentary covers the cases that quietly decide what the state may do to you. The full episode is linked at the top.\n\n#Shorts #Correa #Law #Documentary",
        "tags": ["Shorts", "Correa", "Law", "Documentary"],
        # v001: generated from the design by gen_short_publish_config.py
        "video_sha256": "ef39640dfadd118a305958d5deaeac217e28df4e6daaa09940a09fb73a64a0cd",
        "thumb_sha256": "749828264ad5ed9e1e653973ad2f7d5371bc43f3ba8cd1d1111006a9b2020001",
    },
    "263": {
        # destination for the funnel link; ensure_funnel_description() verifies it is public
        "longform": "D5zX7PcL6zQ",
        "ep": "PD-2026-063-correa",
        "rev": "v001",
        "title": "The court treated the word appropriate as undefined and built an even-handed screening rule #Shorts",
        "description": "The court treated the word appropriate as undefined and built an even-handed screening rule.\n\nIf the rule requires sameness, what happens when a hospital treats every similar patient equally badly?\n\nPrime Documentary covers the cases that quietly decide what the state may do to you. The full episode is linked at the top.\n\n#Shorts #Correa #Law #Documentary",
        "tags": ["Shorts", "Correa", "Law", "Documentary"],
        # v001: generated from the design by gen_short_publish_config.py
        "video_sha256": "8efc8996b2bbeee2b923a2158517b4bce2b3ab858740cb2ba95e5f7451532a18",
        "thumb_sha256": "65b0fd51794cfff95c4933d3c7e506d78e78d836799a8b186da9752fee5efe13",
    },
    "264": {
        # destination for the funnel link; ensure_funnel_description() verifies it is public
        "longform": "D5zX7PcL6zQ",
        "ep": "PD-2026-063-correa",
        "rev": "v001",
        "title": "The seven-hundred-thousand-dollar award separated the decedent's account from the survivors' #Shorts",
        "description": "The seven-hundred-thousand-dollar award separated the decedent's account from the survivors'.\n\nWhat argument did the appeals court refuse to reach because the hospital raised it too late?\n\nPrime Documentary covers the cases that quietly decide what the state may do to you. The full episode is linked at the top.\n\n#Shorts #Correa #Law #Documentary",
        "tags": ["Shorts", "Correa", "Law", "Documentary"],
        # v001: generated from the design by gen_short_publish_config.py
        "video_sha256": "38b6dc9436f28fce5e55522bda764e432f22742cd9c1e0c6950dca13fb0b3da1",
        "thumb_sha256": "2002b4c222fa3a7baa65d8324b60646bb2777943cd58448f1328084cda5d92fa",
    },
    "265": {
        # destination for the funnel link; ensure_funnel_description() verifies it is public
        "longform": "0EerFIEJbRk",
        "ep": "PD-2026-064-memphis",
        "rev": "v001",
        "title": "Two utility accounts differed by one middle initial, while the record itself disagreed about #Shorts",
        "description": "Two utility accounts differed by one middle initial, while the record itself disagreed about.\n\nIf the record cannot settle which account is yours, who can resolve the dispute before shutoff?\n\nPrime Documentary covers the cases that quietly decide what the state may do to you. The full episode is linked at the top.\n\n#Shorts #Memphis #Law #Documentary",
        "tags": ["Shorts", "Memphis", "Law", "Documentary"],
        # v001: generated from the design by gen_short_publish_config.py
        "video_sha256": "bd30ef61bf93017fc4384c136e3a32992c98575cdd46393aabf455f2d69614dd",
        "thumb_sha256": "bc3355872bba6c5d0ca45dc639f11870f6f711f822da70f8935269ac7d00c413",
    },
    "266": {
        # destination for the funnel link; ensure_funnel_description() verifies it is public
        "longform": "0EerFIEJbRk",
        "ep": "PD-2026-064-memphis",
        "rev": "v001",
        "title": "The final notice threatened termination but omitted the place, hours, and decision-maker #Shorts",
        "description": "The final notice threatened termination but omitted the place, hours, and decision-maker.\n\nThe Court did not abolish shutoffs, so what procedural protection did it actually add?\n\nPrime Documentary covers the cases that quietly decide what the state may do to you. The full episode is linked at the top.\n\n#Shorts #Memphis #Law #Documentary",
        "tags": ["Shorts", "Memphis", "Law", "Documentary"],
        # v001: generated from the design by gen_short_publish_config.py
        "video_sha256": "321e41ff4d2bda95291012895d254cd030c8302cfd2f7a48e4d2fd730e526cc2",
        "thumb_sha256": "a345cdbc37a15e2da63cb7263a91e4af805545f8f23504d56fd4c5180d85376e",
    },
    "267": {
        # destination for the funnel link; ensure_funnel_description() verifies it is public
        "longform": "0EerFIEJbRk",
        "ep": "PD-2026-064-memphis",
        "rev": "v001",
        "title": "The dissent described an operating phone system for about two thousand monthly cutoffs #Shorts",
        "description": "The dissent described an operating phone system for about two thousand monthly cutoffs.\n\nWhat did the Court leave undecided, and did the Crafts ever recover any money?\n\nPrime Documentary covers the cases that quietly decide what the state may do to you. The full episode is linked at the top.\n\n#Shorts #Memphis #Law #Documentary",
        "tags": ["Shorts", "Memphis", "Law", "Documentary"],
        # v001: generated from the design by gen_short_publish_config.py
        "video_sha256": "ad62a632487760d7ada3a1e8fa6be1e085fe38693208952e037ff9ace6389deb",
        "thumb_sha256": "c6feb8cfcf5b9a5e6dd33f2ec30869b3739e29030981df802f29b28d3c6d70fc",
    },
    "268": {
        # destination for the funnel link; ensure_funnel_description() verifies it is public
        "longform": "m19yjXNVotk",
        "ep": "PD-2026-065-marmet",
        "rev": "v001",
        "title": "Two nursing-home agreements sent every dispute to arbitration except claims for the home's #Shorts",
        "description": "Two nursing-home agreements sent every dispute to arbitration except claims for the home's.\n\nCan a family member's signature bind the patient who never signed? The Supreme Court left that question open.\n\nPrime Documentary covers the cases that quietly decide what the state may do to you. The full episode is linked at the top.\n\n#Shorts #Marmet #Law #Documentary",
        "tags": ["Shorts", "Marmet", "Law", "Documentary"],
        # v001: generated from the design by gen_short_publish_config.py
        "video_sha256": "3d59b0e70f78e49e90dfb97830fbafa77bb17268b3453a33c8434207a0044281",
        "thumb_sha256": "388f121cd7b0d81c59bef31be8f898e1d9a019157a331c2012ffbecc38472327",
    },
    "269": {
        # destination for the funnel link; ensure_funnel_description() verifies it is public
        "longform": "m19yjXNVotk",
        "ep": "PD-2026-065-marmet",
        "rev": "v001",
        "title": "The Supreme Court vacated and remanded without holding any arbitration clause valid #Shorts",
        "description": "The Supreme Court vacated and remanded without holding any arbitration clause valid.\n\nWhat happened to Brown, Taylor, and Marchio after remand, and why were their outcomes different?\n\nPrime Documentary covers the cases that quietly decide what the state may do to you. The full episode is linked at the top.\n\n#Shorts #Marmet #Law #Documentary",
        "tags": ["Shorts", "Marmet", "Law", "Documentary"],
        # v001: generated from the design by gen_short_publish_config.py
        "video_sha256": "8ac3533d0de5a324fe1c737800d8e21db7ea112038acf7bcfd83e1ff788336e9",
        "thumb_sha256": "c4b052f11a8c45492fc0880ff5c10b76e54b291d4d33d5ba4ca1bab98b1489cb",
    },
    "270": {
        # destination for the funnel link; ensure_funnel_description() verifies it is public
        "longform": "m19yjXNVotk",
        "ep": "PD-2026-065-marmet",
        "rev": "v001",
        "title": "West Virginia used unusually sharp language against Supreme Court FAA doctrine, then #Shorts",
        "description": "West Virginia used unusually sharp language against Supreme Court FAA doctrine, then.\n\nWho controls when a state court and the Supreme Court disagree about federal arbitration law and state contract law?\n\nPrime Documentary covers the cases that quietly decide what the state may do to you. The full episode is linked at the top.\n\n#Shorts #Marmet #Law #Documentary",
        "tags": ["Shorts", "Marmet", "Law", "Documentary"],
        # v001: generated from the design by gen_short_publish_config.py
        "video_sha256": "5e65304106633b858cfe3eede1f143fa01eb13f06b2cbd840c4e4b87ac2db7f3",
        "thumb_sha256": "97e44f70526bc38b58afb6f29b4cac829646acaa4fe28cf2cdd168a4326c1c34",
    },
    "271": {
        # destination for the funnel link; ensure_funnel_description() verifies it is public
        "longform": "hIuvo897Mr4",
        "ep": "PD-2026-066-openfields",
        "rev": "v001",
        "title": "A state wildlife officer walked onto ninety-three private acres, cut a branch off a tree #Shorts",
        "description": "A state wildlife officer walked onto ninety-three private acres, cut a branch off a tree.\n\nIf the land is yours and the Fourth Amendment does not reach it, what does?\n\nPrime Documentary covers the cases that quietly decide what the state may do to you. The full episode is linked at the top.\n\n#Shorts #Openfields #Law #Documentary",
        "tags": ["Shorts", "Openfields", "Law", "Documentary"],
        # v001: generated from the design by gen_short_publish_config.py
        "video_sha256": "1b3ce269ea14204ea016778ca2c3a03331b8dcbb0a426447d78dcb91f52a13c4",
        "thumb_sha256": "4f89d16231639424b69cee48e1e436171e3eef12baf8e886270f64ac9cadd294",
    },
    "272": {
        # destination for the funnel link; ensure_funnel_description() verifies it is public
        "longform": "hIuvo897Mr4",
        "ep": "PD-2026-066-openfields",
        "rev": "v001",
        "title": "Tennessee wrote three constitutions and three times refused the federal word. Where #Shorts",
        "description": "Tennessee wrote three constitutions and three times refused the federal word. Where.\n\nOne noun stood between a farm and a warrantless camera. Was it enough?\n\nPrime Documentary covers the cases that quietly decide what the state may do to you. The full episode is linked at the top.\n\n#Shorts #Openfields #Law #Documentary",
        "tags": ["Shorts", "Openfields", "Law", "Documentary"],
        # v001: generated from the design by gen_short_publish_config.py
        "video_sha256": "f87a4b0b176e3c754578dfa42e6888b5f6436fcfd0c4ce6db45dbb9ed6f415b1",
        "thumb_sha256": "ab2fc57f26f719be6ebbededebc7279d8d7841dc3d01be64a0cb7b884966d7a8",
    },
    "273": {
        # destination for the funnel link; ensure_funnel_description() verifies it is public
        "longform": "hIuvo897Mr4",
        "ep": "PD-2026-066-openfields",
        "rev": "v001",
        "title": "Three judges, no dissent, and an answer two sentences long: the statute is constitutional #Shorts",
        "description": "Three judges, no dissent, and an answer two sentences long: the statute is constitutional.\n\nHow can one law be lawful on its face and unlawful in the hands that used it?\n\nPrime Documentary covers the cases that quietly decide what the state may do to you. The full episode is linked at the top.\n\n#Shorts #Openfields #Law #Documentary",
        "tags": ["Shorts", "Openfields", "Law", "Documentary"],
        # v001: generated from the design by gen_short_publish_config.py
        "video_sha256": "2882381d832b6e815eaf7ac2b4213abe82c61266542302a671d5b7b706942ce3",
        "thumb_sha256": "897df5a14b4d42d08fb42112d4b933ae44c0e664a217e59da8d9fc44beebc342",
    },
    "274": {
        # destination for the funnel link; ensure_funnel_description() verifies it is public
        "longform": "DgpF4UxcsH4",
        "ep": "PD-2026-067-ramirez",
        "rev": "v001",
        "title": "A man went to buy a car with his wife and his father-in-law. The credit check said his name #Shorts",
        "description": "A man went to buy a car with his wife and his father-in-law. The credit check said his name.\n\nThe letter that followed did not say how to argue with it. Who does a person appeal to?\n\nPrime Documentary covers the cases that quietly decide what the state may do to you. The full episode is linked at the top.\n\n#Shorts #Ramirez #Law #Documentary",
        "tags": ["Shorts", "Ramirez", "Law", "Documentary"],
        # v001: generated from the design by gen_short_publish_config.py
        "video_sha256": "a50f6ac2c49141169e6c201263f7fdf50404a795004693badb1e9a39d544a4e1",
        "thumb_sha256": "423368fc2d2f3424bbe162b659064d316fa6153a7bf7b73b3d31db3bab44b00b",
    },
    "275": {
        # destination for the funnel link; ensure_funnel_description() verifies it is public
        "longform": "DgpF4UxcsH4",
        "ep": "PD-2026-067-ramirez",
        "rev": "v001",
        "title": "The system that flagged him compared first and last name only. Not birth dates, not middle #Shorts",
        "description": "The system that flagged him compared first and last name only. Not birth dates, not middle.\n\nA jury had already punished the same failure once, six years earlier. Why did it keep happening?\n\nPrime Documentary covers the cases that quietly decide what the state may do to you. The full episode is linked at the top.\n\n#Shorts #Ramirez #Law #Documentary",
        "tags": ["Shorts", "Ramirez", "Law", "Documentary"],
        # v001: generated from the design by gen_short_publish_config.py
        "video_sha256": "e9d48527e26ee4b902648ad12be514b1d2a74c05fa04d91299948a5600670f6d",
        "thumb_sha256": "cac4415d3035e4a6741404cd1dae24e0725db8c711eeb6424f8c8c5fb97b8ecd",
    },
    "276": {
        # destination for the funnel link; ensure_funnel_description() verifies it is public
        "longform": "DgpF4UxcsH4",
        "ep": "PD-2026-067-ramirez",
        "rev": "v001",
        "title": "Five to four: a company can break a law Congress wrote for you, and that alone does not get #Shorts",
        "description": "Five to four: a company can break a law Congress wrote for you, and that alone does not get.\n\nThe company could not confirm that a single alert it sold was accurate. Why was that not the question?\n\nPrime Documentary covers the cases that quietly decide what the state may do to you. The full episode is linked at the top.\n\n#Shorts #Ramirez #Law #Documentary",
        "tags": ["Shorts", "Ramirez", "Law", "Documentary"],
        # v001: generated from the design by gen_short_publish_config.py
        "video_sha256": "0c88a5c55a40a0f030a2101dc865d416b110d7b543d938f2e45068c95a598d25",
        "thumb_sha256": "9b7ab41de244bc1696224c95d3b96aeebc01c218289902d253089243144100fc",
    },
    "277": {
        # destination for the funnel link; ensure_funnel_description() verifies it is public
        "longform": "yW_-diNLfO8",
        "ep": "PD-2026-068-pinto",
        "rev": "v001",
        "title": "Two engineers wrote an eight-page report with a table that counted deaths and priced them #Shorts",
        "description": "Two engineers wrote an eight-page report with a table that counted deaths and priced them.\n\nThe document has a title nobody reads out. What does it say it is?\n\nPrime Documentary covers the cases that quietly decide what the state may do to you. The full episode is linked at the top.\n\n#Shorts #Pinto #Law #Documentary",
        "tags": ["Shorts", "Pinto", "Law", "Documentary"],
        # v001: generated from the design by gen_short_publish_config.py
        "video_sha256": "f76c8e1ef4a8eeca10c070362cecf7d7afed4f0567cf77cdbd9c3454849ce2a6",
        "thumb_sha256": "9e0034f6ce09d55a69fcd7415adc6aec1e839f8955197316e0be931a28156bea",
    },
    "278": {
        # destination for the funnel link; ensure_funnel_description() verifies it is public
        "longform": "yW_-diNLfO8",
        "ep": "PD-2026-068-pinto",
        "rev": "v001",
        "title": "The car stalled on a freeway and the reason was not the fuel tank. A carburettor float had #Shorts",
        "description": "The car stalled on a freeway and the reason was not the fuel tank. A carburettor float had.\n\nHow fast the car behind was going is the single most contested fact in the case. Why could nobody settle it?\n\nPrime Documentary covers the cases that quietly decide what the state may do to you. The full episode is linked at the top.\n\n#Shorts #Pinto #Law #Documentary",
        "tags": ["Shorts", "Pinto", "Law", "Documentary"],
        # v001: generated from the design by gen_short_publish_config.py
        "video_sha256": "b7b997fb419b3c923235abbea6ad634da5379086d9e27bedbcbb5b34a5d29307",
        "thumb_sha256": "c478d0e5ad36d1ff3ed0d07b5728f2a1d54831111902caf03d592acf9b2c3871",
    },
    "279": {
        # destination for the funnel link; ensure_funnel_description() verifies it is public
        "longform": "yW_-diNLfO8",
        "ep": "PD-2026-068-pinto",
        "rev": "v001",
        "title": "A grand jury indicted the company itself for reckless homicide. The maximum penalty #Shorts",
        "description": "A grand jury indicted the company itself for reckless homicide. The maximum penalty.\n\nWhat does a fine of that size mean against a company of that size?\n\nPrime Documentary covers the cases that quietly decide what the state may do to you. The full episode is linked at the top.\n\n#Shorts #Pinto #Law #Documentary",
        "tags": ["Shorts", "Pinto", "Law", "Documentary"],
        # v001: generated from the design by gen_short_publish_config.py
        "video_sha256": "c77f49221f8cfc0a0aa611c7dc2beafeb35a5dd7b2b583a5fdd3003cdf2880b0",
        "thumb_sha256": "724e7a4b0f0f5db08b1a50eb911e0eb178fef01375ea19e83a57244d25dff31c",
    },
    "280": {
        # destination for the funnel link; ensure_funnel_description() verifies it is public
        "longform": "R6IRqClVnLo",
        "ep": "PD-2026-069-hyatt",
        "rev": "v001",
        "title": "One long steel rod became two shorter ones, four inches apart. On the drawing it looks like #Shorts",
        "description": "One long steel rod became two shorter ones, four inches apart. On the drawing it looks like.\n\nOn the drawing it looks like the same thing. What did the change actually do?\n\nPrime Documentary covers the cases that quietly decide what the state may do to you. The full episode is linked at the top.\n\n#Shorts #Hyatt #Law #Documentary",
        "tags": ["Shorts", "Hyatt", "Law", "Documentary"],
        # v001: generated from the design by gen_short_publish_config.py
        "video_sha256": "9d8d12831e75fa83a994a17fe513c45e77497f7e2edf6e93bc6d804c93615f42",
        "thumb_sha256": "c049ff051346cad80852ef7249e29c648f01a9e57548ed8f2b350b90122088ec",
    },
    "281": {
        # destination for the funnel link; ensure_funnel_description() verifies it is public
        "longform": "R6IRqClVnLo",
        "ep": "PD-2026-069-hyatt",
        "rev": "v001",
        "title": "A senator's office asked the National Bureau of Standards for help. A court order limited #Shorts",
        "description": "A senator's office asked the National Bureau of Standards for help. A court order limited.\n\nInvestigators could not weigh the spans or cut into them until the parties in the litigation agreed. What were they allowed to conclude?\n\nPrime Documentary covers the cases that quietly decide what the state may do to you. The full episode is linked at the top.\n\n#Shorts #Hyatt #Law #Documentary",
        "tags": ["Shorts", "Hyatt", "Law", "Documentary"],
        # v001: generated from the design by gen_short_publish_config.py
        "video_sha256": "a3fc6b5d66d5d2c16c83755db04fe675a1f8c0560f2e7a0aba15e0d40129678f",
        "thumb_sha256": "4a2f1cdf95617582958ce29bec47e023cf3e9d081f1ef084e286ad59e25881d3",
    },
    "282": {
        # destination for the funnel link; ensure_funnel_description() verifies it is public
        "longform": "R6IRqClVnLo",
        "ep": "PD-2026-069-hyatt",
        "rev": "v001",
        "title": "No one was ever charged with a crime. What happened instead came from a licensing board #Shorts",
        "description": "No one was ever charged with a crime. What happened instead came from a licensing board.\n\nInsurers had paid out and nobody had taken responsibility. What can a licensing board do that a prosecutor could not?\n\nPrime Documentary covers the cases that quietly decide what the state may do to you. The full episode is linked at the top.\n\n#Shorts #Hyatt #Law #Documentary",
        "tags": ["Shorts", "Hyatt", "Law", "Documentary"],
        # v001: generated from the design by gen_short_publish_config.py
        "video_sha256": "6e96eb480d1340da867c098293fa9aa99fd2423768ee97f66ad39fc306eebd3e",
        "thumb_sha256": "74edb0b7d278ca611c18e300b92300ab176c2334ecfaf9db0aed1f1313ccd273",
    },
    "289": {
        # destination for the funnel link; ensure_funnel_description() verifies it is public
        "longform": "1nxecNneBVk",
        "ep": "PD-2026-070-wronghouse",
        "rev": "v001",
        "title": "Nobody on that team broke a rule, because the FBI has no rule that says check the address #Shorts",
        "description": "Nobody on that team broke a rule, because the FBI has no rule that says check the address.\n\nIf no rule was broken, what is left for the family to sue over?\n\nPrime Documentary covers the cases that quietly decide what the state may do to you. The full episode is linked at the top.\n\n#Shorts #Wronghouse #Law #Documentary",
        "tags": ["Shorts", "Wronghouse", "Law", "Documentary"],
        # v001: generated from the design by gen_short_publish_config.py
        "video_sha256": "bcd23c03658e504186e9d0cbe6d4e71ead9c57eb2dce3a6b3f26f4f62de4ec92",
        "thumb_sha256": "99bcd746efd8c839825f7f1c088739f586d7e2af1f8ac58cede3868195a86724",
    },
    "290": {
        # destination for the funnel link; ensure_funnel_description() verifies it is public
        "longform": "1nxecNneBVk",
        "ep": "PD-2026-070-wronghouse",
        "rev": "v001",
        "title": "He navigated to the wrong house with his own GPS, steered by a car that belonged #Shorts",
        "description": "He navigated to the wrong house with his own GPS, steered by a car that belonged.\n\nEverything he saw confirmed he was at the right house. What was he looking at?\n\nPrime Documentary covers the cases that quietly decide what the state may do to you. The full episode is linked at the top.\n\n#Shorts #Wronghouse #Law #Documentary",
        "tags": ["Shorts", "Wronghouse", "Law", "Documentary"],
        # v001: generated from the design by gen_short_publish_config.py
        "video_sha256": "5bae657f5b1ad9cd63e8c4bec1ebcdfb04f27b2a65ff25bf3775def886d13561",
        "thumb_sha256": "7c27f7306963098f666050b259813f11f15455b05b03b354c5b8152d34032cd5",
    },
    "291": {
        # destination for the funnel link; ensure_funnel_description() verifies it is public
        "longform": "1nxecNneBVk",
        "ep": "PD-2026-070-wronghouse",
        "rev": "v001",
        "title": "Two hundred and twenty-three docket entries, a unanimous Supreme Court win, and not one #Shorts",
        "description": "Two hundred and twenty-three docket entries, a unanimous Supreme Court win, and not one.\n\nThey won at the Supreme Court unanimously and still have no trial. What is in the way?\n\nPrime Documentary covers the cases that quietly decide what the state may do to you. The full episode is linked at the top.\n\n#Shorts #Wronghouse #Law #Documentary",
        "tags": ["Shorts", "Wronghouse", "Law", "Documentary"],
        # v001: generated from the design by gen_short_publish_config.py
        "video_sha256": "9c23f0030c9cb588a44f8c655f656da536a3a9cd380398f86dd4958061fff4df",
        "thumb_sha256": "c4b4f9ce9c96677a903cb358b75686fd9332f00926a1a056f4e409f6bec190b8",
    },
    "292": {
        # destination for the funnel link; ensure_funnel_description() verifies it is public
        "longform": "YuVBUlqrkdI",
        "ep": "PD-2026-071-oroville",
        "rev": "v001",
        "title": "The court did not find the evacuation zone was drawn too widely. It found no zone had ever #Shorts",
        "description": "The court did not find the evacuation zone was drawn too widely. It found no zone had ever.\n\nIf there was never a zone, what did the word mandatory mean that afternoon?\n\nPrime Documentary covers the cases that quietly decide what the state may do to you. The full episode is linked at the top.\n\n#Shorts #Oroville #Law #Documentary",
        "tags": ["Shorts", "Oroville", "Law", "Documentary"],
        # v001: generated from the design by gen_short_publish_config.py
        "video_sha256": "109aa859a4c0663636f525ddc31a8df75c8c99ee41a232e6ea7b09c39b2ed6da",
        "thumb_sha256": "e7b01bc19e808205def4ef10a92b191c8486f5ba18336e1465f5c4b348d236e1",
    },
    "293": {
        # destination for the funnel link; ensure_funnel_description() verifies it is public
        "longform": "YuVBUlqrkdI",
        "ep": "PD-2026-071-oroville",
        "rev": "v001",
        "title": "A broadcast has no delivery receipt, so nobody -- including the people themselves -- could #Shorts",
        "description": "A broadcast has no delivery receipt, so nobody -- including the people themselves -- could.\n\nShe had the receipts from her own two days and still could not say if she was in it. Why?\n\nPrime Documentary covers the cases that quietly decide what the state may do to you. The full episode is linked at the top.\n\n#Shorts #Oroville #Law #Documentary",
        "tags": ["Shorts", "Oroville", "Law", "Documentary"],
        # v001: generated from the design by gen_short_publish_config.py
        "video_sha256": "b3cf348dc43a713375a8680e73650191762273361290067b0d6bf3d293ad3843",
        "thumb_sha256": "07f1144ccc5acd1ecff109df876f92d1044953d67c91cb1f6739174059170047",
    },
    "294": {
        # destination for the funnel link; ensure_funnel_description() verifies it is public
        "longform": "YuVBUlqrkdI",
        "ep": "PD-2026-071-oroville",
        "rev": "v001",
        "title": "Four people asked the State to reimburse two days of expenses, and were ordered to pay #Shorts",
        "description": "Four people asked the State to reimburse two days of expenses, and were ordered to pay.\n\nTwo days of expenses went in. A costs order came out. What happened in between?\n\nPrime Documentary covers the cases that quietly decide what the state may do to you. The full episode is linked at the top.\n\n#Shorts #Oroville #Law #Documentary",
        "tags": ["Shorts", "Oroville", "Law", "Documentary"],
        # v001: generated from the design by gen_short_publish_config.py
        "video_sha256": "617fa155dfdf954b27726f48989fe42df6c2b95982bd1e003679ff09d116dc88",
        "thumb_sha256": "0770b9f7134543c059f8531c0e7848a438a1f41eb9b47b03ac66452e152d5f90",
    },
    "295": {
        # destination for the funnel link; ensure_funnel_description() verifies it is public
        "longform": "RFDPSfllbk0",
        "ep": "PD-2026-074-itaewon",
        "rev": "v001",
        "title": "Four hours before anything happened, a caller standing in the alley used the words crushed #Shorts",
        "description": "Four hours before anything happened, a caller standing in the alley used the words crushed.\n\nWhere were the officers instead that night - and why did the official answer take three years?\n\nPrime Documentary covers the cases that quietly decide what the state may do to you. The full episode is linked at the top.\n\n#Shorts #Itaewon #Law #Documentary",
        "tags": ["Shorts", "Itaewon", "Law", "Documentary"],
        # v001: generated from the design by gen_short_publish_config.py
        "video_sha256": "54ea63d96995575be40e0309ad44195ccfb48ca1a0ee5582edcfa414e4124be2",
        "thumb_sha256": "952932e30659852839c523b1833902e7cf8db977c1f018fcae46e00868d23841",
    },
    "296": {
        # destination for the funnel link; ensure_funnel_description() verifies it is public
        "longform": "RFDPSfllbk0",
        "ep": "PD-2026-074-itaewon",
        "rev": "v001",
        "title": "Nine people on a doormat: the measured geometry of a fifty-metre sloping alley, and why #Shorts",
        "description": "Nine people on a doormat: the measured geometry of a fifty-metre sloping alley, and why.\n\nWho was supposed to decide, before the evening started, what that street was for on a Saturday night?\n\nPrime Documentary covers the cases that quietly decide what the state may do to you. The full episode is linked at the top.\n\n#Shorts #Itaewon #Law #Documentary",
        "tags": ["Shorts", "Itaewon", "Law", "Documentary"],
        # v001: generated from the design by gen_short_publish_config.py
        "video_sha256": "e0f5c74cb3ca8b79aa49c3479fe49cf80e2bf5e4add73337b7664f196b52a3eb",
        "thumb_sha256": "2bef6ba1f407d8305e050cd9a0ea19e3de32d871444df1fff450eb8bd881cffc",
    },
    "297": {
        # destination for the funnel link; ensure_funnel_description() verifies it is public
        "longform": "RFDPSfllbk0",
        "ep": "PD-2026-074-itaewon",
        "rev": "v001",
        "title": "The acquittal was built on a definition: the law attached no duty to a crowd with no #Shorts",
        "description": "The acquittal was built on a definition: the law attached no duty to a crowd with no.\n\nWhat is the sentence that replaced the definition - and why did it take fourteen months to write?\n\nPrime Documentary covers the cases that quietly decide what the state may do to you. The full episode is linked at the top.\n\n#Shorts #Itaewon #Law #Documentary",
        "tags": ["Shorts", "Itaewon", "Law", "Documentary"],
        # v001: generated from the design by gen_short_publish_config.py
        "video_sha256": "2254b6a06047ff3f33374d205f30b6673a3c2ee5273f6cfa03b8d17fdc0381a5",
        "thumb_sha256": "a1c98759d30e96b47d86b90692af789079c501db9d6ed97463650c921e94e94c",
    },
    "298": {
        # destination for the funnel link; ensure_funnel_description() verifies it is public
        "longform": "3AgCeXG3qGI",
        "ep": "PD-2026-075-lahaina",
        "rev": "v001",
        "title": "The largest outdoor siren warning system in the world, tested in public every month #Shorts",
        "description": "The largest outdoor siren warning system in the world, tested in public every month.\n\nThe man who decided not to sound them was asked if he regretted it - his answer was three words. What were they?\n\nPrime Documentary covers the cases that quietly decide what the state may do to you. The full episode is linked at the top.\n\n#Shorts #Lahaina #Law #Documentary",
        "tags": ["Shorts", "Lahaina", "Law", "Documentary"],
        # v001: generated from the design by gen_short_publish_config.py
        "video_sha256": "26ae5625546fc2ffed00066bce615ccc35a1c4a7aba44d6a76dc03ed87aedd39",
        "thumb_sha256": "85dea64afa477ec8e819f5173ac21c8af2c8dea1a400c3ee341936903f247dc4",
    },
    "299": {
        # destination for the funnel link; ensure_funnel_description() verifies it is public
        "longform": "3AgCeXG3qGI",
        "ep": "PD-2026-075-lahaina",
        "rev": "v001",
        "title": "The first evacuation order naming a Lahaina neighbourhood went out at sixteen minutes past #Shorts",
        "description": "The first evacuation order naming a Lahaina neighbourhood went out at sixteen minutes past.\n\nWhat was the warning system the state had actually built for this - and why had it never been used?\n\nPrime Documentary covers the cases that quietly decide what the state may do to you. The full episode is linked at the top.\n\n#Shorts #Lahaina #Law #Documentary",
        "tags": ["Shorts", "Lahaina", "Law", "Documentary"],
        # v001: generated from the design by gen_short_publish_config.py
        "video_sha256": "d8959eb56cca35d77fb6ba6c483b5fbf275cad9f28f910e5435e5db2317b7295",
        "thumb_sha256": "8dc0cf6a79e81bcf324ca7351e74cbfaa695b258edd955d033e8210e80b9069d",
    },
    "300": {
        # destination for the funnel link; ensure_funnel_description() verifies it is public
        "longform": "3AgCeXG3qGI",
        "ep": "PD-2026-075-lahaina",
        "rev": "v001",
        "title": "The hydrants-went-dry story everyone carries is wrong: the pumps never stopped and the power #Shorts",
        "description": "The hydrants-went-dry story everyone carries is wrong: the pumps never stopped and the power.\n\nIf a town's water system cannot be built to fight the town, what was supposed to stand between the town and the fire?\n\nPrime Documentary covers the cases that quietly decide what the state may do to you. The full episode is linked at the top.\n\n#Shorts #Lahaina #Law #Documentary",
        "tags": ["Shorts", "Lahaina", "Law", "Documentary"],
        # v001: generated from the design by gen_short_publish_config.py
        "video_sha256": "d774ec60e3d622ab421fc3d01d7fd27025c4ce8573a60400155d95117de173ca",
        "thumb_sha256": "a28b2e2ab5effdef16a91ac00e96fa0c3b2f5e53d1a52a94ea2b33b85392a337",
    },
    "301": {
        # destination for the funnel link; ensure_funnel_description() verifies it is public
        "longform": "ippMyC49OyI",
        "ep": "PD-2026-076-morandi",
        "rev": "v001",
        "title": "The inspection found broken wires; the company's own manual says broken wires are a seventy #Shorts",
        "description": "The inspection found broken wires; the company's own manual says broken wires are a seventy.\n\nWhat was inside the concrete the inspectors were scoring - and what happened the one time anybody cut into it?\n\nPrime Documentary covers the cases that quietly decide what the state may do to you. The full episode is linked at the top.\n\n#Shorts #Morandi #Law #Documentary",
        "tags": ["Shorts", "Morandi", "Law", "Documentary"],
        # v001: generated from the design by gen_short_publish_config.py
        "video_sha256": "b6462382e201d10c1df4f043aef7a6f9444afdde943b11e50470406f40ac5f16",
        "thumb_sha256": "9621a8597746d718dd7725507f50c078003fdd2febe50b3659b0f079f82a1fb1",
    },
    "302": {
        # destination for the funnel link; ensure_funnel_description() verifies it is public
        "longform": "ippMyC49OyI",
        "ep": "PD-2026-076-morandi",
        "rev": "v001",
        "title": "Italy ordered a formal safety assessment of its strategic structures; the deadline #Shorts",
        "description": "Italy ordered a formal safety assessment of its strategic structures; the deadline.\n\nWhat did the same paper trail record about the project that was supposed to fix the stays - and who was allowed not to check it?\n\nPrime Documentary covers the cases that quietly decide what the state may do to you. The full episode is linked at the top.\n\n#Shorts #Morandi #Law #Documentary",
        "tags": ["Shorts", "Morandi", "Law", "Documentary"],
        # v001: generated from the design by gen_short_publish_config.py
        "video_sha256": "9b97ebdb539afc0edbb5a45c92635dcfd1d686f286be6ea7769d72e5939ecddb",
        "thumb_sha256": "0db890da1698c60788af49a739f6ecc581f2c021623709e89e86fb2dd0947fe4",
    },
    "303": {
        # destination for the funnel link; ensure_funnel_description() verifies it is public
        "longform": "ippMyC49OyI",
        "ep": "PD-2026-076-morandi",
        "rev": "v001",
        "title": "The commission totalled thirty-six years of structural spending on the viaduct: ninety-eight #Shorts",
        "description": "The commission totalled thirty-six years of structural spending on the viaduct: ninety-eight.\n\nWhat was the twenty-million-euro project those numbers ended in - and who was allowed to approve it?\n\nPrime Documentary covers the cases that quietly decide what the state may do to you. The full episode is linked at the top.\n\n#Shorts #Morandi #Law #Documentary",
        "tags": ["Shorts", "Morandi", "Law", "Documentary"],
        # v001: generated from the design by gen_short_publish_config.py
        "video_sha256": "989a81f18f05091a79e60a403edbfb15976908ea1fc886b363dd3cc7174a1ca7",
        "thumb_sha256": "fb4855a3857b4ab16198b66f58e0c13a26b405a39fdf4d2cd86917cb897f8a95",
    },
    "304": {
        # destination for the funnel link; ensure_funnel_description() verifies it is public
        "longform": "sylgSOcCe1k",
        "ep": "PD-2026-072-lacmegantic",
        "rev": "v001",
        "title": "The securement check was done, and done as understood - but it was performed #Shorts",
        "description": "The securement check was done, and done as understood - but it was performed.\n\nWho was standing in that yard at the end of the shift, and what happened to the engine two hours later?\n\nPrime Documentary covers the cases that quietly decide what the state may do to you. The full episode is linked at the top.\n\n#Shorts #Lacmegantic #Law #Documentary",
        "tags": ["Shorts", "Lacmegantic", "Law", "Documentary"],
        # v001: generated from the design by gen_short_publish_config.py
        "video_sha256": "28422b5cd0b93c7afaacdb376661e5ff12d932a09010aa33646ff3852c259292",
        "thumb_sha256": "b08c96198c99a09230d8eabbb6437d7b79cad583c5007fb512cb8cf76d31f850",
    },
    "305": {
        # destination for the funnel link; ensure_funnel_description() verifies it is public
        "longform": "sylgSOcCe1k",
        "ep": "PD-2026-072-lacmegantic",
        "rev": "v001",
        "title": "All sixty-three derailed tank cars were in compliance with their specification #Shorts",
        "description": "All sixty-three derailed tank cars were in compliance with their specification.\n\nWhat was in those cars, and did the shipping papers say what it really was?\n\nPrime Documentary covers the cases that quietly decide what the state may do to you. The full episode is linked at the top.\n\n#Shorts #Lacmegantic #Law #Documentary",
        "tags": ["Shorts", "Lacmegantic", "Law", "Documentary"],
        # v001: generated from the design by gen_short_publish_config.py
        "video_sha256": "4a70e1f681e4f37b57e5b1719a32992a079bcdfb0957a3b97b54380d06c4096b",
        "thumb_sha256": "3e0e609bd9488e9f5feb0a93544b4443f0df5d56c2d9e0b1268b232a7be6c7f8",
    },
    "306": {
        # destination for the funnel link; ensure_funnel_description() verifies it is public
        "longform": "sylgSOcCe1k",
        "ep": "PD-2026-072-lacmegantic",
        "rev": "v001",
        "title": "The firefighters did the correct thing and the fire went out - and with every engine shut #Shorts",
        "description": "The firefighters did the correct thing and the fire went out - and with every engine shut.\n\nWhat happened when a train doing sixty-five entered a curve built for twenty - and who, if anyone, was ever found responsible?\n\nPrime Documentary covers the cases that quietly decide what the state may do to you. The full episode is linked at the top.\n\n#Shorts #Lacmegantic #Law #Documentary",
        "tags": ["Shorts", "Lacmegantic", "Law", "Documentary"],
        # v001: generated from the design by gen_short_publish_config.py
        "video_sha256": "4606e090cd9a9c18f0cb63003f90af21570b13e17a85156234cb36b503b49188",
        "thumb_sha256": "45ee95e47bf0b1f54e1d0fbe99e796968b066d44f16d9dd95bda782303cdea48",
    },
    "307": {
        # destination for the funnel link; ensure_funnel_description() verifies it is public
        "longform": "l0o898ZG6j4",
        "ep": "PD-2026-073-uri",
        "rev": "v001",
        "title": "A recommendation is a document; a standard is a rule with a mechanism behind it. The 2011 #Shorts",
        "description": "A recommendation is a document; a standard is a rule with a mechanism behind it. The 2011.\n\nWhy does Texas answer to nobody outside its borders on this - and what did that cost on the night the order was given?\n\nPrime Documentary covers the cases that quietly decide what the state may do to you. The full episode is linked at the top.\n\n#Shorts #Uri #Law #Documentary",
        "tags": ["Shorts", "Uri", "Law", "Documentary"],
        # v001: generated from the design by gen_short_publish_config.py
        "video_sha256": "4396c0c617c3ffecedba683fff8c42edec2a8c3b20850d4aa81c18f1bb989f63",
        "thumb_sha256": "0c375fb98679eef0987531939171894d622610f74060a08cc15eb896ce917406",
    },
    "308": {
        # destination for the funnel link; ensure_funnel_description() verifies it is public
        "longform": "l0o898ZG6j4",
        "ep": "PD-2026-073-uri",
        "rev": "v001",
        "title": "The largest manually controlled load shedding in American history was ordered at twenty past #Shorts",
        "description": "The largest manually controlled load shedding in American history was ordered at twenty past.\n\nThe customers cut that night included the gas fields that fuelled the plants being saved. What happens when a grid's rescue feeds its emergency?\n\nPrime Documentary covers the cases that quietly decide what the state may do to you. The full episode is linked at the top.\n\n#Shorts #Uri #Law #Documentary",
        "tags": ["Shorts", "Uri", "Law", "Documentary"],
        # v001: generated from the design by gen_short_publish_config.py
        "video_sha256": "9365d481361d410d0d9a7cf7b50f8c869dfabff0eb282a452cfd91968cd13be1",
        "thumb_sha256": "ccdb94ff6ce1e1439ad015afe9e110572a24f9c7e3c156ceaeb629b51fedff94",
    },
    "309": {
        # destination for the funnel link; ensure_funnel_description() verifies it is public
        "longform": "l0o898ZG6j4",
        "ep": "PD-2026-073-uri",
        "rev": "v001",
        "title": "Every grid keeps a critical-load list of the customers who never get shed. The gas fields #Shorts",
        "description": "Every grid keeps a critical-load list of the customers who never get shed. The gas fields.\n\nHow close did the grid come to going down entirely - and what was the number that measured it?\n\nPrime Documentary covers the cases that quietly decide what the state may do to you. The full episode is linked at the top.\n\n#Shorts #Uri #Law #Documentary",
        "tags": ["Shorts", "Uri", "Law", "Documentary"],
        # v001: generated from the design by gen_short_publish_config.py
        "video_sha256": "280dac899731187e14818ff8eaf9a698d97641371cbb9f3ef140b7042c40fe9f",
        "thumb_sha256": "67d1a7adbb2e04f6368e4d939844ce555e5482db4a2f7acdc0928f560a2fe644",
    },
    "310": {
        # destination for the funnel link; ensure_funnel_description() verifies it is public
        "longform": "Z91ZsyPsRi0",
        "ep": "PD-2026-077-keybridge",
        "rev": "v001",
        "title": "Everyone on the water did the right thing in the right order - closed the breakers by hand #Shorts",
        "description": "Everyone on the water did the right thing in the right order - closed the breakers by hand.\n\nIf nobody on that ship made a mistake, what was it that kept switching the power off?\n\nPrime Documentary covers the cases that quietly decide what the state may do to you. The full episode is linked at the top.\n\n#Shorts #Keybridge #Law #Documentary",
        "tags": ["Shorts", "Keybridge", "Law", "Documentary"],
        # v001: generated from the design by gen_short_publish_config.py
        "video_sha256": "5323aae9fb777bfdbf25dccf0edbc001369e51afa51a3dcab7db9c6a6c3c1732",
        "thumb_sha256": "934e76d3b62b9fee8d7754d3fed825a5a0406eec7202cd0bb575e3568ee809d2",
    },
    "311": {
        # destination for the funnel link; ensure_funnel_description() verifies it is public
        "longform": "Z91ZsyPsRi0",
        "ep": "PD-2026-077-keybridge",
        "rev": "v001",
        "title": "The National Transportation Safety Board took twenty months to name the probable cause #Shorts",
        "description": "The National Transportation Safety Board took twenty months to name the probable cause.\n\nThe wire explains the first blackout. Why did a ship built to restart itself not come back?\n\nPrime Documentary covers the cases that quietly decide what the state may do to you. The full episode is linked at the top.\n\n#Shorts #Keybridge #Law #Documentary",
        "tags": ["Shorts", "Keybridge", "Law", "Documentary"],
        # v001: generated from the design by gen_short_publish_config.py
        "video_sha256": "7fe567e45d7095ef1a74a853c2d899bebe102b6f2c61f24eb2589aec6fd23ca7",
        "thumb_sha256": "1651ea57d01259ff08ec9f8ecd6f02dcbf4f3f9609db0b173bf93014e041149f",
    },
    "312": {
        # destination for the funnel link; ensure_funnel_description() verifies it is public
        "longform": "Z91ZsyPsRi0",
        "ep": "PD-2026-077-keybridge",
        "rev": "v001",
        "title": "The Board's quieter finding: the bridge had no countermeasures against a modern ship #Shorts",
        "description": "The Board's quieter finding: the bridge had no countermeasures against a modern ship.\n\nWho is supposed to do that arithmetic for the bridge you drove over this morning?\n\nPrime Documentary covers the cases that quietly decide what the state may do to you. The full episode is linked at the top.\n\n#Shorts #Keybridge #Law #Documentary",
        "tags": ["Shorts", "Keybridge", "Law", "Documentary"],
        # v001: generated from the design by gen_short_publish_config.py
        "video_sha256": "532ab9b48c266a6bd00079d2ef25e9cb9a05adcb28073c4f1632896d26fcc5eb",
        "thumb_sha256": "dc29541553d12e63410ad855f38e49ebf3682f8e97de3dcefc8cd5978806adf9",
    },
    "316": {
        # destination for the funnel link; ensure_funnel_description() verifies it is public
        "longform": "0a_MnQuJF3s",
        "ep": "PD-2026-079-alaska261",
        "rev": "v001",
        "title": "The entire safety net was a number in thousandths of an inch read off a needle - #Shorts",
        "description": "The entire safety net was a number in thousandths of an inch read off a needle -.\n\nIf nobody could see a number creeping up, what was happening to the threads between the checks?\n\nPrime Documentary covers the cases that quietly decide what the state may do to you. The full episode is linked at the top.\n\n#Shorts #Alaska261 #Law #Documentary",
        "tags": ["Shorts", "Alaska261", "Law", "Documentary"],
        # v001: generated from the design by gen_short_publish_config.py
        "video_sha256": "38902ae403fbe7284e9484f3f3da4cb3f065bc71adbf08963d9c7631238a146d",
        "thumb_sha256": "2529d4154ddb7134323b5f0ae1aabe8bdf0b8c787ea7bdb54c11247a0e9a6de6",
    },
    "317": {
        # destination for the funnel link; ensure_funnel_description() verifies it is public
        "longform": "0a_MnQuJF3s",
        "ep": "PD-2026-079-alaska261",
        "rev": "v001",
        "title": "Sixteen years before the accident the manufacturer wrote to operators describing this exact #Shorts",
        "description": "Sixteen years before the accident the manufacturer wrote to operators describing this exact.\n\nIf the warning was circulated in 1984, what happened to the interval that was supposed to act on it?\n\nPrime Documentary covers the cases that quietly decide what the state may do to you. The full episode is linked at the top.\n\n#Shorts #Alaska261 #Law #Documentary",
        "tags": ["Shorts", "Alaska261", "Law", "Documentary"],
        # v001: generated from the design by gen_short_publish_config.py
        "video_sha256": "7d6e64d5db8b0e2b28705d4b1f4c498021c0595cfaadaea0ba55e81d52782987",
        "thumb_sha256": "9f9ee2e95b8f00d49355392fb5e96a296321711115ff2f098d43ec6c90b5e7fd",
    },
    "318": {
        # destination for the funnel link; ensure_funnel_description() verifies it is public
        "longform": "0a_MnQuJF3s",
        "ep": "PD-2026-079-alaska261",
        "rev": "v001",
        "title": "The greasing interval grew by four hundred per cent over fifteen years, and the check #Shorts",
        "description": "The greasing interval grew by four hundred per cent over fifteen years, and the check.\n\nThere was a second line of defence, a gauge with one needle. What happened to that one?\n\nPrime Documentary covers the cases that quietly decide what the state may do to you. The full episode is linked at the top.\n\n#Shorts #Alaska261 #Law #Documentary",
        "tags": ["Shorts", "Alaska261", "Law", "Documentary"],
        # v001: generated from the design by gen_short_publish_config.py
        "video_sha256": "518b928553f111008f3deaee613ac97aa111cf1479bf74f60a79687a0ba8db3c",
        "thumb_sha256": "823800f6f2a1e165d6ea2df826b8eb62036a05050b0b145e1ec02a6dde5d1bae",
    },
    "319": {
        # destination for the funnel link; ensure_funnel_description() verifies it is public
        "longform": "o98hKLTK93g",
        "ep": "PD-2026-080-concordia",
        "rev": "v001",
        "title": "The investigators ran the alternative timeline themselves: signal at 22:39, boats #Shorts",
        "description": "The investigators ran the alternative timeline themselves: signal at 22:39, boats.\n\nThe order came sixty-nine minutes after the rock. What used up the sixty-nine minutes?\n\nPrime Documentary covers the cases that quietly decide what the state may do to you. The full episode is linked at the top.\n\n#Shorts #Concordia #Law #Documentary",
        "tags": ["Shorts", "Concordia", "Law", "Documentary"],
        # v001: generated from the design by gen_short_publish_config.py
        "video_sha256": "c0c728f24123bb6662b38729784ba63f29b041f9ed02c5d34113d0e9b633a3f5",
        "thumb_sha256": "253ea73725b21f193d225d53cb1ca3154921cc55ca8c9089c83b22492819fdb8",
    },
    "320": {
        # destination for the funnel link; ensure_funnel_description() verifies it is public
        "longform": "o98hKLTK93g",
        "ep": "PD-2026-080-concordia",
        "rev": "v001",
        "title": "A muster drill is engineering made of people: it converts several thousand strangers #Shorts",
        "description": "A muster drill is engineering made of people: it converts several thousand strangers.\n\nWhat happens to a video briefing in a corridor after the ship loses all power in ninety seconds?\n\nPrime Documentary covers the cases that quietly decide what the state may do to you. The full episode is linked at the top.\n\n#Shorts #Concordia #Law #Documentary",
        "tags": ["Shorts", "Concordia", "Law", "Documentary"],
        # v001: generated from the design by gen_short_publish_config.py
        "video_sha256": "cdbf1897001a237602f2a792a24781083bb8601bd1e5006f609c1dbeec4c7075",
        "thumb_sha256": "7f62fafb9ebbd0b3c933102ee7347b981ee0473f6f36baea3a326f0d579ed1fd",
    },
    "321": {
        # destination for the funnel link; ensure_funnel_description() verifies it is public
        "longform": "o98hKLTK93g",
        "ep": "PD-2026-080-concordia",
        "rev": "v001",
        "title": "The report's verdict is that the human element is the root cause - and its own pages show #Shorts",
        "description": "The report's verdict is that the human element is the root cause - and its own pages show.\n\nThe investigators modelled a night where everybody got off. What was the difference between that night and this one?\n\nPrime Documentary covers the cases that quietly decide what the state may do to you. The full episode is linked at the top.\n\n#Shorts #Concordia #Law #Documentary",
        "tags": ["Shorts", "Concordia", "Law", "Documentary"],
        # v001: generated from the design by gen_short_publish_config.py
        "video_sha256": "338411dd68deab3fd23063faa098d7e859e369bd541c8b3ca5e392bae3689951",
        "thumb_sha256": "7743528dbf23a56cb41225221817f17b61bc8c634618eac88a7b04d99d24ffb7",
    },
    "322": {
        # destination for the funnel link; ensure_funnel_description() verifies it is public
        "longform": "KDNJwRywx2M",
        "ep": "PD-2026-081-station",
        "rev": "v001",
        "title": "From the car park the way in is a pair of wide doors. Behind them is a small lobby #Shorts",
        "description": "From the car park the way in is a pair of wide doors. Behind them is a small lobby.\n\nNinety seconds is not long. What was on the walls that made it ninety?\n\nPrime Documentary covers the cases that quietly decide what the state may do to you. The full episode is linked at the top.\n\n#Shorts #Station #Law #Documentary",
        "tags": ["Shorts", "Station", "Law", "Documentary"],
        # v001: generated from the design by gen_short_publish_config.py
        "video_sha256": "1e90a6dd961cb7da9f7afb132b1242e29c669108ec2c5ef3e0bc781b72371393",
        "thumb_sha256": "97840ac85297593a3cca9d8f6c77716182297f9bc671e35987b6d8ee70b85e88",
    },
    "323": {
        # destination for the funnel link; ensure_funnel_description() verifies it is public
        "longform": "KDNJwRywx2M",
        "ep": "PD-2026-081-station",
        "rev": "v001",
        "title": "NIST ran the test nobody had run in that building: the same device, the same arrangement #Shorts",
        "description": "NIST ran the test nobody had run in that building: the same device, the same arrangement.\n\nIf the foam was only the ignition, what was the building made of?\n\nPrime Documentary covers the cases that quietly decide what the state may do to you. The full episode is linked at the top.\n\n#Shorts #Station #Law #Documentary",
        "tags": ["Shorts", "Station", "Law", "Documentary"],
        # v001: generated from the design by gen_short_publish_config.py
        "video_sha256": "cec23ccba47207aca394916dc9c6943ca0d07924419b09b50ed94db9fa999cc1",
        "thumb_sha256": "c91a3bb9d0df3689d31d8a02369253ca53023ce8d226eab3846e86c30acc066a",
    },
    "324": {
        # destination for the funnel link; ensure_funnel_description() verifies it is public
        "longform": "KDNJwRywx2M",
        "ep": "PD-2026-081-station",
        "rev": "v001",
        "title": "An occupant limit is arithmetic tied to the exits - a statement about the doors. The number #Shorts",
        "description": "An occupant limit is arithmetic tied to the exits - a statement about the doors. The number.\n\nIf the constraint that kills is the door, what did the door on this building actually measure?\n\nPrime Documentary covers the cases that quietly decide what the state may do to you. The full episode is linked at the top.\n\n#Shorts #Station #Law #Documentary",
        "tags": ["Shorts", "Station", "Law", "Documentary"],
        # v001: generated from the design by gen_short_publish_config.py
        "video_sha256": "eaa8ee731ea5f3f2c2c9bba3842d2481a2cea98e1aab51d80e5a6a0840434da6",
        "thumb_sha256": "7cced7eebe5bcfb7e5c4378f9341a3d1eca53413841302cc0b954ac3700323fd",
    },
    "325": {
        # destination for the funnel link; ensure_funnel_description() verifies it is public
        "longform": "wgjY-OHAQZI",
        "ep": "PD-2026-082-valdez",
        "rev": "v001",
        "title": "Every ship carries a number: the smallest crew it may sail with. This one was worked out #Shorts",
        "description": "Every ship carries a number: the smallest crew it may sail with. This one was worked out.\n\nIf the crew was set for a longer voyage, what was the first thing that got dropped on the short one?\n\nPrime Documentary covers the cases that quietly decide what the state may do to you. The full episode is linked at the top.\n\n#Shorts #Valdez #Law #Documentary",
        "tags": ["Shorts", "Valdez", "Law", "Documentary"],
        # v001: generated from the design by gen_short_publish_config.py
        "video_sha256": "ed55272b39fbb24e96d0fdf008a83405dce80152eb8199ef8e8152f570516dae",
        "thumb_sha256": "ec9e1d9792cb7e79a8c3e0dc7b17a4778c0071b646d7c96874441e545a0f020f",
    },
    "326": {
        # destination for the funnel link; ensure_funnel_description() verifies it is public
        "longform": "wgjY-OHAQZI",
        "ep": "PD-2026-082-valdez",
        "rev": "v001",
        "title": "A lookout is a person whose whole job is to look at the water and say what is on it #Shorts",
        "description": "A lookout is a person whose whole job is to look at the water and say what is on it.\n\nThe company had its own rule about two officers on the bridge. What did the Board say about relying on it?\n\nPrime Documentary covers the cases that quietly decide what the state may do to you. The full episode is linked at the top.\n\n#Shorts #Valdez #Law #Documentary",
        "tags": ["Shorts", "Valdez", "Law", "Documentary"],
        # v001: generated from the design by gen_short_publish_config.py
        "video_sha256": "303ceb317ffb7530dfa438eab5ac9a31684d7560cda8c7f7955cdcc24467aa5f",
        "thumb_sha256": "d933fd859316e912b4dd821b5a2173396fa543133835a2a83b871c2ba6a8f302",
    },
    "327": {
        # destination for the funnel link; ensure_funnel_description() verifies it is public
        "longform": "wgjY-OHAQZI",
        "ep": "PD-2026-082-valdez",
        "rev": "v001",
        "title": "The Board listed four things it could find no reasonable explanation for. The third #Shorts",
        "description": "The Board listed four things it could find no reasonable explanation for. The third.\n\nNineteen years later a second institution found the same shape from different evidence. What did it write down?\n\nPrime Documentary covers the cases that quietly decide what the state may do to you. The full episode is linked at the top.\n\n#Shorts #Valdez #Law #Documentary",
        "tags": ["Shorts", "Valdez", "Law", "Documentary"],
        # v001: generated from the design by gen_short_publish_config.py
        "video_sha256": "8d2320595dfe3bc75e4f00393bb698710d3dc53ccf795fa2d676813c1e6f8dd5",
        "thumb_sha256": "ecefead561f22111dcf636c774ebb7326d24dc9acf68d67f1a0226e621b0d555",
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
    # The custom thumbnail is what the channel page, search and suggested rails show, and those are
    # 16:9. Setting the vertical 1080x1920 cover there letterboxes it into two black bars with the
    # headline cropped away - measured on the live channel, 40 Shorts were shipped like that. Use
    # the dedicated ShortThumbYT render when it exists and only fall back to the vertical cover.
    thumb = ROOT / "runs" / "shorts_thumbs" / "samples" / f"{short_id}.png"
    if not thumb.is_file():
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
