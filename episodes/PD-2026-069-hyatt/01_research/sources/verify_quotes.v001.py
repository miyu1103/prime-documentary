"""EP69 quotation verifier. Run from this directory:  py -3.11 verify_quotes.v001.py

Re-locates every quotation used in EP69_hyatt_FACTS_LEDGER.v001.md by exact string
search in the persisted source texts, and prints its character offset.
Exit code 1 if any quotation cannot be found.

Sources (all retrieved 2026-08-11, sha256 recorded in the ledger):
  NBS  = SRC-0001_nbs_bss143.txt              NBS Building Science Series 143 (1982)
  MOCA = SRC-0002_duncan_744sw2d524.txt       Duncan v. Missouri Bd., 744 S.W.2d 524 (Mo. App. 1988)
  JPCF = SRC-0003_pfatteicher_jpcf_14_2_62.txt  Pfatteicher, J. Perf. Constr. Facil. 14(2):62-66 (2000)
"""
import io
import json
import os
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
H = os.path.dirname(os.path.abspath(__file__))


def load(name):
    return open(os.path.join(H, name), encoding="utf-8").read()


DOC = {
    "NBS": load("SRC-0001_nbs_bss143.txt"),
    "MOCA": load("SRC-0002_duncan_744sw2d524.txt"),
    "JPCF": load("SRC-0003_pfatteicher_jpcf_14_2_62.txt"),
}

