# qanat scope discussion (2026-10-23)

Claude's response to the new qanat goals (a tunnel-specific design library in an ecosystem with hangtu and a future settlement library). Input for `SPEC.md`; nothing here is decided.

I think the plan holds up, and the most useful thing qanat can do is tell you where numerical analysis is needed. A 60% design is mostly choosing between options, sizing elements and deciding which risks need more analysis. Closed-form and empirical methods are the right tools for that, as long as every result shows its inputs, its method and where the method stops being valid. hangtu's judgments file already does this for parameters. qanat would do the same for design decisions.

## What I'd add to the scope

You've listed the core. These are the gaps I see, from most to least important:

1. **Face stability and face pressure.** This is the biggest gap. For EPB and slurry TBMs and MTBMs it means support pressure (Anagnostou & Kovári, Broms & Bennermark stability number, Leca & Dormieux). For open-face mining it means stand-up time and face stability. Thrust depends on face pressure, so you need it either way.
2. **Segmental lining.** Closed-form ring forces (Muir Wood/Curtis, Duddeck–Erdmann), jacking loads on segments, and handling and stacking cases. A one-pass segmental lining is a large share of tunnel design.
3. **Convergence–confinement.** The ground reaction curve, the support's own load–deformation curve, the longitudinal displacement profile (Vlachopoulos & Diederichs), and squeezing assessment (Hoek & Marinos). This method ties your support types to the ground's behavior. It's also the clearest test for "does this section need a numerical model?"
4. **Rock loads and support selection.** Q-system and RMR support charts, Terzaghi rock load, and kinematic wedge screening. Q and RMR as numbers belong in hangtu. Picking support from them belongs in qanat.
5. **Pipe jacking and MTBM jacking force.** Face resistance plus friction, joint capacity, and where intermediate jacking stations go. It sits next to TBM thrust.
6. **Shaft checks beyond basal heave.** Base uplift and piping (hydraulic blow-in), tremie or jet-grout plug thickness, flotation, hoop compression in circular walls, arching-reduced earth pressure for circular shafts (Berezantzev, Prater), and toe embedment.
7. **Groundwater beyond tunnel inflow.** Shaft inflow, dewatering well systems (Dupuit/Theis), and seepage around a cutoff. Steady-state analytical inflow methods (Goodman, Heuer's correction, El Tani) for tunnels.
8. **Ground improvement and pre-support.** Ground freezing (frozen wall thickness, freeze time), groutability ratios, jet grout columns, spiling and pipe canopies. These come up often for cross passages and shaft breakouts.
9. **TBM performance.** Penetration rate and cutter wear (CSM, NTNU) and torque, next to thrust. It also links to schedule.
10. **Later:** seismic ovaling and racking (Wang, Penzien), portals and cross passages.

<!-- agreed with all the above, I will figure out order of these later on -->

**Where the settlement library starts:** qanat could produce volume loss, or a face-pressure-based estimate of it, as an output that the settlement library consumes. Decide which library owns volume loss early, because it's the main thing passed between the two.

<!-- qanat produces volume loss -->

## Cross-cutting decisions qanat needs early

These would go in SPEC.md because two analyses could each decide them differently:

- **How qanat and hangtu share data without depending on each other.** Each library could define its own input/output contract: column names, units in `df.attrs`, and a judgments file format. The risk is that hangtu and qanat drift into two slightly different judgments formats. The alternatives are a shared conventions document that both follow, or a third, very small package for judgments and units that both depend on. Without either, the format will drift.
  <!-- good point. I think a shared format would be good, as a reference for a whole project run. For now, lets plan for it to be a smaller package that connects the two. I want each of them to be pretty independent, so thats the way to go for now. Definitely subject to change. Since there will be more packages (like the settle library), a separate one to store project decisions and workflows is probably the way to go. -->
- **Design parameters vs design judgments.** qanat gets most of its ground inputs from hangtu's selected parameters, and it should record where they came from (for example, a characteristic value from a specific hangtu file and hash). It also adds its own judgments: design code, load and resistance factors, surcharges, construction stage, and target factors of safety. These are the same idea as hangtu's judgments file, but at the design level.
- **What every result reports.** I'd use one result shape for every analysis: values, utilization or factor of safety, the method and reference, the judgments used, and a **validity verdict**:
  - within the method's range;
  - marginal;
  - outside the method's range, so run a numerical model.

  The third case is what makes "deciding where to run numerical analyses" a direct output instead of something you infer.
- **One section vs a whole alignment.** I'd write every analysis for one section or one shaft, and add a thin table of reaches (stations, ground class, cover, water) that applies them along the alignment. A support class per reach and a summary of flagged sections is a typical 60% deliverable, so this should be planned from the start.
- **Design codes and structural checks.** LRFD or ASD, which editions (AASHTO, ACI, AISC, Eurocode?), and how far structural checks go. I'd limit qanat to simple capacity checks and leave full code compliance to the structural engineer.
- **The calc package.** At 60% design the deliverable is a set of calculations someone can review. A report view of each result (inputs, judgments, equations, references, verdict) may matter as much as the numbers. hangtu's "one calculation, many views" idea fits this.
  <!-- agreed, for now dont worry about it. I'll format reports/figures/deliverables outside of these packages. This might be a rolled into the judgments/project decisions library discussed earlier. The library could be the reporting layer where the user defines project specifics, then runs them through the various tools. -->

## What happens to the current qanat repo

The current scaffold (`schemas/` for cost and schedule, the `data/` benchmark corpus, `projects/`) belongs to the old goal. Under your new split it also conflicts with keeping sensitive work on the work machine. I'd replace it: archive or delete it, rewrite `CLAUDE.md`, and start with `SPEC.md`. That's the "product spec first" step of `/spec-driven-development`. If you still want the benchmark-corpus idea, it probably belongs on the work machine or in a separate repo.

<!-- get rid of everything here, I am just keeping the name. No need to archive. -->

## Questions before I draft SPEC.md

1. **Users and distribution.** Open source on PyPI under MIT, like hangtu, for a geotechnical or tunnel engineer with beginner-to-intermediate Python?
  <!-- yes -->
2. **Codes and units.** Are you working to US codes first, with SI and US units like hangtu, or should it be neutral between codes?
   <!-- neutral, but like hangtu, prefer SI units. Though I konw plenty of empirical equations require US units. -->
3. **The shared contract with hangtu.** A shared conventions document, a small shared package, or independent contracts with adapters in your work-machine skills?
   <!-- see comments above -->
4. **First milestone after scaffolding.** I'd suggest circular shaft SOE plus basal heave. It's well bounded and uses hangtu's outputs directly. Or is something else more urgent on your projects?
   <!-- great suggestion, directly related to my current work -->