Q = [
    # ---------------- NBS Building Science Series 143 ----------------
    ("N01", "NBS", "it is concluded that the most probable cause of failure was insufficient load capacity of the box beam-hanger rod connections."),
    ("N02", "NBS", "Two factors contributed to the collapse: inadequacy of the original design for the box beam-hanger rod connection, which was identical for all three walkways, and a change in hanger rod arrangement during construction that essentially doubled the load on the box beam-hanger rod connections at the fourth floor walkway."),
    ("N03", "NBS", "As actually constructed, two sets of hanger rods were used, one set extending from the fourth floor box beams to the roof framing and another set from the second floor box beams to the fourth floor box beams."),
    ("N04", "NBS", "the maximum load on a fourth floor box beam-hanger rod connection at the time of collapse was only 31 percent of the ultimate capacity expected of a connection designed under the Kansas City Building Code."),
    ("N05", "NBS", "With this change in hanger rod arrangement, the ultimate capacity of the walkways was so significantly reduced that, from the day of construction, they had only minimal capacity to resist their own weight and had virtually no capacity to resist additional loads imposed by people."),
    ("N06", "NBS", "On July 17, 1981, at approximately 7:05 p.m., two suspended walkways within the atrium area of the Hyatt Regency Hotel in Kansas City, Mo., collapsed, killing 111 people and injuring 188. Two of the injured subsequently died."),
    ("N07", "NBS", "this was the most devastating structural collapse ever to take place in the United States."),
    ("N08", "NBS", "At the time of the collapse, the hotel had been in service for approximately 1 year."),
    ("N09", "NBS", "However, during construction, shop drawings were prepared by the steel fabricator which called for the use of two sets of hanger rods rather than a single set."),
    ("N10", "NBS", "Under this arrangement all of the second floor walkway load was first transferred to the fourth floor box beams, where both that load and the fourth floor walkway load were transmitted through the box beam-hanger rod connections to the ceiling hanger rods."),
    ("N11", "NBS", "As indicated by their stamps, these shop drawings were reviewed by the contractor, structural engineer"),
    ("N12", "NBS", "The design load to be transferred to each hanger rod at the second floor walkway would have been one-half the sum of the dead load and the resultant live load for a single span, or approximately 20.3 kips (90 kN)"),
    ("N13", "NBS", "However, the load to be transferred from the fourth floor box beam to the upper hanger rod under this arrangement was essentially doubled, thus compounding an already critical condition."),
    ("N14", "NBS", "Had this change in hanger rod detail not been made, the ultimate capacity of the box beam-hanger rod connection would still have been far short of that expected of a connection designed in accordance with the AISC Specification."),
    ("N15", "NBS", "Thus the ultimate capacity actually available using the original connection detail would have been approximately 60 percent of that expected of a connection designed in accordance with the AISC Specification."),
    ("N16", "NBS", "Note that, because of the greater dead load and design live load, the third floor walkway connection would have had approximately 53 percent of the expected ultimate capacity. Had the change in hanger rod arrangement not been made, the third floor walkway would have been the most critical of the three."),
    ("N17", "NBS", "It would be expected that the ultimate load capacity of the resulting connection would be at least 1.67 times 40.7, or 68 kips (302 kN)"),
    ("N18", "NBS", "should have been able to support an ultimate load of at least 68 kips (302 kN)"),
    ("N19", "NBS", "Thus the maximum load acting on a fourth floor box beam-hanger rod connection at the time of collapse was 53 percent of what was required for design under the Kansas City Building Code."),
    ("N20", "NBS", "it is clear that each of the 6 fourth floor box beam-hanger rod connections had a high probability of failure; each connection was a candidate for initiation of walkway collapse."),
    ("N21", "NBS", "Thus, failure of any one connection would have led to complete collapse of the walkway system."),
    ("N22", "NBS", "Neither the quality of workmanship nor the materials used in the walkway system played a significant role in initiating the collapse"),
    ("N23", "NBS", "The walkway hangers were 1 1/4 in (32 mm) diameter rods threaded top and bottom to receive a nut and washer."),
    ("N24", "NBS", "The box beams were fabricated from MC8 x 8.5 shapes joined toe to toe by continuous longitudinal welds."),
    ("N25", "NBS", "Efforts to obtain copies of the structural design calculations were unsuccessful"),
    ("N26", "NBS", "7:00 PM - Crowd in atrium area is estimated at 1500 to 2000."),
    ("N27", "NBS", "7:04 PM - Band returns from break and begins to play for dance contest."),
    ("N28", "NBS", "7:05 PM - Second and fourth floor walkways collapse."),
    ("N29", "NBS", "4:30 AM - Last survivor removed from debris."),
    ("N30", "NBS", "It is concluded that a total of 63 people represents a credible upper-bound combined occupancy of the second and fourth floor walkways at the time of collapse."),
    ("N31", "NBS", "the dead load prior to collapse averaged 17.8 kips (79 kN) per walkway span. This is approximately 8 percent higher than the nominal dead load that would be estimated on the basis of the contract drawings."),
    ("N32", "NBS", "Dynamic loads induced by walking or dancing on the walkways would not have been significant in comparison to the static loads."),
    ("N33", "NBS", "The change in hanger rod arrangement from a continuous rod to interrupted rods essentially doubled the load to be transferred by the fourth floor box beam-hanger rod connections"),
    ("N34", "NBS", "For the continuous hanger rod arrangement, the design load to be transferred to each hanger rod at the second and fourth floor levels would have been approximately 20.3 kips (90 kN)"),
    ("N35", "NBS", "For the interrupted hanger rod arrangement, the design load to be transferred by a fourth floor box beam-hanger rod connection would have been 40.7 kips (181 kN)"),
    ("N36", "NBS", "The box beam-hanger rod connection would not have satisfied the Kansas City Building Code under the original hanger rod detail (continuous rod)."),
    ("N37", "NBS", "Based on NBS structural tests, the mean ultimate capacity of a single-rod connection as detailed on the contract drawings is estimated to be 20.5 kips (91 kN)"),
    ("N38", "NBS", "would have had the capacity to resist the loads estimated to have been acting at the time of collapse"),
    ("N39", "NBS", "The maximum load (estimated dead load plus upper-bound live load) believed to have been acting on a second floor box beam-hanger rod connection at the time of collapse is 11.5 kips (51 kN)"),
    ("N40", "NBS", "Mean ultimate capacities of the fourth floor box beam-hanger rod connections were estimated on the basis of the NBS test series and these capacities ranged from 18.2 kips (81 kN) to 19.3 kips (86 kN) with an average value of 18.6 kips (83 kN)"),
    ("N41", "NBS", "Based on information obtained from the KMBC TV videotape, it is likely that the second floor walkway was occupied by approximately 40 people shortly before the collapse."),
    ("N42", "NBS", "In view of the conflicting nature of eyewitness accounts and the availability of videotape showing parts of the walkways a few minutes before the collapse, this investigation did not include any organized effort to interview the injured or to solicit eyewitness accounts of the collapse."),
    ("N43", "NBS", "the number of people and their location on the walkways at the time of collapse can only be estimated and will never be"),
    ("N44", "NBS", "Under this arrangement each box beam would separately transfer its load directly into the hanger rods."),
    ("N45", "NBS", "The project design criteria specify a design live load of 100 psf (4.8 kPa) for hotel corridors and lobby areas. This is interpreted by NBS to include the walkways"),
    ("N46", "NBS", "The AISC Specification for the Design, Fabrication and Erection of Structural Steel for Buildings forms the basis for the steel design provisions of the Kansas City Building Code."),
    ("N47", "NBS", "the fourth floor to ceiling hanger rods, and the third floor walkway hanger rods did not satisfy the design provisions of the Kansas City Building Code."),
    ("N48", "NBS", "Observed distortions of structural components strongly suggest that failure of the walkway system initiated in the box beam-hanger rod connection at location 9UE (east end of middle box beam in fourth floor walkway)"),
    ("N49", "NBS", "In the early phases of the investigation, NBS involvement was limited by court order to visual and photographic observations and measurements."),
    ("N50", "NBS", "On July 22, Mayor Berkley formally requested that the NBS independently ascertain the most probable cause of the collapse of the Hyatt Regency walkways."),
    ("N51", "NBS", "The third floor walkway was offset from the other two and was independently suspended from the roof framing by another set of hanger rods."),
    ("N52", "NBS", "The atrium is a large open area approximately 117 ft (36 m) by 145 ft (44 m) in plan and 50 ft (15 m) high."),
    ("N53", "NBS", "The second floor walkway was suspended from the fourth floor walkway which was directly above it."),
    ("N54", "NBS", "In the collapse, the second and fourth floor walkways fell to the atrium floor, with the fourth floor walkway coming to rest on top of the lower walkway."),
    ("N55", "NBS", "Each walkway consisted of four spans made up of W16 x 26 stringers"),
    ("N56", "NBS", "Three suspended walkways spanned the atrium at the second, third, and fourth floor levels."),
    ("N57", "NBS", "an investigation conducted by the U.S. Occupational Safety and Health Administration (OSHA) following a fatal construction accident at the Hyatt Regency Hotel in October 1979"),
    ("N58", "NBS", "the welding symbol used on the shop drawings is interpreted to require a prequalified partial joint penetration groove weld"),
    # ---------------- Duncan v. Missouri Board, 744 S.W.2d 524 ----------------
    ("M01", "MOCA", "On July 17, 1981, the second and fourth floor walkways of the Hyatt Regency Hotel in Kansas City collapsed and fell to the floor of the main lobby. Approximately 1500 to 2000 people were in the lobby. The walkways together weighed 142,000 pounds. One hundred and fourteen people died and at least 186 were injured."),
    ("M02", "MOCA", "In February 1984, the Missouri Board for Architects, Professional Engineers and Land Surveyors filed its complaint seeking a determination that the engineering certificates of registration of Daniel Duncan and Jack Gillum and the engineering certificate of authority of G.C. E. International were subject to discipline"),
    ("M03", "MOCA", "Upon remand for assessment of appropriate disciplinary action, the Board ordered all three certificates revoked. Upon appeal the trial court affirmed. We do likewise."),
    ("M04", "MOCA", "The Commission conducted twenty-seven days of hearing."),
    ("M05", "MOCA", "Duncan was found to have been guilty of gross negligence in the preparation and completion of a structural drawing (S405.1, Sections 10 and 11); and in failing to review shop drawings of the Hyatt project"),
    ("M06", "MOCA", "He was further found guilty of misconduct in misrepresenting to the architects the safety of a connection (the double hanger rod-box beam connection) when he was ignorant of the safety due to a failure to perform engineering tests and calculations to determine such safety."),
    ("M07", "MOCA", "As originally designed the fourth and second floor walkways were to be supported by what is referred to as a “one rod” design."),
    ("M08", "MOCA", "A “non-redundant” connection which fails will cause collapse of the structure. The box beam-hanger rod connections were “non-redundant.”"),
    ("M09", "MOCA", "The Commission found that the structural drawings (S405.1 Secs. 10 and 11) did not communicate to the fabricator that it was to design the box beam-hanger rod connection, and did communicate to the fabricator that those connections had been designed by the engineer."),
    ("M10", "MOCA", "Duncan testified that he intended for the fabricator to design the connections. Havens prepared its shop drawings on the basis that the connections shown on the design drawings had been designed by the structural engineer."),
    ("M11", "MOCA", "Because of certain fabricating problems Havens proposed to Duncan the use of a “double rod” system to suspend the second and fourth floor walkways."),
    ("M12", "MOCA", "The effect of this change was to double the load on the fourth floor walkway and the box beam-hanger rod connections on that walkway."),
    ("M13", "MOCA", "There was evidence that one of the architects contacted Duncan to verify that the double rod arrangement was structurally sound and was advised by Duncan that it was."),
    ("M14", "MOCA", "It is a reasonable inference from the evidence that Duncan did not make the engineering calculations and tests necessary to determine the structural soundness of the double rod design."),
    ("M15", "MOCA", "He called to Duncan’s attention questions concerning the strength of the rods and the change from one rod to two. Duncan stated to the technician that the change to two rods was “basically the same as the one rod concept.”"),
    ("M16", "MOCA", "Duncan did not “review” the fourth floor box beam connection shown on the Havens shop drawings nor did he, in accord with usual engineering practice, assemble its components to determine what the connection looked like in detail."),
    ("M17", "MOCA", "Duncan and Gillum approved the shop drawings."),
    ("M18", "MOCA", "Under the contract, and under the statute, review and approval of the shop drawings is an engineering function."),
    ("M19", "MOCA", "Shop drawing review by the engineer is contractually required, universally accepted and always done as part of the design engineer’s responsibility."),
    ("M20", "MOCA", "The responsibility for the structural integrity and safety of the walkway connections was Duncan’s and that responsibility was non-delegable."),
    ("M21", "MOCA", "His reliance upon others to perform that duty serves as no justification for his indifference to his obligations and responsibility."),
    ("M22", "MOCA", "The Commission defined the phrase in the licensing context as “an act or course of conduct which demonstrates a conscious indifference to a professional duty.”"),
    ("M23", "MOCA", "The structural engineer’s duty is to determine that the structural plans which he designs or approves will provide structural safety because if they do not a strong probability of harm exists. Indifference to the duty is indifference to the harm."),
    ("M24", "MOCA", "In their report to the architects, appellants advised “we then checked the suspended bridges and found them to be satisfactory.”"),
    ("M25", "MOCA", "Appellants did not do a complete check of the design of all steel in the atrium nor a complete check of the suspended bridges."),
    ("M26", "MOCA", "The third floor walkway, which did not collapse, had a “high probability” of failure during the life of the building."),
    ("M27", "MOCA", "In essence he placed the responsibility for the improper design of the connections on Havens and took the position that the structural engineer was entitled to rely on Havens’ expertise."),
    ("M28", "MOCA", "By section 327.411.2 the owner of the seal is responsible for the “whole ... engineering project” when he places his seal on “any plans” unless he expressly disclaims responsibility and specifies the documents which he disclaims."),
    ("M29", "MOCA", "The finding of misconduct against Gillum arising from the “atrium design review” is reversed. In all other respects the order of the Commission and the discipline imposed by the Board is affirmed."),
    ("M30", "MOCA", "The National Bureau of Standards found as originally designed the connection capacity was 60 percent of that required by the Building Code; as ultimately constructed the capacity was 31 percent of Code requirements."),
    ("M31", "MOCA", "G.C.E.’s total fee for the Hyatt was $247,500."),
    ("M32", "MOCA", "While construction of the Hyatt was in progress the atrium roof collapsed. Investigation into that collapse established that the cause was poor construction workmanship."),
    ("M33", "MOCA", "Gillum assured the owner’s representative that “he would personally look at every connection in the hotel.”"),
    ("M34", "MOCA", "Because the shop drawings that were prepared under the direction of another engineer have to be the responsibility of the other engineer. They were not prepared under my direction and therefore I cannot accept that responsibility"),
    ("M35", "MOCA", "Its “Statement of the case, Findings of Fact, Conclusions of Law and Decision” are 442 pages in length."),
    ("M36", "MOCA", "The hanger rods and the box beam-hanger rod connections shown on the structural drawings did not meet the design specifications of the Kansas City Building Code."),
    ("M37", "MOCA", "The cause of the walkway collapse was the failure of the fourth floor box beam-hanger rod connections."),
    ("M38", "MOCA", "The Commission found, and appellants do not dispute, that its own internal procedures called for a detailed check of all special connections."),
    ("M39", "MOCA", "All connections are the responsibility of the structural engineer."),
    ("M40", "MOCA", "The Commission found the box beam-hanger rod connections to be special connections."),
    ("M41", "MOCA", "Duncan was the project engineer for the Hyatt construction in direct charge of the actual structural engineering work on the project. He was under the direct supervision of Gillum."),
    ("M42", "MOCA", "His professional seal was utilized on structural engineering plans for the Hyatt."),
    ("M43", "MOCA", "it is only after a complete analysis of their overall performance within the system that any judgment of their conduct can be made under the terms of the licensing statute."),
    ("M44", "MOCA", "It is the combination of a series of acts and omissions which created the structurally unsound walkways."),
    ("M45", "MOCA", "the original inadequacies of the structural drawings might not have been critical if a meaningful review of the shop drawings had occurred."),
    ("M46", "MOCA", "The steel fabricator on the Hyatt project, Havens Steel Company, had engineers capable of designing simple, complex, or special connections."),
    ("M47", "MOCA", "No review was made nor calculations performed to determine whether the box beam-hanger rod connection shown on the shop drawings met Code requirements."),
    # NOTE: the reporter text breaks "Gillum" across a line as "Gil-lum" here. Quoted exactly.
    ("M48", "MOCA", "Gil-lum was found vicariously liable and responsible for the acts and omissions of Duncan which liability and responsibility he assumed by affixing his professional engineering seal on the structural drawings."),
    ("M49", "MOCA", "He was further found grossly negligent in failing to himself review or assure that someone had reviewed drawing S405.1 before affixing his seal thereto."),
    ("M50", "MOCA", "Gillum was also found to have engaged in unprofessional conduct in failing and refusing to take responsibility for the entire engineering project"),
    ("M51", "MOCA", "Gillum-Colaco, Inc., a Texas corporation, contracted with the architects of the Hyatt construction to perform structural engineering services in connection with the erection of that building."),
    ("M52", "MOCA", "Certain information concerning loads and other aspects of the box beam-hanger rod connections which appeared on Duncan’s preliminary sketches was not included on the final structural drawings sent to the fabricator."),
    ("M53", "MOCA", "That breach occurred at the latest when their design was incorporated into the building with their approval and they were subject to discipline whether or not any collapse subsequently occurred."),
    # ---------------- Pfatteicher, JPCF 14(2) 2000 ----------------
    ("P01", "JPCF", "Between 1,500 and 2,000 area residents chose to escape the heat at the Hyatt Regency Hotel’s tea dance, a weekly event featuring big band music and a dance contest."),
    ("P02", "JPCF", "The final count of 114 dead and nearly 200 injured led one group of investigators to declare the Hyatt disaster ‘‘the most devastating structural collapse’’ in U.S. history"),
    ("P03", "JPCF", "The board’s investigation revealed that project engineer Duncan had been asked about the implications of the design change on at least six separate occasions during construction. Duncan assured each inquirer that replacing the single, long hanger rods with double, offset rods would not compromise the safety of the walkways."),
    ("P04", "JPCF", "Duncan later testified that the connection and any changes to it were not his responsibility because the engineers had not designed it in the first place"),
    ("P05", "JPCF", "Engineers shall hold paramount the safety, health and welfare of the public in the performance of their professional duties"),
    ("P06", "JPCF", "In December 1983, the county prosecutor and the U.S. Attorney announced that they had found insufficient evidence to convict anyone involved in the Hyatt construction with criminal negligence and that no criminal charges would be filed."),
    ("P07", "JPCF", "By this time, insurance companies had paid out over $78,000,000 to settle civil lawsuits filed by many of the victims and their families, but no one had yet taken responsibility for the collapse"),
    ("P08", "JPCF", "On November 15, 1985, Judge Deutsch filed his decision."),
    ("P09", "JPCF", "the board carried out the punishment on January 22, 1986, 4 1/2 years after the walkway collapse, and the two Hyatt engineers became the first to lose their licenses for gross negligence"),
    ("P10", "JPCF", "while the engineer may properly delegate the work of performing engineering design functions, he cannot delegate the responsibility"),
    ("P11", "JPCF", "The three walkways were removed"),
    ("P12", "JPCF", "The chain of events has never been exactly determined, but two possible scenarios have been proposed in studies of the Hyatt."),
    ("P13", "JPCF", "The Hyatt Regency Hotel, to which Gillum assigned Duncan, was a fast-track construction project, meaning that the construction team had begun to build the hotel while the design team was still finalizing the plans."),
    ("P14", "JPCF", "the committee members concluded unanimously that Gillum should be ‘‘expelled with no privilege ever to rejoin’’"),
    ("P15", "JPCF", "They voted to suspend him for just 3 years. Gillum voluntarily relinquished his membership altogether."),
    ("P16", "JPCF", "The engineers left the detail unspecified, indicating that the fabricators were to complete the calculations for the design. The fabricators later argued that the connection was not their responsibility."),
    ("P17", "JPCF", "Duncan and Gillum refused to concede that this made them responsible, particularly as there was no proof as to who had altered the plans."),
    ("P18", "JPCF", "had told the board the accident was the result of poor communication"),
    ("P19", "JPCF", "In the 1980s, he held licenses in 28 states, including Missouri."),
    ("P20", "JPCF", "Although Gillum lost 24 of his 28 state licenses, Ohio never saw fit to revoke his certificate, 3 other states simply never renewed his license, and California granted him reinstatement in July 1994"),
    ("P21", "JPCF", "In October 1979, two accidents at the Kansas City Hyatt (one resulting in a death) had brought attention to the hotel’s design"),
    ("P22", "JPCF", "Duncan was free from any discipline by an ethics committee because he had never been a member of any national society."),
    ("P23", "JPCF", "Actually, Duncan has not practiced engineering since his Missouri license was revoked"),
    ("P24", "JPCF", "In their place stands a single span, supported not by delicate, graceful rods, but standing on stout, sturdy columns"),
    ("P25", "JPCF", "The board had also chosen, for reasons that remain unclear, not to investigate the architects, over whom they also had licensing authority"),
]


def main():
    ok, bad, out = 0, [], {}
    seen = set()
    for rid, doc, q in Q:
        if rid in seen:
            print("DUPLICATE ID", rid)
            bad.append(rid)
            continue
        seen.add(rid)
        d = DOC[doc]
        i = d.find(q)
        if i < 0:
            bad.append(rid)
            print("FAIL", rid, doc, repr(q[:80]))
            lo, hi = 0, len(q)
            while lo < hi:
                mid = (lo + hi + 1) // 2
                if d.find(q[:mid]) >= 0:
                    lo = mid
                else:
                    hi = mid - 1
            j = d.find(q[:lo]) if lo else -1
            if j >= 0:
                print("     longest prefix", lo, "chars -> actual:", repr(d[j:j + lo + 120]))
        else:
            if d.find(q, i + 1) >= 0:
                pass  # multiple occurrences are fine; first is canonical
            ok += 1
            out[rid] = [doc, i]
            print("OK  %-5s %-5s @%d" % (rid, doc, i))
    print()
    print("VERIFIED", ok, "of", len(Q), " FAILED", len(bad))
    json.dump(out, open(os.path.join(H, "verified_offsets.v001.json"), "w"), indent=0)
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
